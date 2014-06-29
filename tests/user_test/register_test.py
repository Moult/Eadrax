import eadrax.user.register

from mock import Mock, call
from nose.tools import assert_raises

from eadrax.data import User
from eadrax.user.register import Usecase, Repository, Registrant
from eadrax.tools import Authenticator, Emailer, Encryptor, Formatter, Validator
from eadrax.errors import AuthorisationError, ValidationError

user = User()
user.username = 'username'
user.password = 'password'
user.email = 'email'

repository = Mock(spec_set = Repository)
authenticator = Mock(spec_set = Authenticator)
emailer = Mock(spec_set = Emailer)
encryptor = Mock(spec_set = Encryptor)
formatter = Mock(spec_set = Formatter)
validator = Mock(spec_set = Validator)

registrant = Registrant(user, repository, authenticator, emailer, encryptor, formatter, validator)

def test_loading_a_usecase():
    user = Mock()
    repository = Mock(spec_set = Repository)
    authenticator = Mock(spec_set = Authenticator)
    emailer = Mock(spec_set = Emailer)
    encryptor = Mock(spec_set = Encryptor)
    formatter = Mock(spec_set = Formatter)
    validator = Mock(spec_set = Validator)

    usecase = eadrax.user.register.load(
        user = user,
        repository = repository,
        authenticator = authenticator,
        emailer = emailer,
        encryptor = encryptor,
        formatter = formatter,
        validator = validator
    )

    assert isinstance(usecase, Usecase)

def test_run():
    registrant = Mock(spec_set = Registrant)

    usecase = eadrax.user.register.Usecase(registrant)
    usecase.run()

    assert registrant.method_calls == [
        call.authorise(),
        call.validate(),
        call.encrypt_password(),
        call.register(),
        call.send_email()
    ]

def test_authorise():
    authenticator.get_authenticated_id = Mock(return_value = None)
    registrant.authorise()
    assert authenticator.get_authenticated_id.called

    authenticator.get_authenticated_id = Mock(return_value = 'id')
    assert_raises(AuthorisationError, registrant.authorise)
    assert authenticator.get_authenticated_id.called

def test_validate():
    validator.setup = Mock()
    validator.is_valid = Mock(return_value = False)
    assert_raises(ValidationError, registrant.validate)
    validator.setup.assert_called_once_with({
        'username': 'username',
        'password': 'password',
        'email': 'email'
    })
    assert validator.add_required_rule.call_args_list == [
        call('username'),
        call('password'),
        call('email')
    ]
    validator.add_email_rule.assert_called_once_with('email')
    validator.add_email_domain_rule.assert_called_once_with('email')
    assert validator.is_valid.called

    validator.is_valid = Mock(return_value = True)
    registrant.validate()

def test_encrypt_password():
    encryptor.encrypt_password = Mock(return_value = 'encrypted_password')
    registrant.encrypt_password()
    encryptor.encrypt_password.assert_called_once_with('password')
    assert registrant.password == 'encrypted_password'

def test_register():
    registrant.password = 'password'
    test_encrypt_password()
    registrant.register()
    repository.save_user.assert_called_once_with(
        username = 'username',
        password = 'encrypted_password',
        email = 'email'
    )

def test_send_email():
    formatter.get_formatted = Mock(
        side_effect = ['subject', 'plaintext', 'html']
    )
    registrant.send_email()
    formatter.setup.assert_called_once_with({'username': 'username'})
    assert formatter.get_formatted.call_args_list == [
        call('user_register_subject'),
        call('user_register_plaintext'),
        call('user_register_html')
    ]
    emailer.set_to.assert_called_once_with('email')
    emailer.set_subject.assert_called_once_with('subject')
    emailer.set_plaintext_body.assert_called_once_with('plaintext')
    emailer.set_html_body.assert_called_once_with('html')
    emailer.send.assert_called_once_with()
