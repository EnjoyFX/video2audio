"""Tests of main functionality of video2audio.py"""
from unittest.mock import Mock, patch
import pytest
from video2audio import Converter

# Mocking external dependencies
@pytest.fixture
def mock_tkinter():
    with patch("video2audio.Tk", autospec=True) as mock_tk:
        yield mock_tk


@pytest.fixture
def mock_filedialog():
    with patch("video2audio.fd.askopenfilenames", autospec=True) as mock_fd:
        yield mock_fd


@pytest.fixture
def mock_video_file_clip():
    with patch("video2audio.me.VideoFileClip", autospec=True) as mock_vfc:
        yield mock_vfc


def test_no_files_selected(mock_tkinter, mock_filedialog, caplog):
    mock_filedialog.return_value = []
    c = Converter()
    with pytest.raises(SystemExit):
        c.video_to_mp3()
    assert "No files selected" in caplog.text


def test_successful_conversion(mock_tkinter, mock_filedialog, mock_video_file_clip, caplog):
    mock_filedialog.return_value = ["test.mp4"]
    mock_video_file_clip.return_value.audio = Mock()

    c = Converter()
    c.video_to_mp3()

    assert "Details:" in caplog.text
    assert "Converted: 1(100.0%)" in caplog.text


def test_unsuccessful_conversion(mock_tkinter, mock_filedialog, mock_video_file_clip, caplog):
    mock_filedialog.return_value = ["test.mp4"]
    mock_video_file_clip.return_value.audio = None

    c = Converter()
    c.video_to_mp3()

    assert "Audio not found in" in caplog.text
    assert "Converted: 0(0.0%)" in caplog.text


def test_error_while_opening_video(mock_tkinter, mock_filedialog, mock_video_file_clip, caplog):
    mock_filedialog.return_value = ["test.mp4"]
    mock_video_file_clip.side_effect = KeyError("Some Error")

    c = Converter()
    with pytest.raises(SystemExit):
        c.video_to_mp3()

    assert "Issue with opening video" in caplog.text
