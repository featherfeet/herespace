class User:
    def __init__(self, user_id, username, password_hashed_and_salted, email, user_type, student_id, is_authenticated = False, is_active = False, is_anonymous = False):
        self.user_id = user_id
        self.username = username
        self.password_hashed_and_salted = password_hashed_and_salted
        self.email = email
        self.user_type = user_type
        self.student_id = student_id
        self.is_authenticated = is_authenticated
        self.is_active = is_active
        self.is_anonymous = is_anonymous
    def get_id(self):
        return str(self.user_id)
