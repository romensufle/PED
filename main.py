from flask import Flask, render_template, request, redirect
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from data import db_session
from data.user import User
from data.posts import Posts
from forms.login import LoginForm
from forms.register_form import RegisterForm
from forms.posts_form import PostForm
from forms.comments_form import CommentForm
from data.comments import Comments
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    sess = db_session.create_session()
    posts = sess.query(Posts).filter(Posts.user_id == '1')
    return render_template("index.html", posts=posts)


@app.route('/users_tasks')
def utasks():
    sess = db_session.create_session()
    posts = sess.query(Posts).filter(Posts.user_id != '1')
    return render_template('index.html', title='Пользовательские задачи', posts=posts)


@app.route('/my_tasks')
def my_tasks():
    sess = db_session.create_session()
    posts = sess.query(Posts).filter(Posts.user_id == current_user.id)
    return render_template('index.html', title='Пользовательские задачи', posts=posts)


@app.route('/we')
def about_us():
    info = []
    with open('static/О нас.txt') as t:
        for st in t.readlines():
            info.append(st)
    return render_template('about_us.html', info=info)


@app.route('/iam')
def profile():
    return render_template('base.html', title='Это ваш профиль')


@app.route('/image', methods=['POST', 'GET'])
def load_photo():
    file_path = 'static/img/img.jpg'
    if os.path.exists(file_path) and request.method == 'GET':
        return render_template('show_photo.html')
    else:
        if request.method == 'GET':
            return render_template('load_photo.html')
        elif request.method == 'POST':
            photo = request.files['file']  # получение файла
            with open('static/img/img.jpg', mode='wb') as f:
                f.write(photo.read())
            return render_template('show_photo.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   form=form, message='Пароли не совпали')

        sess = db_session.create_session()

        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   form=form, message='Такой пользователь есть!')

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            fav_prog_lang=form.fav_prog_lang.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
        return render_template('register.html',
                               form=form, message='Пользователь зарегестрирован!')
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('auth.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('auth.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/publication', methods=['GET', 'POST'])
@login_required
def publication():
    form = PostForm()
    if request.method == 'POST':
        sess = db_session.create_session()

        post = Posts(
            name=form.name.data,
            hard=form.hard.data,
            text=form.text.data,
            decision=form.decision.data,
            user_id=current_user.id
        )
        current_user.posts.append(post)
        sess.merge(current_user)
        sess.commit()
        return render_template('posts.html',
                               form=form, message='Задача опубликована!')
    return render_template('posts.html', form=form)


@app.route('/comments/<task_id>/<name_of_task>')
def comments(task_id, name_of_task):
    sess = db_session.create_session()
    comments = sess.query(Comments).filter(Comments.post_id == task_id)
    return render_template('comments.html', task_id=task_id, name=name_of_task, comments=comments)


@app.route('/comments_form/<task_id>/<name>', methods=['GET', 'POST'])
@login_required
def comments_form(task_id, name):
    form = CommentForm()
    if request.method == 'POST':
        sess = db_session.create_session()

        comm = Comments(
            text=form.text.data,
            post_id=task_id,
            user_id=current_user.id
        )
        sess.add(comm)
        sess.merge(current_user)
        sess.commit()
        return redirect(f'/comments/{task_id}/{name}')
    return render_template('comment_form.html', form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
