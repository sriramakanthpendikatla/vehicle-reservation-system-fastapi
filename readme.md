# Corporate Vehicle Pool Management System
Business Context & Value Proposition

The system manages a company's shared fleet of vehicles, including cars, bikes, and vans, used by employees for official business activities such as client visits, inter-office travel, and field operations. The platform ensures efficient vehicle allocation, prevents double bookings, tracks vehicle usage, and maintains maintenance schedules. Proper control is essential to maximize fleet utilization while ensuring safety, compliance, and operational efficiency.

Business Capabilities & Rules

Department-Based Vehicle Access: Every vehicle belongs to a specific department or is shared across departments. Employees can reserve only vehicles they are authorized to access through their department.

Reservation Scheduling: Employees can reserve vehicles for a specific time period. The system must prevent overlapping reservations for the same vehicle.

Driver Eligibility Validation: Employees must possess a valid company-approved driving license. Reservations must be rejected if the license has expired.

Reservation Quota Enforcement: Each employee has a configurable reservation limit. The system must prevent employees from exceeding their active reservation quota.

Availability Enforcement: Vehicles can be reserved only when their status is AVAILABLE. Vehicles marked as RESERVED, IN_USE, MAINTENANCE, or OUT_OF_SERVICE cannot be booked.

Maintenance Blocking: Vehicles scheduled for maintenance must be automatically excluded from reservation availability during the maintenance window.

Check-Out Workflow: Before using a vehicle, employees must perform a check-out operation. Vehicle status changes from RESERVED to IN_USE.

Check-In Workflow: Upon trip completion, employees must check the vehicle back in. The system records trip completion details and restores vehicle availability.

Trip Tracking Validation: Every completed trip must record starting and ending odometer readings along with fuel levels before and after the trip. Invalid mileage or fuel data must be rejected.

Audit Trail Generation: Every vehicle-related action must be logged, including reservations, check-outs, check-ins, cancellations, and maintenance activities. Logs must retain employee, vehicle, department, timestamp, and action details.

Ambiguity Areas for Developers to Resolve

Concurrent Reservation Handling: How should the system safely process simultaneous reservation requests for the same vehicle and overlapping time period without causing double bookings or inconsistent reservation records? 

Vehicle Status Management: Should vehicle status be stored directly in the database and updated on every operation, or should it be dynamically derived from active reservations and maintenance schedules?

Automatic Trip Expiry: How should the system handle vehicles that remain checked out beyond their expected return time and were never formally checked back in?

Maintenance Conflict Validation: How should future maintenance schedules be validated against existing reservations to prevent scheduling conflicts?

Transactional Consistency: How can reservation creation, vehicle status updates, trip tracking updates, and audit log creation be executed atomically so that partial failures do not leave inconsistent system data?


## Overview

The Corporate Vehicle Pool Management System is a backend fleet management platform designed to manage a company's shared vehicle fleet, including cars, bikes, and vans used for official business activities such as client visits, inter-office travel, and field operations.

The system ensures efficient vehicle allocation, prevents double bookings, tracks vehicle utilization, automates maintenance scheduling, and maintains a complete audit trail of vehicle activities.

Built using FastAPI, PostgreSQL, SQLAlchemy, Alembic, and Pydantic.

---

## Business Value

Organizations with shared vehicle fleets often face challenges such as:

* Vehicle overbooking
* Lack of maintenance visibility
* Inefficient allocation
* Missing trip records
* Poor accountability

This system addresses these issues through reservation controls, trip tracking, maintenance automation, and audit logging.

---

## Core Features

### Department Management

* Create Departments
* View Departments
* Update Departments
* Delete Departments

### Employee Management

* Employee Registration
* Department Assignment
* Driving License Validation
* Vehicle Reservation Quota Management

### Vehicle Management

* Vehicle Registration
* Vehicle Status Tracking
* Odometer Tracking
* Department-Based Allocation

### Vehicle Reservation

* Reserve Available Vehicles
* Prevent Double Booking
* Department Authorization Validation
* Reservation Quota Enforcement
* Driving License Verification

### Trip Management

* Vehicle Check-Out Workflow
* Vehicle Check-In Workflow
* Fuel Tracking
* Odometer Tracking
* Trip Validation
* Overdue Trip Detection

### Maintenance Management

* Automatic Maintenance Scheduling
* Maintenance Completion Workflow
* Maintenance Blocking
* Maintenance Threshold Tracking

### Vehicle Audit Logs

The system maintains complete logs for:

* Vehicle Created
* Vehicle Reserved
* Vehicle Checked Out
* Vehicle Checked In
* Reservation Cancelled
* Maintenance Started
* Maintenance Completed
* Overdue Trips

---

## Business Rules Implemented

### Department-Based Access Control

Employees can reserve only vehicles that belong to their department.

### Driver Eligibility Validation

Reservations are rejected when:

* Driving license has expired

### Reservation Quota Enforcement

Each employee has a configurable reservation quota.

The system prevents employees from exceeding their active reservation limit.

### Vehicle Availability Validation

Reservations are allowed only when vehicle status is:

