import flask
from application import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Document):
    name = db.StringField(max_length=20)
    email = db.StringField(max_length = 50,unique=True)
    password = db.StringField(max_length=30)
    user_id = db.IntField()
    total_urls = db.IntField(default=0)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class ShortUrls(db.Document):
    __tablename__ = 'shorted_url'
    user_id = db.IntField()
    url_id = db.IntField()
    original_url = db.StringField(max_length=500)
