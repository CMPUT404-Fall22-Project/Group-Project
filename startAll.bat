start cmd @cmd /k "venv.bat && cd backend && python -m pip install --upgrade pip -r requirements.txt --quiet && python manage.py runserver"
start cmd @cmd /k "cd frontend && yarn install && yarn start"