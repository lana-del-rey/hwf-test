from passlib.apps import custom_app_context as pwd_context
import config
import postgresql

class User(object):
    def __init__(self, login, isExternalAccount, password_hash=None, password=None, id=None):
        self.login = login
        if password is not None:
            self.password_hash = self.hash_password(password)
        else:
            self.password_hash = password_hash

        self.id = id
        self.isExternalAccount = isExternalAccount

    def hash_password(self, password):
        if password is not None:
            self.password_hash = pwd_context.encrypt(password)
        else:
            self.password_hash = None
        return self.password_hash

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def create_in_db(self):
        db = postgresql.open(config.db_connect)


        if not self.isExternalAccount:
            insert = db.prepare("INSERT INTO users (login, is_external_user)"
                                " VALUES ($1, $2)")
            r = insert(self.login, 1 if self.isExternalAccount else 0)
        else:
            insert = db.prepare("INSERT INTO users (login, password, is_external_user)"
                                " VALUES ($1, $2, $3)")
            r = insert(self.login, self.password_hash, 1 if self.isExternalAccount else 0)

        db.close()

    def update_pass_in_db(self, newPassword):
        self.hash_password(newPassword)
        db = postgresql.open(config.db_connect)
        upgrade = db.prepare("UPDATE users SET password = $1 WHERE id = $2")
        upgrade(self.password_hash, self.id)

    # @staticmethod
    # def check_password(password):
    #     db = postgresql.open(config.db_connect)
    #     select = db.prepare("""select * from password_policy""")
    #     rows = select()
    #     db.close()
    #
    #     policy = {}
    #     for row in rows:
    #         policy[row[0]] = row[1]
    #
    #     check = True
    #
    #     for p in policy:
    #         if p in ['lenght', 'lowercase_latters', 'numbers', 'special_symbols', 'uppercase_latters']:
    #             if p == 'lenght':
    #                 check = (len(password) == policy[p])
    #
    #             if p == 'lowercase_latters':
    #                 check = any(c.islower() for c in password) and policy[p]
    #
    #
    #
    #         if not check:
    #             return False
    #
    #     return check



    @classmethod
    def create_by_login(cls, login):
        db = postgresql.open(config.db_connect)
        select = db.prepare('SELECT * FROM users WHERE login = $1')
        user = select(login)
        db.close()

        if user:
            return cls(
                id=user[0][0],
                login=user[0][1],
                password_hash=user[0][2],
                isExternalAccount=True if user[0][3] else False,
            )

        else:
            return None

    @classmethod
    def create_by_id(cls, id):
        db = postgresql.open(config.db_connect)
        select = db.prepare('SELECT * FROM users WHERE id = $1')
        user = select(int(id))
        db.close()

        if user:
            return cls(
                id=user[0][0],
                login=user[0][1],
                password_hash=user[0][2],
                isExternalAccount=True if user[0][3] else False,
            )

        else:
            return None