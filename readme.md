Corporate Vehicle Pool Management System
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


----------------------------------------------------------------------------------------------------------------------------------
Entities : 
Department
    id
    title

Employee
    id
    name
    department_id
    driving_license_date
    vehicle_quota

Vehicle
    id
    type
    department_id

Vehicle_Reservation
    id
    vehicle_id
    employee_id
    department_id
    reservation_start
    reservation_end

Maintenance_Schedule
    id
    vehicle_id
    maintenance_start
    maintenance_end
    description

Vehicle_status :ENUM
    AVAILABLE
    RESERVED
    IN_USE
    MAINTENANCE
    OUT_OF_SERVICE

Vehicle_Logs
    id
    vehicle_id
    employee_id
    department_id
    timestamp
    action:
        RESERVED
        CHECKED_OUT
        CHECKED_IN
        CANCELLED
        MAINTENANCE_STARTED
        MAINTENANCE_COMPLETED 

Trip
    id
    reservation_id
    start_odometer
    end_odometer
    fuel_level_before
    fuel_level_after
    check_out_time
    check_in_time


routes and services for vehicle usage table :

1.vehicle_assignment : id,Department_id,Employee_id,vehicle_id)
check for deparmtent , employee , vehicle , employee driving_licence validity
check for employee quota . ----
check for vechile status = available



###check for maintenance blocking : if vehicle is scheduled for maintenance then availability == false  
vehicle status update to reserved (upto 30min)

vehicle assigned.

update transaction in logs table with timestamp


2.vehicle checkout work flow : 

check for employee_id
check vehicle_id , status = reserved then checkout 
trip start date ==datetime.now()
trip ending date == start date + 24hrs(timedelta) 
fill the fields of vehicle : odometer , fuel , checkout time = current time 
update vehicle status to in use (db.commit())

update transaction in logs table with timestamp



3.vehicle Checkin workflow:
   -----------------------------------------> validations: 

   ending_odometer < starting_odometer
   
check vehicel_id , status = use in then check in or invalid 
update  the fields of vehicle : odometer,fuel , return time = current time

update vehicle_status = AVAILABLE 
vechicle trip count +1
update transaction in logs table with timestamp


4.maintenance:
   if vehicle  maintenance_trips_count == vehicle.trip count 
      return Vehicle_status update = "MAINTENANCE"
commit()
update transaction in logs table with timestamp

### vehicle -> checkin,status-available(not in maintenace), 
### if vehicle overdue and maintenance start date >now -> staatus -> Maintenance 

5.maintenance_expiry:

      if Vehicle_status == maintenance > timedelta (3days)
            return vechicle_status update = AVAILABLE

update transaction in logs table with timestamp


6.overdue:

if (
    vehicle.status == CHECKED_OUT
    and datetime.utcnow() > trip return date
):
    vehicle.status = OVERDUE
####
7. if trip_count +1 then quota -1 ---->

---------------------------------------------------------------------

concurrency handling -------> with db.begin() , with_for_update

update database for ecery operation -------> commit() , flush()