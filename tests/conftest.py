import typing
import os
import pytest
from sploitkit.core.console import Console
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.history import History
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.shortcuts import PromptSession


@pytest.fixture()
def dummy_prompt():
    class DummyPrompt(PromptSession):

        def __init__(self, *args, **kwargs):
            self.input_pipe = create_pipe_input()
            kwargs['input'] = self.input_pipe
            kwargs['output'] = DummyOutput()
            super(DummyPrompt, self).__init__(*args, **kwargs)

        def send_text(self, text: str):
            pass

        def send_bytes(self, bytes_: bytes):
            pass

    yield DummyPrompt


@pytest.fixture()
def cli_input(
        content: typing.Union[str, bytes],
        mode: str = EditingMode.EMACS,
        multiline: bool = False,
        history: typing.Optional[History] = None,
        key_bindings: typing.Optional[KeyBindings] = None
):
    pipe = create_pipe_input()
    _send_func_select: typing.Dict[typing.Type, typing.Callable] = {
        str: pipe.send_text,
        bytes: pipe.send_bytes
    }
    try:
        _send_func = _send_func_select[type(content)]
    except KeyError:
        raise TypeError(f'CLI accepts "str" or "bytes", not "{type(content)}"')
    try:
        _send_func(content)
        session = PromptSession(
            input=pipe,
            output=DummyOutput(),
            editing_mode=mode,
            history=history,
            multiline=multiline,
            key_bindings=key_bindings,
        ).prompt()
        # session.prompt()
        return session.default_buffer.document, session.app
    finally:
        pipe.close()


@pytest.fixture()
def send_to_console():
    def send_to_console(
            console: Console,
            content: typing.Union[str, bytes],
    ):
        pipe = create_pipe_input()
        _send_func_select: typing.Dict[typing.Type, typing.Callable] = {
            str: pipe.send_text,
            bytes: pipe.send_bytes
        }
        try:
            _send_func = _send_func_select[type(content)]
        except KeyError:
            raise TypeError(f'CLI accepts "str" or "bytes", not "{type(content)}"')

        try:
            _send_func(content)
            session = PromptSession(
                input=pipe,
                completer=getattr(console._session, 'completer'),
                history=getattr(console._session, 'history'),
                validator=getattr(console._session, 'validator'),
                style=getattr(console._session, 'style'),
            )
            session.prompt()
            return session.default_buffer.document, session.app
        finally:
            pipe.close()
    return send_to_console


# cd into a temporary directory before running each test
# default location: /tmp/pytest-of-$(whoami)/pytest-N
# where N is the run ID (by default, 3 runs are kept)
@pytest.fixture(autouse=True)
def _tmp_test_dir(tmp_path):
    old_dir = os.getcwd()
    tmp_dir = tmp_path
    tmp_dir.mkdir(exist_ok=True)
    os.chdir(str(tmp_dir))
    yield
    os.chdir(old_dir)

