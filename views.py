from flask import render_template, redirect, url_for, request, session

from models import Account, Notes
from config import app, db


# main index or the login page
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']

        session['user-response'] = uname
        session['user-notes'] = uname
        session['current_uid'] = uname

        user_check = bool(Account.query.filter_by(username=f'{uname}').first())

        if user_check == True:
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    
    if 'user-notes' in session or 'user-response' in session:
        return redirect(url_for('home'))
        
    return render_template('login.html')
        

#register name
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username_form = request.form['username-form']

        user = Account(username=username_form)

        db.session.add(user)
        db.session.commit()

    return render_template('register.html', users=Account.query.all(), notes=Notes.query.all(), notesJoined=db.session.query(Notes, Account).outerjoin(Notes, Notes.account_id == Account.user_id).all())

#after logging in go to the notes
@app.route('/notes')
def home():
    if 'user-notes' in session:
        usr_name = session['user-notes']

        user_id = db.session.query(Account.user_id).filter_by(username=usr_name)

        notes_id = db.session.query(Notes.id, Notes.title).filter_by(account_id=user_id).all()
       
        return render_template('index.html', Notes=notes_id, usr_name=usr_name)
    else:
        return redirect(url_for('login'))

#add notes
@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == "POST":
        title = request.form['titles']  

        if 'current_uid' in session:
            current_user = session['current_uid']

            current_id = db.session.query(Account.user_id).filter_by(username=f'{current_user}')
            note = Notes(title=title, content='', account_id=current_id)
            
            db.session.add(note)
            db.session.commit()

    return redirect(url_for('home'))

#when notes click get its id
@app.route('/<int:id_>')
def response(id_):
    if 'user-response' in session:
        usr_name = session['user-response']
        return render_template('response.html',notes_id=Notes.query.get(id_), Notes=Notes, id_content=id_, usr_name=usr_name)
    else:
        return redirect(url_for('login'))

#update the notes
@app.route('/update/<int:content_id>', methods=['POST', 'GET'])
def update(content_id):
    if request.method == "POST":
        notes_id=Notes.query.get(content_id)

        text_content = request.form['text-content']
        notes_id.content = str(text_content)
        db.session.commit()

        return redirect(f'/{content_id}')
    
#delete notes in the list
@app.route('/delete/<int:id_>')
def delete(id_):

    id_num = Notes.query.get_or_404(id_)

    db.session.delete(id_num)   
    db.session.commit()

    return redirect(url_for('home'))

#for admin just remove account
@app.route('/remove_account/<int:remove_id>')
def remove_account(remove_id):
    rm_id = Account.query.get_or_404(remove_id)

    db.session.delete(rm_id)
    db.session.commit()

    return redirect(url_for('register'))

#delete a note, admin only
@app.route('/delete_note/<int:note_id>')
def note_del(note_id):
    rm_note = Notes.query.get_or_404(note_id)

    db.session.delete(rm_note)
    db.session.commit()

    return redirect(url_for('register'))

#when logout session will be gone
@app.route('/logout')
def logout():
    for i in ['user-notes', 'user-response', 'current_uid']:
        session.pop(i, None)
    return redirect(url_for('login'))

