ComeonDa : A Sports Prediction App

Description
A FastAPI-based Sports Prediction Application where:
    Users can register and login
    Users can predict match outcomes
    Admin can create sports, tournaments, teams, matches and questions
    Leaderboard tracks user points
    History stores the users previous prediction results
    JWT authentication is used for security
    MySQL is used as database
    Alembic is used for database migrations

STEPS
1.Clone the Repository

2.Create Virtual Environment

    Code:uv venv

3.Activate Virtual Environment

    Code:.venv\Scripts\activate

4.Install Dependencies

    Code:uv pip install -r requirements.txt

5.Create MySQL Database

    Code:CREATE DATABASE sports_prediction;

6.Configure .env File

7.Run Database Migration using alembic

    Code:alembic upgrade head

8.Run Project

    code:uvicorn main:app --reload

9.Open swagger docs and give input to all apis to get final output

Admin already given:
Email : admin@gmail.com
Password : admin123

Methods Used in the live Project
Python for coding
FastAPI for visualising apis
MySQL for database
SQLAlchemy
Alembic
JWT for authentication
Pydantic
PyMySQL
