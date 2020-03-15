SELECT * FROM scores
    INNER JOIN student_schedules
        ON scores.student_schedule_id = student_schedules.student_schedule_id
    INNER JOIN students
        ON student_schedules.student_id = students.student_id
    WHERE
        student_name = "Neil Parkhi"
    ORDER BY
        score_id ASC;
