#!/usr/bin/python3
#TODO 控制这个playerctl 使用歌曲下一个 上一个 暂停等
import json
import time

from song import SUPPORTED_PLAYER,get_player_name,get_song_title

def title_print():
    player_name = get_player_name(SUPPORTED_PLAYER)
    if player_name == None:
        return f"Qcm"
    title=get_song_title(player_name)
    return f'{title}'

def print_string():
    songstring =dict()
    while True:
        result = title_print()
        current_string = result if result is not None else current_string
        print(f'{current_string}',flush=True)
        time.sleep(1)

if __name__ == '__main__':
    print_string()
