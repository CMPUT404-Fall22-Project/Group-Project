# 404 Project
This project was made for the 2022 Fall semester CMPUT 404 required class project.  [<ins>Rubric Link</ins>](https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org)    

This project was made by **Team 16**:
* Aaron Skiba
* Marcus Der
* Mateo Paez
* William Wong
* Amrit Aujla

Teams we collaberated with:   
Team 1:  https://github.com/CMPUT404-Social-Distribution-Project/mondaylab-cmput404-project  
Team 15: https://github.com/CMPUT404FALL2022/CMPUT404-GroupProject  
Team 19: https://github.com/CMPUT404Project/social-distribution

<br/>

# Demo Video
[![Demo Video Link](https://img.youtube.com/vi/fbk5VAsZHrk/maxresdefault.jpg)](https://www.youtube.com/watch?v=fbk5VAsZHrk)

<br/>

# Public Deployment
Frontend: https://team-sixteen-social-scene.herokuapp.com  
Backend: https://team-sixteen.herokuapp.com  

Backend django administration login:  
Username: team16  
Password: 12345

<br/>

# Local Installation Instructions

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

### 6. In your browser, navigate to http://127.0.0.1:3000/ for the frontend and http://127.0.0.1:8000/ for the backend
