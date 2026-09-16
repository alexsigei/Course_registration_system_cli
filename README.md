# Course Registration System

A Python command-line application for managing courses, modules, cohorts, student enrollment, academic results, and module progression.

The system is designed around an object-oriented architecture with a clear separation between the CLI, business services, domain models, and JSON persistence.

## Features

### Authentication

* Student and administrator registration/login
* Password hashing and salted password storage
* Role-based access to student and administrator functionality
* Students are not tied to a course during registration or login

### Course Management

* View available courses
* Add courses
* Add modules to courses
* Organize modules into a defined sequence
* Support students enrolling in multiple courses

### Cohort Management

* Create cohorts for specific courses
* Define cohort capacity
* Define cohort start and end dates
* Display available seats
* Prevent enrollment into full cohorts
* Prevent students from joining cohorts that have already started
* Display cohort status:

  * `UNSCHEDULED`
  * `NOT_STARTED`
  * `IN_PROGRESS`
  * `COMPLETED`
* Display cohort progress based on start and end dates

### Student Enrollment

Students first enroll in a course and select an available cohort.

A student's current cohort is maintained separately for each course.

For example:

```text
Alex
├── Computer Science → CS001 Cohort 2
└── Information Technology → IT Cohort 1
```

This allows a student to participate in multiple courses without mixing their progression or cohort information.

### Module Enrollment

* Students enroll in modules belonging to courses they are enrolled in
* The system automatically uses the student's current cohort for that course
* Students do not select a cohort separately when enrolling in a normal module
* Students cannot enroll in a module until the previous module in that course has been passed

### Results and Grading

Administrators can enter student results.

The system:

* Stores the student's score
* Uses the module's pass mark
* Determines whether the student passed or failed
* Calculates the corresponding grade
* Updates the module enrollment status

### Progression

Module progression is sequential and course-specific.

For example:

```text
MOD001 → MOD002 → MOD003
```

A student must pass `MOD001` before `MOD002` becomes available.

Progress statuses include:

* `PASSED`
* `IN PROGRESS`
* `REPEAT REQUIRED`
* `AVAILABLE`
* `LOCKED`

Progression is calculated independently for each course.

A result in one course does not affect progression in another course.

### Failed Module Repeats

When a student fails a module:

1. The failed attempt remains in the system.
2. The module is marked `REPEAT REQUIRED`.
3. The student is shown eligible cohorts for the repeat.
4. The previous cohort is excluded.
5. The new cohort must:

   * Belong to the same course
   * Have available seats
   * Not have started
6. A new module enrollment is created.
7. The student's current cohort for that course is changed to the new cohort.
8. The historical failed enrollment remains unchanged.

Example:

```text
Original attempt:
MOD001 → COH001 → FAILED

Repeat:
MOD001 → COH002 → ACTIVE
```

After passing the repeat:

```text
MOD001 → PASSED
MOD002 → AVAILABLE
```

The next module is then enrolled using the student's new current cohort.

### Enrollment History

Module enrollment records preserve historical cohort information.

For example:

```text
ENR002 → MOD001 → COH001 → failed
ENR003 → MOD001 → COH002 → active
```

The original failed attempt is not overwritten when the student repeats the module.

---

## Architecture

The application follows a layered architecture:

```text
                    ┌──────────────┐
                    │   main.py    │
                    └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              │                         │
       ┌──────▼──────┐           ┌──────▼──────┐
       │ Student CLI │           │  Admin CLI  │
       └──────┬──────┘           └──────┬──────┘
              │                         │
              └────────────┬────────────┘
                           │
                    ┌──────▼──────┐
                    │   Services  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Models   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ JSONStorage  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ data/*.json  │
                    └─────────────┘
```

### Main Layers

#### CLI

Located in:

```text
cli/
```

Responsible for:

* Displaying menus
* Collecting user input
* Displaying tables and messages
* Calling application services

#### Services

Located in:

```text
services/
```

Contains the application's business logic.

Examples include:

