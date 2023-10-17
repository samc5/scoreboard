
# WatchPeglegs

A website displaying a live scoreboard above a Stuyvesant Baseball Facebook livestream. The scoreboard, if copied, will work for any gamechanger game
## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python3 app.py
```



## Notes
The scoreboard requires a private gamechanger API to recieve game data. This is obtained with selenium by running `tester.getPushURL(game_url)` in the python console
- `game_url` is the base url of the game on the gamechanger website. You can copy/paste this into the admin portal
The Admin Portal is accessed by `your_domain/admin`. Here, you paste in a facebook live embed code, and the URL obtained from selenium, as well as admin code as found in `app.py`
- This is a tedious process, but it works