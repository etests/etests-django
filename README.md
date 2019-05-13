
# eTests
## backend
- Create a virtual environment in root (say venv). 
- Edit venv/bin/activate as follows:
	-  In deactivate function, write *unset SECRET_KEY* at the bottom. 
	- Acquire the secret key from repo owner. Finally, write export SECRET_KEY= "<the_secret_key>" at the bottom of the file.
- cd backend
- pip install -r requirements.txt
- ./manage.py runserver 0.0.0.0:8888 to start the backend development server.

## frontend
- Install npm (node package manager)
- cd frontend
- npm install
- npm run dev to start the frontend development server.

## editor
- Install these extensions
	- Vue extension pack
	- ESLint
	- Prettier