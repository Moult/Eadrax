from ...errors import AuthorisationError

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
        encrypted_password = self.repository.get_password_by_username(self.user.username)
        if self.encryptor.is_correct_password(self.user.password,
                                              encrypted_password) is not True:
            raise AuthorisationError

        self.authenticator.authenticate(self.repository.get_id_by_username(self.user.username))

class Repository(object):

    def get_password_by_username(self):
        raise NotImplementedError

    def get_id_by_username(self):
        raise NotImplementedError
