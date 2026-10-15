<p align="left">
  <img src="backend/app/static/images/sona.guard_assets/sg_logo-full.png" alt="sona.guard logo" width="320">
</p>

**Estate Access Control & Visitor Management System**

sona.guard is a Flask-based access-control system designed to help residential estates manage residents, visitors, entrances, and access verification through a centralised application.

The project is being developed as a practical exploration of backend engineering, authentication, role-based permissions, database relationships, and access-control business logic.

> **Project status:** In active development. This is a development project and has not been represented as production-ready or security-certified.

## Current Features

- **Authentication:** Staff login and session-based authentication.
- **Role-based access control:** Separate roles for System Owners, Estate Administrators, Security Supervisors, and Security Officers.
- **Estate scoping:** Restricting estate-specific operations according to a user's assigned property.
- **Access verification:** Checking resident and entrance details against access-control rules.
- **Unit management foundation:** Database models and service logic for residential units and resident assignments.
- **Database migrations:** Version-controlled schema changes using Flask-Migrate and Alembic.
- **Audit and access records:** Models and services for recording access attempts and audit activity.
- **Seed data:** Fictional demonstration records for local development and testing.

Features are being implemented and tested incrementally. The list above describes the current development scope, not a claim that every feature is complete.

## Database architecture

The database is organised around estates, the people associated with them, and the records needed to verify and review access.

The main models currently include:

**Property** — an estate or residential property.

**Entrance** — an access point associated with a property.

**Unit** — a residential unit belonging to a property.

**Resident** — a resident associated with a property and, where assigned, a unit.

**Visitor** — a visitor record.

**VisitorAuthorization** — a record used to represent visitor authorisation.

**User** — a staff account with a role and property assignment.

**AccessAttempt** — a record of an access verification attempt.

**AuditLog** — a record of relevant system activity.

The intended structure uses relationships between properties, entrances, units, residents and access records. The database schema is managed through migrations.

An entity relationship diagram will be added once the relationships and constraints have been checked against the current models.

## Technology Stack

- Python
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Migrate and Alembic
- SQLite for local development
- HTML, CSS, and vanilla JavaScript
- Pytest

## Project structure

The application lives in the `backend` folder.

The `app` folder contains the main Flask application. Its `models` folder defines the database models, `routes` handles the application endpoints, and `services` contains the application logic. The `templates` folder holds the HTML pages, while `static` contains the CSS, JavaScript and images.

The `migrations` folder contains database schema changes, and `tests` contains the project's tests. The `requirements.txt` file lists the Python dependencies, `run.py` is the application entry point, and `seed.py` provides demonstration data.

The root folder contains the README and Git configuration.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/oriah-studios-TSF/Sona.Guard.git
cd Sona.Guard
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv backend/.venv
backend/.venv/Scripts/Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 4. Configure environment variables

Create a `backend/.env` file using `backend/.env.example` as a reference. Set a securely generated Flask `SECRET_KEY` and a suitable `DATABASE_URI` for your local database.

Never commit real secrets, credentials, or private database files.

### 5. Initialise the database

From the repository root, activate the virtual environment and use the project's Flask application configuration to apply the existing migrations. Database initialisation and seed commands may depend on the current development setup.

### 6. Run the application

Follow the application's current configuration and entry point in `backend/run.py`. The setup instructions will be refined as the development workflow becomes more standardised.

## Development Approach

The project is developed incrementally, with emphasis on:

- Clear separation between routes, services, and database models.
- Backend permission checks rather than relying on interface visibility alone.
- Estate-level data access restrictions.
- Validation and predictable error handling.
- Database integrity and migration discipline.
- Testing important access-control rules.

## Security and Limitations

This project is under development and is intended for learning, demonstration, and continued engineering work. It has not been independently audited or certified for deployment in a real residential estate.

Use fictional data in demonstrations. Do not use this project to control real-world access until appropriate security reviews, testing, operational safeguards, and deployment hardening have been completed.

## Author

**Oriah Studios**

GitHub: [oriah-studios-TSF](https://github.com/oriah-studios-TSF)

---

*Built incrementally while learning and applying practical software engineering principles.*
