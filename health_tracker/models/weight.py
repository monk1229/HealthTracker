from health_tracker import db 

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Numeric(2))
    date = db.Column(db.Date())
    notes = db.Column(db.Text())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    user = db.relationship('User', backref=db.backref('weights', lazy='dynamic'))
    __mapper_args__={"order_by":date}

    def __init__(self, weight, date, notes, user):
        self.weight = weight
        self.date = date
        self.notes = notes
        self.user = user

    def __repr__(self):
        return '<Weight %r>' % self.weight