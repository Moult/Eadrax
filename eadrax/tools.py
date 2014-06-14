class Authenticator(object):

    def get_authenticated_id(self):
        raise NotImplementedError

    def authenticate(self, id):
        raise NotImplementedError

class Formatter(object):

    def setup(self, dictionary):
        raise NotImplementedError

    def get_formatted(self, template):
        raise NotImplementedError

class Emailer(object):

    def set_to(self, email):
        raise NotImplementedError

    def set_subject(self, subject):
        raise NotImplementedError

    def set_plaintext_body(self, body):
        raise NotImplementedError

    def set_html_body(self, body):
        raise NotImplementedError

    def send(self):
        raise NotImplementedError

class Encryptor(object):

    def encrypt_password(self, password):
        raise NotImplementedError

    def is_correct_password(self, password, encrypted_password):
        raise NotImplementedError

class Validator(object):

    def setup(self, dictionary):
        raise NotImplementedError

    def add_required_rule(self, key):
        raise NotImplementedError

    def add_email_rule(self, key):
        raise NotImplementedError

    def add_email_domain_rule(self, key):
        raise NotImplementedError

    def add_callback(self, callback, keys):
        raise NotImplementedError

    def is_valid(self):
        raise NotImplementedError

    def get_error_keys(self):
        raise NotImplementedError
