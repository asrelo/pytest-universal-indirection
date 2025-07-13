import pytest

from ._common import BasisCallableWrapper, BasisGeneratorFunctionWrapper
from .simple import make_universal_indirection_simple_wrapped


__all__ = (
    'BasisCallableWrapper',
    'BasisGeneratorFunctionWrapper',
    'make_universal_indirection_wrapped',
    'make_universal_indirection_simple_wrapped',
)


def make_universal_indirection_wrapped(name, *, scope='function', autouse=False):
    """Create a wrapping fixture for `universal_indirection`

    This function creates a new named fixture that can have non-default `scope`
    or `autouse`.

    Args:
        name:
            The name of the fixture. `@pytest.fixture`, being a decorator,
            usually takes the name of the function it decorates; we can't do
            that here because this function creates the fixture itself.
            (Reminder: pytest needs fixtures to be named to dynamically inject
            them into tests).
        scope:
            The scope for which this fixture is shared. (see pytest docs)
        autouse:
            Whether the fixture is activated for all tests that can see it.
            (see pytest docs)

    Returns:
        A registered pytest fixture trivially wrapping
        `universal_indirection`.
    """
    def universal_indirection_wrapped_ff(universal_indirection):
        return universal_indirection
    return pytest.fixture(
        universal_indirection_wrapped_ff, scope=scope, autouse=autouse, name=name,
    )
