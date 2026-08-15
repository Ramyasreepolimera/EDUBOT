# EduBot

EduBot is a Django-based educational platform that provides student accounts, study-material management, feedback collection, and a chatbot-oriented learning experience.

## Features

- Student registration, login, and profile management
- Admin dashboard for managing students and study materials
- Study-material and video access
- Student feedback and sentiment-analysis views
- Django-based web application with MySQL support

## Requirements

- Python 3.8 or later
- MySQL Server
- pip

## Setup

1. Clone the repository and enter the project folder.

   ```bash
   git clone https://github.com/Ramyasreepolimera/EDUBOT.git
   cd EDUBOT
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\\Scripts\\Activate.ps1
   ```

3. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables. Copy `.env.example` to `.env` as a reference, then set the variables in your shell or deployment environment. Do not commit `.env`.

   Required database variables:

   ```text
   DB_NAME=edu_chatbot
   DB_USER=root
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=3306
   ```

   Also set a strong `DJANGO_SECRET_KEY` before deploying.

5. Create the MySQL database named `edu_chatbot` (or use the value you set for `DB_NAME`), then run migrations.

   ```bash
   python manage.py migrate
   ```

6. Start the development server.

   ```bash
   python manage.py runserver
   ```

   Open `http://127.0.0.1:8000/` in your browser.

## Configuration

The application reads its Django, database, and email settings from environment variables. See `.env.example` for the complete list.

For local PowerShell development, variables can be set for the current session:

```powershell
$env:DJANGO_SECRET_KEY = "replace-with-a-long-random-secret"
$env:DB_PASSWORD = "your-password"
```

## Project structure

```text
SmartChatbox/   Django project configuration
adminapp/       Administrative features
mainapp/        Main site pages
studentapp/     Student features
templates/      HTML templates
static/         CSS, JavaScript, fonts, and images
```

## Security notes

- Keep `.env` and any credentials out of version control.
- Set `DEBUG=False` and configure `ALLOWED_HOSTS` before production deployment.
- Use a strong, unique `DJANGO_SECRET_KEY` in production.

## License

No license has been specified yet.
