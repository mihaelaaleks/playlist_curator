<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class SpotifyUser extends Model
{
    use HasFactory;

    protected $fillable = [
        'spotify_id',
        'display_name',
        'profile_image',
        'access_token',
        'refresh_token',
        'token_expires_at'
    ];

    protected $hidden = [
        'access_token',
        'refresh_token',
        'token_expires_at'
    ];
}
