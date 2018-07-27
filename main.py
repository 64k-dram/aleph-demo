import sqlite3
from flask import g, Flask, request, render_template
app = Flask(__name__,template_folder=".")

def get_page(page, rpp):
    db = sqlite3.connect('factbook.db')
    db.row_factory = sqlite3.Row #use col names instead of index
    cur = db.cursor()
    maxid = cur.execute('SELECT * FROM facts ORDER BY id DESC LIMIT 1').fetchone()['id']
    countries = cur.execute('SELECT * FROM facts WHERE id > ? ORDER BY id LIMIT ?', ((page-1)*rpp, rpp)).fetchall()
    return countries, maxid

@app.route('/')
def home():
    page = int(request.args['page']) if 'page' in request.args else 1
    rpp = int(request.args['rpp']) if 'rpp' in request.args else 20
    countries, maxid = get_page(page,rpp)
    return render_template('home.html', countries=countries, page=page, rpp=rpp, maxid=maxid)

app.run(host='0.0.0.0',port=8080, debug=True)