# Doorbot website

This is a simple website running with Flask (Python) backend and SQLite db largely influenced by the [Flask tutorial](https://flask.palletsprojects.com/en/2.0.x/tutorial/).

### About the app

Admins can only be made by the Flask CLI command `add-admin`. New passkeys can only be made by admins and can be done through the website (URL TBD).

Passkeys have several properties:
* Expiration
* Number of uses
* Notes

A passkey will be rejected if it is either past the expiration date or has been used more than its allocated number of times.

Passkeys are stored as salted hashes in the SQLite db. However I would not recommend using passkeys that you are using someplace else.

Go to `URL/admin.html` (if you have an admin passkey) in order to access the admin page and view status on all passkeys ever given out.

### How to use
```
source venv/bin/activate
export FLASK_APP=webapp
export FLASK_ENV=development
```

My venv environment is this:
TODO

To wipe the existing db and start over (or running an instance for the first time), run:
```
flask init-db
```

To add an admin, run:
```
flask add-admin $ADMIN_PW_OF_YOUR_CHOICE
```

To restart an instance, run:
```
flask run
```

You'll probably want to run all three of these lines the first time you set up or if you are starting over.

