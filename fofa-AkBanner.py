# -*- coding: utf-8 -*-
import requests
import argparse
import base64
import sys
import json
import os
import threading
from threading import Thread

def banner():
    print('''
 ______ ____  ______                 _    ____                              
|  ____/ __ \|  ____/\         /\   | |  |  _ \                             
| |__ | |  | | |__ /  \       /  \  | | _| |_) | __ _ _ __  _ __   ___ _ __ 
|  __|| |  | |  __/ /\ \     / /\ \ | |/ /  _ < / _` | '_ \| '_ \ / _ \ '__|
| |   | |__| | | / ____ \   / ____ \|   <| |_) | (_| | | | | | | |  __/ |   
|_|    \____/|_|/_/    \_\ /_/    \_\_|\_\____/ \__,_|_| |_|_| |_|\___|_|   
                                                                                                                 
        ''')

def fofa():
    # fofa email
    email = ""
    # fofa key
    key = ""
    url = "https://fofa.so/api/v1/info/my?email=" + email + "&key=" + key
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url, headers=header)
    if "errmsg" not in response.text:
        print("\033[1;32memail和key均正确\033[0m")
        while 1:
            sentence = input("\033[1;36mfofa语句 >>>\033[0m")
            print("最多查询条数为10000")
            size = input("\033[1;36m查询条数 >>>\033[0m")
            sentence = base64.b64encode(sentence.encode('utf-8')).decode("utf-8")
            # 查询语句
            # https://fofa.so/api/v1/search/all?email=zhangweifeng@secpt.com.cn&key=6d246c166f2ce3c7bce66cc52e4f3572&size=1000&qbase64=dGl0bGU9IuWlpee+juWumiI=
            url = "https://fofa.so/api/v1/search/all?email=" + email + "&key=" + key + "&size=" + size + "&qbase64=" + sentence
            response = requests.get(url, headers=header)
            file_name = "result.txt"
            file = os.path.isfile(file_name)
            if file == "True":
                os.remove("result.txt")
                if 'errmsg' not in response.text:
                    print("保存文件到result.txt")
                    r1 = json.loads(response.text)
                    for i in r1['results']:
                        s = i[0]
                        print(s)
                        mu = threading.Lock()
                        if mu.acquire(True):
                            f = open('result.txt', 'a')
                            f.write(s + "\n")
                            mu.release()
                else:
                    print("fofa语句错误！")

            else:
                print("result.txt文件不存在！")
                print("正在创建result.txt")
                if 'errmsg' not in response.text:
                    print("保存文件到result.txt")
                    r1 = json.loads(response.text)
                    for i in r1['results']:
                        s = i[0]
                        print(s)
                        f = open('result.txt', 'a')
                        f.write(s + "\n")
                else:
                    print("fofa语句错误！")

        else:
            print("api或者email错误！")

def main():
    banner()
    Thread(target = fofa(),args=()).start()


if __name__ == '__main__':
    main()