* `auth_service.py`
* `course_service.py`
* `cohort_service.py`
* `enrollment_service.py`
* `course_enrollment_service.py`
* `progression_service.py`
* `result_service.py`
* `student_service.py`

Services handle validation, enrollment rules, progression rules, result processing, and persistence operations.

#### Models

Located in:

```text
models/
```

Contains the domain objects used by the application.

Examples:

* `User`
* `Student`
* `Admin`
* `Course`
* `Module`
* `Cohort`
* `CourseEnrollment`
* `Enrollment`
* `Result`

#### Storage

Located in:

```text
storage/
```

The application uses `JSONStorage` to persist application data in JSON files.

---

## Course and Cohort Relationship

Courses own modules, while cohorts belong to courses.

```text
Course
│
├── Module 1
├── Module 2
└── Module 3
```

A course can have multiple cohorts:

```text
Computer Science
│
├── CS001 Cohort 1
└── CS001 Cohort 2
```

A student has a course enrollment that stores their current cohort:

```text
Student
    │
    └── CourseEnrollment
            ├── Student
            ├── Course
            └── Current Cohort
```

Module enrollments preserve the cohort used for each individual attempt.

---

## Project Structure

```text
course-registration-cli/
│
├── cli/
│   ├── admin_cli.py
│   ├── auth_cli.py
│   └── student_cli.py
│
├── models/
│   ├── admin.py
│   ├── cohort.py
│   ├── course.py
│   ├── course_enrollment.py
│   ├── enrollment.py
│   ├── module.py
│   ├── result.py
│   ├── student.py
│   └── user.py
│
├── services/
│   ├── auth_service.py
│   ├── cohort_service.py
│   ├── course_enrollment_service.py
│   ├── course_service.py
│   ├── enrollment_service.py
│   ├── progression_service.py
│   ├── result_service.py
│   └── student_service.py
│
├── storage/
│   └── json_storage.py
│
├── utils/
│   └── validators.py
│
├── data/
│   ├── courses.json
│   ├── modules.json
│   ├── cohorts.json
│   ├── course_enrollments.json
│   ├── enrollments.json
│   ├── results.json
│   ├── students.json
│   └── users.json
│
├── tests/
│   ├── test_auth.py
│   ├── test_cohort.py
│   ├── test_course.py
│   ├── test_course_enrollment.py
│   ├── test_enrollment.py
│   ├── test_progression.py
│   ├── test_result.py
│   └── ...
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Technologies

* **Python 3.12+**
* **pytest** — automated testing
* **Rich** — formatted CLI tables and output
* **JSON** — persistent data storage
* **Git/GitHub** — version control

---

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd course-registration-cli
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the interactive CLI with:

```bash
python3 main.py
```

The main menu provides:

```text
Main Menu
1. Login
2. Register
3. Exit
```

---

## Student Menu

After logging in as a student:

```text
Student Menu
1. View Profile
2. Browse Courses
3. Enroll in Course
4. View Course Modules
5. Enroll in Module
6. My Enrollments
7. My Progress
8. Repeat Failed Module
9. Logout
```

### Typical Student Workflow

```text
Register/Login
      ↓
Browse Courses
      ↓
Enroll in Course
      ↓
Select Cohort
      ↓
View Course Modules
      ↓
Enroll in Available Module
      ↓
Receive Result
      ↓
Pass?
  ┌───┴───┐
 YES      NO
  │        │
  ↓        ↓
Next     Repeat
Module   Module
  │        │
  └───┬────┘
      ↓
Continue Progression
```

---

## Administrator Menu

Administrators can manage the academic structure and student results.

Administrator functionality includes:

* View administrator profile
* Manage courses
* Add courses
* Add modules
* Manage cohorts
* View cohorts
* Add cohorts
* View students
* View student enrollments
* Enter student results
* Logout

---

## Testing

The project uses `pytest`.

Run the complete test suite with:

```bash
pytest -v
```

Current automated test status:

```text
73 passed
```

The automated tests cover areas including:

* Authentication
* Course management
* Module management
* Cohort management
* Course enrollment
* Module enrollment
* Results
* Progression
* Failed module handling
* Repeat enrollment
* Cohort changes
* Historical enrollment preservation

The core student workflow has also been manually tested end-to-end, including:

```text
Multiple course enrollment
        ↓
