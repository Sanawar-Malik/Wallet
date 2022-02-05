from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique=True)
    email_address = db.Column(db.String(900), nullable=False)
    password_hash = db.Column(db.String(900), nullable=False)
    wallets = db.relationship('Wallet', backref='user', lazy="dynamic", cascade="all,delete")
    entriesrelationuser = db.relationship('Entry', backref='user', lazy="dynamic", cascade="all,delete")
    created_Date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)  
    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')  
    def check_password_correction(self, attempted_password):
       return bcrypt.check_password_hash(self.password_hash, attempted_password)
class Wallet(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100),nullable = False)
  balance = db.Column(db.Integer(),nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  entries = db.relationship('Entry', backref='wallet', lazy="dynamic", cascade="all,delete")
  created_Date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
class Entry(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  amount = db.Column(db.Integer(),nullable=False)
  wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
  created_Date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
  userentries_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)