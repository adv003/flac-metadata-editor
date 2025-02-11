import pytest
from project import (
    read_metadata,
    validate_metadata_input,
    modify_metadata,
    print_metadata,
    get_user_metadata_changes
)
import os  
from unittest.mock import patch, MagicMock

@pytest.fixture
def sample_flac_path(tmp_path):
    return str(tmp_path / "test.flac")

@pytest.fixture
def sample_metadata():
    return {
        'TITLE': ['Test Song'],
        'ARTIST': ['Test Artist'],
        'ALBUM': ['Test Album']
    }

def test_read_metadata(sample_flac_path):
    with patch('project.FLAC') as mock_flac:
        mock_flac.return_value.tags = {'TITLE': ['Test'], 'ARTIST': ['Test']}
        result = read_metadata(sample_flac_path)
        assert result == {'TITLE': ['Test'], 'ARTIST': ['Test']}

    result = read_metadata("nonexistent.flac")
    assert result is None

    with patch('project.FLAC', side_effect=Exception("Invalid FLAC")):
        result = read_metadata(sample_flac_path)
        assert result is None

def test_validate_metadata_input():
    valid_input = {
        'TITLE': 'Test Song',
        'ARTIST': ['Test Artist'],
        'ALBUM': 'Test Album'
    }
    result = validate_metadata_input(valid_input)
    assert result == {
        'TITLE': ['Test Song'],
        'ARTIST': ['Test Artist'],
        'ALBUM': ['Test Album']
    }

    invalid_input = {
        'TITLE': 123,
        'ARTIST': '',
        'ALBUM': ['', '']
    }
    result = validate_metadata_input(invalid_input)
    assert result == {}

    result = validate_metadata_input("not a dict")
    assert result == {}

def test_modify_metadata(sample_flac_path):
    with patch('project.FLAC') as mock_flac:
        mock_instance = MagicMock()
        mock_flac.return_value = mock_instance
        
        new_metadata = {'TITLE': 'New Title'}
        result = modify_metadata(sample_flac_path, new_metadata)
        
        assert result is True
        mock_instance.update.assert_called_once()
        mock_instance.save.assert_called_once()

    result = modify_metadata(sample_flac_path, {})
    assert result is None

    result = modify_metadata("nonexistent.flac", {'TITLE': 'Test'})
    assert result is None

def test_print_metadata(capsys, sample_metadata):
    print_metadata(sample_metadata)
    captured = capsys.readouterr()
    assert "FLAC Metadata:" in captured.out
    assert "TITLE" in captured.out
    assert "ARTIST" in captured.out
    assert "ALBUM" in captured.out

    print_metadata(None)
    captured = capsys.readouterr()
    assert "No metadata found" in captured.out

def test_get_user_metadata_changes():
    with patch('builtins.input', side_effect=[
        'New Title',  # TITLE
        '',           # ARTIST
        'New Album',  # ALBUM
        '',           # DATE
        '',           # GENRE
        'TEST',       # New field
        'Test Value', # New value
        ''            # Finish
    ]):
        current_metadata = {
            'TITLE': ['Old Title'],
            'ARTIST': ['Old Artist'],
            'ALBUM': ['Old Album']
        }
        result = get_user_metadata_changes(current_metadata)
        assert result == {
            'TITLE': 'New Title',
            'ALBUM': 'New Album',
            'TEST': 'Test Value'
        }, f"Unexpected result: {result}"

    with patch('builtins.input') as mock_input:
        mock_input.side_effect = [
            '', '', '', '', '',  # Skip predefined fields
            'TEST', 'Test Value', ''
        ]
        result = get_user_metadata_changes({})
        assert result == {'TEST': 'Test Value'}, f"Unexpected result: {result}"

def test_main_view_flow():
    with patch('builtins.input') as mock_input:
        with patch('project.read_metadata') as mock_read:
            mock_input.return_value = 'V'
            mock_read.return_value = {'TITLE': ['Test Song']}
            
            from project import main
            with pytest.raises(SystemExit) as e:
                main()
            
            assert e.type == SystemExit

def test_main_modify_flow():
    with patch('builtins.input') as mock_input:
        with patch('project.read_metadata') as mock_read:
            with patch('project.modify_metadata') as mock_modify:
                mock_input.side_effect = [
                    'M',           # Modify
                    'New Title',    # TITLE
                    '',             # ARTIST
                    'New Album',    # ALBUM
                    '',             # DATE
                    '',             # GENRE
                    '',             # No new fields
                    'Y'             # Confirm
                ]
                mock_read.return_value = {
                    'TITLE': ['Old Title'],
                    'ARTIST': ['Old Artist']
                }
                mock_modify.return_value = True
                
                from project import main
                with pytest.raises(SystemExit) as e:
                    main()
                
                assert e.type == SystemExit