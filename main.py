from flask import Flask, render_template, request, redirect
from flask_login import login_user, LoginManager

from data import db_session
from data.user import User
from forms.login import LoginForm
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('base.html', title='Сайт для ежедневного решения задач')


@app.route('/users_tasks')
def utasks():
    return render_template('base.html', title='Пользовательские задачи')


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


# @app.route('/image', methods=['POST', 'GET'])
# def load_photo():
#     if request.method == 'GET':
#         return render_template('load_photo.html')
#     elif request.method == 'POST':
#         photo = request.files['file']  # получение файла
#         with open('static/img/img.jpg', mode='wb') as f:
#             f.write(photo.read())
#         return render_template('show_photo.html')

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
            email=form.email.data
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
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('auth.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('auth.html', form=form)


@app.route('/publication')
def publication():
    return render_template('base.html', title='Здесь вы оформляете свою задачу')


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
