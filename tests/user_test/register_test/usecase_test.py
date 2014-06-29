import eadrax.user.register.usecase

from mock import Mock

from eadrax.user.register.usecase import Interactor, Repository
from eadrax.user.register.registrant import Registrant
from eadrax.tools import Authenticator, Emailer, Encryptor, Formatter, Validator

def test_loading_a_usecase():
    user = Mock()
    repository = Mock(spec_set = Repository)
    authenticator = Mock(spec_set = Authenticator)
    emailer = Mock(spec_set = Emailer)
    encryptor = Mock(spec_set = Encryptor)
    formatter = Mock(spec_set = Formatter)
    validator = Mock(spec_set = Validator)

    interactor = eadrax.user.register.usecase.load(
        user = user,
        repository = repository,
        authenticator = authenticator,
        emailer = emailer,
        encryptor = encryptor,
        formatter = formatter,
        validator = validator
    )

    assert isinstance(interactor, Interactor)

def test_interaction():
    registrant = Mock(spec_set = Registrant)
    registrant.authorise_guests = Mock()
    registrant.validate = Mock()
    registrant.encrypt_password = Mock()
    registrant.register = Mock()
    registrant.send_welcome_message = Mock()

    interactor = eadrax.user.register.usecase.Interactor(registrant)
    interactor.interact()

    registrant.authorise_guests.assert_called_once_with()
    registrant.validate.assert_called_once_with()
    registrant.encrypt_password.assert_called_once_with()
    registrant.register.assert_called_once_with()
    registrant.send_welcome_message.assert_called_once_with()
