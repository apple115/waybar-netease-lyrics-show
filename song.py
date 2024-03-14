#!/usr/bin/python3
import os
import subprocess
import time

playerName = os.popen("playerctl --list-all |  head -n 1").read().strip()
# playerShell=f'playerctl --player={playerName}'
playerShell = f"playerctl --player=Qcm"


def getSongId():
    # 构建获取歌曲 ID 的命令
    command = (
        f"{playerShell} metadata mpris:trackid | cut -d '/' -f3 | cut -d \"'\" -f1"
    )

    # 使用 subprocess 运行命令并获取输出
    result = subprocess.check_output(command, shell=True, text=True)

    # 返回处理后的结果
    return result.strip()


def getSongTitle():
    command = f"{playerShell} metadata title"
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()


def get_playing_song_position():
    command = f"{playerShell} metadata --format '{{{{ duration(position) }}}}'"
    result = subprocess.check_output(command, shell=True, text=True)
    return result.strip()


# print(getSongId())


def getSongLyricsbyApi(id):
    """
    这个函数通过读取到网易云的歌词api
    Args：
      id：网易云音乐的歌词id
    Returns：
      返回None
    Raise：
      id 是空
    """
    try:
        if id is None:
            raise ValueError("ID is None")
        command = f'curl -s "music.163.com/api/song/media?id={id}" | jq -r ".lyric"'
        result = subprocess.check_output(command, shell=True, text=True).strip()
        return result
    except subprocess.CalledProcessError as emit:
        print(f"Error executing command:{emit}")
        return None
    except ValueError as emit:
        print(f"Error:{emit}")
        return None


# 如果这个文件夹没有这个歌词列表
def getSongLyricsByFile(songId, SongTitle):
    # 如果当前目录没有lyricfiles 则创造一个文件夹
    if not os.path.exists("lyricfiles"):
        os.makedirs("lyricfiles")
        print("Created directory: lyricfiles")
    # 如果lyricfiles里 没有songTitle+songid的歌词文件
    # 则添加这个“songTitlesongid.lrc”
    lyric_file = f"./lyricfiles/{SongTitle}{songId}.lrc"
    if not os.path.exists(lyric_file):
        lyric = getSongLyricsbyApi(songId)
        # TODO: 尝试增加三次再返回错误
        if lyric == "":
            raise ValueError(f"api没有返回歌词{songId}")
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
            position = get_playing_song_position()
            if title != oldtitle or lyric == "":
                lyric = getSongLyricsByFile(songId, title)
                oldtitle = title
            for line in lyric.split("\n"):
                if line.strip().startswith("["):
                    line_position = line[2:6]
                    # print(line_position)
                    if position == line_position:
                        pasts = line.split("]")
                        if len(pasts)==2:
                            currentLyric = pasts[1]
                        else:
                            currentLyric=""
                        # currentLyric = "" if line[11:] is None else line[11:]

        print(currentLyric, flush=True)
        time.sleep(1)


song()
