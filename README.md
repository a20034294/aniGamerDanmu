# aniGamerDanmu 動畫瘋彈幕下載 lib
將動畫瘋彈幕轉換成 .ass 字幕

# Dependency
```shell
pip3 install requests beautifulsoup4
```

# Usage
可以直接跑
```shell
python3 Danmu.py -h
python3 Danmu.py -s 12345
python3 Danmu.py -s 12345 --all
```
也可以 ```import Danmu``` 有兩個函數
```python
def download(sn, full_filename)
# sn: 動畫的 sn
# full_filename: 輸出的 path + filename

def downlaod_all(sn, bangumi_path)
# sn: 動畫的 sn
# bangumi_path: 彈幕會下載在 bangumi_path/<ANIME_NAME>/*.ass
```

# Warning
本專案僅供學習程式設計以及字幕設計所用，請勿用於不法用途