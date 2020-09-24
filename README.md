# aniGamerDanmu 動畫瘋彈幕下載 lib
將動畫瘋彈幕轉換成 .ass 字幕

# Dependency
```shell
pip3 install requests beautifulsoup4
```

# Usage
可以直接跑
```shell
# 看 help
python3 Danmu.py -h

# 下載 sn=12345 的彈幕
python3 Danmu.py -s 12345

# 下載 sn=12345 作品的所有集數彈幕
python3 Danmu.py -s 12345 --all
```
也可以 ```import Danmu``` 有兩個函數
```python
def download(sn, full_filename)
# sn: 動畫的 sn
# full_filename: 輸出的 path + filename

def downlaod_all(sn, bangumi_path, format_str='{anime_name}[{episode}].ass')
# sn: 動畫的 sn
# bangumi_path: 彈幕會下載在 bangumi_path/<ANIME_NAME>/*.ass
# format_str: 自訂字幕的檔名 可省略
```

若想要變更字體等可以至 ```DanmuTemplate.ass``` 修改，程式會將此檔案作為字幕開頭
# Warning
本專案僅供學習程式設計以及字幕設計所用，請勿用於不法用途