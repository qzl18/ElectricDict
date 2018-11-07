# -*- coding:utf-8 -*-
from socket import *
import os
import struct as st
import time
HOST = '127.0.0.1'
PORT = 8888
ADDR = (HOST,PORT)

class Client():
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def menu1(self):
        print(
            '''
            ****************************************
            ******          1.注册               ****
            ******          2.登录               ****
            ******          3.退出               ****
            ****************************************
            '''
        )
    def menu2(self):
        print(
            '''
            ****************************************
            ******          1.查看单词           ****
            ******          2.查看历史记录        ****
            ******          3.注销               ****
            ****************************************
            '''
        )
    def do_pack(self,type_,data):
        ss = str(len(type_.encode()))+'s'+str(len(data.encode()))+'s'
        #发送格式
        self.sockfd.send(ss.encode())
        time.sleep(0.1)
        #打包 请求类型和 数据
        data1 = st.pack(ss,type_.encode(),data.encode())
        #发送打包的数据
        self.sockfd.send(data1)
        #接收返回信息
        msg = self.sockfd.recv(1024).decode()
        return msg

    def sign_up(self):
        while True: 
            username = input("请输入要注册的用户名:")
            if not username:
                print("用户名输入有误!")
                break
            msg = self.do_pack('sign_up_username',username)
            if msg == 'OK':
                while True:
                    password1 = input("请输入密码:")
                    password2 = input('请再次输入密码:')
                    if password1 ==password2:
                        msg = self.do_pack("sign_up_password",password1)
                        if msg == 'OK':
                            print("注册成功!!")
                            print("记住您的用户名和密码并重新登录")
                            return
                        else:
                            print(msg)
                            break
                    else:
                        print('输入有误,请重新输入:')
                        continue
                
            else:
                print(msg)
                print("请重新输入用户名:")
                continue

    def sign_in(self):
        while True:
            username = input("请输入用户名:")
            msg = self.do_pack('sign_in_username',username)
            if msg =="OK":
                password = input("请输入密码:")
                msg = self.do_pack('sign_in_password',password)
                if msg =='OK':
                    print("登录成功")
                    #进入二级界面操作
                    self.denglu()
                    return 
                else:
                    print(msg)
                    continue
            else:
                print(msg)
                continue

    def denglu(self):    
        self.menu2()
##############################################################################



def main():
    #创建套接字
    sockfd = socket()
    sockfd.connect(ADDR)
    cl = Client(sockfd)
    # pid = os.fork()

    # if pid <0:
    #     pass
    # elif pid == 0:

    while True:
        cl.menu1()
        cmd = input('请输入指令:')
        if cmd == '1':
            msg = cl.do_pack('sign_up',"##")
            if msg =="OK":
                cl.sign_up()
        if cmd == '2':
            msg = cl.do_pack('sign_in',"##")
            if msg =="OK":
                cl.sign_in()






if __name__ == "__main__":
   main()