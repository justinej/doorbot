from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from webapp.db import get_db
from webapp.auth import admin_required, login_required
import dateutil
from dateutil import parser
from datetime import timedelta
from webapp.auth import passkey_gives_error

bp = Blueprint('internal', __name__)

@bp.route('/admin')
@admin_required
def admin():
    db = get_db()
    keys = db.execute('SELECT * from passkeys ORDER BY created DESC').fetchall()
    # Passing delta time = 5 hours bc db stores created as GMT. GMT - 5 hrs = EST
    return render_template(
        'internal/admin.html',
        keys=keys,
        dt=timedelta(hours=5),
        error=passkey_gives_error
     )

@bp.route('/')
def open():
    return render_template('internal/open.html')


# var target = "http://192.168.1.145/printIp";
# client.get(target, function(response) {
#   // do something with response
# });
