const app = new Vue(
    {
        el: "#vue_div",
        data: {
            students: [],
            student_to_create_name: ""
        },
        methods: {
            deleteClickedStudent: function(event) {
                var student_index = $(event.target.parentElement).attr("data-student-index");
                // Delete the clicked student from the server.
                console.log(event.target);
                deleteStudent(this.students[student_index].student_id);
                // Remove the clicked student from the Vue.js template.
                this.students.splice(student_index, 1);
            },
            createStudentOnClick: function(event) {
                var self = this;
                var student_name = self.student_to_create_name;
                self.student_to_create_name = "";
                createStudent(student_name).then(function(student_id) {
                    self.students.push(new Student(student_id, student_name));
                });
            }
        },
        mounted: function() {
            // JS hackery.
            var self = this;
            // Retrieve students from the server.
            retrieveStudents().then((students) => {
                console.log(`${students.length} students retrieved from server.`);
                self.students = students;
            });
        }
    }
);