* AVAILABLE

Reservations are blocked when status is:

* RESERVED
* IN_USE
* MAINTENANCE
* OUT_OF_SERVICE

### Maintenance Blocking

Vehicles scheduled for maintenance are automatically excluded from reservation availability.

### Trip Validation

The system validates:

* Ending odometer cannot be less than starting odometer
* Fuel levels must be valid
* Vehicle must be checked out before check-in

---

## Vehicle Lifecycle

```text
AVAILABLE
    ↓
RESERVED
    ↓
IN_USE
    ↓
AVAILABLE
```

Maintenance Flow:

```text
AVAILABLE
    ↓
RESERVED
    ↓
IN_USE
    ↓
MAINTENANCE
    ↓
AVAILABLE
```

---

## Database Design

### Department

| Field | Type    |
| ----- | ------- |
| id    | Integer |
| title | String  |

### Employee

| Field                | Type     |
| -------------------- | -------- |
| id                   | Integer  |
| name                 | String   |
| department_id        | Integer  |
| driving_license_date | DateTime |
| vehicle_quota        | Integer  |

### Vehicle

| Field                | Type    |
| -------------------- | ------- |
| id                   | Integer |
| type                 | String  |
| number               | String  |
| department_id        | Integer |
| status               | Enum    |
| current_odometer     | Integer |
| maintenance_intervel | Integer |
| maintenance_atkms    | Integer |

### Vehicle Reservation

| Field             | Type     |
| ----------------- | -------- |
| id                | Integer  |
| vehicle_id        | Integer  |
| employee_id       | Integer  |
| department_id     | Integer  |
| reservation_start | DateTime |
| reservation_end   | DateTime |

### Trip

| Field             | Type     |
| ----------------- | -------- |
| id                | Integer  |
| reservation_id    | Integer  |
| start_odometer    | Integer  |
| end_odometer      | Integer  |
| fuel_level_before | Integer  |
| fuel_level_after  | Integer  |
| expected_end_time | DateTime |
| actual_end_time   | DateTime |
| check_in_time     | DateTime |

### Maintenance Schedule

| Field             | Type     |
| ----------------- | -------- |
| id                | Integer  |
| vehicle_id        | Integer  |
| maintenance_start | DateTime |
| maintenance_end   | DateTime |
| description       | String   |

### Vehicle Logs

| Field         | Type     |
| ------------- | -------- |
| id            | Integer  |
| vehicle_id    | Integer  |
| employee_id   | Integer  |
| department_id | Integer  |
| timestamp     | DateTime |
| action        | Enum     |

---

## Vehicle Status Enum

```python
AVAILABLE
RESERVED
IN_USE
MAINTENANCE
OUT_OF_SERVICE
```

---

## Vehicle Log Actions

```python
CREATED
RESERVED
CHECKED_OUT
CHECKED_IN
CANCELLED
MAINTENANCE_STARTED
MAINTENANCE_COMPLETED
OVERDUE
```

---

## Ambiguity Resolution Decisions

### Concurrent Reservation Handling

Implemented using:

```python
with db.begin()
with_for_update()
```

to prevent double bookings and race conditions.

### Vehicle Status Management

Vehicle status is stored directly in the database and updated on every operation.

This improves query performance and simplifies availability checks.

### Automatic Trip Expiry

Trips exceeding their expected return time are marked as:

```python
OVERDUE
```

and logged in the audit trail.

### Maintenance Conflict Validation

The system validates that no active maintenance schedule already exists before creating a new maintenance schedule.

### Transactional Consistency

Reservation creation, status updates, trip tracking, maintenance scheduling, and audit logging are executed within database transactions to avoid partial failures.

---

## API Modules

### Departments

* Create Department
* Get Departments
* Get Department by ID
* Update Department
* Delete Department

### Employees

* Create Employee
* Get Employees
* Get Employee by ID
* Update Employee
* Delete Employee

### Vehicles

* Create Vehicle
* Get Vehicles
* Get Vehicle Status
* Vehicle Logs

### Vehicle Reservations

* Create Reservation
* Get Reservations

### Trips

* Vehicle Checkout
* Vehicle Check-In
* Overdue Tracking

### Maintenance

* Create Maintenance Schedule
* Complete Maintenance
* Get Maintenance Records

---

## Tech Stack

### Backend

* FastAPI

### Database

* PostgreSQL

### ORM

* SQLAlchemy

### Database Migrations

* Alembic

### Validation

* Pydantic

### API Documentation

* Swagger UI

---

## Running the Project

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Migrations

```bash
alembic upgrade head
```

Start Server

```bash
uvicorn app.main:app --reload
```

Swagger Documentation

```text
http://localhost:8000/docs
```

---

## Future Enhancements

* JWT Authentication
* Role-Based Access Control
* Vehicle Reservation Time Slots
* Notification Service
* Email Alerts
* Dashboard Analytics
* Fleet Utilization Reports
* GPS Integration

---

## Author

**Pendikatla Sri RamaKanth**

AI/ML Enthusiast | Backend Developer | FastAPI Developer
