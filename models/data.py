
from utils.db import db

# parent table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    UserBehaviorClass = db.Column(db.String(100), nullable=False)

    # Relationship to the Mobile table
    data = db.relationship('Mobile', backref='user', lazy=True)

class Mobile(db.Model):
    mobile_id = db.Column(db.Integer, primary_key=True)  # Corrected column name
    DeviceModel = db.Column(db.String(100), nullable=False)
    OperatingSystem = db.Column(db.String(100), nullable=False)
    AppusageTime = db.Column(db.Integer, nullable=False)
    BatteryDrain = db.Column(db.Integer, nullable=False)
    ScreenOnTime_hours_per_day = db.Column(db.Integer, nullable=False)  # Corrected column name
    NumberofAppsInstalled = db.Column(db.Integer, nullable=False)
    DataUsage_MB_per_day = db.Column(db.Integer, nullable=False)  # Corrected column name

    # ForeignKey to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
