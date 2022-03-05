import flask
from application import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Document):
    email = db.EmailField(max_length = 50,unique=True)
    password = db.PasswordField(max_length=20)
    name = db.StringField(max_length=20)
    user_id = db.StringField(max_length=50,unique=True)
    total_urls = db.IntField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class Urls(db.Document):
    user_id = db.StringField(max_length=50,unique=True)
    url_id = db.IntField()
    original_url = db.StringField(max_length=500)
    