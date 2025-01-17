<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\SpotifyUser;
use Illuminate\Http\Request;
use SpotifyWebAPI\Session;
use SpotifyWebAPI\SpotifyWebAPI;
use Illuminate\Support\Facades\Log;

/**
 * @property Session $session
 * @property SpotifyWebAPI $spotify
 */

class SpotifyController extends Controller
{
    private $spotify;
    private $session;

    public function __construct()
    {
        $this-> session = new Session(
            config('services.spotify.client_id'),
            config('services.spotify.client_secret'),
            config('services.spotify.redirect_uri')
        );
        
        $this->spotify = new SpotifyWebAPI();
    }

    public function redirectToSpotify()
    {
        $options = [
            'scope' => [
                'user-read-private',
                'user-read-email',
            ]
        ];

        return redirect($this->session->getAuthorizeUrl($options));
    }

    public function handleSpotifyCallback(Request $request)
    {
        //If the user has denied the authorization
        if ($request->has('error')) {
            return response() ->json(['error' => 'Authorization denied'], 401);
        }
        $code = $request->get('code');
        
        try {
            // Request an access token using the code
            $this->session->requestAccessToken($code);
            
            info('Access Token: ' . $code);
            info('Access Token: ' . $this->session->getAccessToken());
            info('Refresh Token: ' . $this->session->getRefreshToken());

            // Set the access token on the API wrapper
            $accessToken = $this->session->getAccessToken();
            $refreshToken = $this->session->getRefreshToken();
            $expiresIn = $this->session->getTokenExpiration();
            //store in laravel session maybe this is where the issue is coming from
            session(['spotify_access_token' => $accessToken]);
            $this->spotify->setAccessToken($accessToken);

            // Get the user's data
            $user = $this->spotify->me();

            // Store the user data in your database
            $spotifyUser = SpotifyUser::updateOrCreate(
                ['spotify_id' => $user->id],
                [
                    'display_name' => $user->display_name,
                    'profile_image' => $user->images[0]->url ?? null,
                    'access_token' => $accessToken,
                    'refresh_token' => $refreshToken,
                    'token_expires_at' => now() ->addSeconds($expiresIn),
                ]
            );

            session([
                'spotify_access_token' => $accessToken,
                'spotify_refresh_token' => $this->session->getRefreshToken(),
                'spotify_token_expires_at' => now()->addSeconds($expiresIn)
            ]);

            // Redirect to your frontend or return a response
            // return response()->json(['status' => 'success', 'user' => $spotifyUser]);
            // return redirect('/')->with('success', 'Successfully logged in with Spotify!');
            return response()->json([
                'success' => true,
                'token_stored' => $spotifyUser->access_token
            ]);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }


    public function search(Request $request)
    {
        try {
            $result = $this->spotify->search($request->q, 'track');

            return response()->json([
                'status' => 'success',
                'data' => $result->tracks->items
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => $e->getMessage()
            ], 500);
        }
    }

    public function getLoggedUser(Request $request)
    {            
        try {
            $spotifyUser = SpotifyUser::where('spotify_id', $request->user_id)->first();
            if (!$spotifyUser || !$spotifyUser->access_token) {
                return response()->json([
                    'status' => 'error',
                    'message' => 'User not authenticated'
                ], 401);
            }

            $this->spotify->setAccessToken($spotifyUser->access_token);
            $spotifyProfile = $this->spotify->me();

            return response()->json([
                'status' => 'success',
                'data' => $spotifyProfile
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => $e->getMessage()
            ], 500);
        }
    }
}
