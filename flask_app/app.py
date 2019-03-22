from flask import Flask
import flask
import json
import config
import postgresql

from flask_httpauth import HTTPBasicAuth

from User import User

auth = HTTPBasicAuth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
@auth.login_required
def main_screen():
    return 'Hello, {}!'.format(auth.username())


@app.route('/api/accounts', methods=['GET'])
@auth.login_required
def getAccounts():
    db = postgresql.open(config.db_connect)
    select = db.prepare('SELECT * FROM users')
    s = select()
    db.close()

    users = []

    for i in s:
        users.append(
            {
                'id': i[0],
                'login': i[1],
                'password': i[2],
                'isExternalUser': True if i[3] else False,
            }
        )

    return json.dumps(users)


@app.route('/api/accounts', methods=['POST'])
def createNewAccount():
    if auth.username() == 'root':
        data = flask.request.form
        __login = data.get('login')
        __password = data.get('password')
        __isExternalAccount = data.get('isExternalAccount')

        print(__login, __password, __isExternalAccount)

        if User.create_by_login(login=__login) is not None:
            flask.abort(400)  # existing user

        user = User(login =__login, isExternalAccount=__isExternalAccount)
        user.hash_password(__password)
        user.create_in_db()

        return json.dumps({
            'login': user.login,
            'status': 'Account {} successfully created'.format(user.login)
        })
    else:
        return 'Access denied'




@app.route('/api/accounts/<id>/password', methods=['PUT'])
@auth.login_required
def changePassword(id):
    data = flask.request.form
    oldPassword = data.get('oldPassword')
    newPassword = data.get('newPassword')

    user = User.create_by_id(id=id)

    if user.verify_password(oldPassword):
        user.update_pass_in_db(newPassword)
        return 'Password Updated'

    else:
        return 'Error. Old password is incorrect'


@app.route('/api/accounts/<id>', methods=['DELETE'])
@auth.login_required
def deleteAccount(id):
    user = User.create_by_id(id=id)
    # Юзер может удалить сам себя либо его может удалить root
    if auth.username() == user.login or auth.username() == 'root':
        db = postgresql.open(config.db_connect)
        delete = db.prepare('DELETE FROM users WHERE id=$1')
        delete(int(user.id))
        db.close()
        return 'User deleted! Id: {}'.format(id)

    else:
        return 'You cant delete this user'


@app.route('/api/accounts/login', methods=['POST'])
def post_login():
    data = flask.request.form
    login = data.get('login')
    password = data.get('password')


    user = User.create_by_login(login)
    if user.verify_password(password):
        return 'Hello, {}! You logged in!'.format(auth.username())
    else:
        return 'Login/password incorrect'.format(auth.username())


@app.route('/api/accounts/logout', methods=['POST'])
@auth.login_required
def logout():
    data = flask.request.form
    login = data.get('login')
    if auth.username() == login:
        return 'Logout user :)'
    else:
        return "Access denied"


@app.route('/api/accounts/password/policy', methods=['POST'])
@auth.login_required
def updatePasswordPolicy():
    if auth.username() == 'root':
        data = flask.request.form

        for i in data:
            piece_of_data = data[i] if type(data[i]) == 'int' else 1 if data[i] else 0
            db = postgresql.open(config.db_connect)
            update = db.prepare("UPDATE password_policy SET value = $1 WHERE key = $2")
            update(piece_of_data, i)
            db.close()

        return json.dumps(data)
    else:
        return "Access denied"


@auth.verify_password
def verify_password(__login, password):
    user = User.create_by_login(login=__login)
    if not user or not user.verify_password(password):
        return False
    return True



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
    )