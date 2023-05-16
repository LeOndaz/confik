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

### Integrate with [AWS Secrets manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html)

```python
# here's the example from official secrets manager docs
# make sure to install the required libraries

import botocore
import botocore.session
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
import confik

client = botocore.session.get_session().create_client('secretsmanager')
cache_config = SecretCacheConfig()
cache = SecretCache(config=cache_config, client=client)


class SecretsManagerProxy(confik.MapConfiKToMappingProxy):
    def get(self, key, default=None):
        value = cache.get_secret_string(key)

        if value is None:
            return default

        return value

    # You could use the async version if you're using an async library
    async def aget(self, key, default=None):
        pass


class SecretsManagerConfiKParser(confik.ConfikParser):
    proxy_class = SecretsManagerProxy


confik = SecretsManagerConfiKParser()
SECRET = confik.get('SECRET_FROM_SECRETS_MANAGER')

# if you're using the async version
async def get_secret(name):
    return await confik.aget(name)
```
