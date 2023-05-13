# Installation

```
pip install confik
```

# Running tests

```
pytest .
```

Examples

```python
import confik

# get a variable
secret_key = confik.get('AWS_SECRET_KEY')

# get a variable and ignore if it doesn't exist
secret_key = confik.get("AWS_SECRET_KEY", raise_exception=False)

# provide a default
admin_username = confik.get("ADMIN_USERNAME", "LeOndaz")
assert admin_username == "LeOndaz"


# provide a default factory

def factory(key):
    return "very_confidential_pwd"


admin_password = confik.get("ADMIN_PASSWORD", default_factory=factory)
# $ very_confidential_pwd

allowed_hosts = confik.get("ALLOWED_HOSTS", cast=confik.csv)

debug = confik.get('DEBUG', cast=bool)

```

The default confik instance looks for .env in the base directory of your project, if
for some reason you have a different place for the .env file, you can use
```python
from confik import read_env

confik = read_env("confik/path/to/.env")
```

and use it with the same interface as mentioned above.

It's worth noting that confik works with both .env and os.env at the same time, it looks in both.
