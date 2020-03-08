// Represents a student from the "students" table in the database.
class Student {
    constructor(student_id, student_name) {
        this.student_id = student_id;
        this.student_name = student_name;
    }

    // Take a raw object (usually one decoded from JSON) and turn it into a Student object (one where methods work).
    static fromRawObject(raw_student) {
        return new Student(
            raw_student.student_id,
            raw_student.student_name
        );
    }
}

// Represents a student scheduling object from the "student_schedules" database table.
class StudentSchedule {
    constructor(student_schedule_id, student, klass_id) {
        this.student_schedule_id = student_schedule_id;
        this.student = student;
        this.klass_id = klass_id;
    }

    // Take a raw object (usually one decoded from JSON) and turn it into a StudentSchedule object (one where methods work).
    static fromRawObject(raw_student_schedule) {
        var student = Student.fromRawObject(raw_student_schedule.student);
        return new StudentSchedule(
            raw_student_schedule.student_schedule_id,
            student,
            raw_student_schedule.klass_id
        );
    }
}

// Represents a student seating from the "seatings" table in the database.
class Seating {
    constructor(seating_id, student_schedule, desk_x, desk_y, desk_width, desk_height, desk_angle) {
        this.seating_id = seating_id;
        this.student_schedule = student_schedule;
        this.desk_x = desk_x;
        this.desk_y = desk_y;
        this.desk_width = desk_width;
        this.desk_height = desk_height;
        this.desk_angle = desk_angle;
    }

    // Calculate distance between two points.
    static distance(x1, y1, x2, y2) {
        return Math.hypot(x2 - x1, y2 - y1);
    }

    // Check if this seating contains a geometric point.
    containsPoint(x, y) {
        // Returns true if the point is within half of a diagonal of the center of the desk. This makes grabbing rotated desks easier.
        var desk_diagonal = Math.hypot(this.desk_width, this.desk_height);
        return Seating.distance(x, y, this.desk_x + this.desk_width / 2.0, this.desk_y + this.desk_height / 2.0) <= desk_diagonal / 2.0;
    }
    
    // Take a raw object (usually one decoded from JSON) and turn it into a Seating object (one where methods work).
    static fromRawObject(raw_seating) {
        var student_schedule = StudentSchedule.fromRawObject(raw_seating.student_schedule);
        return new Seating(raw_seating.seating_id,
                          student_schedule,
                          raw_seating.desk_x,
                          raw_seating.desk_y,
                          raw_seating.desk_width,
                          raw_seating.desk_height,
                          raw_seating.desk_angle);
    }
}

// Class to represent an assignment from the "assignments" table in the database.
class Assignment {
    constructor(assignment_id, user_id, klass_id, assignment_name, points) {
        this.assignment_id = assignment_id;
        this.user_id = user_id;
        this.klass_id = klass_id;
        this.assignment_name = assignment_name;
        this.points = points;
    }
    
    // Take a raw object (usually one decoded from JSON) and turn it into an Assignment object (one where methods work).
    static fromRawObject(raw_assignment) {
        return new Assignment(
            raw_assignment.assignment_id,
            raw_assignment.user_id,
            raw_assignment.klass_id,
            raw_assignment.assignment_name,
            raw_assignment.points
        );
    }
}

// Class to represent a score (one score that a student recieved at a specific time on a specific assignment). A student may have multiple scores per assignment (the one with the highest score_id is the most recent).
class Score {
    constructor(score_id, user_id, assignment_id, student_schedule_id, points) {
        this.score_id = score_id;
        this.user_id = user_id;
        this.assignment_id = assignment_id;
        this.student_schedule_id = student_schedule_id;
        this.points = points;
    }

    // Take a raw object (usually one decoded from JSON) and turn it into an Score object (one where methods work).
    static fromRawObject(raw_score) {
        return new Score(
            raw_score.score_id,
            raw_score.user_id,
            raw_score.assignment_id,
            raw_score.student_schedule_id,
            raw_score.points
        );
    }
}

// Retrieve all students from the server.
function retrieveStudents() {
    return new Promise(
        (resolve, reject) => {
            $.getJSON("/get_students", function(data) {
                var students = new Array();
                for (var i = 0; i < data.length; i++) {
                    students.push(new Student(data[i].student_id, data[i].student_name));
                }
                resolve(students);
            });
        }
    );
}

// Delete a student by id.
function deleteStudent(student_id_to_delete) {
    return new Promise(
        (resolve, reject) => {
            $.post("/delete_student", {student_id: student_id_to_delete}, function(data) {
                resolve();
            });
        }
    );
}

// Create a new student and return its id.
function createStudent(student_name_to_create) {
    return new Promise(
        (resolve, reject) => {
            $.post("/create_student", {student_name: student_name_to_create}, function(data) {
                resolve(parseInt(data));
            });
        }
    );
}

// Retrieve all seatings from a specific klass from the server.
function retrieveSeatings(klass_id_to_fetch) {
    return new Promise(
        (resolve, reject) => {
            $.getJSON("/get_seatings", {klass_id: klass_id_to_fetch}, function(seatings_raw) {
                var seatings = seatings_raw.map(seating_raw => Seating.fromRawObject(seating_raw));
                resolve(seatings);
            });
        }
    );
}

// Retrieve all assignments from a specific klass on the server.
function retrieveAssignmentsByKlassId(klass_id_to_fetch) {
    return new Promise(
        (resolve, reject) => {
            $.getJSON("/get_assignments", {klass_id: klass_id_to_fetch}, function(assignments_raw) {
                var assignments = assignments_raw.map(assignment_raw => Assignment.fromRawObject(assignment_raw));
                resolve(assignments);
            });
        }
    );
}

// Create a new assignment and return its id.
function createAssignment(assignment_name_to_create, assignment_points_to_create, klass_id_to_create) {
    return new Promise(
        (resolve, reject) => {
            $.post("/create_assignment", {assignment_name: assignment_name_to_create, assignment_points: assignment_points_to_create, klass_id: klass_id_to_create}, function(data) {
                resolve(parseInt(data));
            });
        }
    );
}

// Delete a assignment by id.
function deleteAssignment(assignment_id_to_delete) {
    return new Promise(
        (resolve, reject) => {
            $.post("/delete_assignment", {assignment_id: assignment_id_to_delete}, function(data) {
                resolve();
            });
        }
    );
}

// Retrieve the most recent scores for a specific assignment.
function retrieveScoresByAssignmentId(assignment_id_to_fetch) {
    return new Promise(
        (resolve, reject) => {
            $.getJSON("/get_scores", {assignment_id: assignment_id_to_fetch}, function(scores_raw) {
                var scores = scores_raw.map(score_raw => Score.fromRawObject(score_raw));
                resolve(scores);
            });
        }
    );
}
