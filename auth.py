import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config import client_secret, client_id, redirect_uri


scopes = [
    "user-follow-read",
    "ugc-image-upload",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-read-private",
    "user-read-email",
    "user-follow-modify",
    "user-follow-read",
    "user-library-modify",
    "user-library-read",
    "streaming",
    "app-remote-control",
    "user-read-playback-position",
    "user-top-read",
    "user-read-recently-played",
    "playlist-modify-private",
    "playlist-read-collaborative",
    "playlist-read-private",
    "playlist-modify-public",
]
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes,
    )
)


def profile() -> dict:
    return sp.current_user()


def main():
    user_profile = profile()
    user_name = user_profile["display_name"]
    print(
        f"{user_name} authenticated successfully!\nNow run python app.py to get started."
    )


if __name__ == "__main__":
    main()
