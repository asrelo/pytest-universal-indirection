# asrelo-pytest-universal-indirection

The universal indirection fixture accepts a *basis object* (see below) as a parameter (typically &mdash; an indirect parameter from a test) and produces a value using that object. This was developed as a (somewhat) convenient solution to pytest's inability to process fixtures passed to a test through `pytest.parametrize`.

*Basis objects* can be standalone objects or factories for objects. Standalone objects are then provided to code in tests directly (and they are better be immutable). Factories for objects follow the pytest's convention for fixture functions: one either returns the object to be used or yields a single object to be used (pytest's [teardown mechanism](https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended)). Factories are either called with no arguments or a single positional argument for a parameter value when the created fixture is parametrized (see below).

Note, you still **cannot just give fixtures as parameters** &mdash; that appears to be impossible with pytest, it won't realize that a test depends on those mapped fixtures.

There are 2 ways to give the basis objects.

* All factories are marked explicitly by wrapping them with a corresponding class:
  * for a factory returning a single object: `BasisCallableWrapper`,
  * for a factory yielding a single object (pytest's teardown mechanism): `BasisGeneratorFunctionWrapper`,
  * standalone objects are not wrapped.

     ```python 
     def factory_1():
         return [-1, 0, 1]

     def factory_2():
         obj = create_env_object()
         yield obj
         delete_env_object(obj)

     BASIS_OBJECTS = [
         (1, 2, 3),
         'abracadabra',
         BasisCallableWrapper(factory_1),
         BasisGeneratorFunctionWrapper(factory_2),
     ]
     ```

* Factories are detected on the fly (the "simple" interface). This method can be less verbose and thus more convenient, but it can misidentify factories in certain situations.

  Functions of the "simple" interface are similar to functions of the normal interface and they are marked as `simple` in their names.

  For the "simple" interface, a the algorithm to determine the kind of a basis object is:

  1. If the object is NOT callable, use it directly.
  2. Otherwise, call it and store the resulting object.
  3. If the result is NOT an instance of `Iterator`, conclude that the basis object was a returning factory, and use the resulting object.
  4. Otherwise, conclude that the basis object was the yielding factory, and proceed to request a single object from that iterator to use.

     ```python 
     def factory_1():
         return [-1, 0, 1]

     def factory_2():
         obj = create_env_object()
         yield obj
         delete_env_object(obj)

     BASIS_OBJECTS_SIMPLE = {
         (1, 2, 3),
         'abracadabra',
         factory_1,
         factory_2,
     }
     ```

You can then use a fixture `universal_indirection` (or `universal_indirection_simple`) with an indirectly parametrized test. The corresponding fixture can be indirectly parametrized without extra code with `parametrize_universal_indirection` (or `parametrize_universal_indirection_simple`):

```python
@parametrize_universal_indirection(BASIS_OBJECTS)
def test_parametrized(universal_indirection):
    # use universal_indirection as the needed value
    ...
```

You can pass `ids` and `scope` arguments to `parametrize_universal_indirection` as well.

There is no way to avoid some boilerplate to use some function as a standalone fixture and as a basis object at the same time. The example below shows minimal code for the case of a fixtre that does not depend on any other fixture.

```python
# factory function
def build_context():
    return Context(...)

# creates a fixture named "context"
context = pytest.fixture(name='context')(fixture_context)

# uses the fixture normally
def test_1(context):
    ...

# uses the underlying factory function as a basis object
@parametrize_universal_indirection([build_context])
def test_2(universal_indirection):
    ...
```

To customize the `universal_indirection` (or `universal_indirection_simple`) fixture, you can use `make_universal_indirection_wrapped` (or `make_universal_indirection_simple_wrapped`) to create a new wrapper fixture **with a new name**, allowing you to specify `scope` and `autouse` arguments. Or you can create wrapping fixtures yourself. You need to specify the name of the wrapping fixture(s) in function signatures of tests and in `parametrize` calls. `parametrize_universal_indirection` can accomodate different name(s) with the `fixtures` keyword argument.

```python
indirect_for_module = make_universal_indirection_wrapped(
    'indirect_for_module', scope='module',
)

@parametrize_universal_indirection(BASIS_OBJECTS, fixtures='indirect_for_module')
def test_smth(indirect_for_module):
    ...
```

You can as well use multiple wrapped fixtures in the same test, in a similar way to how you use `pytest.mark.parametrize` to set multiple parameters at once:

```python
indirect_x = make_universal_indirection_wrapped('x')
indirect_y = make_universal_indirection_wrapped('y')

@parametrize_universal_indirection(
    (
        (lambda: [-1, 0, 1], 'a'),
        (lambda: [1, 2, 3], 'b'),
    ),
    fixtures=('indirect_x', 'indirect_y'),
)
def test_smth(indirect_x, indirect_y):
    ...
```

## Supported version of pytest

The developer chose to have the plugin support only the major release 8 of pytest for now. Support can be extended to past and future pytest releases in the future.
