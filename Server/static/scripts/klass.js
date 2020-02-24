const app = new Vue(
    {
        el: "#vue_div",
        data: {
            klass_editor: null,
            klass_id: -1,
            assignments: [],
            assignment_to_create_name: "",
            assignment_to_create_points: ""
        },
        methods: {
            deleteClickedAssignment: function(event) {
                var assignment_index = $(event.target.parentElement).attr("data-assignment-index");
                // Delete the clicked assignment from the server.
                console.log(event.target);
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
            }
        },
        mounted: function() {
            var self = this;

            const raw_url = window.location.href;
            const url = new URL(raw_url);
            self.klass_id = parseInt(url.searchParams.get("klass_id"));

            var canvas = $("canvas")[0];
            self.klass_editor = new KlassEditor(canvas, null, false);

            retrieveSeatings(self.klass_id).then(function(seatings) {
                self.klass_editor.setSeatings(seatings);
            });

            retrieveAssignmentsByKlassId(self.klass_id).then((assignments) => {
                console.log(`${assignments.length} assignments retrieved from server.`);
                self.assignments = assignments;
            });
        }
    }
);
