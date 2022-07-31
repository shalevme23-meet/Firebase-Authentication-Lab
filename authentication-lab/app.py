from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyDAdVhYNYG7lCpwLTiggSeQ4k6XiwVJ2Nc",
    "authDomain": "authentication-lab-de1af.firebaseapp.com",
    "projectId": "authentication-lab-de1af",
    "storageBucket": "authentication-lab-de1af.appspot.com",
    "messagingSenderId": "607156653908",
    "appId": "1:607156653908:web:f5c07927c3ccfaec3482c1",
    "measurementId": "G-WT5F2HEZJB",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    # error = ""
    if request.method == 'POST':
        user_email = request.form["email"]
        user_password = request.form["password"]
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(user_email, user_password)
            return redirect(url_for('add_tweet'))
        except:
            return render_template("signin.html", error = "Auth Failed")
            # error = "Auth Failed"
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        try:
            user_email = request.form["email"]
            user_password = request.form["password"]
            login_session['user'] = auth.create_user_with_email_and_password(user_email, user_password)
            return redirect(url_for('signin'))
        except:
            error = "Auth Failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)