from collections.abc import Callable, Iterable

from confik.exceptions import ConfikError
from confik.proxies import EnvMappingProxy, MapConfiKToMappingProxy
from confik.utils import boolean


class ConfikParser:
    proxy_class = None

    def __init__(self, *args, **kwargs):
        self.source: MapConfiKToMappingProxy = self.proxy_class(*args, **kwargs)

    def validate_params(
        self,
        key,
        cast,
        default,
        default_factory,
        choices,
        raise_exception,
    ):
        assert isinstance(key, str), "key must be a string"
        assert isinstance(cast, Callable) or cast is None, "cast must be a callable"
        assert (
            isinstance(default_factory, Callable) or default_factory is None
        ), "Must provide a callable for default_factory"
        assert not all(
            [default, default_factory]
        ), "default and default_factory parameters are mutually exclusive, must only provide one of them."

        assert isinstance(choices, Iterable), "choices must be an iterable"
        assert isinstance(raise_exception, bool), "raise_exception must be a boolean"

        if default and choices:
            assert (
                default in choices
            ), "default value is not in the list of provided choices"

    def process_env(
        self,
        env,
        key,
        cast,
        default_factory,
        choices,
        raise_exception,
    ):
        if env is None:
            if default_factory:
                return default_factory(key)
            elif raise_exception:
                raise ConfikError(
                    "{key} variable can't be of type None".format(key=key)
                )

        if choices:
            assert env in choices, "{key}={value} is not in choices={choices}".format(
                key=key,
                value=env,
                choices=", ".join(choices),
            )

        if cast:
            try:
                if cast is bool:
                    return boolean(env)
                return cast(env)
            except ValueError:
                raise ConfikError(
                    "value {v} can't be casted into {c}".format(v=env, c=cast.__name__)
                )

        return env

    def get(
        self,
        key,
        default=None,
        cast=None,
        default_factory=None,
        choices=tuple(),
        raise_exception=True,
    ):
        self.validate_params(
            key, cast, default, default_factory, choices, raise_exception
        )

        env = self.source.get(key, default)
        return self.process_env(
            env, key, cast, default_factory, choices, raise_exception
        )

    async def aget(
        self,
        key,
        default=None,
        cast=None,
        default_factory=None,
        choices=tuple(),
        raise_exception=True,
    ):
        self.validate_params(
            key, cast, default, default_factory, choices, raise_exception
        )
        env = await self.source.aget(key, default)
        return self.process_env(
            env, key, cast, default_factory, choices, raise_exception
        )


class EnvConfikParser(ConfikParser):
    proxy_class = EnvMappingProxy
