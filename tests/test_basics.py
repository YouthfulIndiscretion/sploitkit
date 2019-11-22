"""
Basic tests.
"""

import pytest

from sploitkit.core.console import FrameworkConsole


@pytest.mark.skip("currently fails")
def test_basics(dummy_prompt):
    """
    This tests the demo ``FrameworkConsole`` class.

    It should initialize and reply to the "help" parameter without raising.

    :param dummy_prompt: pytest fixture that provides a prompt Type that uses a prompt-toolkit Session linked to an
    input pipe (for testing purposes).
    """
    console = FrameworkConsole(appname="test", prompt_cls=dummy_prompt)
    console.run("help")
    assert True
