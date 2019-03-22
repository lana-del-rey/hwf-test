import requests

def test_create_new_account():
    data = {
        'login': 'DOMAIN\\aivanov',
        'password': None,
        'isExternalAccount': True,
    }

    data = {
        'login': 'root1',
        'password': 'root',
        'isExternalAccount': False,
    }

    r = requests.post('http://0.0.0.0/api/accounts', data=data, auth= ('root', 'root'))

    print(r.text)
    print(r.status_code)

    pass


def test_getAllUsers():
    r = requests.get('http://0.0.0.0/api/accounts', auth = ('aivanov', 1234))
    print(r.text)


def test_changePassword():
    data = {
        'oldPassword': 12345,
        'newPassword': 1234,
    }
    r = requests.put('http://0.0.0.0/api/accounts/9/password', data=data, auth=('aivanov', 12345))
    print(r.text)


def test_deleteUser():
    delete_id = '1'
    r = requests.delete('http://0.0.0.0/api/accounts/{}'.format('1'), auth=('root', 'root'))
    print(r.text)


def test_post_login():
    data = {
        'login': 'root',
        'password': 'root',
    }

    r = requests.post('http://0.0.0.0/api/accounts/login', data=data)
    print(r.text)


def test_update_policy():
    data = {
        'lenght': 7,
        'numbers': True,
        'uppercase_latters': True,
        'lowercase_latters': True,
        'special_symbols': False,
    }
    r = requests.post('http://0.0.0.0/api/accounts/password/policy', data=data)
    print(r.text)



if __name__ == '__main__':
    # test_getAllUsers()
    # print(int(True))
    test_update_policy()
    # test_changePassword()








# from User import User
#
# print(User.create_by_login(login='login'))

#
#
# data = {
#     'lenght': 8,
#     'numbers': True,
#     'uppercase_latters': True,
#     'lowercase_latters': True,
#     'special_symbols': False,
# }
#
# # r = requests.post('http://0.0.0.0/api/accounts/password/policy', data=data, )
#
# r = requests.get('http://0.0.0.0/api/accounts')
# print(r.text)
#
# # import postgresql
# # import config
# #
# # db = postgresql.open(config.db_connect)
# #
# # select = db.prepare("""select * from password_policy""")
# # rows = select()
# # db.close()
# #
# # policy = {}
# # for row in rows:
# #     policy[row[0]] = row[1]
# #
# # print(policy)
#
#
# def test1():
#     pass
#

