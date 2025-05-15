from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('base.html', title='Сайт для ежедневного решения задач')


@app.route('/users_tasks')
def utasks():
    return render_template('base.html', title='Пользовательские задачи')


@app.route('/we')
def about_us():
    return render_template('base.html', title='На этой странице написано о нас')


@app.route('/iam')
def profile():
    return render_template('base.html', title='Это ваш профиль')


@app.route('/publication')
def publication():
    return render_template('base.html', title='Здесь вы оформляете свою задачу')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
