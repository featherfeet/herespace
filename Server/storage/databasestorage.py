import sqlite3
import threading
from passlib.hash import pbkdf2_sha512
from storage.user import User
from storage.klass import Klass
from storage.student import Student
from storage.studentschedule import StudentSchedule
from storage.seating import Seating
from storage.assignment import Assignment
from storage.score import Score

USERS_TABLE_USER_ID_COLUMN = 0
USERS_TABLE_USERNAME_COLUMN = 1
USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN = 2
USERS_TABLE_EMAIL_COLUMN = 3
USERS_TABLE_USER_TYPE_COLUMN = 4
USERS_TABLE_STUDENT_ID_COLUMN = 5

KLASSES_TABLE_KLASS_ID_COLUMN = 0
KLASSES_TABLE_USER_ID_COLUMN = 1
KLASSES_TABLE_KLASS_NAME_COLUMN = 2

STUDENTS_TABLE_STUDENT_ID_COLUMN = 0
STUDENTS_TABLE_STUDENT_NAME_COLUMN = 1
STUDENTS_TABLE_USER_ID_COLUMN = 2

ASSIGNMENTS_TABLE_ASSIGNMENT_ID_COLUMN = 0
ASSIGNMENTS_TABLE_USER_ID_COLUMN = 1
ASSIGNMENTS_TABLE_KLASS_ID_COLUMN = 2
ASSIGNMENTS_TABLE_ASSIGNMENT_NAME_COLUMN = 3
ASSIGNMENTS_TABLE_POINTS_COLUMN = 4

