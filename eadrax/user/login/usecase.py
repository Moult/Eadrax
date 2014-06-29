from eadrax.errors import AuthorisationError

def load(**data):
    return Interactor(
        data['user'],
        data['repository'],
        data['authenticator'],
        data['encryptor']
    );

class Interactor(object):

    def __init__(self, user, repository, authenticator, encryptor):
        self.user = user
        self.repository = repository
        self.authenticator = authenticator
        self.encryptor = encryptor

    def interact(self):
        self.validate_password()
        self.login()

    def validate_password(self):
        encrypted_password = self.repository.get_password_by_username(self.user.username)

        if self.encryptor.is_same_password(self.user.password,
                                           encrypted_password) is False:
            raise AuthorisationError

    def login(self):
        self.authenticator.authenticate(self.repository.get_id_by_username(self.user.username))

class Repository(object):

    def get_password_by_username(self, username):
        raise NotImplementedError

    def get_id_by_username(self, username):
        raise NotImplementedError
