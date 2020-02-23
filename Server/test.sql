.headers on
.mode columns
SELECT * FROM student_schedules
   INNER JOIN seatings
       ON student_schedules.student_schedule_id = seatings.student_schedule_id
   INNER JOIN students
       ON student_schedules.student_id = students.student_id
   WHERE
       student_schedules.user_id = 1
       AND
       student_schedules.klass_id = 1;
