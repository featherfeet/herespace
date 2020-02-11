const app = new Vue(
    {
        el: "#vue_div",
        data: {
            students: [],
            klass_editor: null
        },
        methods: {
            addStudentToSeatingChart: function(event) {
                var student_select = $("#student_select")[0];
                var student = new Student(student_select.value, student_select[student_select.selectedIndex].text);
                var student_schedule = new StudentSchedule(-1, student, -1);
                var seating = new Seating(-1, student_schedule, 200, 200, 200, 200, 0);
                this.klass_editor.addSeating(seating);
            }
        },
        mounted: function() {
            // JS hackery so that the Vue object can be accessed by Promise callbacks.
            var self = this;
            // Retrieve students from the server.
            retrieveStudents().then((students) => {
                console.log(`${students.length} students retrieved from server.`);
                self.students = students;
            });
            // Initialize the canvas's klass editor.
            var canvas = $("canvas")[0];
            var rotate_seating_slider = $("#rotate_seating_slider")[0];
            self.klass_editor = new KlassEditor(canvas, rotate_seating_slider);
        }
    }
);
