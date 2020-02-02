import sqlite3
from passlib.hash import pbkdf2_sha512
from storage.user import User
from storage.klass import Klass

USERS_TABLE_USER_ID_COLUMN = 0
USERS_TABLE_USERNAME_COLUMN = 1
USERS_TABLE_PASSWORD_HASHED_AND_SALTED_COLUMN = 2
USERS_TABLE_EMAIL_COLUMN = 3
USERS_TABLE_USER_TYPE_COLUMN = 4
USERS_TABLE_STUDENT_ID_COLUMN = 5

KLASSES_TABLE_KLASS_ID_COLUMN = 0
KLASSES_TABLE_USER_ID_COLUMN = 1
KLASSES_TABLE_KLASS_NAME_COLUMN = 2

class DatabaseStorage:
    def __init__(self, database_path):
        self.conn = sqlite3.connect(database_path, check_same_thread = False)
        self.cursor = self.conn.cursor()

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

    def fetchKlassesByUserId(self, user_id):
        klasses_raw = self.cursor.execute("SELECT klass_id, user_id, klass_name FROM klasses WHERE user_id = ?", (user_id,))
        klasses = []
        for klass_raw in klasses_raw:
            klasses.append(Klass(klass_raw[KLASSES_TABLE_KLASS_ID_COLUMN], klass_raw[KLASSES_TABLE_USER_ID_COLUMN], klass_raw[KLASSES_TABLE_KLASS_NAME_COLUMN]))
        return klasses

    def fetchKlassByKlassId(self, klass_id):
        klasses_raw = self.cursor.execute("SELECT klass_id, user_id, klass_name FROM klasses WHERE klass_id = ?", (klass_id,))
        klass_raw = klasses_raw.fetchone()
        if klass_raw is not None:
            return Klass(klass_raw[KLASSES_TABLE_KLASS_ID_COLUMN], klass_raw[KLASSES_TABLE_USER_ID_COLUMN], klass_raw[KLASSES_TABLE_KLASS_NAME_COLUMN])
        return None
