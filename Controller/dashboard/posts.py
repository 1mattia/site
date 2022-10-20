from flask import Blueprint , render_template
from flask import Flask
from flask_login import login_required
import sqlite3

Posts = Blueprint('posts', __name__)

app = Flask(__name__)

@Posts.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    user = connection.execute('SELECT * FROM user').fetchall()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.commit()

    return render_template('/dashboard/posts.html' , user=user, posts=posts)

