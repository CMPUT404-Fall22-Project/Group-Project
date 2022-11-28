# Group-Project

[<ins>Rubric Link</ins>](https://github.com/abramhindle/CMPUT404-project-socialdistribution)



# Installation Instructions

### 1. Clone the repo

### 2. Install PostgreSQL and create a new database with the following details:
	i.   Name     = project_404 
	ii.  User     = postgres
	iii. Password = password
	iv.  Host     = localhost
	v.   Port     = 5432

### 3. In Group-Project/backend/
	i.    Run: ‘virtualenv venv --python=python3.10’
	ii.   Run: (For Windows) venv\Scripts\activate.bat	(For Mac) source venv/bin/activate
	iii.  Run: ‘pip install -r requirements.txt’
	iv.   Run: ‘python manage.py migrate’    (or possibly  ‘python3 manage.py migrate’ )
	v.    Run: ‘python manage.py runserver’  (or possibly ‘python3 manage.py runserver’)

### 5. In Group-Project/frontend/
	i.  Run:  ‘yarn install’
	ii. Run:  ‘yarn start’

### 6. In your browser, navigate to http://127.0.0.1:3000/
