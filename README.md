# Realtime Spotify Github Profile

This is a Python script that allows you to automatically update your Github profile README with your latest Spotify activity. The program uses the Spotipy library to access your Spotify data, and then generates a new README file with the current song you're listening to, your top artists, and your top tracks and it will then be committed and pushed to your Github profile, allowing anyone who visits your profile to see your latest musical interests.

## How to Use

To use this program, you'll need to follow a few steps:

- Clone this repository to your local machine.
- Install the required dependencies by running `'pip install -r requirements.txt'` in your terminal.
- Create a Spotify Developer account and create a new app. You'll need to set the redirect URI to `http://localhost:8080` | `http://localhost:5000` or `any`.
- Make sure that the redirect uri in config file is same as the spotify app redirect uri.
- Get your github token from `https://github.com/settings/tokens`.
- Rename `example.config.py` to `config.py` and fill in the appropriate values for its contents. You'll also need to add your display username.
- Run `'python app.py'` in your terminal. This will update your README.md file

That's it! Your Github profile will now display your latest musical interests.

## Todo

- [ ] Implement caching to avoid making unnecessary requests to the Spotify API.
- [x] ~Allow users to choose the time range (e.g. last week, last month) for their top tracks and artists.~
- [ ] Add support for generating a "recommended tracks" section based on the user's top tracks or currently playing song.
- [ ] Add a feature to display the popularity score of the currently playing song.

## Contributing

Contributions to this project are welcome. Please follow the existing code style and conventions for new features or bug fixes, thank you!
