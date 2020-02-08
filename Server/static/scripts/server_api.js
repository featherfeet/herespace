// Represents a student from the "students" table in the database.
class Student {
    constructor(student_id, student_name) {
        this.student_id = student_id;
        this.student_name = student_name;
    }
}

// Represents a student scheduling object from the "student_schedules" database table.
class StudentSchedule {
    constructor(student_schedule_id, student, klass_id) {
        this.student_schedule_id = student_schedule_id;
        this.student = student;
        this.klass_id = klass_id;
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

    // Check if this seating contains a geometric point.
    containsPoint(x, y) {
        // Returns true if the point is within half of a diagonal of the center of the desk. This makes grabbing rotated desks easier.
        var desk_diagonal = Math.hypot(this.desk_width, this.desk_height);
        return distance(x, y, this.desk_x + this.desk_width / 2.0, this.desk_y + this.desk_height / 2.0) <= desk_diagonal / 2.0;
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
