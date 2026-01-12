# Fitness Club Management System  
COMP 3005 — Final Project  
Author: Prisca Love
ID: 101259306
Database: PostgreSQL  
ORM: SQLAlchemy (ORM Bonus Included)

---

## Overview

This project implements a Fitness Club Management System using PostgreSQL and Python with SQLAlchemy ORM. It supports three main roles:

- Member
- Trainer
- Administrator

## Core Features

### Member Operations
1. Register a new member  
2. Update profile details  
3. Log health metrics  
4. Register for group fitness classes  

### Trainer Operations
5. Set trainer availability  
6. View trainer schedule (personal training sessions and group classes)  

### Administrator Operations 

7. Create a trainer 
8. Create group fitness classes  
9. Book personal training sessions 
10. Create a room

### Validation Logic
The system implements several important validation rules:

- Prevention of double-booking trainers  
- Prevention of room conflicts  
- Enforcing class capacity limits  
- Preventing duplicate class registration  
- Detecting overlapping trainer availability  

---

## Installation and Setup

### 1. Navigate to the project folder
cd FinalProject

2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install required packages

pip install sqlalchemy psycopg2-binary

4. Create the PostgreSQL database

psql -U postgres

5. Create the database:

CREATE DATABASE fitness_club;

6. Configure the database URL
Inside app/database.py, update:

DATABASE_URL = "postgresql+psycopg2://postgres:YOURPASSWORD@localhost:5432/fitness_club"
Replace YOURPASSWORD with your actual PostgreSQL password.

7. Initializing the Database
The database tables are created through SQLAlchemy ORM. Run:

python3 -c "from app.database import init_db; init_db()"

This automatically generates all tables defined in the ORM models.

8. RUN CLI

python3 cli.py



9. Demo Video

Video Link:
https://youtu.be/L8gZe2hl1_s

10. Documentation
All supporting documentation for this project is located in the docs/ folder, including:

ERD.pdf (ER Diagram, Schema Mapping, Normalization)

