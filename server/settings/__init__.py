from os import environ

import django_stubs_ext
from split_settings.tools import include, optional

django_stubs_ext.monkeypatch()

# Managing environment via `DJANGO_ENV` variable:
environ.setdefault("DJANGO_ENV", "development")


_ENV = environ["DJANGO_ENV"]

_base_settings = (
    "components/common.py",
    "components/rest_framework.py",
    "components/jwt_authentication.py",
    "components/swagger.py",
    "components/db.py",
    # Select the right env:
    "environments/{0}.py".format(_ENV),
    # Optionally override some settings:
    optional("environments/local.py"),
)

# Include settings:
include(*_base_settings)
