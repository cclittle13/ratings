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


@app.route('/homepage')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/movies")
def movie_list():
    """Show all movies ordered by title"""

    movies = Movie.query.order_by('title').all()
    return render_template("movies.html", movies=movies)



@app.route("/login")
def login():
    """Page for user to login"""


    # if request.method == 'POST':
    #     print "hi"
    # else:
    # session.add("user")
    return render_template('login.html')


    # if user_id in db
    #   log them in and then
        # return render_template(homepage.html)
    # else:
        # return render_template(register-new-user.html)


@app.route("/logout")
def logout():
    """Process the user to logout"""
    session.pop("user", None)
    flash('You have been logged out')
    return redirect('/homepage')


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
            return redirect("/homepage")
        else:
            flash("Incorrect password, please try again")
            return redirect("/login")
            
    else:
        return redirect("/register-new-user")



@app.route("/register-new-user")
def register_new_user():
    """Sending new user to form to register"""
    flash("You are not a registered user, please input your information")
    return render_template("register-new-user.html")


@app.route("/process-new-user", methods=['POST'])
def process_new_user():
    """Saves the new user to the database"""

    email= request.form.get('email')
    print email 
    password = request.form.get('password')
    print password
    zipcode = request.form.get('zipcode')
    print zipcode
    age = int(request.form.get('age'))
    print age 

    user = User.query.filter_by(email=email).first()

    if user:
        return redirect("/login")
    else:
        user = User(email=email, password=password, zipcode=zipcode, age=age)
        flash("You've been added")
        print "Successful new user" 
    
        db.session.add(user)

        db.session.commit()

        # return render_template("/user_page.html", user=user)
        return redirect("/users/%s" % user.user_id)



@app.route("/users/<int:user_id>")
def load_user_page(user_id):
    """Loads a page that has the user's age, zicode, and movies they rated"""
    
    user = User.query.get(user_id)

    return render_template("user_page.html", user=user)


@app.route("/movies/<int:movie_id>")
def movie_details(movie_id):
    """Loads a page that has movie details"""

    movie = Movie.query.get(movie_id)
    rating = Rating.query.get(movie_id)

    return render_template("movie_details.html", movie=movie, rating=rating)


@app.route("/movies/rate-movie", methods=['POST'])
def rate_movie(movie_id):
    """Adds user rating of movie to database"""

    score = request.form.get("rating")

    user_id= session.get("user")

    rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()


    if rating:
        rating.score = score
        flash("Rating updated.")

    # else:
    #     rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
    #     flash("Rating added.")
    #     db.session.add(rating)


    db.session.commit()

    return render_template("movie_details.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    # DEBUG_TB_INTERCEPT_REDIRECTS = False
    app.run()
