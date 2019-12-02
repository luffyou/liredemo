#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: loveNight

import json
import itertools
import urllib
import requests
import os
import re
import sys
from PIL import Image
import shutil

str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}

name_dict = {
    '定窑白瓷':'dingyao',
    '哥窑':'geyao',
    '钧窑':'junyao',
    '汝窑':'ruyao',
    '元青花瓷':'yuanqinghuaci'
}

word_list = ['元青花瓷','定窑白瓷','钧窑 玫瑰紫', '汝窑 天青水仙盆', '哥窑 弦纹瓶']

# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
char_table = {ord(key): ord(value) for key, value in char_table.items()}

# 解码图片URL
def decode(url):
    # 先替换字符串
    for key, value in str_table.items():
        url = url.replace(key, value)
    # 再替换剩下的字符
    return url.translate(char_table)

# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

# 解析JSON获取图片URL
re_url = re.compile(r'"objURL":"(.*?)"')
def resolveImgUrl(html):
    imgUrls = [decode(x) for x in re_url.findall(html)]
    return imgUrls

def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=1)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":" , imgUrl)
            return False
    except Exception as e:
        print("抛出异常：", imgUrl)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

def app(word):
    #print("欢迎使用百度图片下载脚本！\n目前仅支持单个关键词。")
    #print("下载结果保存在脚本目录下的results文件夹中。")
    print("=" * 50)
    #word = input("请输入你要下载的图片关键词：\n")

    # word = '元青花瓷'

    # dirpath = mkDir("F:/Glasses data/results/")
    # dirpath = mkDir("F:/Glasses data/results/"+word)
    dirpath = 'images'
    
    urls = buildUrls(word)
    index = 0
    for url in urls:
        print("正在请求：", url)
        html = requests.get(url, timeout=10).content.decode('utf-8')
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, name_dict[word.split()[0]] + '_' + str(index) + ".jpg"):
                index += 1
                print("已下载 %s 张" % index)

                if index>=50000:
                    break

        if index>=52:
            break


def is_valid_image(path):
    '''
    检查文件是否损坏
    '''
    try:
        bValid = True
        fileObj = open(path, 'rb') # 以二进制形式打开
        buf = fileObj.read()
        if not buf.startswith(b'\xff\xd8'): # 是否以\xff\xd8开头
            bValid = False
        elif buf[6:10] in (b'JFIF', b'Exif'): # “JFIF”的ASCII码
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'): # 是否以\xff\xd9结尾
                bValid = False
            else:
                try:
                    Image.open(fileObj).verify()
                except Exception as e:
                    bValid = False
                    print(e)
    except Exception as e:
        return False
    return bValid
   
def checkImage():
    img_dir = 'images'
    img_list = os.listdir(img_dir)
    broken_dir = 'broken'
    if not os.path.exists(broken_dir):
        os.makedirs(broken_dir)
    for img_path in img_list:
        img_name = os.path.join(img_dir, img_path)
        if not is_valid_image(img_name):
            print(img_name)
            # os.remove(os.path.join(img_name)
            broken_name = os.path.join(broken_dir, img_path)
            shutil.move(img_name, broken_name)

if __name__ == '__main__':
    for word in word_list: 
        app(word)

    checkImage()