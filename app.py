from health_tracker import app
from health_tracker.models import user, workout, weight
from health_tracker import db

def create_users():
    user1 = user.User("Monika", "blah")
    user2 = user.User("Andres", ":D")
    user3 = user.User("Karla", "BAMBAM")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

def print_users():
    users = user.User.query.all()
    print(users)

def create_db():
    #from health_tracker.models import *
    #from health_tracker import db

    db.create_all()

if __name__ == "__main__":
    #create_db()
    #create_users()
    #print_users()
    app.run(debug=True)
