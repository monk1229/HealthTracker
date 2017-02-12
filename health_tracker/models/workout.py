from health_tracker import db 

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout = db.Column(db.String(160))
    date = db.Column(db.Date())
    notes = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    user = db.relationship('User', backref=db.backref('workouts', lazy='dynamic'))
    __mapper_args__={"order_by":date}

    def __init__(self, workout, date, notes, user):
        self.workout = workout
        self.date = date
        self.notes = notes
        self.user = user

    def __repr__(self):
        return '<Workout %r>' % self.workout