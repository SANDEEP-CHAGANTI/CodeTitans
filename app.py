from flask import Flask, render_template, request, redirect, url_for, session
import os
from pymongo import MongoClient
from bson import ObjectId
kk = os.urandom(24)



app = Flask(__name__)
app.secret_key = b'kk'

mongo_uri = 'mongodb://localhost:27017'
client = MongoClient(mongo_uri)
db = client.get_database("MyData3")
registered_users = db.get_collection("users")


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    already_registered = False

    if request.method == 'POST':
        email = request.form.get('email')
        existing_user = registered_users.find_one({"email": email})
        if existing_user:
            already_registered = True
        else:
            name = request.form.get('name')
            phone = request.form.get('phone')
            password = request.form.get('password')
            registered_users.insert_one({'name': name, 'email': email, 'phone': phone, 'password': password})
            return redirect(url_for('login'))
    
    return render_template('register.html', already_registered=already_registered)

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_not_found = False
    wrong_password = False

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        
        user = registered_users.find_one({"email": email})

        if user:
            if user['password'] == password:
                user['_id'] = str(user['_id'])
                session['user_data'] = user
                return redirect(url_for('home'))
            else:
                wrong_password = True
        else:
            user_not_found = True

    return render_template('login.html', user_not_found=user_not_found, wrong_password=wrong_password)

@app.route('/home')
def home():
    user_data = session.get('user_data')
    if user_data:
        user_data['_id'] = ObjectId(user_data['_id'])
    return render_template('home.html', user_data=user_data)

@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/work_with_us')
def work_with_us():
    return render_template('work_with_us.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/latest_tech')
def latest_tech():
    return render_template('latest_tech.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/terms_and_codetitans')
def terms_and_codetitans():
    return render_template('terms_and_codetitans.html')


if __name__ == '__main__':
    app.run(debug=True)
