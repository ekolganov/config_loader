import os
from contextlib import contextmanager
from typing import Iterable, NamedTuple, Any, Callable
from read_config import load_config

import yaml

TConfig = Any


class TestCase(NamedTuple):
    key: str
    conf: dict
    assert_exists: Iterable[str] = None
    assert_not_exists: Iterable[str] = None

    def run_assert(self, result: TConfig):
        for key in self.assert_exists:
            # check __contains__ method
            assert key in result
            # check that value has passed
            assert result[key] is not None

        for key in self.assert_not_exists:
            assert key not in result

            try:
                result[key]
            except KeyError:
                pass
            else:
                AssertionError(f'config[{key}] should raise KeyError')


@contextmanager
def test_case(params: TestCase) -> Callable[[TConfig], None]:
    filename = f'{params.key}.yaml'
    with open(filename, 'w') as file:
        file.write(yaml.dump(params.conf))
    try:
        yield params.run_assert
    finally:
        os.remove(filename)


def run_tests():
    with test_case(TestCase(
            'test_1',
            {'a': 1, 'b': {'ba': 2, 'bb': 'vvvv'}},
            ('a', 'b', 'b.ba', 'b.bb'),
            ('ba.b', 'bb', 'ba'),
    )) as run_case:
        config = load_config('test_1.yaml')
        run_case(config)

    with test_case(TestCase(
            'test_2',
            {'pwd': '$PWD', 'web': {'port': 10, 'url': {'value': 'yandex.ru', 'params': {'one': 1, 'funny': False}}}},
            ('pwd', 'web.port', 'web', 'web.url.value', 'web.url', 'web.url.params.funny'),
            ('port', 'url', 'port.url', 'one.params.url.web'),
    )) as run_case:
        config = load_config('test_2.yaml')
        run_case(config)


if __name__ == '__main__':
    run_tests()
