import pytest

from song import get_player_name

def test_get_player_name_supported_player_found(mocker):
    mocked_check_output = mocker.patch('song.subprocess.check_output',return_value='Qcm')
    SUPPERTED_PLAYER=['Qcm']
    player_name = get_player_name(SUPPERTED_PLAYER)
    mocked_check_output.assert_called_once_with('playerctl --list-all', shell=True, text=True)
    assert player_name in SUPPERTED_PLAYER

def test_get_player_name_supported_player_not_found(mocker):
    mocker.patch('song.subprocess.check_output',return_value="No players found")
    SUPPERTED_PLAYER=['Qcm']
    with pytest.raises(ValueError):
        get_player_name(SUPPERTED_PLAYER)

def test_get_player_name_empty_supported_player_not_found(mocker):
    mocker.patch('song.subprocess.check_output',return_value="Qcm")
    SUPPERTED_PLAYER=[]
    with pytest.raises(ValueError):
        get_player_name(SUPPERTED_PLAYER)
