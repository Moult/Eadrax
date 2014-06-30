import eadrax.user.delete

from mock import Mock
from nose.tools import assert_raises
from eadrax.user.delete import Usecase, Repository
from eadrax.tools import Authenticator
from eadrax.errors import AuthorisationError

authenticator = Mock(spec_set = Authenticator)
repository = Mock(spec_set = Repository)

def test_loading_a_usecase():
    usecase = eadrax.user.delete.load(
        repository = repository,
        authenticator = authenticator
    )
    assert isinstance(usecase, Usecase)

def test_run():
    authenticator.get_authenticated_id = Mock(return_value = None)
    usecase = Usecase(repository, authenticator)
    assert_raises(AuthorisationError, usecase.run)
    assert authenticator.get_authenticated_id.called

    authenticator.get_authenticated_id = Mock(return_value = 'authenticated_id')
    usecase.run()
    repository.delete_user.assert_called_once_with('authenticated_id')
