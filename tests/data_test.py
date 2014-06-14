from eadrax.data import User

class TestUser(object):

    def setUp(self):
        self.user = User()

    def test_has_id(self):
        assert hasattr(self.user, 'id')

    def test_has_username(self):
        assert hasattr(self.user, 'username')

    def test_has_password(self):
        assert hasattr(self.user, 'password')

    def test_has_email(self):
        assert hasattr(self.user, 'email')
