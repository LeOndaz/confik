from collections.abc import Callable, Iterable

from confik.exceptions import ConfikError
from confik.proxies import EnvMappingProxy


class ConfikParser:
    proxy_class = EnvMappingProxy

    def __init__(self, path=".", *args, **kwargs):
        self.source = self.proxy_class(*args, path=path, **kwargs)

    def validate_params(
        self,
        key,
        cast,
        default,
        default_factory,
        choices,
        raise_exception,
    ):
        if choices is None:
            choices = set()

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
                    truthy_values = ("True", "true", "1")
                    falsy_values = ("False", "false", "0")
                    allowed_values = (*truthy_values, *falsy_values)

                    assert env in allowed_values, "{} not in [{}]".format(
                        env, ", ".join(allowed_values)
                    )
                    return env in truthy_values

                return cast(env)
            except ValueError:
                raise ConfikError(
                    "value {v} can't be casted into {c}".format(v=env, c=cast.__name__)
                )

        return env
