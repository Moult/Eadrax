def load(**data):
    return Usecase(data['authenticator'])

class Usecase(object):

    def __init__(self, authenticator):
        self.authenticator = authenticator

    def run(self):
        self.authenticator.deauthenticate()
