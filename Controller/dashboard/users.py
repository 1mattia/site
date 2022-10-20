from flask import Blueprint
from flask import Flask , render_template
from flask_login import login_required
import sqlite3

Users = Blueprint('users', __name__)

app = Flask(__name__)

@Users.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    user = connection.execute('SELECT * FROM user').fetchall()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.commit()

    return render_template('/dashboard/users.html' , user=user, posts=posts)