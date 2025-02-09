import pytest
import os
from project import read_metadata, modify_metadata, validate_metadata_input
from mutagen.flac import FLAC

@pytest.fixture
def sample_flac(tmp_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(current_dir, "samples", "04. All Falls Down.flac")
    dest = tmp_path / "test.flac"
    with open(source, 'rb') as f:
        dest.write_bytes(f.read())
    return dest

def test_read_metadata_valid(sample_flac):
    metadata = read_metadata(str(sample_flac))
    assert isinstance(metadata, dict)
    assert 'TITLE' in metadata
    assert metadata['TITLE'][0] == 'All Falls Down'

def test_read_metadata_file_not_found():
    assert read_metadata("nonexistent.flac") is None

def test_read_metadata_invalid_file(tmp_path):
    invalid_file = tmp_path / "invalid.txt"
    invalid_file.write_text("Not a FLAC file")
    assert read_metadata(str(invalid_file)) is None

def test_modify_metadata_valid(sample_flac):
    new_metadata = {'TITLE': 'New Title'}
    assert modify_metadata(str(sample_flac), new_metadata) is True
    updated = read_metadata(str(sample_flac))
    assert updated['TITLE'][0] == 'New Title'

def test_modify_metadata_invalid_type(sample_flac):
    assert modify_metadata(str(sample_flac), "not a dict") is None

def test_modify_metadata_invalid_value(sample_flac, caplog):
    new_metadata = {'ARTIST': '', 'TITLE': ['', 'Valid']}
    assert modify_metadata(str(sample_flac), new_metadata) is True
    updated = read_metadata(str(sample_flac))
    assert 'ARTIST' not in updated or updated['ARTIST'][0] != ''

def test_validate_metadata_input_valid():
    valid = {'TITLE': 'Valid Title', 'ARTIST': ['Valid Artist']}
    assert len(validate_metadata_input(valid)) == 2

def test_validate_metadata_input_invalid():
    invalid = {'TITLE': '', 'ARTIST': [123], 'ALBUM': 'Valid Album'}
    valid = validate_metadata_input(invalid)
    assert 'TITLE' not in valid and 'ARTIST' not in valid
    assert 'ALBUM' in valid