import pytest

from ._common import parametrize_universal_indirection_base

__all__ = (
    'parametrize_universal_indirection_simple',
    'make_universal_indirection_simple_wrapped',
)


def parametrize_universal_indirection_simple(
    basis_objects, ids=None, *, scope=None, fixture_name='universal_indirection_simple',
):
    """Add new invocations to the underlying test function using the list
    of basis objects (trying to detect factories automatically)
    for `universal_indirection`

    This is a wrapper over `pytest.mark.parametrize`.

    Can be combined with `pytest.mark.parametrize`.

    Arguments:
        basis_objects:
            A list of basis objects, with any factories having been wrapped
            explicitly (see the package docs).
        ids:
            Sequence of ids each corresponding to the params so that they are
            part of the test id. If no ids are provided they will be generated
            automatically from the params. (see pytest docs)
        scope:
            The scope for which this fixture is shared. (see pytest docs)
        fixture_name:
            Can be used to override the default fixture name. Useful
            for wrapped fixtures.
    """
    return parametrize_universal_indirection_base(
        fixture_name, basis_objects, ids=ids, scope=scope,
    )


def make_universal_indirection_simple_wrapped(name, *, scope='function', autouse=False):
    """Create a wrapping fixture for `universal_indirection_simple`

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
        `universal_indirection_simple`.
    """
    def universal_indirection_simple_wrapped_ff(universal_indirection_simple):
        return universal_indirection_simple
    return pytest.fixture(
        universal_indirection_simple_wrapped_ff, scope=scope, autouse=autouse,
        name=name,
    )
