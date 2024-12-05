from flask import Flask, render_template, request, redirect, url_for
from utils.db import db
from models.data import Mobile, User
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(flask_app)

# Home route
@flask_app.route('/')
def index():
    data = Mobile.query.all()
    return render_template('index.html', content=data)

# Help page
@flask_app.route('/help')
def help():
    return render_template('help.html')

# Add data page
@flask_app.route('/add_data')
def add_data():
    return render_template('add_data.html')

# Explore data page
@flask_app.route('/explore')
def explore():
    data = Mobile.query.all()
    return render_template('explore.html', content=data)

# Submit new data
@flask_app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()

    age = form_data.get('age')
    gender = form_data.get('gender')
    user_behavior_class = form_data.get('UserBehaviorClass')

    device_model = form_data.get('DeviceModel')
    operating_system = form_data.get('OperatingSystem')
    app_usage_time = form_data.get('AppusageTime')
    battery_drain = form_data.get('BatteryDrain')
    screen_on_time = form_data.get('ScreenOnTime_hours_per_day')
    num_apps_installed = form_data.get('NumberofAppsInstalled')
    data_usage = form_data.get('DataUsage_MB_per_day')

    # Check if user exists
    user = User.query.filter_by(age=age).first()
    if not user:
        user = User(age=age, gender=gender, UserBehaviorClass=user_behavior_class)
        db.session.add(user)
        db.session.commit()

    # Add mobile data
    data = Mobile(
        DeviceModel=device_model,
        OperatingSystem=operating_system,
        AppusageTime=app_usage_time,
        BatteryDrain=battery_drain,
        ScreenOnTime_hours_per_day=screen_on_time,
        NumberofAppsInstalled=num_apps_installed,
        DataUsage_MB_per_day=data_usage,
        user_id=user.id
    )
    db.session.add(data)
    db.session.commit()

    return redirect('/')

# Edit data
@flask_app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_data(id):
    data = Mobile.query.get(id)
    if request.method == 'POST':
        data.DeviceModel = request.form.get('DeviceModel')
        data.OperatingSystem = request.form.get('OperatingSystem')
        data.AppusageTime = request.form.get('AppusageTime')
        data.BatteryDrain = request.form.get('BatteryDrain')
        data.ScreenOnTime_hours_per_day = request.form.get('ScreenOnTime_hours_per_day')
        data.NumberofAppsInstalled = request.form.get('NumberofAppsInstalled')
        data.DataUsage_MB_per_day = request.form.get('DataUsage_MB_per_day')

        db.session.commit()
        return redirect('/explore')

    return render_template('edit.html', data=data)

# Delete data
@flask_app.route('/delete/<int:id>', methods=['POST'])
def delete_data(id):
    data = Mobile.query.get(id)
    if data:
        db.session.delete(data)
        db.session.commit()
    return redirect('/explore')

# Charts page
@flask_app.route('/charts')
def charts():
    filter_os = request.args.get('filter_os', '')
    filter_behavior_class = request.args.get('filter_behavior_class', '')

    query = Mobile.query
    if filter_os:
        query = query.filter_by(OperatingSystem=filter_os)
    if filter_behavior_class:
        query = query.filter_by(UserBehaviorClass=filter_behavior_class)

    mobile_data = query.all()

    users = [{
        'device_model': mobile.DeviceModel,
        'operating_system': mobile.OperatingSystem,
        'app_usage_time': mobile.AppusageTime,
        'screen_on_time': mobile.ScreenOnTime_hours_per_day,
        'battery_drain': mobile.BatteryDrain,
        'num_apps_installed': mobile.NumberofAppsInstalled,
        'data_usage': mobile.DataUsage_MB_per_day,
        'age': mobile.user.age,
        'gender': mobile.user.gender,
        'behavior_class': mobile.user.UserBehaviorClass
    } for mobile in mobile_data]

    return render_template('charts.html', users=users, filter_os=filter_os, filter_behavior_class=filter_behavior_class)

# Initialize database
with flask_app.app_context():
    db.create_all()

# Run the Flask app
if __name__ == '__main__':
    flask_app.run(host='127.0.0.1', port=8005, debug=True)
