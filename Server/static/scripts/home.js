const app = new Vue(
    {
        el: "#vue_div",
        data: {
            students: []
        },
        methods: {
            deleteClickedStudent: function(event) {
                var student_index = $(event.target.parentElement).attr("data-student-index");
                // Delete the clicked student from the server.
                console.log(event.target);
                deleteStudent(this.students[student_index].student_id);
                // Remove the clicked student from the Vue.js template.
                this.students.splice(student_index, 1);
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
