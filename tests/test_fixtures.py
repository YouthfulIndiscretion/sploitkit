"""
Tests custom-made fixtures
"""


def test_make_random_file(here, make_random_file):
    assert len(list(here.iterdir())) == 0
    random_file = list(make_random_file())[0]
    assert len(list(here.iterdir())) == 1
    assert random_file.exists()
    assert random_file.parent == here


def test_make_random_files(here, make_random_files):
    assert len(list(here.iterdir())) == 0
    files = list(make_random_files())
    for file in files:
        assert file.exists()
        assert file.is_file()
        assert file.stat().st_size > 0
    assert len(list(here.iterdir())) == 10


def test_make_random_file_in_subfolder(here, make_random_files):
    subfolder = here.joinpath("dummy")
    assert not subfolder.exists()
    list(make_random_files(parent_dir=subfolder, count=25, min_size=10, max_size=10))
    assert subfolder.exists()
    assert len(list(subfolder.iterdir())) == 25


def test_random_file_size(here, make_random_files):
    files = list(make_random_files(min_size=0, max_size=32))
    for file in files:
        assert 0 <= file.stat().st_size <= 32
