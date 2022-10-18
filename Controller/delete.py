from flask import Blueprint
from flask import Flask , redirect
from flask_login import login_required
import sqlite3

delete = Blueprint('delete', __name__)

app = Flask(__name__)



@delete.route('/<int:idx>/delete', methods=('POST',))
@login_required
def delete(idx):
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    connection.execute('DELETE FROM user WHERE id = ?', (idx,))
    connection.execute('DELETE FROM posts WHERE id = ?', (idx,))
    connection.commit()
    connection.close()
    return redirect('/dashboard')