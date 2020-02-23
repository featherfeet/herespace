const app = new Vue(
    {
        el: "#vue_div",
        data: {
            students: [],
            klass_editor: null,
            klass_name: ""
        },
        methods: {
            addStudentToSeatingChart: function() {
                var student_select = $("#student_select")[0];
                if (student_select.selectedIndex == -1) {
                    return;
                }
                var student = new Student(student_select.value, student_select[student_select.selectedIndex].text);
                var student_schedule = new StudentSchedule(-1, student, -1);
                var seating = new Seating(-1, student_schedule, 200, 200, 200, 100, 0);
                this.klass_editor.addSeating(seating);
                this.students.splice(student_select.selectedIndex, 1);
            },
            finishCreatingKlass: function() {
                if (this.klass_name === "") {
                    alert("You must enter a name for this class.");
                    return;
                }
                var seatings = this.klass_editor.getSeatings();
                var payload = {"klass_name": this.klass_name, "seatings": seatings};
                $.post("/create_klass", {"json": JSON.stringify(payload)}, function() {
                    window.location.replace("/home");
                });
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
            self.klass_editor = new KlassEditor(canvas, rotate_seating_slider, true);
        }
    }
);
