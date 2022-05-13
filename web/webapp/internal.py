from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, request
)
from webapp.db import get_db
from webapp.auth import admin_required, login_required
from datetime import timedelta
from webapp.auth import passkey_gives_error
import requests


IP_FNAME = "webapp/ip.txt" # Sensitive: hostname of ESP32 server
ip = open(IP_FNAME).read()[:-1]

bp = Blueprint('internal', __name__)

@bp.route('/admin')
@admin_required
def admin():
    db = get_db()
    keys = db.execute('SELECT * from passkeys ORDER BY created DESC').fetchall()
    return render_template(
        'internal/admin.html',
        keys=keys,                # render all the existing passkeys
        dt=timedelta(hours=5),    # db stores some times as GMT. GMT - 5 hrs = EST
        error=passkey_gives_error # green if valid, red invalid
     )

@bp.route('/')
@login_required
def open():
    return render_template('internal/open.html')

@bp.route('/buzz')
@login_required
def buzz():
    db = get_db()
    error = passkey_gives_error(g.passkey)
    if error is not None:
      flash(error)
      return redirect(url_for('auth.login'))

    # Update num times used before buzzing door open
    db.execute(
        'UPDATE passkeys SET used = ? WHERE id = ?',
        (g.passkey['used'] + 1, g.passkey['id'])
    )
    db.commit()
    requests.get(url=ip)
    return redirect(url_for("internal.open"))

@bp.route('/revoke/<passkey_id>')
@admin_required
def revoke(passkey_id):
    db = get_db()
    # Sets passkey as expired
    db.execute(f'UPDATE passkeys SET num_uses=1, used=1 WHERE id={passkey_id};')
    db.commit()
    return redirect(url_for("internal.admin"))