class DatabaseStorage:
    def __init__(self, database_path):
        self.conn_lock = threading.Lock()
        self.conn = sqlite3.connect(database_path, check_same_thread = False, isolation_level = None)
        self.cursor = self.conn.cursor()
        # Enable foreign keys so that DELETE CASCADE columns automatically delete all data related to deleted objects (see "createschema.sql").
        self.cursor.execute("PRAGMA foreign_keys = on")

    def loadUser(self, user_id):
        user_id = int(user_id)
        
        self.conn_lock.acquire()
        users = self.cursor.execute("SELECT user_id, username, password_hashed_and_salted, email, user_type, student_id FROM users WHERE user_id = ?", (user_id,))
        user = users.fetchone()
        self.conn_lock.release()
        if user is None:
            return None
        return User(user_id, user[USERS_TABLE_USERNAME_COLUMN], user[USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN], user[USERS_TABLE_EMAIL_COLUMN], user[USERS_TABLE_USER_TYPE_COLUMN], user[USERS_TABLE_STUDENT_ID_COLUMN], is_authenticated = True, is_active = True, is_anonymous = False)

    def verifyUser(self, username, password):
        username = str(username)
        password = str(password)
        
        self.conn_lock.acquire()
        users = self.cursor.execute("SELECT user_id, username, password_hashed_and_salted, email, user_type, student_id FROM users WHERE username = ?", (username,))
        user = users.fetchone()
        self.conn_lock.release()
        if user is None:
            return None
        if pbkdf2_sha512.verify(password, user[USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN]):
            return User(user[USERS_TABLE_USER_ID_COLUMN], username, user[USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN], user[USERS_TABLE_EMAIL_COLUMN], user[USERS_TABLE_USER_TYPE_COLUMN], user[USERS_TABLE_STUDENT_ID_COLUMN], is_authenticated = True, is_active = True, is_anonymous = False)
        return None

    def createTeacherUser(self, username, password, email):
        username = str(username)
        password = str(password)
        email = str(email)
        
        password_hashed_and_salted = pbkdf2_sha512.hash(password)
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO users (username, password_hashed_and_salted, email, user_type, student_id) VALUES (?, ?, ?, 'teacher', NULL)", (username, password_hashed_and_salted, email))
        user_id = self.cursor.lastrowid
        self.conn_lock.release()
        return User(user_id, username, password_hashed_and_salted, email, "teacher", None, is_authenticated = True, is_active = True, is_anonymous = False)

    def fetchKlassesByUserId(self, user_id):
        user_id = int(user_id)
        
        self.conn_lock.acquire()
        klasses_raw = self.cursor.execute("SELECT klass_id, user_id, klass_name FROM klasses WHERE user_id = ?", (user_id,))
        klasses = []
        for klass_raw in klasses_raw:
            klasses.append(Klass(klass_raw[KLASSES_TABLE_KLASS_ID_COLUMN], klass_raw[KLASSES_TABLE_USER_ID_COLUMN], klass_raw[KLASSES_TABLE_KLASS_NAME_COLUMN]))
        self.conn_lock.release()
        return klasses

    def fetchKlassByKlassId(self, user_id, klass_id):
        user_id = int(user_id)
        klass_id = int(klass_id)

        self.conn_lock.acquire()
        klasses_raw = self.cursor.execute("SELECT klass_id, user_id, klass_name FROM klasses WHERE user_id = ? AND klass_id = ?", (user_id, klass_id))
        klass_raw = klasses_raw.fetchone()
        self.conn_lock.release()
        if klass_raw is not None:
            return Klass(klass_raw[KLASSES_TABLE_KLASS_ID_COLUMN], klass_raw[KLASSES_TABLE_USER_ID_COLUMN], klass_raw[KLASSES_TABLE_KLASS_NAME_COLUMN])
        return None

    def fetchStudents(self, user_id):
        user_id = int(user_id)
        
        self.conn_lock.acquire()
        students_raw = self.cursor.execute("SELECT student_id, student_name, user_id FROM students WHERE user_id = ?", (user_id,))
        students = []
        for student_raw in students_raw:
            students.append(Student(student_raw[STUDENTS_TABLE_STUDENT_ID_COLUMN], student_raw[STUDENTS_TABLE_STUDENT_NAME_COLUMN], student_raw[STUDENTS_TABLE_USER_ID_COLUMN]))
        self.conn_lock.release()
        return students

    def deleteStudentByStudentId(self, user_id, student_id):
        user_id = int(user_id)
        student_id = int(student_id)

        try:
            student_id = int(student_id)
        except ValueError:
            return
        self.conn_lock.acquire()
        self.cursor.execute("DELETE FROM students WHERE user_id = ? AND student_id = ?", (user_id, student_id))
        self.conn_lock.release()

    def createStudent(self, user_id, student_name):
        user_id = int(user_id)
        student_name = str(student_name)
        
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO students (student_name, user_id) VALUES (?, ?)", (student_name, user_id))
        student_id = self.cursor.lastrowid
        self.conn_lock.release()
        return student_id

    def createKlass(self, user_id, klass_name):
        user_id = int(user_id)
        klass_name = str(klass_name)
        
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO klasses (user_id, klass_name) VALUES (?, ?)", (user_id, klass_name))
        klass_id = self.cursor.lastrowid
        self.conn_lock.release()
        return klass_id

    def createStudentSchedule(self, user_id, student_id, klass_id):
        user_id = int(user_id)
        student_id = int(student_id)
        klass_id = int(klass_id)
        
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO student_schedules (user_id, student_id, klass_id) VALUES (?, ?, ?)", (user_id, student_id, klass_id))
        student_schedule_id = self.cursor.lastrowid
        self.conn_lock.release()
        return student_schedule_id

    def createSeating(self, user_id, student_schedule_id, desk_x, desk_y, desk_width, desk_height, desk_angle):
        user_id = int(user_id)
        student_schedule_id = int(student_schedule_id)
        desk_x = float(desk_x)
        desk_y = float(desk_y)
        desk_width = float(desk_width)
        desk_height = float(desk_height)
        desk_angle = float(desk_angle)
        
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO seatings (user_id, student_schedule_id, desk_x, desk_y, desk_width, desk_height, desk_angle) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, student_schedule_id, desk_x, desk_y, desk_width, desk_height, desk_angle))
        seating_id = self.cursor.lastrowid
        self.conn_lock.release()
        return seating_id

    def fetchSeatingsByKlassId(self, user_id, klass_id):
        user_id = int(user_id)
        klass_id = int(klass_id)
        
        self.conn_lock.acquire()
        raw_data = self.cursor.execute("""SELECT seatings.seating_id, seatings.student_schedule_id, seatings.desk_x, seatings.desk_y, seatings.desk_width, seatings.desk_height, seatings.desk_angle, students.student_id, students.student_name FROM student_schedules
                                   INNER JOIN seatings
                                       ON student_schedules.student_schedule_id = seatings.student_schedule_id
                                   INNER JOIN students
                                       ON student_schedules.student_id = students.student_id
                                   WHERE
                                       student_schedules.user_id = ?
                                       AND
                                       student_schedules.klass_id = ?""", (user_id, klass_id))
        seatings = []
        for row in raw_data:
            seating_id = row[0]
            student_schedule_id = row[1]
            desk_x = row[2]
            desk_y = row[3]
            desk_width = row[4]
            desk_height = row[5]
            desk_angle = row[6]
            student_id = row[7]
            student_name = row[8]

            student = Student(student_id, student_name, user_id)
            student_schedule = StudentSchedule(student_schedule_id, student, klass_id)
            seating = Seating(seating_id, student_schedule, desk_x, desk_y, desk_width, desk_height, desk_angle)

            seatings.append(seating)
        self.conn_lock.release()
        return seatings

    def createAssignment(self, user_id, klass_id, assignment_name, points):
        user_id = int(user_id)
        klass_id = int(klass_id)
        assignment_name = str(assignment_name)
        points = float(points)

        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO assignments (user_id, klass_id, assignment_name, points) VALUES (?, ?, ?, ?)", (user_id, klass_id, assignment_name, points))
        assignment_id = self.cursor.lastrowid
        self.conn_lock.release()
        return assignment_id
        
    def deleteAssignmentByAssignmentId(self, user_id, assignment_id):
        user_id = int(user_id)
        assignment_id = int(assignment_id)

        self.conn_lock.acquire()
        self.cursor.execute("DELETE FROM assignments WHERE user_id = ? AND assignment_id = ?", (user_id, assignment_id))
        self.conn_lock.release()
        
    def fetchAssignmentsByKlassId(self, user_id, klass_id):
        user_id = int(user_id)
        klass_id = int(klass_id)

        self.conn_lock.acquire()
        assignments_raw = self.cursor.execute("SELECT assignment_id, user_id, klass_id, assignment_name, points FROM assignments WHERE user_id = ? AND klass_id = ?", (user_id, klass_id))
        assignments = []

        for assignment_raw in assignments_raw:
            assignment_id = int(assignment_raw[ASSIGNMENTS_TABLE_ASSIGNMENT_ID_COLUMN])
            user_id = int(assignment_raw[ASSIGNMENTS_TABLE_USER_ID_COLUMN])
            klass_id = int(assignment_raw[ASSIGNMENTS_TABLE_KLASS_ID_COLUMN])
            assignment_name = str(assignment_raw[ASSIGNMENTS_TABLE_ASSIGNMENT_NAME_COLUMN])
            points = float(assignment_raw[ASSIGNMENTS_TABLE_POINTS_COLUMN])
            
            assignment = Assignment(assignment_id, user_id, klass_id, assignment_name, points)
            assignments.append(assignment)

        self.conn_lock.release()

        return assignments

    def setScore(self, user_id, assignment_id, student_schedule_id, points):
        user_id = int(user_id)
        assignment_id = int(assignment_id)
        student_schedule_id = int(student_schedule_id)
        points = float(points)
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO scores (user_id, assignment_id, student_schedule_id, points) VALUES (?, ?, ?, ?)", (user_id, assignment_id, student_schedule_id, points))
        self.conn_lock.release()

    def getScoresByAssignmentId(self, user_id, assignment_id):
        self.conn_lock.acquire()
        scores_raw = self.cursor.execute("SELECT score_id, student_schedule_id, points FROM scores WHERE user_id = ? AND assignment_id = ?", (user_id, assignment_id))
        scores = []
        for score_raw in scores_raw:
            score_id = int(score_raw[0])
            student_schedule_id = int(score_raw[1])
            points = float(score_raw[2])

            score = Score(score_id, user_id, assignment_id, student_schedule_id, points)
            scores.append(score)
        self.conn_lock.release()
        return scores
