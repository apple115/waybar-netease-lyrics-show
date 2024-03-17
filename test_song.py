import pytest

from song import get_player_name,get_song_id

def test_get_player_name_supported_player_found(mocker):
    mocker.patch('song.subprocess.check_output',return_value='Qcm')
    SUPPERTED_PLAYER=['Qcm']
    player_name = get_player_name(SUPPERTED_PLAYER)
    assert player_name in SUPPERTED_PLAYER

def test_get_player_name_supported_player_not_found(mocker):
    mocker.patch('song.subprocess.check_output',return_value="No players found")
    SUPPERTED_PLAYER=['Qcm']
    player_name = get_player_name(SUPPERTED_PLAYER)
    assert player_name is None

def test_get_player_name_empty_supported_player_not_found(mocker):
    mocker.patch('song.subprocess.check_output',return_value="Qcm")
    SUPPERTED_PLAYER=[]
    with pytest.raises(ValueError):
        get_player_name(SUPPERTED_PLAYER)
