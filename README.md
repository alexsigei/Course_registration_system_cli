# Course Registration System CLI

A Python command-line application for managing courses, cohorts, student enrollments, module progression, results, and repeat modules.

## Features

* Student and admin authentication
* Browse available courses
* Enroll in courses and cohorts
* View course modules
* Enroll in modules
* Track academic progress
* Record and view module results
* Repeat failed modules using a different cohort
* Manage courses, modules, cohorts, students, and results
* JSON-based data persistence

## Technologies

* Python 3.12+
* Rich
* Pytest
* JSON
* Git & GitHub

## Setup

Clone the repository and enter the project:

```bash
git clone <repository-url>
cd course-registration-cli
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 main.py
```

## How to Use

### Student

1. Register for an account or log in.
2. Browse available courses.
3. Enroll in a course and select an available cohort.
4. View the course modules.
5. Enroll in the available module.
6. Check **My Progress** to track progression.
7. Once a module is passed, the next module becomes available.
8. If a module is failed, use **Repeat Failed Module** to select another available cohort.
9. View previous and current enrollments under **My Enrollments**.

### Admin

Log in using the administrator account below.

**Admin credentials**

```text
Email: admin@example.com
Password: password
```

The admin can:

* Manage courses
* Add modules
* View and add cohorts
* View students
* View enrollments
* Enter module results
* View student progress

## Course & Cohort Structure

```text
Course
 └── Cohort
      └── Modules
           └── Student Enrollments
```

A student selects a cohort when enrolling in a course. Module enrollments automatically use the student's current cohort.

When a student repeats a failed module, the system moves them to the selected new cohort for that course while preserving their previous enrollment history.

## Testing

Run all tests with:

```bash
pytest -v
```

Current test status:

```text
73 passed
```

## Project Structure

```text
course-registration-cli/
├── cli/             # Student and admin interfaces
├── models/          # Application models
├── services/        # Business logic
├── storage/         # JSON persistence
├── data/            # Application data
├── tests/            # Automated tests
├── main.py
├── requirements.txt
└── README.md
```

## Data Storage

The application currently uses JSON files in the `data/` directory for persistence.

Main data files include:

* `users.json`
* `students.json`
* `courses.json`
* `modules.json`
* `cohorts.json`
* `course_enrollments.json`
* `enrollments.json`
* `results.json`

## Project Status

The core registration, cohort management, module progression, results, and repeat-module workflows are implemented and tested.
