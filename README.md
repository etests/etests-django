# eTests

## Setup

- Create a virtual environment (say venv).
- Edit venv/bin/activate as follows: - In deactivate function, write `unset SECRET_KEY` at the bottom.
- Acquire the secret key from repo owner. Finally, write `export SECRET_KEY= "<the_secret_key>"` at the bottom of the file.
- `pip install -r requirements.txt`
- `./manage.py runserver` to start the development server.
