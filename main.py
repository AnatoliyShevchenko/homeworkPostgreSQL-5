from flask import (Flask, render_template, request, redirect,)
from typing import Any
from services import Connecting


app = Flask(__name__)
conn: Connecting = Connecting()

conn.connect_db()
conn.create_table()
name = ''

@app.route('/', methods=['GET', 'POST'])
def main():
    global name
    error = ''
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        data = conn.get_current_user(login, password)
        name = data[0][1]
        if conn.check_auth(login, password):
            return redirect('/articles')
        error = 'Wrong Login or Password'
    return render_template('main.html', error=error)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    global name
    error = ''
    if request.method == "POST":
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if conn.check_users(login) and password == cpassword:
            conn.reg_user(name, login, password)
            return redirect('/')
        elif password != cpassword:
            error = 'Пароли не совпадают'
            return render_template('registration.html', error=error)
        elif not conn.check_users(login):
            error = 'Login is busy'
            return render_template('registration.html', error=error)

    return render_template('registration.html')

@app.route('/articles', methods=['GET', 'POST'])
def articles():
    global name
    data = conn.get_articles()
    message = ''
    if request.method == "POST":
        title = request.form.get('title')
        article = request.form.get('article')
        if title != '' and article != '':
            conn.create_article(title, article, name)
            message = 'article created, refresh the page'
            return render_template('/articles.html', message=message, data=data)
        else:
            message = 'fields must not be empty'
            return render_template('/articles.html', message=message, data=data)
    elif not data:
        message = 'no posts yet, be the first'
        return render_template('/articles.html', message=message)
    return render_template('/articles.html', data=data)


if __name__ == '__main__':
    app.run(port=8090, debug=True)