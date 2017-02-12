from health_tracker import app
from flask import render_template, request, session, redirect, url_for, abort
from datetime import datetime
from health_tracker.models.user import User
from health_tracker.models.workout import Workout
from health_tracker.models.weight import Weight
from health_tracker import db
from health_tracker.decorators import login_required


@app.route('/')
@login_required
def home_page():
    today = datetime.now()
    time = today.strftime("%I:%M:%S %p")
    today = today.strftime("%A %b. %w, %Y")

    user = User.query.filter_by(username=session["user_name"]).first()
    if user.workouts.count() > 3:
        workouts = user.workouts[-3:]
        workouts.reverse()
    else:
        workouts = user.workouts

    if user.weights.count() > 1: 
        last_weight = user.weights[-1]
    else:
        last_weight = False

    return render_template('home.html', workouts=workouts, last_weight=last_weight)

@app.route('/hello/<name>')
@login_required
def hello_word(name=None):
    # See: http://flask.pocoo.org/docs/0.12/quickstart/#rendering-templates
    # Docs on templates and how they work
    return render_template('hello.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # NEED TO HASH PASSWORDS
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form["user_name"]).first()
        if user is None:
            abort(401)
        if user.password == request.form["user_pass"]:
            session["user_name"] = request.form["user_name"]
            return redirect(url_for("home_page"))
        else:
            abort(401)

        #print(request.form)
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form["user_name"]).first()
        if user is None:
            if request.form["user_pass_confirm"] == request.form["user_pass"]:
                new_user = User(request.form["user_name"], request.form["user_pass"])
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                return render_template('signup.html')
        else:
            abort(401)

    else:
        return render_template('signup.html')

@app.route('/workout/new', methods=['GET', 'POST'])
@login_required
def new_workout():
    if request.method == 'POST':
        user = User.query.filter_by(username=session["user_name"]).first()
        if user is not None:
            date = datetime.strptime(request.form["user_date"], "%Y-%m-%d")
            new_workout = Workout(request.form["user_workout"], date, request.form["user_message"], user)
            db.session.add(new_workout)
            db.session.commit()
            return redirect(url_for("workout", workout_id=new_workout.id))
        else:
            abort(401)

    else:
        return render_template('workout.html')

@app.route('/workout/<workout_id>', methods=['GET'])
@login_required
def workout(workout_id=None):
    workout_session = Workout.query.get(int(workout_id))

    return render_template('workout_show.html', workout=workout_session)

@app.route('/workouts', methods=['GET'])
@login_required
def workouts():
    user = User.query.filter_by(username=session["user_name"]).first()
    return render_template('workout_list.html', workouts=user.workouts)

@app.route('/weight/new', methods=['GET', 'POST'])
@login_required
def new_weight():
    if request.method == 'POST':
        user = User.query.filter_by(username=session["user_name"]).first()
        if user is not None:
            date = datetime.strptime(request.form["user_date"], "%Y-%m-%d")
            new_weight = Weight(request.form["user_weight"], date, request.form["user_message"], user)
            db.session.add(new_weight)
            db.session.commit()
            return redirect(url_for("weights"))
        else:
            abort(401)

    else:
        return render_template('weight.html')

@app.route('/weights', methods=['GET'])
@login_required
def weights():
    user = User.query.filter_by(username=session["user_name"]).first()
    weights = user.weights
    final_weights = []

    for weight in weights:
        x = weight.date
        y = float(weight.weight)
        final_weights.append({
            "x":x,
            "y":y
            })

    return render_template('weight_list.html', weights=user.weights, final_weights=final_weights)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))



