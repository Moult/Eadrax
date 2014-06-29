# Eadrax

Eadrax is a diary for your creations, that allows you to create from anywhere.

## Usage

In this example, `wipup` is the name of your delivery layer.

```
import eadrax.data
import eadrax.user.login
from eadrax.errors import AuthorisationError

usecase = eadrax.user.login.load(
    user = eadrax.data.User(),
    repository = wipup.repositories.user.Login(),
    authenticator = wipup.tools.Authenticator(),
    encryptor = wipup.tools.Encryptor()
)

try:
    usecase.run()
except AuthorisationError:
    pass
```

More detailed implementations can be seen in [WIPUP](http://github.com/Moult/wipup).
