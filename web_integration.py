from flask import Flask, render_template, request, url_for, jsonify, send_from_directory, session, abort
from werkzeug.utils import secure_filename
from os import path, remove, listdir
from async_sched import FileDeletionScheduler
from json import load
from random import choices
from Converters import *

UPLOAD_FOLDER = path.join(path.dirname(path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'db', 'db3', 's3db', 'sl3', 'sqlite', 'sqlite3', 'csv', 'tsv', 'txt', 'xlsx', 'xls', 'html', 'htm', 'xhtml', 'xht', 'json'}

win = Flask(__name__)
win.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
win.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
win.secret_key = 'my secret key'
win.permanent_session_lifetime = 60*60*24*7 # 1 week
symbols = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
uids = ['abcdefgh', '12345678', 'ABCDEFGH']

with open('messages.json', 'r', encoding='utf-8') as file:
    messages_dt = load(file)

sched = FileDeletionScheduler(win=win, interval=300)
sched.start()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@win.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        if not session.get('uid'):
            session['uid'] = 'abcdefgh'
            while session['uid'] in uids:
                session['uid'] = ''.join(choices(symbols, k=8))
            uids.append(session['uid'])
        return render_template('index.html')
    
    country_code = request.headers['Accept-Language'].split(',')[-1][:2]
    messages = messages_dt.get(country_code, messages_dt['en'])

    typeinput = request.form['from']
    typeoutput = request.form['to']
    website = request.form['url']

    if typeinput == typeoutput:
        return {'error':messages[4]}

    abspath = ''
    file = request.files.get('file')
    
    if file:
        if not allowed_file(file.filename):
            return {'error':messages[2]}
        file.seek(0, 2)
        if file.tell() > win.config['MAX_CONTENT_LENGTH']:
            return {'error':messages[1]}
        file.seek(0) # reset the file pointer
        filename = secure_filename(file.filename)
        abspath = path.join(win.config['UPLOAD_FOLDER'], filename)
        file.save(abspath)

    match typeinput:
        case 'SQLite':
            df = sqlitetodf(abspath)
        case 'CSV':
            df = csvtodf(abspath)
        case 'JSON':
            df = jsontodf(abspath)
        case 'Excel':
            df = exceltodf(abspath)
        case 'HTML':
            if not website:
                df = htmltodf(abspath)
            else:
                df = htmltodf(website)

    if isinstance(df, int): # Une valeur entière est renvoyée en cas d'erreur
        return {'error':messages[df]}
    if abspath:
        remove(abspath)

    ext = extensions[typeoutput].split(',')[0]
    newfile = f'{session.get("uid")}{ext}'
    newpath = path.join(win.config['UPLOAD_FOLDER'], newfile)
    
    # Seulement un fichier est autorisé par utilisateur
    if newfile in listdir(win.config['UPLOAD_FOLDER']):
        remove(path.join(win.config['UPLOAD_FOLDER'], newfile))
        
    match typeoutput:
        case 'SQLite':
            result = dftosqlite(df, newpath)
        case 'CSV':
            result = dftocsv(df, newpath)
        case 'JSON':
            result = dftojson(df)
        case 'Excel':
            result = dftoexcel(df, newpath)
        case 'HTML':
            result = dftohtml(df, theme='dark')
    
    # trois cas possibles : un code d'erreur, une liste de contenu ou un nom de fichier
    if isinstance(result, int):
        output = {'error':messages[result]}
    elif isinstance(result, str):
        if path.isfile(path.join(win.config['UPLOAD_FOLDER'], result)):
            output = {'name':typeoutput, 'url':url_for('uploads', filename=result), 'success':messages[6]}
            sched.schedule_deletion(newfile)
    elif isinstance(result, list):
        output = {'name':typeoutput, 'content':result, 'success':messages[5]}
    else:
        output = {'error':messages[4]}
    return output


@win.route('/uploads/<filename>')
def uploads(filename):
    uid = session.get('uid')
    if not uid or filename[:8] != uid:
        abort(403)
    return send_from_directory(win.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@win.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(win.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@win.route('/info', methods=['POST'])
def info():
    return jsonify({'extensions':extensions, 'icons':fileicons, 'formats':formats})

with win.test_request_context():
    formats = ['SQLite', 'CSV', 'JSON', 'Excel', 'HTML'],
    fileicons = {'SQLite':url_for('static', filename='sqlite.png'), 
                 'CSV':url_for('static', filename='csv.png'), 
                 'Excel':url_for('static', filename='excel.png'), 
                 'HTML':url_for('static', filename='html.png'), 
                 'JSON':url_for('static', filename='json.png')}, 
    extensions = {'SQLite':'.db, .db3, .s3db, .sl3, .sqlite, .sqlite3', 
                  'CSV':'.csv, .tsv, .txt', 
                  'Excel':'.xlsx, .xls', 
                  'HTML':'.html, .htm, .xhtml, .xht', 
                  'JSON':'.json'}

if __name__ == '__main__':
    win.run(debug=True)