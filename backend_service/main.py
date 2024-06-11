import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette import status

from app.api import spotify, spotify_authenticate

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost:5173/curator",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Do regex of ALL but that's kinda naughty
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spotify.router)
app.include_router(spotify_authenticate.router)


@app.get("/")
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
