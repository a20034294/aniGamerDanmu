import requests
import json
import random
from bs4 import BeautifulSoup
import re
import os
import argparse

def download(sn, full_filename):
    h = {
        'Content-Type':
        'application/x-www-form-urlencoded;charset=utf-8',
        'origin':
        'https://ani.gamer.com.tw',
        'authority':
        'ani.gamer.com.tw',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    data = {'sn': str(sn)}
    r = requests.post(
        'https://ani.gamer.com.tw/ajax/danmuGet.php', data=data, headers=h)

    if r.status_code != 200:
        print('sn=' + str(sn) + ' 彈幕下載失敗, status_code=' + str(status_code))
        return

    output = open(full_filename, 'w', encoding='utf8')
    with open('DanmuTemplate.ass', 'r', encoding='utf8') as temp:
        for line in temp.readlines():
            output.write(line)

    j = json.loads(r.text)

    height = 50
    last_time = 0
    for danmu in j:
        output.write('Dialogue: ')
        output.write('0,')

        start_time = int(danmu['time'] / 10)
        hundred_ms = danmu['time'] % 10
        m, s = divmod(start_time, 60)
        h, m = divmod(m, 60)
        output.write(f'{h:d}:{m:02d}:{s:02d}.{hundred_ms:d}0,')

        if danmu['position'] == 0: # Roll danmu
            end_time = start_time + random.randint(8, 12)
            m, s = divmod(end_time, 60)
            h, m = divmod(m, 60)
            output.write(f'{h:d}:{m:02d}:{s:02d}.{hundred_ms:d}0,')

            if start_time - last_time >= 3:
                height = 50
            last_time = start_time

            output.write(
                'Roll,,0,0,0,,{\\move(1920,' + str(height) + ',-500,' + str(height) + ')\\1c&H4C' + danmu['color'][1:] + '}')
            height = (height % 500) + 50
        elif danmu['position'] == 1: # Top danmu
            end_time = start_time + 5
            m, s = divmod(end_time, 60)
            h, m = divmod(m, 60)
            output.write(f'{h:d}:{m:02d}:{s:02d}.{hundred_ms:d}0,')
            output.write(
                'Top,,0,0,0,,{\\1c&H4C' + danmu['color'][1:] + '}')
        else: # Bottom danmu
            end_time = start_time + 5
            m, s = divmod(end_time, 60)
            h, m = divmod(m, 60)
            output.write(f'{h:d}:{m:02d}:{s:02d}.{hundred_ms:d}0,')
            output.write(
                'Bottom,,0,0,0,,{\\1c&H4C' + danmu['color'][1:] + '}')


        output.write(danmu['text'])
        output.write('\n')

    print('彈幕下載完成 file: ' + full_filename)

def downlaod_all(sn, bangumi_path):
    h = {
        'Content-Type':
        'application/x-www-form-urlencoded;charset=utf-8',
        'origin':
        'https://ani.gamer.com.tw',
        'authority':
        'ani.gamer.com.tw',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    r = requests.get('https://ani.gamer.com.tw/animeVideo.php?sn=' + str(sn), headers=h)

    if r.status_code != 200:
        print(str(sn) + '彈幕下載失敗, status_code=' + str(status_code))
        return

    soup = BeautifulSoup(r.text, 'lxml')
    anime_name = re.match(r'(^.+)\s\[.+\]$', soup.find_all('div', class_='anime_name')[0].h1.string).group(1)
    print(anime_name)

    sn_list = soup.find_all('section', class_='season')[0].find_all('a')

    os.makedirs(os.path.join(bangumi_path, anime_name), exist_ok=True)

    for s in sn_list:
        download(s['href'][4:], os.path.join(bangumi_path, anime_name, anime_name + '[' + s.string + '].ass'))

def get_info(sn):
    h = {
        'Content-Type':
        'application/x-www-form-urlencoded;charset=utf-8',
        'origin':
        'https://ani.gamer.com.tw',
        'authority':
        'ani.gamer.com.tw',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    r = requests.get('https://ani.gamer.com.tw/animeVideo.php?sn=' + str(sn), headers=h)

    if r.status_code != 200:
        print(str(sn) + '獲取資訊失敗, status_code=' + str(status_code))
        return

    soup = BeautifulSoup(r.text, 'lxml')
    anime_name = re.match(r'(^.+)\s\[.+\]$', soup.find_all('div', class_='anime_name')[0].h1.string).group(1)
    episode = re.match(r'^.+\s\[(.+)\]$', soup.find_all('div', class_='anime_name')[0].h1.string).group(1)
    return anime_name, episode

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sn', '-s', type=int, help='動畫 SN 碼(數字)')
    parser.add_argument('--all', '-a', action='store_true', help='下載所有彈幕')
    # parser.add_argument('--episode', '-e', type=str, help='根據集數下載，以逗號分開')
    parser.add_argument('--path', '-p', type=str, help='下載的資料夾位置，預設為 ./bangumi/<ANIME_NAME>/*.ass', default='bangumi')

    arg = parser.parse_args()
    if arg.sn == None:
        print('請輸入 SN')
        exit(0)
    if arg.all == True:
        downlaod_all(arg.sn, arg.path)
        exit(0)

    anime_name, episode = get_info(arg.sn)
    os.makedirs(os.path.join(arg.path, anime_name), exist_ok=True)
    download(arg.sn, os.path.join(arg.path, anime_name, anime_name + '[' + episode + '].ass'))

