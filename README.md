# waybar-netease-lyrics-show
display lyrics on waybar

这是一个简单的的实验项目 思路来自[waybar-netease-music-lyrics](https://github.com/kangxiaoju/waybar-netease-music-lyrics)
因为使用的网易云api 短时间内多次调用 会不返回歌词 所以在此基础上实现了这个lyric的缓存 *lyricfiles/*
在waybar 上显示歌词 目前只支持Qcm
![显示图片](./images/showbar)

需要jq playerctl Qcm curl

如何配置waybar

```
"custom/lyrics":{
    "format": "{icon} {}",
    "format-icons": ["", ""],
    "exec":"~/.config/waybar/plugin/LyricShow/song.py"
    }
```
这个是简单[讲解](https://apple115.github.io/2024/03/18/waybar-netease-lyrics-show%E7%9A%84%E8%AE%B2%E8%A7%A3/)

希望大家给出意见

- [] TODO: 添加上一首 下一首  暂停
