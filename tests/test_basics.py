import pytest
from sploitkit.core.console import FrameworkConsole


# @pytest.mark.parametrize('dummy', range(10))
def test_basics(dummy_prompt):
    console = FrameworkConsole(appname='test', prompt_cls=dummy_prompt)
    console.run('help')
    # send_to_console(console, 'help')


@pytest.mark.parametrize('dummy', range(10))
def test_dummy(dummy):
    assert True
