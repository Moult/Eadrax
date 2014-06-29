from eadrax.errors import AuthorisationError

def load(**data):
    return Usecase(
        data['user'],
        data['repository'],
        data['authenticator'],
        data['encryptor']
    );

class Usecase(object):

    def __init__(self, user, repository, authenticator, encryptor):
        self.user = user
        self.repository = repository
        self.authenticator = authenticator
        self.encryptor = encryptor

    def run(self):
        self.check_password()
        self.login()

    def check_password(self):
        encrypted_password = self.repository.get_password_by_username(self.user.username)

        if not self.encryptor.is_same_password(self.user.password, encrypted_password):
            raise AuthorisationError

    def login(self):
        self.authenticator.authenticate(self.repository.get_id_by_username(self.user.username))

class Repository(object):

    def get_password_by_username(self, username):
        raise NotImplementedError

    def get_id_by_username(self, username):
        raise NotImplementedError
