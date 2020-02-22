import sqlite3
import threading
from passlib.hash import pbkdf2_sha512
from storage.user import User
from storage.klass import Klass
from storage.student import Student

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

class DatabaseStorage:
    def __init__(self, database_path):
        self.conn_lock = threading.Lock()
        self.conn = sqlite3.connect(database_path, check_same_thread = False, isolation_level = None)
        self.cursor = self.conn.cursor()
        # Enable foreign keys so that DELETE CASCADE columns automatically delete all data related to deleted objects (see "createschema.sql").
        self.cursor.execute("PRAGMA foreign_keys = on")

    def loadUser(self, user_id):
        users = self.cursor.execute("SELECT user_id, username, password_hashed_and_salted, email, user_type, student_id FROM users WHERE user_id = ?", (user_id,))
        user = users.fetchone()
        if user is None:
            return None
        return User(user_id, user[USERS_TABLE_USERNAME_COLUMN], user[USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN], user[USERS_TABLE_EMAIL_COLUMN], user[USERS_TABLE_USER_TYPE_COLUMN], user[USERS_TABLE_STUDENT_ID_COLUMN], is_authenticated = True, is_active = True, is_anonymous = False)

    def verifyUser(self, username, password):
        users = self.cursor.execute("SELECT user_id, username, password_hashed_and_salted, email, user_type, student_id FROM users WHERE username = ?", (username,))
        user = users.fetchone()
        if user is None:
            return None
        if pbkdf2_sha512.verify(password, user[USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN]):
            return User(user[USERS_TABLE_USER_ID_COLUMN], username, user[USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN], user[USERS_TABLE_EMAIL_COLUMN], user[USERS_TABLE_USER_TYPE_COLUMN], user[USERS_TABLE_STUDENT_ID_COLUMN], is_authenticated = True, is_active = True, is_anonymous = False)
        return None

    def createTeacherUser(self, username, password, email):
        password_hashed_and_salted = pbkdf2_sha512.hash(password)
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO users (username, password_hashed_and_salted, email, user_type, student_id) VALUES (?, ?, ?, 'teacher', NULL)", (username, password_hashed_and_salted, email))
        user_id = self.cursor.lastrowid
        self.conn_lock.release()
        return User(user_id, username, password_hashed_and_salted, email, "teacher", None, is_authenticated = True, is_active = True, is_anonymous = False)

    def fetchKlassesByUserId(self, user_id):
        klasses_raw = self.cursor.execute("SELECT klass_id, user_id, klass_name FROM klasses WHERE user_id = ?", (user_id,))
        klasses = []
        for klass_raw in klasses_raw:
            klasses.append(Klass(klass_raw[KLASSES_TABLE_KLASS_ID_COLUMN], klass_raw[KLASSES_TABLE_USER_ID_COLUMN], klass_raw[KLASSES_TABLE_KLASS_NAME_COLUMN]))
        return klasses

    def fetchKlassByKlassId(self, user_id, klass_id):
        klasses_raw = self.cursor.execute("SELECT klass_id, user_id, klass_name FROM klasses WHERE user_id = ? AND klass_id = ?", (user_id, klass_id))
        klass_raw = klasses_raw.fetchone()
        if klass_raw is not None:
            return Klass(klass_raw[KLASSES_TABLE_KLASS_ID_COLUMN], klass_raw[KLASSES_TABLE_USER_ID_COLUMN], klass_raw[KLASSES_TABLE_KLASS_NAME_COLUMN])
        return None

    def fetchStudents(self, user_id):
        students_raw = self.cursor.execute("SELECT student_id, student_name, user_id FROM students WHERE user_id = ?", (user_id,))
        students = []
        for student_raw in students_raw:
            students.append(Student(student_raw[STUDENTS_TABLE_STUDENT_ID_COLUMN], student_raw[STUDENTS_TABLE_STUDENT_NAME_COLUMN], student_raw[STUDENTS_TABLE_USER_ID_COLUMN]))
        return students

    def deleteStudentByStudentId(self, user_id, student_id):
        try:
            student_id = int(student_id)
        except ValueError:
            return
        self.cursor.execute("DELETE FROM students WHERE user_id = ? AND student_id = ?", (user_id, student_id))

    def createStudent(self, user_id, student_name):
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO students (student_name, user_id) VALUES (?, ?)", (student_name, user_id))
        student_id = self.cursor.lastrowid
        self.conn_lock.release()
        return student_id

    def createKlass(self, user_id, klass_name):
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO klasses (user_id, klass_name) VALUES (?, ?)", (user_id, klass_name))
        klass_id = self.cursor.lastrowid
        self.conn_lock.release()
        return klass_id

    def createStudentSchedule(self, user_id, student_id, klass_id):
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO student_schedules (user_id, student_id, klass_id) VALUES (?, ?, ?)", (user_id, student_id, klass_id))
        student_schedule_id = self.cursor.lastrowid
        self.conn_lock.release()
        return student_schedule_id

    def createSeating(self, user_id, student_schedule_id, desk_x, desk_y, desk_width, desk_height, desk_angle):
        self.conn_lock.acquire()
        self.cursor.execute("INSERT INTO seatings (user_id, student_schedule_id, desk_x, desk_y, desk_width, desk_height, desk_angle) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, student_schedule_id, desk_x, desk_y, desk_width, desk_height, desk_angle))
        seating_id = self.cursor.lastrowid
        self.conn_lock.release()
        return seating_id
