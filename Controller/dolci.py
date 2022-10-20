from flask import Blueprint
from flask import Flask , render_template
import sqlite3

Dolci = Blueprint('dolci', __name__)

app = Flask(__name__)

@Dolci.route('/dolci')
def dolci():
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('dolci.html', posts=posts)