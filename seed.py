"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app

from datetime import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"
    
    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        row = row.split("|")
        movie_id = row[0]
        title = row[1]
        release_date = row[2]
        imdb_url = row[4]

        title = title[:-7]
        # title = title.strip("0123456789()")
        # title = title.rstrip()

        if release_date:
            release_date = datetime.strptime(release_date, "%d-%b-%Y")
        else:
            release_date = "01-01-1900"


        movie = Movie(movie_id=movie_id,title=title,release_date=release_date, imdb_url=imdb_url)

        db.session.add(movie)

    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        row = row.split()
        user_id = row[0]
        movie_id = row[1]
        score = row[2]

     


        rating = Rating(user_id=user_id, movie_id=movie_id, score=score)

        db.session.add(rating)

    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

# def datetime_as_string(release_date):
#     """Formats release date. Strings should be in this format, "%d-%b-%Y". """

#     release_date = release_date.strptime(release_date, "%d-%b-%Y")
#     # release_date = release_date.strftime("%d-%b-%Y")

#     return release_date



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
