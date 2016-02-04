"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session 
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/login")
def login():
    """Page for user to login"""


    # if request.method == 'POST':
    #     print "hi"
    # else:
    
    return render_template('login.html')


    # if user_id in db
    #   log them in and then
        # return render_template(homepage.html)
    # else:
        # return render_template(register-new-user.html)
   


@app.route("/process-login-info", methods=['POST'])
def process_login():
    """Takes all the user input to login"""

    email= request.form.get('email')
    print email 
    password = request.form.get('password')
    print password

    user = User.query.filter_by(email=email).first()

    if user:
        if user.password == password:
            session["user"]=user.email 
        else:
            return redirect("/login")
    else:
        return redirect("/register-new-user")


@app.route("/register-new-user")
def register_new_user():
    """Sending new user to form to register"""
    return render_template("register-new-user.html")


@app.route("/process-new-user", methods=['POST'])
def process_new_user():
    """Saves the new user to the database"""

    email= request.form.get('email')
    print email 
    password = request.form.get('password')
    print password

    user = User.query.filter_by(email=email).first()

    users = 

    if user:
        return redirect("/login")
    else:
        users.insert().values(email=email, password=password)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
