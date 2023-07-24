from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config= { 'apiKey': "AIzaSyDxFLL8BcyM78ZpE8YV0N8vBtgI-KcDgrg", 'authDomain': "cs-lab-5f2a3.firebaseapp.com", 'projectId': "cs-lab-5f2a3", 'storageBucket': "cs-lab-5f2a3.appspot.com", 'messagingSenderId': "469598563500", 'appId': "1:469598563500:web:067bcdd8527cea163e0309", 'measurementId': "G-Z66V0HNG4W",
'databaseURL':'https://cs-lab-5f2a3-default-rtdb.europe-west1.firebasedatabase.app/'
}

firebase= pyrebase.initialize_app(config)
auth= firebase.auth()
db= firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
     email = request.form['email']
     password = request.form['password']
     try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
     except:
        error = "Authentication failed"

    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    name= request.form['full_name']
    username=request.form['username']
    bio= request.form['username']
    user = { 'email': email, 'name': name, 'username': username, "bio": bio}
    try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID= login_session['user']['localId']
        user= db.child('Users').child(UID).get().val()
        return redirect(url_for('add_tweet'))
    except:
        error = "Authentication failed"
   return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=="POST":
        ti= request.form['ti']
        text= request.form['text']
        tweet = {'title':ti, 'text':text, "UID": login_session['user']['localId'] }
        try:
            db.child("Tweets").push(tweet)
        except: 
            error="can't add tweet"
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def alltweets():
    tweets= db.child('Tweets').get().val()
    return render_template("tweets.html", tweets = tweets)


if __name__ == '__main__':
    app.run(debug=True)