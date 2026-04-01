# AI Career Counselor System

The AI Career Counselor System is a Flask-based intelligent web application that helps students choose suitable career paths by analyzing their academic marksheets, interests, and assessment responses using OCR and AI-based recommendations.

## Features

* Upload 10th / 12th marksheets (PDF or Image)
* Extract academic information using OCR (Tesseract)
* Interest-based career analysis
* AI-powered career recommendations using GROQ API
* Skill gap identification
* MySQL database integration
* Secure environment variable handling using `.env`
* Structured Flask backend with modular architecture

## Tech Stack

**Frontend**

* HTML
* CSS
* Bootstrap

**Backend**

* Python
* Flask

**Database**

* MySQL

**AI & Processing**

* GROQ API
* pdfplumber
* pytesseract
* Pillow

## Project Structure

Career Counselling System/
│
├── app.py
├── backend/
├── templates/
├── static/
├── requirements.txt
├── database_setup.sql
├── README.md
└── .env.example

## Installation Steps

Clone repository

git clone https://github.com/yourusername/AI-Career-Counselor-System.git

Move into project directory

cd AI-Career-Counselor-System

Create virtual environment

python -m venv venv

Activate environment (Windows)

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Create `.env` file and add:

SECRET_KEY=your_secret_key
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=career_counselor_db
GROQ_API_KEY=your_api_key

Run project

python app.py

Open browser

http://127.0.0.1:5000

## Database Setup

Run database_setup.sql inside MySQL:

CREATE DATABASE career_counselor_db;

## Future Improvements

* Add aptitude test scoring module
* Deploy project on cloud platform
* Add dashboard analytics
* Resume-based recommendation support

