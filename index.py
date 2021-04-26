import os
import random

import requests

from flask import Flask
from flask import render_template, redirect, abort, jsonify

from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user


from data.loginform import LoginForm
from data.registerform import RegisterForm
from data.add_job_form import AddJobForm
from data.add_meeting_form import AddMeetingForm

from data import database_session
from data.jobs import Jobs
from data.users import User
from data.meetings import Meeting

# from users_resource import UsersResource, UsersListResource
# from jobs_resourse import JobsResource, JobsListResource

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
UPLOAD_FOLDER = 'static/carousel-images'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# api = Api(app)
# api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
# api.add_resource(UsersListResource, '/api/v2/users')
# api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')
# api.add_resource(JobsListResource, '/api/v2/jobs')

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    session = database_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def job_list():
    session = database_session.create_session()
    jobs = session.query(Jobs).all()

    names = {
        user.id: ' '.join([user.surname, user.name])
        for user in session.query(User).all()
    }

    params = {"title": "DOBRODEL", "jobs": jobs, "names": names}
    return render_template("jobs_list.html", **params)


@app.route('/meetings')
def show_meetings():
    session = database_session.create_session()
    meetings = session.query(Meeting).all()

    names = {
        user.id: ' '.join([user.surname, user.name])
        for user in session.query(User).all()
    }

    params = {
        'title': "Cобрания", 'names': names, 'meetings': meetings
    }
    return render_template('meetings.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = database_session.create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        session = database_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            params = {
                "title": "Регистрация", "form": form,
                "message": "Такой пользователь уже есть"
            }
            return render_template('register.html', **params)

        user = User()
        user.surname = form['surname'].data
        user.name = form['name'].data
        user.age = form['age'].data
        user.position = form['position'].data
        user.speciality = form['speciality'].data
        user.address = form['address'].data
        user.email = form['email'].data
        user.set_password(form['password'].data)
        session.add(user)
        session.commit()
        return redirect('/login')

    params = {
        "title": "Регистрация", "form": form,
        "message": False
    }
    return render_template("register.html", **params)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()

    if form.validate_on_submit():
        session = database_session.create_session()

        job = Jobs()
        if session.query(User).filter(form.team_leader.data != User.id).first():
            # params = {
            #     "title": "Добавление дела", "form": form,
            #     "message": 'Такого пользователя не существует'
            # }
            return render_template('add_job.html', message='такого пользователя нет', form=form)
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data

        session.add(job)
        session.commit()

        return redirect('/')

    params = {
        "title": "Добавление дела",
        "form": form
    }
    return render_template("add_job.html", **params)


@app.route('/add_meeting', methods=['GET', 'POST'])
def add_meeting_page():
    form = AddMeetingForm()

    if form.validate_on_submit():
        session = database_session.create_session()

        meeting = Meeting()
        meeting.tema = form.tema.data
        meeting.leader = form.leader.data
        meeting.members = form.members.data
        meeting.email = form.email.data

        session.add(meeting)
        session.commit()

        return redirect('/meetings')

    params = {
        "title": "Добавить Собрание",
        "form": form
    }
    return render_template("add_meeting.html", **params)


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = AddJobForm()
    session = database_session.create_session()
    job: Jobs = session.query(Jobs).get(job_id)

    if job is None:
        abort(404)
    elif job.team_leader != current_user.id and not current_user.id == 1:
        abort(404)

    if form.validate_on_submit():
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        session.commit()
        return redirect('/')

    form.team_leader.data = job.team_leader
    form.job.data = job.job
    form.work_size.data = job.work_size
    form.collaborators.data = job.collaborators
    form.is_finished.data = job.is_finished

    params = {
        "title": "Редактировать задачу", "form": form
    }
    return render_template("add_job.html", **params)


@app.route('/edit_meeting/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def edit_meeting(meeting_id):
    form = AddMeetingForm()
    session = database_session.create_session()
    meeting: Meeting = session.query(Meeting).get(meeting_id)

    if meeting is None:
        abort(404)
    elif meeting.leader != current_user.id and not current_user.id == 1:
        abort(404)

    if form.validate_on_submit():
        meeting.leader = form.leader.data
        meeting.tema = form.tema.data
        meeting.members = form.members.data
        meeting.email = form.email.data
        session.commit()
        return redirect('/meetings')

    form.leader.data = meeting.leader
    form.tema.data = meeting.tema
    form.members.data = meeting.members
    form.email.data = meeting.email

    params = {
        "title": "Редактировать собрание", "form": form
    }
    return render_template("add_meeting.html", **params)


@app.route('/del_job/<int:job_id>')
@login_required
def delete_job(job_id):
    session = database_session.create_session()
    job: Jobs = session.query(Jobs).get(job_id)

    if job is None:
        abort(404)
    elif job.team_leader != current_user.id and not current_user.id == 1:
        abort(404)
    else:
        session.delete(job)
        session.commit()

    return redirect('/')


@app.route('/del_meeting/<int:meeting_id>')
@login_required
def delete_meeting(meeting_id):
    session = database_session.create_session()
    meetings: Meeting = session.query(Meeting).get(meeting_id)

    if meetings is None:
        abort(404)
    elif meetings.leader != current_user.id and not current_user.id == 1:
        abort(404)
    else:
        session.delete(meetings)
        session.commit()

    return redirect('/meetings')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.errorhandler(404)
def error_handler_404(error):
    return jsonify({'message': 'Error', 'status_code': 404})


def run_app():
    database_session.global_init('db/db.db')
    port = os.environ.get('PORT', 5000)
    app.run(host="127.0.0.1", port=port, debug=True)


if __name__ == '__main__':
    run_app()
