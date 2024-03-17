#!/usr/bin/python3
import os
import subprocess
import time

# TODO: 如果这个QCM没有反应 返回什么
# TODO: 将这个输出字符串的地方进行独立
# TODO： 添加args 利于这个代码调试

SUPPORTED_PLAYER = ["Qcm"]


def get_player_name(SUPPORTED_PLAYER):
    """
    return player

    Args:
    SUPPORTED_PLAYER is  all support song player

    Return:
      current_play | none
    """
    if SUPPORTED_PLAYER == None:
        raise ValueError("support player is none")
    command = f"playerctl --list-all"
    result = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True,text=True)
    result = result.strip()
    current_play = next(
        (player for player in SUPPORTED_PLAYER if player in result), None
    )
    # current_play=None
    # for player in SUPPORTED_PLAYER:
    #     if player in result:
    #         current_play = player
    #         break
    return current_play

#get_player_name(SUPPORTED_PLAYER)


def get_song_id(playerName):
    """
    返回songid
    """
    playerShell = f"playerctl --player={playerName}"

    command = (
        f"{playerShell} metadata mpris:trackid | cut -d '/' -f3 | cut -d \"'\" -f1"
    )
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()




def get_song_title(playerName):
    """
    返回songtitle
    """
    playerShell = f"playerctl --player={playerName}"
    command = f"{playerShell} metadata title"
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()


def get_playing_song_position(playerName):
    """
    返回song位置
    """
    playerShell = f"playerctl --player={playerName}"
    command = f"{playerShell} metadata --format '{{{{ duration(position) }}}}'"
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()



def get_song_lyrics_by_api(id):
    """
    这个函数通过读取到网易云的歌词api
    Args：
      id：网易云音乐的歌词id
    Returns：
      返回result
    Raise：
      id 是空 valueError
    """
    if id is None:
        raise ValueError("songId is None")
    command = f'curl -s "music.163.com/api/song/media?id={id}" | jq -r ".lyric"'
    result = subprocess.check_output(command, shell=True, text=True).strip()
    return result


def get_song_lyrics_by_file(songId, SongTitle):
    # 如果当前目录没有lyricfiles 则创造一个文件夹
    if not os.path.exists("lyricfiles"):
        os.makedirs("lyricfiles")
        # print("Created directory: lyricfiles")
    # 如果lyricfiles里 没有songTitle+songid的歌词文件
    # 则添加这个“songTitlesongid.lrc”
    lyric_file = f"./lyricfiles/{SongTitle}{songId}.lrc"
    if not os.path.exists(lyric_file):
        attempts = 0
        lyric = get_song_lyrics_by_api(songId)
        while lyric == "" and attempts < 3:
            time.sleep(1)
            lyric = get_song_lyrics_by_api(songId)
            attempts += 1
        if lyric == "":
            raise ValueError(f"API没有返回歌词 歌词id：{songId}")
        with open(lyric_file, "w") as file:
            file.write(f"{lyric}")
        # print("api")
    else:
        with open(lyric_file, "r") as file:
            lyric = file.read()
            if lyric == "":
                raise ValueError("此文件为空")
    return lyric




def get_song_current_lyric_from_lyrics_by_current_position(lyrics, current_position):
    """
    这个函数通过读取到网易云的歌词api
    Args：
      lyrics:全部歌词
      current_time：当前时间
    Returns：
      当前时间有返回当前时间有返回current_Lyrics : string
      当前时间没有返回None
    Raise：
      无
    """
    for line in lyrics.split("\n"):
        if line.strip().startswith("["):
            position = line[2:6]
            if current_position == position:
                pasts = line.split("]")
                if len(pasts) == 2:
                    current_Lyric = pasts[1]
                else:
                    current_Lyric = ""
                return current_Lyric
    else:
        return None


lyrics_cache = {}


# TODO：优化这个代码
def song():
    """
    Args:

    Return:
    player_name is None  return string'no song player'player
    else return currentLyric

    """
    global lyrics_cache

    player_name = get_player_name(SUPPORTED_PLAYER)
    if player_name is None:
        return f"no song player"
    title = get_song_title(player_name)
    if title == "":
        return f"song is not play"
    songId = get_song_id(player_name)
    current_position = get_playing_song_position(player_name)
    if title in lyrics_cache:
        lyric = lyrics_cache[title]
    else:
        lyric = get_song_lyrics_by_file(songId, title)
        # 将获取的歌词存入缓存
        lyrics_cache[title] = lyric

    result = get_song_current_lyric_from_lyrics_by_current_position(
        lyric, current_position
    )

    currentLyric = result if result is not None else ""
    return currentLyric


def print_string():
    current_string = "current_string is None"
    while True:
        current_string = song()
        print(current_string, flush=True)
        time.sleep(1)

if __name__ == '__main__':
    print_string()
