# Job Portal API

This project is an API for a **Job Portal** system that facilitates the connection between **employers** and **job seekers**. Employers can post job listings, while job seekers can apply for jobs, manage their profiles, and upload resumes.

The project supports categorizing job listings by fields of work, allows bookmarking jobs, and enables employers to manage their companies and postings efficiently.

The project is fully dockerized for easy deployment and scalability.

## Prerequisites

Before setting up the project, ensure that you have the following installed:

- Docker and Docker Compose
- Python 3.11
- Django 5.1 or higher
- Django REST Framework
- PostgreSQL
- Virtualenv (optional but recommended)


## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammd-1819/Employee-Management.git
   cd Employee-Management
   ```

2. **Create and activate a virtual environment (optional if not using Docker):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   - Update the `DATABASES` section in `settings/local.py` with your PostgreSQL credentials.

5. **Apply the migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser for the admin panel:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server (if not using Docker):**
   ```bash
   python manage.py runserver
   ```

8. **Using Docker:**
   - Build and run the Docker containers:
     ```bash
     docker compose up --build
     ```
   - The application will be accessible at [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/).


## Features

- **Employer Features:**
  - Create and manage job listings.
  - Register and manage their company profile.


- **Job Seeker Features:**
  - Apply for job postings.
  - Create a profile with resume upload and skills section.
  - Bookmark jobs as saved jobs.


- **General Features:**
  - JWT-based authentication for secure access.

- **Admin Panel:**
  - Full control over users, job posts, companies, and categories.


## API Endpoints

- **Authentication:**
  - Register, login, and obtain JWT tokens.


- **Employers:**
  - Create and manage company profiles.
  - Post, update, and delete job listings.


- **Job Seekers:**
  - Create and update profiles.
  - Upload resumes and add skills.
  - Apply for jobs.
  - Save/bookmark jobs.


## Technologies Used

- **Backend:** Django REST Framework
- **Database:** PostgreSQL - Redis
- **Containerization:** Docker
- **Authentication:** JWT-based authentication system



