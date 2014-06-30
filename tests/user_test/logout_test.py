import eadrax.user.logout

from mock import Mock
from eadrax.user.logout import Usecase
from eadrax.tools import Authenticator

authenticator = Mock(spec_set = Authenticator)

def test_loading_a_usecase():
    usecase = eadrax.user.logout.load(
        authenticator = authenticator
    )
    assert isinstance(usecase, Usecase)

def test_run():
    usecase = Usecase(authenticator)
    usecase.run()
    assert authenticator.deauthenticate.called
