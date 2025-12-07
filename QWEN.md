# Qwen Code Context: Django Reservation System

## Project Overview

This is a **Django 5-based reservation system** for managing show bookings for a production company. The project follows the PID (Projet d'Intégration et Développement) curriculum for Bachelor's in Computer Science and Management. It's built on top of a Django 5 starter kit and includes:

- A **show catalog** with artists and venues
- An **online reservation system**
- An **admin back-office** for content management
- A **RESTful API** for affiliates
- Planned ReactJS frontend integration

## Project Architecture

### Main Components

- **reservations/**: Main Django project
  - Settings, URL routing, WSGI configuration
- **catalogue/**: Core application for the reservation system
  - Organized into modular subdirectories:
    - `models/`: Data models (`artist.py`)
    - `views/`: View functions (`artist.py`)
    - `forms/`: Form classes (`ArtistForm.py`)
    - `templates/`: HTML templates (`artist/` subdirectory)
    - `static/`: Static assets
    - `fixtures/`: Initial data fixtures

### Technology Stack

- **Backend**: Python 3.11+, Django 5.0.14
- **Database**: MySQL/MariaDB 11+
- **Frontend**: Bootstrap 5 (planned ReactJS integration)
- **Environment**: Virtual environments with `.env` support
- **Version Control**: Git/GitHub collaboration

## Current Implementation Status

### Implemented Features
- Artist management (CRUD operations)
- Basic URL routing system
- Form handling with ModelForms
- Admin interface foundation
- Database connectivity with MySQL

### Project Iterations Plan
1. Framework installation and Git setup
2. Starter Kit (basic CRUD for Artists)
3. Relational mapping (Type, Locality, Price entities)
4. Authentication system
5. Complex relationships (Shows, Reservations)
6. RESTful API implementation
7. ReactJS frontend integration

## Development Conventions

### File Structure Conventions
- Models organized in `catalogue/models/`
- Views organized in `catalogue/views/`
- Forms in `catalogue/forms/`
- Templates in application-specific subdirectories
- URL names follow the pattern `app_name:view_name`

### Coding Standards
- Model classes using Django's ORM
- View functions with proper HTTP method handling
- ModelForms for form processing
- Template context passing using dictionaries
- URL namespaced using `app_name` in `urls.py`

## Building and Running

### Prerequisites
- Python 3.11+
- MySQL or MariaDB server
- Git for version control

### Setup Commands
```bash
# Clone the repository
git clone https://github.com/mouedarbi/PID_Reservations_Groupe_Django.git
cd PID_Reservations_Groupe_Django

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# or source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The application will be available at [http://localhost:8000](http://localhost:8000)

### Environment Configuration
- Create a `.env` file in the project root to configure database connection:
  ```
  DB_NAME=your_database_name
  DB_USER=your_database_user
  DB_PASSWORD=your_database_password
  DB_HOST=localhost
  DB_PORT=3306
  ```

### Available Management Commands
- `python manage.py runserver` - Start development server
- `python manage.py migrate` - Apply database migrations
- `python manage.py makemigrations` - Create new migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py shell` - Django interactive shell

## Key Django Settings
- Database engine: MySQL
- Debug mode: Enabled (for development)
- Installed apps: Django built-ins + catalogue app
- Static files: Standard Django static file handling
- Timezone: UTC

## URL Structure
- `/catalogue/artist/` - List all artists
- `/catalogue/artist/<id>/` - View specific artist
- `/catalogue/artist/create` - Create new artist
- `/catalogue/artist/edit/<id>/` - Edit existing artist
- `/catalogue/artist/delet/<id>/` - Delete artist
- `/admin/` - Django admin interface

## Project Context
This project is part of an academic curriculum focusing on:
- Django project structure
- Collaborative development via GitHub
- ORM mapping and CRUD operations
- Authentication and API development
- Deployment best practices with Django 5