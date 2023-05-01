import time
import logging
import datetime
import requests
from io import BytesIO
from github import Github
from PIL import Image, ImageDraw
from logging.handlers import RotatingFileHandler

from helpers import read_write_file, has_readme, check_avatar_exists
from config import github_reponame, github_token, discord_url, website
from constructor import (
    get_user_status,
    add_recently_played,
    add_top_artists,
    add_top_songs,
    update_mood,
    sync_status,
    prepare_layout,
)


g = Github(github_token)

user = g.get_user()
avatar_url = user.avatar_url

handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=1)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logging.getLogger("").addHandler(handler)
logging.getLogger("").addHandler(logging.StreamHandler())
logging.getLogger("").setLevel(logging.INFO)


def prepare_avatar(avatar_url, save_path) -> None:
    try:
        # Download the avatar image
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content))

        size = avatar.size
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        avatar.putalpha(mask)
        cropped_avatar = Image.new("RGBA", size, 0)
        cropped_avatar.paste(avatar, (0, 0), avatar)
        cropped_avatar.save(save_path)
        logging.info("Avatar modified successfully.\n")
    except Exception as e:
        logging.info(f"An error occurred while preparing the avatar: {e}\n")


def update_readme_file(content: str) -> None:
    try:
        repo = g.get_repo(github_reponame)
        gitcontent = repo.get_contents("README.md", ref="main")
        if gitcontent.decoded_content.decode("utf-8") != content:
            repo.update_file(
                gitcontent.path,
                message="Spotify stats Updated.",
                content=content,
                sha=gitcontent.sha,
                branch="main",
            )
            logging.info("Successfully updated the README.md file with changes.\n")
        else:
            logging.info("No changes were made to README.md. Reloading.\n")
        upload_image()
    except Exception as e:
        logging.info(f"Failed to update the README.md: {e}\n")


def upload_image():
    try:
        repo = g.get_repo(github_reponame)
        if check_avatar_exists(repo=repo, github_reponame=github_reponame) == False:
            with open("files/avatar.png", "rb") as file:
                content = file.read()
            repo.create_file(
                path="avatar.png",
                message="Add avatar",
                content=content,
                branch="main",
            )
            logging.info(f"Successfully uploaded avatar to {github_reponame}!\n")
    except FileNotFoundError as e:
        logging.info(f"Error uploading avatar: File not found - {e}\n")
    except Exception as e:
        logging.info(f"Error uploading avatar to {github_reponame}: {e}\n")


def prepare_files():
    try:
        repo = g.get_repo("sxoxgxi/sxoxgxi")
        data = repo.get_contents("README.md", ref="main")
        if has_readme(data=data.decoded_content.decode("utf-8")):
            pass
    except UnicodeEncodeError as e:
        logging.info(f"Error encoding README.md content: {e}\n")
        return
    except Exception as e:
        logging.info(f"Error preparing files: {e}\n")
        return


def main():
    prepare_files()
    prepare_avatar(avatar_url=avatar_url, save_path="files/avatar.png")
    prepare_layout(website=website, discord_url=discord_url, avatar_url="avatar.png")
    try:
        while True:
            now = datetime.datetime.now()
            sleep_time = max(0, 10 - now.second % 10)
            time.sleep(sleep_time)
            # get the Spotify user status
            try:
                if get_user_status():
                    logging.info("User Online\n")
                else:
                    logging.info("User Online\n")
            except Exception as e:
                logging.info(f"Error updating user status: {e}\n")

            try:
                try:
                    layout_recents = add_recently_played()
                except Exception as e:
                    logging.info(f"Error adding recently played songs: {e}\n")
                try:
                    layout_artists = add_top_artists()
                except Exception as e:
                    logging.info(f"Error adding recently played songs: {e}\n")
                try:
                    layout_songs = add_top_songs()
                except Exception as e:
                    logging.info(f"Error adding recently played songs: {e}\n")
                try:
                    update_mood()
                except Exception as e:
                    logging.info(f"Error adding recently played songs: {e}\n")
            except Exception as e:
                logging.info(
                    f"Error updating Spotify status or adding tracks/artists/songs/mood: {e}\n"
                )
            try:
                if not layout_recents or not layout_artists or not layout_songs:
                    try:
                        sync_status(condi=False)
                    except Exception as e:
                        logging.info(f"Error updating layout sync status: {e}\n")
                else:
                    try:
                        sync_status(condi=True)
                    except Exception as e:
                        logging.info(f"Error updating layout sync status: {e}\n")
            except Exception as e:
                logging.info(f"Error updating layout sync status: {e}\n")
            # update the README file
            try:
                pushfile = read_write_file(file_path="files/README.md", mode="r")
                update_readme_file(pushfile)
            except Exception as e:
                logging.info(f"Error updating README file: {e}\n")

            # sleep until the next 10-second interval
            now = datetime.datetime.now()
            sleep_time = max(0, 10 - now.second % 10)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting...\n")
        return


if __name__ == "__main__":
    main()
