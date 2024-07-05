# Django Project Setup Guide

This guide will help you get your Django project up and running on your local development environment.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Python 3.6 or higher
- pip (Python package manager)

## Installation
**Create a Virtual Environment**

It's recommended to create a virtual environment for your project dependencies. Run:


    python3 -m venv venv

    or

    python -m venv venv    

Activate the virtual environment:

- On macOS/Linux:
  ```
  source venv/bin/activate
  ```

- On Windows:
  ```
  .\venv\Scripts\activate
  ```

**Install Dependencies**

Install the project dependencies using pip:

```
pip install -r requirements.txt
```

**Database Migrations**

Apply the database migrations to set up your database schema:
```
python manage.py migrate
```

## Setting up environment variable
This project need an environment variable configured before it is able to run

follow `.env.copy` file as the environment template and fill the necessary credentials and save the new file as `.env`

## Running the project
Start the Django development server:
```
python manage.py runserver
```

## Features and Interface
### Features
:rocket: This chatbot able to store chat history and store it in memory for now

### available interface
Here is available endpoints that the backend currently supports

Endpoints                 |     Description     |       Headers         |
--------------------------|---------------------|-----------------------|
/POST api/prompt          | simple prompt chat bot with LLM without any context stored | N/A |
/POST api/prompt-history  | simple prompt chat bot with LLM that can learn and gain context from chat history | "session-id": "{session-id e.g. session-123, must be unique} |