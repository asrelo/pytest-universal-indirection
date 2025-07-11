from collections.abc import Iterator

import pytest


def _get_value_from_basis_object(obj):
    if callable(obj):
        res = obj()
        if isinstance(res, Iterator):
            yield next(res)  #pylint: disable=stop-iteration-return
            return res.close()
        return res
    return obj


@pytest.fixture(name='universal_indirection_simple')
def universal_indirection_simple_ff(request):
    """Universal indirection fixture

    **Attention**: This fixture has a "simple" interface in relation to basis
    objects, meaning it tries to detect factories in the mapping on the fly.
    It can make mistakes in certain situations; see the package docs.
    
    Requires a parameter:
        A basis object.

    Produces:
        A value acquired from the basis object passed as parameter.
    """
    return _get_value_from_basis_object(request.param)
