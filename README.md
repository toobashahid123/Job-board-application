# Job Board Application

Welcome to the Job Board Application! This project is a full-featured job board platform where users can post job listings, search for jobs, and apply for them. The application is built using Django, Django REST Framework, and MySQL.

## Features

- **User Authentication:** Secure user registration, login, and password management.
- **Job Listings:** Post, view, edit, and delete job listings.
- **Job Search:** Search for jobs by keywords, location, and job type.
- **Job Application:** Apply for jobs and manage applications.
- **Email Notifications:** Receive notifications for job postings and applications via email.
- **Real-time Chat:** Chat with recruiters and job seekers in real-time.

## Technology Stack

- **Backend:** Django, Django REST Framework
- **Database:** MySQL
- **Email Service:** SendGrid
- **Real-time:** Redis, Django Channels
- **Environment Management:** Python-dotenv

## Getting Started

### Prerequisites

- Python 3.7+
- MySQL
- Redis

### Installation

Follow these steps to set up the project on your local machine:

1- Clone the repository:
   git clone https://github.com/toobashahid123/Job-board-application.git
   cd Job-board-application/jobboard

2- Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3- Install the required Python packages:
   pip install -r requirements.txt

4- Run database migrations:
   python manage.py migrate

5- Create a superuser for accessing the Django admin panel:
   python manage.py createsuperuser

6- Run the development server:
   python manage.py runserver

8- Access the application:
   Admin Panel: http://127.0.0.1:8000/admin/
   Job Board: http://127.0.0.1:8000/

**Usage**
Admin Panel: Manage jobs, users, and other administrative tasks.
Job Board: Post and apply for jobs, search for job listings, and more.

**License**
This project is licensed under the MIT License. See the LICENSE file for details.

**Contributing**
Contributions are welcome! Please fork the repository and submit a pull request. For significant changes, open an issue to discuss your ideas.

**Contact**
For any questions or feedback, feel free to reach out to tooba7987@gmail.com.
   
