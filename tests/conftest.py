import os
import random
import string
from pathlib import Path

import pytest
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.shortcuts import PromptSession


@pytest.fixture()
def here():
    yield Path(".").absolute()


@pytest.fixture()
def random_string():
    def random_string(length: int = 10):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
        )

    return random_string


@pytest.fixture()
def make_random_file(random_string):
    def make_random_file(
        parent_dir: Path = None, min_size: int = 128, max_size: int = 512
    ):
        parent_dir = Path(parent_dir) if parent_dir else Path(".")
        parent_dir.mkdir(exist_ok=True, parents=True)
        file_name = random_string()
        file_size = random.randint(min_size, max_size)
        output_file = Path(parent_dir, file_name).absolute()
        output_file.write_bytes(os.urandom(file_size))
        yield output_file

    return make_random_file


@pytest.fixture()
def make_random_files(make_random_file):
    def make_random_files(
        parent_dir: Path = None,
        count: int = 10,
        min_size: int = 128,
        max_size: int = 512,
    ):
        parent_dir = Path(parent_dir) if parent_dir else Path(".")
        for _ in range(count):
            yield from make_random_file(parent_dir, min_size, max_size)

    return make_random_files


@pytest.fixture()
def make_random_dir(make_random_files, random_string):
    def make_random_dir(
        min_file_count: int = 10,
        max_file_count: int = 50,
        min_size: int = 128,
        max_size: int = 512,
    ):
        file_count = random.randint(min_file_count, max_file_count)
        dir_name = random_string()
        dir_path = Path(dir_name)
        yield from make_random_files(dir_path, file_count, min_size, max_size)

    return make_random_dir


@pytest.fixture()
def make_random_dirs(make_random_dir):
    def make_random_dirs(
        count: int = 10,
        min_file_count: int = 10,
        max_file_count: int = 50,
        min_size: int = 128,
        max_size: int = 512,
    ):
        for _ in range(count):
            yield from make_random_dir(
                min_file_count, max_file_count, min_size, max_size
            )

    return make_random_dirs


@pytest.fixture()
def dummy_prompt():
    class DummyPrompt(PromptSession):
        def __init__(self, *args, **kwargs):
            self.input_pipe = create_pipe_input()
            kwargs["input"] = self.input_pipe
            kwargs["output"] = DummyOutput()
            super(DummyPrompt, self).__init__(*args, **kwargs)

        def send_text(self, text: str):
            pass

        def send_bytes(self, bytes_: bytes):
            pass

    yield DummyPrompt


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
