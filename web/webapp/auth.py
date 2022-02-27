import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from webapp.db import get_db
import datetime


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        passkey = request.form['passkey']

        expiration = request.form['expiration']
        num_uses = request.form['num_uses']
        notes = request.form['notes']

        db = get_db()
        error = None
        if not passkey:
            error = 'Passkey is required.'
        if len(expiration) > 0:
            try:
                datetime.datetime.strptime(expiration, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                error = "Datetime needs to be in YYYY-MM-DD HH-MM-SS format"
        if len(num_uses) > 0:
            try:
                if int(num_uses) <= 0:
                    error = "Number of uses allowed must be positive."
            except:
                error = "Number of uses must be an integer."
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO passkeys " + 
                    "(passkey, used, admin, num_uses, expiration, notes) VALUES (?, ?, ?, ?, ?, ?)",
                    (generate_password_hash(passkey), 0, 0, num_uses, expiration, notes),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Passkey {passkey} is already registered."
            else:
                return redirect(url_for("internal.admin"))
        flash(error)
    return render_template('auth/register.html')


def get_passkey(passkey):
    db = get_db()
    tmp_db = db.execute("SELECT * FROM passkeys").fetchall()
    for row in tmp_db:
        if check_password_hash(row['passkey'], passkey):
            return row
    flash("Invalid passkey!")
    return None



def passkey_gives_error(passkey_row):
    error = None
    if passkey_row['expiration'] and passkey_row['expiration'] <= datetime.datetime.now():
        error = "Passkey has expired!"
    elif passkey_row['num_uses'] and passkey_row['num_uses'] >= passkey_row['used']:
        error = "Passkey reached limit on times used"
    return error


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        passkey = request.form['passkey']
        db = get_db()
        passkey_row = get_passkey(passkey)

        error = None
        if passkey_row is None:
            error = "Please enter a passkey!"
        else:
            error = passkey_gives_error(passkey_row)
        if error is not None:
            flash(error)
            return redirect(url_for('auth.login'))

        db.execute(
            'UPDATE passkeys SET used = ? WHERE id = ?',
            (passkey_row['used'] + 1, passkey_row['id'])
        )
        db.commit()
        session.clear()
        session['passkey'] = passkey
        return redirect(url_for('internal.open'))
    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    passkey = session.get('passkey')
    if passkey is None:
        g.passkey = None
        g.admin = None
    else:
        g.passkey = get_passkey(passkey)
        g.admin = g.passkey['admin']


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.passkey is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin != 1:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
