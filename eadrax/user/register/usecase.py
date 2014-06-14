from .registrant import Registrant

def load(**data):
    return Interactor(
        Registrant(
            data['user'],
            data['repository'],
            data['authenticator'],
            data['emailer'],
            data['encryptor'],
            data['formatter'],
            data['validator']
        )
    )

class Interactor(object):

    def __init__(self, registrant):
        self.registrant = registrant

    def interact(self):
        self.registrant.authorise_guests()
        self.registrant.validate()
        self.registrant.encrypt_password()
        self.registrant.register()
        self.registrant.send_welcome_message()

class Repository(object):

    def save_user(self, **user):
        raise NotImplementedError
