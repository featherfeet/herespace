const app = new Vue(
    {
        el: "#vue_div",
        data: {
            klass_editor_editable: false,
            klass_id: -1,
            assignments: [],
            assignment_to_create_name: "",
            assignment_to_create_points: "",
            selected_assignment_id: -1
        },
        methods: {
            deleteClickedAssignment: function(event) {
                var assignment_index = $(event.target.parentElement).attr("data-assignment-index");
                // Delete the clicked assignment from the server.
                deleteAssignment(this.assignments[assignment_index].assignment_id);
                // Remove the clicked assignment from the Vue.js template.
                this.assignments.splice(assignment_index, 1);
            },
            createAssignmentOnClick: function(event) {
                var self = this;
                var assignment_name = self.assignment_to_create_name;
                var assignment_points = self.assignment_to_create_points;
                self.assignment_to_create_name = "";
                self.assignment_to_create_points = "";
                createAssignment(assignment_name, assignment_points, self.klass_id).then(function(assignment_id) {
                    self.assignments.push(new Assignment(assignment_id, -1, self.klass_id, assignment_name, assignment_points));
                });
            },
            assignmentSelected: function() {
                var self = this;
                self.selected_assignment_id = parseInt($("#assignment_select").val());
                retrieveScoresByAssignmentId(self.selected_assignment_id).then(function(scores) {
                    self.$refs.klass_editor.setScores(scores);
                });
            },
            handleScoreIncremented: function(seating) {
                console.log(`Score incremented for student "${seating.student_schedule.student.student_name}" on assignment with id ${this.selected_assignment_id}.`);
                seating.score += 1.0;
                addScore(this.selected_assignment_id, seating.student_schedule.student_schedule_id, seating.score);
            },
            handleScoreDecremented: function(seating) {
                console.log(`Score decremented for student "${seating.student_schedule.student.student_name}" on assignment with id ${this.selected_assignment_id}.`);
                seating.score -= 1.0;
                addScore(this.selected_assignment_id, seating.student_schedule.student_schedule_id, seating.score);
            }
        },
        mounted: function() {
            var self = this;

            const raw_url = window.location.href;
            const url = new URL(raw_url);
            self.klass_id = parseInt(url.searchParams.get("klass_id"));

            retrieveSeatings(self.klass_id).then(function(seatings) {
                self.$refs.klass_editor.setSeatings(seatings);
            });

            retrieveAssignmentsByKlassId(self.klass_id).then((assignments) => {
                console.log(`${assignments.length} assignments retrieved from server.`);
                self.assignments = assignments;
            });
        }
    }
);
