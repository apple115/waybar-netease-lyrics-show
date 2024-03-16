#!/usr/bin/python3
import os
import subprocess
import time

# TODO: 如果这个QCM没有反应 返回什么
# TODO: 将这个输出字符串的地方进行独立
# TODO： 添加args 利于这个代码调试

SUPPERTED_PLAYER=['Qcm']

def get_player_name(SUPPERTED_PLAYER):
    if SUPPERTED_PLAYER==None:
        raise ValueError("suppert player is none")
    command = f'playerctl --list-all'
    result = subprocess.check_output(command,shell=True,text=True).strip()
    current_play=next((player for player in SUPPERTED_PLAYER if player in result),None)
    # current_play=None
    # for player in SUPPERTED_PLAYER:
    #     if player in result:
    #         current_play = player
    #         break
    if current_play is None:
        raise ValueError("no suppert player")
    return current_play

#print(get_player_name(SUPPERTED_PLAYER))

def getPlayShell():
    pass


playerName = os.popen("playerctl --list-all |  head -n 1").read().strip()
# playerShell=f'playerctl --player={playerName}'
playerShell = f"playerctl --player=Qcm"


def getSongId():
    """
    返回songid
    """

    command = (
        f"{playerShell} metadata mpris:trackid | cut -d '/' -f3 | cut -d \"'\" -f1"
    )
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()


def getSongTitle():
    """
    返回songtitle
    """

    command = f"{playerShell} metadata title"
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()


def get_playing_song_position():
    """
    返回song位置
    """

    command = f"{playerShell} metadata --format '{{{{ duration(position) }}}}'"
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()


def getSongLyricsbyApi(id):
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


def getSongLyricsByFile(songId, SongTitle):
    # 如果当前目录没有lyricfiles 则创造一个文件夹
    if not os.path.exists("lyricfiles"):
        os.makedirs("lyricfiles")
        print("Created directory: lyricfiles")
    # 如果lyricfiles里 没有songTitle+songid的歌词文件
    # 则添加这个“songTitlesongid.lrc”
    lyric_file = f"./lyricfiles/{SongTitle}{songId}.lrc"
    if not os.path.exists(lyric_file):
        attempts = 0
        lyric = getSongLyricsbyApi(songId)
        while lyric == "" and attempts < 3:
            time.sleep(1)
            lyric = getSongLyricsbyApi(songId)
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


# print(get_playing_song_position())


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


# TODO：优化这个代码
def song():
    # print(title)
    currentLyric = ""
    lyric = ""
    while True:
        title = getSongTitle()
        oldtitle = ""
        if title != "":
            songId = getSongId()
            current_position = get_playing_song_position()
            if title != oldtitle or lyric == "":
                lyric = getSongLyricsByFile(songId, title)
                oldtitle = title
            result = get_song_current_lyric_from_lyrics_by_current_position(
                lyric, current_position
            )
            currentLyric = result if result is not None else currentLyric
        print(currentLyric, flush=True)
        time.sleep(1)

def print_string():
    pass

# song()
