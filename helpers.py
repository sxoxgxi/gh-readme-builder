import os
import sys
import spotipy
import logging
from spotipy.oauth2 import SpotifyOAuth

from config import client_secret, client_id, redirect_uri

# token = os.getenv('token')
# CLIENT_ID = os.getenv('id')
# CLIENT_SECRET = os.getenv('secret')

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
public_sp = spotipy.Spotify()


def profile() -> dict:
    return sp.current_user()


def recently_played(limit: int) -> dict:
    return sp.current_user_recently_played(limit=limit)


def top_artists(limit: int) -> dict:
    return sp.current_user_top_artists(limit=limit, time_range="short_term")


def top_songs(limit: int) -> dict:
    return sp.current_user_top_tracks(limit=limit, time_range="short_term")


def playing() -> dict:
    return sp.current_user_playing_track()


def double_hyphen(song) -> str:
    if "-" not in song:
        return song
    parts = song.split("-")
    new_parts = []
    for i in range(len(parts)):
        new_parts.append(parts[i].strip())
        if i < len(parts) - 1:
            new_parts.append("--")
    return " ".join(new_parts)


def read_write_file(file_path: str, mode: str, data=None) -> str | None:
    if mode == "r":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif mode == "w":
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(data)
            return None
    else:
        raise ValueError('Mode must be either "r" or "w".')


def check_avatar_exists(repo, github_reponame):
    contents = repo.get_contents("")
    for content in contents:
        if content.path == "avatar.png":
            return True
    logging.info(f"avatar.png does not exist in {github_reponame}\n")
    return False


def has_readme(data: str) -> bool:
    if os.path.exists("files/README.md"):
        if os.stat("files/README.md").st_size > 0:
            return True
        logging.info("README.md file is empty. Please fill it with the template.\n")
        sys.exit(1)
    else:
        with open("files/README.md", "w", encoding="utf-8") as f:
            f.write(data)
        logging.info("README.md was successfully created and written.\n")
        return True


def get_audio_features(track_ids: list) -> list:
    audio_features = sp.audio_features(track_ids)
    return audio_features


def get_average_happiness(audio_features: list) -> float:
    happiness = [item["valence"] for item in audio_features]
    return sum(happiness) / len(happiness) if happiness else 0.5


def get_music_mood(top_songs: list) -> tuple:
    if top_songs is None:
        return ("Error: Could not retrieve top songs.",)

    audio_features = get_audio_features(top_songs)
    if audio_features is None:
        return ("Error: Could not retrieve audio features.",)

    average_happiness = get_average_happiness(audio_features)
    if average_happiness >= 0.8:
        return ("😃: Very Happy!", f"Happiness Level: {average_happiness:.0%}")
    elif average_happiness >= 0.6:
        return ("😊: Happy", f"Happiness Level: {average_happiness:.0%}")
    elif average_happiness >= 0.4:
        return ("😐: Neutral", f"Happiness Level: {average_happiness:.0%}")
    elif average_happiness >= 0.2:
        return ("😔: Sad", f"Happiness Level: {average_happiness:.0%}")
    else:
        return ("😭: Very Sad!", f"Happiness Level: {average_happiness:.0%}")


def classify_music_tastes(track_ids: list) -> str:
    audio_features = get_audio_features(track_ids)
    danceability = sum(track["danceability"] for track in audio_features) / len(
        audio_features
    )
    energy = sum(track["energy"] for track in audio_features) / len(audio_features)
    loudness = sum(track["loudness"] for track in audio_features) / len(audio_features)
    speechiness = sum(track["speechiness"] for track in audio_features) / len(
        audio_features
    )
    valence = sum(track["valence"] for track in audio_features) / len(audio_features)

    if energy > 0.5 and speechiness > 0.1:
        return "Energetic and Vocal"
    elif energy > 0.5 and danceability > 0.5:
        return "Energetic and Danceable"
    elif valence > 0.5:
        return "Happy and Danceable" if danceability > 0.5 else "Happy and Upbeat"
    elif loudness < -10:
        return "Calm and Quiet"
    elif danceability < 0.3 and valence < 0.3:
        return "Sad and Slow"
    else:
        return "Difficult to classify"


if __name__ == "__main__":
    print("Try python app.py")
