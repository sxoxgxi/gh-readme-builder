import logging
import pandas as pd

from config import username, user_url, limit
from helpers import (
    playing,
    recently_played,
    top_artists,
    top_songs,
    double_hyphen,
    classify_music_tastes,
    get_music_mood,
    read_write_file,
)


def get_user_status() -> bool:
    pendingupdate = read_write_file(file_path="files/README.md", mode="r")
    # fetch user's status
    data = playing()
    if data:
        try:
            is_playing = data["is_playing"]
            song = data["item"]["name"]
            action = "Playing" if is_playing else "Paused"
        except TypeError:
            logging.info("Spotify returned NoneType.\n")
            song = "Advertisement 😞"
            action = "Playing"
    else:
        song = "Offline"
        action = username

    content = f"""<p status, align='center'>
  <a href='{user_url}'>
    <img src="https://img.shields.io/badge/{action}-{double_hyphen(song)}-&?style=social&logo=spotify">
  </a>
</p status>"""

    startblock = pendingupdate.index("<p status, align='center'>")
    endblock = pendingupdate.index("</p status>")
    newcontent = (
        pendingupdate[:startblock]
        + content
        + pendingupdate[endblock + len("</p status>") :]
    )

    read_write_file(file_path="files/README.md", mode="w", data=newcontent)
    return bool(data)


def add_recently_played() -> bool:
    # Fetch recently played tracks data
    recent_tracks_data = recently_played(limit=limit)["items"]
    num_tracks = min(len(recent_tracks_data), limit)

    df = pd.DataFrame(recent_tracks_data)
    df = pd.json_normalize(df["track"])
    df = df[["name", "external_urls.spotify", "album.images"]]
    df.columns = ["song", "song_url", "image_url"]
    df["image_url"] = df["image_url"].apply(lambda x: x[0]["url"])

    table_html = "<table style='width:100%'>\n" + "<tr align='center'>\n"
    for i in range(num_tracks):
        table_html += f"<td>\n"
        table_html += f"<img class='artists' src='{df['image_url'][i]}' alt='{df['song'][i]}' style='width:50%'>\n"
        table_html += f"</td>\n"
    table_html += "</tr>\n"
    table_html += "<tr align='center'>\n"
    for i in range(num_tracks):
        table_html += f"<td>\n"
        table_html += f"<a href='{df['song_url'][i]}'>{df['song'][i]}</a>\n"
        table_html += f"</td>\n"
    table_html += "</tr>\n"
    table_html += "</table>\n"

    # Update README.md file
    readme = read_write_file(file_path="files/README.md", mode="r")
    startblock = readme.index("<p recentlyplayed, float='left'>")
    endblock = readme.index("</p recentlyplayed>")
    new_content = f"""<p recentlyplayed, float='left'>
  <br>
  <h1>Recently played tracks</h1>
  <p></p>
  {table_html}
</p recentlyplayed>"""
    new_readme = (
        readme[:startblock]
        + new_content
        + readme[endblock + len("</p recentlyplayed>") :]
    )

    read_write_file(file_path="files/README.md", mode="w", data=new_readme)
    return num_tracks == limit


def add_top_artists() -> bool:
    # Fetch top artists data
    top_artists_data = top_artists(limit=limit)["items"]
    num_artists = min(len(top_artists_data), limit)

    artists = []
    for artist_data in top_artists_data:
        artist = {
            "name": artist_data["name"],
            "artist_url": artist_data["external_urls"]["spotify"],
            "image_url": artist_data["images"][0]["url"],
        }
        artists.append(artist)

    table_html = "<table style='width:100%'>\n" + "<tr align='center'>\n"

    for i in range(num_artists):
        table_html += f"<td>\n"
        table_html += f"<img class='artists' src='{artists[i]['image_url']}' alt='{artists[i]['name']}' style='width:50%'>\n"
        table_html += f"</td>\n"

    table_html += "</tr>\n"
    table_html += "<tr align='center'>\n"

    for i in range(num_artists):
        table_html += f"<td>\n"
        table_html += f"<a href='{artists[i]['artist_url']}' target='_blank'>{artists[i]['name']}</a>\n"
        table_html += f"</td>\n"

    table_html += "</tr>\n"
    table_html += "</table>\n"

    # Update README.md file
    readme = read_write_file(file_path="files/README.md", mode="r")
    startblock = readme.index("<p topartists, float='left'>")
    endblock = readme.index("</p topartists>")
    new_content = f"""<p topartists, float='left'>
  <br>
  <h1>Top artists this month</h1>
  <p></p>
  {table_html}
</p topartists>"""
    new_readme = (
        readme[:startblock] + new_content + readme[endblock + len("</p topartists>") :]
    )

    read_write_file(file_path="files/README.md", mode="w", data=new_readme)
    return num_artists == limit


