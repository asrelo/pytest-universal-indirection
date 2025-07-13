class BasisCallableWrapper:
    """Wrapper for a factory function returning an object

    Attributes:
        callable_: The wrapped callable object.
    """
    def __init__(self, callable_):
        """Args:
            callable_: A callable object to wrap.
        """
        self.callable_ = callable_
    def get_value(self):
        return self.callable_()
    def get_value_parametrized(self, param):
        return self.callable_(param)


class BasisGeneratorFunctionWrapper:
    """Wrapper for a generator function yielding a single object before being
    closed

    **Attention**: this functools.wraps a generator function, not generator object!
    For example, a function that `yield`s is a generator function (good),
    and a generator expression produces a generator object (bad).
    See [Yield
    expressions](https://docs.python.org/3/reference/expressions.html#yield-expressions).

    Attributes:
        callable_: The wrapped generator function.
    """
    def __init__(self, generator_function):
        """Args:
            callable_: A generator function to wrap.
        """
        self.generator_function = generator_function
    def get_value(self):
        gen = self.generator_function()
        yield next(gen)  #pylint: disable=stop-iteration-return
        return gen.close()
    def get_value_parametrized(self, param):
        gen = self.generator_function(param)
        yield next(gen)  #pylint: disable=stop-iteration-return
        return gen.close()
