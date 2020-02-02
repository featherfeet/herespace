var canvas = $("canvas")[0];
var klass_editor = new KlassEditor(canvas);
var student = new Student(-1, "Oliver Trevor");
var student_schedule = new StudentSchedule(-1, student, 1);
var seating = new Seating(-1, student_schedule, 200, 200, 200, 200, Math.sqrt(2.0) / 2.0 * Math.PI);
klass_editor.addSeating(seating);