def add_top_songs() -> bool:
    # fetch top songs
    data_songs = top_songs(limit=max(limit, 5))["items"]
    global song_id
    song_id = [item["id"] for item in data_songs]
    song_num = len(song_id)
    song_info = []

    for item in data_songs:
        album = item["album"]
        album_url = album["external_urls"]["spotify"]
        artist = item["artists"][0]
        artist_url = artist["external_urls"]["spotify"]
        song_url = item["external_urls"]["spotify"]
        song = item["name"]
        image_url = album["images"][0]["url"]
        song_info.append(
            (
                song,
                song_url,
                album["name"],
                album_url,
                artist["name"],
                artist_url,
                image_url,
            )
        )

    content = """<p topsongs, float='left' >
  <br>
  <h1>Top tracks this month</h1>
  <p></p>
  <table style='width:100%'>
    <tr align='center'>
      <td>
      <h2>Poster</h2>
      </td>
      <td>
      <h2>Song</h2>
      </td>
      <td>
      <h2>Album</h2>
      </td>
      <td>
      <h2>Artist</h2>
      </td>
    </tr>"""

    for i in range(song_num):
        song, song_url, album, album_url, artist, artist_url, image_url = song_info[i]
        content += f"""<tr align='center'>
      <td><img class='artists' src='{image_url}' alt='{song}' style='width:10%'>
      </td>
      <td>
      <a href='{song_url}'>{song}</a>
      </td>
      <td>
      <a href='{album_url}'>{album}</a>
      </td>
      <td>
      <a href='{artist_url}'>{artist}</a>
      </td>
    </tr>"""

    content += """</table>
</p topsongs>"""

    data = read_write_file(file_path="files/README.md", mode="r")
    startblock = data.index("<p topsongs, float='left' >")
    endblock = data.index("</p topsongs>")
    newcontent = data[:startblock] + content + data[endblock + len("</p topsongs>") :]

    read_write_file(file_path="files/README.md", mode="w", data=newcontent)
    return song_num == 5


def update_mood():
    # classify music features
    music_classification = get_music_mood(song_id)
    mood, happiness = music_classification[0], music_classification[1]

    data = read_write_file(file_path="files/README.md", mode="r")
    clas_start = data.index("<td>Music Mood is")
    clas_end = data.index("Music</td>")
    clas_content = f"<td>Music Mood is {mood} | {happiness} | Current Taste: {classify_music_tastes(song_id)} Music</td>"
    # print(clas_content)
    new_clas_content = (
        data[:clas_start] + clas_content + data[clas_end + len("Music</td>") :]
    )

    read_write_file(file_path="files/README.md", mode="w", data=new_clas_content)


def sync_status(condi: bool):
    readme = read_write_file(file_path="files/README.md", mode="r")
    if condi:
        content = """<img src='https://img.shields.io/badge/Layout-Synced-brightgreen' class='layout'>"""
    else:
        content = """<img src='https://img.shields.io/badge/Layout-Unsynced-red' class='layout'>"""

    startblock = readme.index("<img src='https://img.shields.io/badge/Layout-")
    endblock = readme.index("class='layout'>")
    newcontent = (
        readme[:startblock] + content + readme[endblock + len("class='layout'>") :]
    )
    read_write_file(file_path="files/README.md", mode="w", data=newcontent)


def prepare_layout(website: str, discord_url: str, avatar_url: str) -> None:
    readme = read_write_file(file_path="files/README.md", mode="r")
    content = f"""<h1 align='center'>
  <br>
  <a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ'><img src='{avatar_url}' alt='{username}' width='200'></a>
  <br>
  {username}
  <br>
</h1>

<h4 align='center'>Raise your words, not voice. It is rain that grows flowers, not thunder. - <a href='https://duckduckgo.com/?q=Rumi' target='_blank'>Rumi</a>.</h4>

<p align='center' socials>
  <a href='{discord_url}'>
    <img src='https://img.shields.io/badge/Discord-server-blue'>
  </a>
  <a href='{website}'>
    <img src='https://img.shields.io/website?down_color=red&down_message=offline&label=Website&up_color=light%20green&up_message=online&url={website}'>
  </a>
  <img src='https://img.shields.io/badge/Layout-Synced-brightgreen' class='layout'>
</p socials>"""
    startblock = readme.index("<h1 align='center'>")
    endblock = readme.index("</p socials>")
    newcontent = (
        readme[:startblock] + content + readme[endblock + len("</p socials>") :]
    )
    read_write_file(file_path="files/README.md", mode="w", data=newcontent)


if __name__ == "__main__":
    print("Try python app.py")
