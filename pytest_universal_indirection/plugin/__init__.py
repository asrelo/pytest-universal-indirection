import pytest

from pytest_universal_indirection._common import (
    BasisCallableWrapper,
    BasisGeneratorFunctionWrapper,
)
from .simple import universal_indirection_simple_ff


def _get_value_from_basis_object(obj):
    if isinstance(obj, BasisGeneratorFunctionWrapper):
        return obj.get_value()
    if isinstance(obj, BasisCallableWrapper):
        return obj.get_value()
    return obj


@pytest.fixture(name='universal_indirection')
def universal_indirection_ff(request):
    """Universal indirection fixture
    
    Requires a parameter:
        A basis object (if it is a factory, it must be marked by wrapping it
        with the corresponding class.)

    Produces:
        A value acquired from the basis object passed as parameter.
    """
    return _get_value_from_basis_object(request.param)
