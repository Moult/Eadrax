import eadrax.user.login

from mock import Mock
from nose.tools import assert_raises

from eadrax.user.login import Usecase, Repository
from eadrax.tools import Authenticator, Encryptor
from eadrax.errors import AuthorisationError

user = Mock()
user.username = 'username'
user.password = 'password'

repository = Mock(spec_set = Repository)
authenticator = Mock(spec_set = Authenticator)
encryptor = Mock(spec_set = Encryptor)

def test_loading_a_usecase():
    usecase = eadrax.user.login.load(
        user = user,
        repository = repository,
        authenticator = authenticator,
        encryptor = encryptor
    )
    assert isinstance(usecase, Usecase)

def test_run():
    repository.get_password_by_username = Mock(return_value = 'encrypted_password')
    encryptor.is_same_password = Mock(return_value = False)
    usecase = Usecase(user, repository, authenticator, encryptor)
    assert_raises(AuthorisationError, usecase.run)
    repository.get_password_by_username.assert_called_once_with('username')
    encryptor.is_same_password.assert_called_once_with('password',
                                                       'encrypted_password')

    encryptor.is_same_password = Mock(return_value = True)
    repository.get_id_by_username = Mock(return_value = 'id')
    usecase.run()
    repository.get_id_by_username.assert_called_once_with('username')
    authenticator.authenticate.assert_called_once_with('id')
