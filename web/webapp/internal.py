from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from webapp.db import get_db
from webapp.auth import admin_required
from datetime import timedelta
from webapp.auth import passkey_gives_error

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
        error=passkey_gives_error # true if passkey gives error
     )

@bp.route('/')
def open():
    return render_template('internal/open.html')


# var target = "http://192.168.1.145/printIp";
# client.get(target, function(response) {
#   // do something with response
# });
