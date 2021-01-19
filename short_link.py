from flask import Flask,render_template,request,flash,g,redirect
from validators import url
from Link import Link
import sqlite3

#Инициализация приложения
app = Flask(__name__)
app.config.from_pyfile('config.py')

#БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn
def create_db():
    db = connect_db()
    with app.open_resource('DB_cnf.sql',mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
def get_db():
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

#routes
@app.route("/", methods=["POST","GET"])
def index():
    db = get_db()
    Lnk = Link(db)
    if request.method == "POST":
        short_link = Lnk.short_link
        res = Lnk.addLinks(request.form["link"],short_link)
        if not res:
            flash('Ошибка генерации ссылки', category='error')
        else:
            flash('Ссылка успешно сгенерирована', category='success')
        for link in Lnk.getLinks():
            if link['full_link'] == request.form["link"]:
               result = render_template("index.html",link=link['short_link'])
    else:
        result = render_template("index.html")
    return result

@app.route('/<short_link>')
def redirect_to_link(short_link):
    db = get_db()
    Lnk = Link(db)
    for link in Lnk.getLinks():
        if link['short_link'] == short_link:
            if url(link['full_link']):
                return redirect(link['full_link'])
            else:
                return redirect("http://" + link['full_link'])
    return render_template("page404.html", title="Страница не найдена")

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'link_db'):
        g.link_db.close()

@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html")

#Запуск приложения
if __name__ == "__main__":
    app.run(debug=True)