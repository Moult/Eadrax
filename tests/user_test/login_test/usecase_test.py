import eadrax.user.login.usecase

from mock import Mock
from nose.tools import assert_raises

from eadrax.user.login.usecase import Interactor, Repository
from eadrax.tools import Authenticator, Encryptor
from eadrax.errors import AuthorisationError

user = Mock()
user.username = 'username'
user.password = 'password'

repository = Mock(spec_set = Repository)
authenticator = Mock(spec_set = Authenticator)
encryptor = Mock(spec_set = Encryptor)

def test_loading_a_usecase():
    interactor = eadrax.user.login.usecase.load(
        user = user,
        repository = repository,
        authenticator = authenticator,
        encryptor = encryptor
    )
    assert isinstance(interactor, Interactor)

def test_interaction():
    repository.get_password_by_username = Mock(return_value = 'encrypted_password')
    encryptor.is_same_password = Mock(return_value = False)

    interactor = Interactor(user, repository, authenticator, encryptor)

    assert_raises(AuthorisationError, interactor.interact)

    assert interactor.user == user
    repository.get_password_by_username.assert_called_once_with('username')
    encryptor.is_same_password.assert_called_once_with('password',
                                                          'encrypted_password')

    encryptor.is_same_password = Mock(return_value = True)
    repository.get_id_by_username = Mock(return_value = 'id')
    authenticator.authenticate = Mock()
    interactor.interact()
    repository.get_id_by_username.assert_called_once_with('username')
    authenticator.authenticate.assert_called_once_with('id')
