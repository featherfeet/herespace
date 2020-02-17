-- Saves the version of this database's schema.
CREATE TABLE IF NOT EXISTS schema_version_data
(
    schema_version INT
);

CREATE UNIQUE INDEX schema_unique_index ON schema_version_data (schema_version);

INSERT OR IGNORE INTO schema_version_data VALUES (1);

-- Stores all users of the system.
CREATE TABLE IF NOT EXISTS users
(
    user_id INTEGER PRIMARY KEY,            -- Each user has a unique id.
    username TEXT,                          -- Username of the user.
    password_hashed_and_salted TEXT,        -- hashlib.hash's pbkdf2_sha512 hash with salt.
    email TEXT,                             -- User's email.
    user_type TEXT,                         -- Either "teacher" or "student".
    student_id INTEGER                      -- If user_type == "student", then this stores the id of the student that the account belongs to. Otherwise, NULL.
);

-- Each klass is a single section (period) of a class, taught by one teacher.
CREATE TABLE IF NOT EXISTS klasses
(
    klass_id INTEGER PRIMARY KEY,           -- Each klass has a unique id.
    user_id INTEGER,                        -- The klass owner (teacher)'s id.
    klass_name TEXT                         -- The title of the class (like "3rd period Engineering").
);

-- Each seating stores where a specific student sits in a specific klass.
CREATE TABLE IF NOT EXISTS seatings
(
    seating_id INTEGER PRIMARY KEY,         -- Each seating (a student-desk pairing) has a unique id.
    user_id INTEGER,                        -- Id of the user who owns this seating.
    student_schedule_id INTEGER,            -- References the student-klass pairing that is associated with this seating.
    desk_x REAL,                            -- x-coordinate on the klass diagram of this seat.
    desk_y REAL,                            -- y-coordinate on the klass diagram of this seat.
    desk_width REAL,                        -- width on the klass diagram of this seat.
    desk_height REAL,                       -- height on the klass diagram of this seat.
    desk_angle REAL                         -- angle of rotation of this seat on the klass diagram. measured in radians clockwise of horizontal.
);

-- Each student is stored as a row in the students table.
CREATE TABLE IF NOT EXISTS students
(
    student_id INTEGER PRIMARY KEY,         -- Each student has a unique id.
    student_name TEXT,                      -- The name of the student.
    user_id INTEGER                         -- The id of the teacher who "owns" this student.
);

-- This table stores which students are in which klasses.
CREATE TABLE IF NOT EXISTS student_schedules
(
    student_schedule_id INTEGER PRIMARY KEY, -- Each student-klass pairing has unique id.
    user_id INTEGER,                         -- The user who owns this student.
    student_id INTEGER,                      -- The id of the student who attends the class specified in klass_id.
    klass_id INTEGER                         -- The id of the klass attended by the student specified in student_id.
);

-- This table stores assignments, which are tasks assigned to students to earn points.
CREATE TABLE IF NOT EXISTS assignments
(
    assignment_id INTEGER PRIMARY KEY,       -- The assignment has a unique id.
    user_id INTEGER,                         -- Id of the user who owns this assignment.
    assignment_name TEXT,                    -- Title of the assignment.
    points REAL                              -- How many points the assignment is worth.
);
