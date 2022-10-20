from flask import Blueprint , request , redirect
from flask import Flask , render_template
from flask_login import login_required
import sqlite3
from werkzeug.utils import secure_filename

Create = Blueprint('create', __name__)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/img/"


@Create.route('/crea', methods=['GET', 'POST'])
@login_required
def crea():
    connection = sqlite3.connect('prova.db')
    connection.row_factory = sqlite3.Row
    user = connection.execute('SELECT * FROM user').fetchall()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.commit()
    
    if request.method == 'POST':
        titolo = request.form['titolo']
        info = request.form['info']
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        connection.execute('INSERT INTO posts (titolo, info, filename) VALUES (?, ?, ?)', (titolo, info, filename))
        connection.commit()
        connection.close()
        return redirect('/dashboard')
    return render_template('/dashboard/crea.html' , user=user, posts=posts)