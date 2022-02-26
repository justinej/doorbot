import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from webapp.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        passkey = request.form['passkey']
        db = get_db()
        error = None
        if not passkey:
            error = 'Passkey is required.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO passkeys (passkey, used) VALUES (?, ?)",
                    (generate_password_hash(passkey), 0),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Passkey {passkey} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')


def get_passkey(passkey):
    db = get_db()
    tmp_db = db.execute("SELECT * FROM passkeys").fetchall()
    for row in tmp_db:
        if check_password_hash(row['passkey'], passkey):
            return row
    abort(404, f"Passkey {passkey} not found.")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        passkey = request.form['passkey']
        db = get_db()
        passkey = get_passkey(passkey)
        db.execute(
            'UPDATE passkeys SET used = ? WHERE id = ?',
            (passkey['used'] + 1, passkey['id'])
        )
        db.commit()
        session.clear()
        return redirect(url_for('index'))
    return render_template('auth/login.html')
    

@bp.before_app_request
def load_logged_in_user():
    passkey = session.get('passkey')

    if passkey is None:
        g.passkey = None
    else:
        g.passkey = get_passkey(passkey)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.passkey is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
