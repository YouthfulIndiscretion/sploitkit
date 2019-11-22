import os
from pathlib import Path

import pytest

from sploitkit.utils.archive import load_from_archive, save_to_archive


@pytest.fixture()
def dummy_archive(here, make_random_files):
    """

    :param here: current working directory
    :type here: Path
    :param make_random_files:
    :type make_random_files: typing.Generator[Path, None, None]
    :return: tuple of archive, list of files
    :rtype: typing.Generator[typing.Tuple[Path, typing.Generator[Path, None, None]]]
    """
    archive = here.joinpath("archive")
    files = list(make_random_files("dummy"))
    assert not archive.exists()
    save_to_archive("./dummy", "./archive")
    yield archive, files


def test_archive_creation(dummy_archive):
    archive, _ = dummy_archive
    assert archive.exists()


def test_archive_creation_then_delete_files(here, make_random_files):
    archive = here.joinpath("archive")
    files = list(make_random_files("dummy"))
    for file in files:
        assert file.exists()
    assert save_to_archive("dummy", "archive", remove=True)
    assert archive.exists()
    for file in files:
        assert not file.exists()


def test_archive_extraction(dummy_archive):
    archive, files = dummy_archive
    Path("output").mkdir()
    assert load_from_archive(str(archive), "output")
    for file in files:
        output_file = Path("output", "dummy", file.name)
        assert output_file.exists()
        assert file.read_bytes() == output_file.read_bytes()


def test_archive_extraction_then_deletion(dummy_archive):
    pass