Course-specific cohorts
        ↓
Sequential module progression
        ↓
Failed module
        ↓
Repeat in different cohort
        ↓
Current cohort updated
        ↓
Repeat passed
        ↓
Next module unlocked
        ↓
Next module uses new cohort
```

---

## Example Progression

For Computer Science:

```text
MOD001 - Python Programming
        ↓
MOD002 - Data Structures and Algorithms
        ↓
MOD003 - Database Systems
```

Initially:

```text
MOD001 → AVAILABLE
MOD002 → LOCKED
MOD003 → LOCKED
```

After passing MOD001:

```text
MOD001 → PASSED
MOD002 → AVAILABLE
MOD003 → LOCKED
```

After passing MOD002:

```text
MOD001 → PASSED
MOD002 → PASSED
MOD003 → AVAILABLE
```

If MOD001 is failed:

```text
MOD001 → REPEAT REQUIRED
MOD002 → LOCKED
MOD003 → LOCKED
```

After repeating and passing MOD001:

```text
MOD001 → PASSED
MOD002 → AVAILABLE
MOD003 → LOCKED
```

---

## Data Persistence

Application data is stored in JSON files under:

```text
data/
```

Examples:

```text
users.json
students.json
courses.json
modules.json
cohorts.json
course_enrollments.json
enrollments.json
results.json
```

The separation between `CourseEnrollment` and module-level `Enrollment` allows the system to maintain both:

* The student's **current cohort for a course**
* The **historical cohort for each module attempt**

---

## Validation and Business Rules

The system enforces important rules such as:

* Course IDs must reference existing courses.
* Cohort IDs must be unique.
* Cohorts must belong to an existing course.
* Cohort capacity must be valid.
* Cohort end dates must be after start dates.
* Full cohorts cannot accept new students.
* Students cannot join cohorts that have already started.
* A student cannot actively enroll in the same course twice.
* A student must be enrolled in a course before enrolling in its modules.
* Students must pass the previous module before progressing.
* A failed module must be repeated in a different eligible cohort.
* Repeat cohorts must belong to the same course.
* Historical module enrollments are preserved.
* Course progression is independent between courses.

---

## Development Approach

The project follows object-oriented and modular design principles.

Key principles include:

* Separation of concerns
* Encapsulation
* Service-layer business logic
* Model-based domain representation
* JSON persistence
* Input validation
* Automated testing
* Git-based collaboration

The architecture is designed so that business rules remain in the service layer rather than being embedded directly into the CLI.

---

## Future Improvements

Potential future enhancements include:

* Automatic course completion status
* More detailed module progress tracking
* Improved CLI navigation
* Additional reporting for administrators
* More comprehensive integration tests
* Database-backed persistence
* Web/API interface
* Improved user management and account administration

---

## Project Status

The core course registration and progression workflow is implemented and tested.

### Current status

* Authentication: **Implemented**
* Course management: **Implemented**
* Module management: **Implemented**
* Cohort management: **Implemented**
* Course enrollment: **Implemented**
* Module enrollment: **Implemented**
* Seat availability: **Implemented**
* Results and grading: **Implemented**
* Sequential progression: **Implemented**
* Failed module handling: **Implemented**
* Repeat enrollment: **Implemented**
* Cohort reassignment: **Implemented**
* Historical enrollment tracking: **Implemented**
* Multi-course support: **Implemented**
* Automated tests: **73 passing**
* End-to-end CLI testing: **Passed**

---

## Team Project

This project was developed as part of the **Moringa School Software Engineering Module 4** group project.

The project demonstrates practical application of:

* Python
* Object-oriented programming
* CLI application development
* Software architecture
* Data persistence
* Testing
* Git collaboration
* Business-rule implementation
