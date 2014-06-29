# Eadrax

Eadrax is a diary for your creations, that allows you to create from anywhere.

## Usage

In the example, `wipup` is the name of your delivery layer.

```
import eadrax.user.login.usecase

usecase = eadrax.user.login.usecase.load(
    user = eadrax.data.User(),
    repository = wipup.repositories.user.Login(),
    authenticator = wipup.tools.Authenticator(),
    encryptor = wipup.tools.Encryptor()
)

usecase.interact()
```

More detailed implementations can be seen in [WIPUP](http://github.com/Moult/wipup).
