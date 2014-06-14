from mock import Mock
from nose.tools import assert_raises

from eadrax.user.register import Registrant, Repository
from eadrax.data import User
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

def test_authorise_guests():
    authenticator.get_authenticated_id = Mock(return_value = None)
    registrant.authorise_guests()
    authenticator.get_authenticated_id.assert_called_once_with()

    authenticator.get_authenticated_id = Mock(return_value = 'id')
    assert_raises(AuthorisationError, registrant.authorise_guests)
    authenticator.get_authenticated_id.assert_called_once_with()

def test_validate():
    validator.setup = Mock()
    validator.add_required_rule = Mock()
    validator.add_email_rule = Mock()
    validator.add_email_domain_rule = Mock()
    validator.is_valid = Mock(return_value = False)

    assert_raises(ValidationError, registrant.validate)

    validator.setup.assert_called_once_with({
        'username': 'username',
        'password': 'password',
        'email': 'email'
    })

    assert validator.add_required_rule.call_args_list[0][0][0] == 'username'
    assert validator.add_required_rule.call_args_list[1][0][0] == 'password'
    assert validator.add_required_rule.call_args_list[2][0][0] == 'email'
    validator.add_email_rule.assert_called_once_with('email')
    validator.add_email_domain_rule.assert_called_once_with('email')
    validator.is_valid.assert_called_once_with()

    validator.is_valid = Mock(return_value = True)
    registrant.validate()

def test_encrypt_password():
    encryptor.encrypt_password = Mock(return_value = 'encrypted_password')
    registrant.encrypt_password()
    encryptor.encrypt_password.assert_called_once_with('password')
    assert registrant.password == 'encrypted_password'

def test_register():
    repository.save_user = Mock()
    registrant.register()
    repository.save_user.assert_called_once_with(
        username = 'username'
    )

def test_send_welcome_message():
    formatter.setup = Mock()
    formatter.get_formatted = Mock(side_effect = ['subject', 'plaintext', 'html'])
    emailer.set_to = Mock()
    emailer.set_subject = Mock()
    emailer.send = Mock()

    registrant.send_welcome_message()

    formatter.setup.assert_called_once_with({
        'username': 'username'
    })

    assert formatter.get_formatted.call_args_list[0][0][0] == 'user_register_subject'
    assert formatter.get_formatted.call_args_list[1][0][0] == 'user_register_plaintext'
    assert formatter.get_formatted.call_args_list[2][0][0] == 'user_register_html'
    emailer.set_to.assert_called_once_with('email')
    emailer.set_subject.assert_called_once_with('subject')
    emailer.set_plaintext_body.assert_called_once_with('plaintext')
    emailer.set_html_body.assert_called_once_with('html')
    emailer.send.assert_called_once_with()
