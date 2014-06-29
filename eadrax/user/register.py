from eadrax.errors import AuthorisationError, ValidationError

def load(**data):
    return Usecase(
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

class Usecase(object):

    def __init__(self, registrant):
        self.registrant = registrant

    def run(self):
        self.registrant.authorise()
        self.registrant.validate()
        self.registrant.encrypt_password()
        self.registrant.register()
        self.registrant.send_email()

class Repository(object):

    def save_user(self, **user):
        raise NotImplementedError

class Registrant(object):

    def __init__(self, user, repository, authenticator, emailer, encryptor, formatter, validator):
        self.username = user.username
        self.password = user.password
        self.email = user.email

        self.repository = repository
        self.authenticator = authenticator
        self.emailer = emailer
        self.encryptor = encryptor
        self.formatter = formatter
        self.validator = validator

    def authorise(self):
        if self.authenticator.get_authenticated_id():
            raise AuthorisationError

    def validate(self):
        self.validator.setup({
            'username': self.username,
            'password': self.password,
            'email': self.email
        })
        self.validator.add_required_rule('username')
        self.validator.add_required_rule('password')
        self.validator.add_required_rule('email')
        self.validator.add_email_rule('email')
        self.validator.add_email_domain_rule('email')
        if not self.validator.is_valid():
            raise ValidationError

    def encrypt_password(self):
        self.password = self.encryptor.encrypt_password(self.password)

    def register(self):
        self.repository.save_user(
            username = self.username,
            password = self.password,
            email = self.email
        )

    def send_email(self):
        self.formatter.setup({
            'username': self.username
        })
        self.emailer.set_to(self.email)
        self.emailer.set_subject(
            self.formatter.get_formatted('user_register_subject')
        )
        self.emailer.set_plaintext_body(
            self.formatter.get_formatted('user_register_plaintext')
        )
        self.emailer.set_html_body(
            self.formatter.get_formatted('user_register_html')
        )
        self.emailer.send()
