/*
var canvas = $("canvas")[0];
var klass_editor = new KlassEditor(canvas);
var student = new Student(-1, "Oliver Trevor");
var student_schedule = new StudentSchedule(-1, student, 1);
var seating = new Seating(-1, student_schedule, 200, 200, 200, 200, Math.sqrt(2.0) / 2.0 * Math.PI);
klass_editor.addSeating(seating);
*/

const app = new Vue(
    {
        el: "#vue_div",
        data: {
            students: [],
            klass_editor: null
        },
        methods: {

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
            self.klass_editor = new KlassEditor(canvas);
        }
    }
);
