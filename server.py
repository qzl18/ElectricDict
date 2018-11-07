# -*- coding:utf-8 -*-
from socket import *
import os,sys
import struct as st
import time
from pymysql import *
from multiprocessing import Process


HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)



class Mysqlpython():
    def __init__(self,database,
                 host = "localhost",
                 user = "root",
                 password = "123456",
                 port = 3306,
                 charset = "utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.port = port
    #创建数据库连接和游标对象   
    def open(self):
        self.db = connect(database = self.database,
                          host = self.host,
                          user = self.user,
                          password = self.password,
                          port = self.port,
                          charset = self.charset)
        self.cur = self.db.cursor()
    #关闭数据库连接和游标对象
    def close(self):
        self.cur.close()
        self.db.close()
    #执行sql命令
    def zhixing(self,sql,L=None):
        if L== None:
            L = []
        self.open()

        self.cur.execute(sql,L)
        self.db.commit()

        self.close()
    
    def all(self,sql,L = None):
        if L == None:
            L = []
        self.open()
        self.cur.execute(sql,L)
        result = self.cur.fetchall()
        self.close()
        return result


#创建服务器
class Server(object):
    def __init__(self,sockfd,sqlh):
        self.sockfd = sockfd
        self.sqlh = sqlh

    def serve_forever(self):
        while True:
            try:
                connfd,addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit("服务器退出")
            except Exception as e:
                print("Error",e)
                continue
            #创建线程处理客户端请求
            clientProcss = Process(target = self.handle,args = (connfd,))
            clientProcss.setDaemon = True
            clientProcss.start()

    def handle(self,connfd):
        while True:
            type_,msg = self.do_unpack(connfd)
            if type_ == "sign_up":
                connfd.send(b"OK")
                self.sign_up(connfd)
            elif type_ == "sign_in":
                connfd.send(b"OK")
                self.sign_in(connfd)
            ##################继续写要######################## 
             











    def do_unpack(self,connfd):
        #发送格式
        ss = connfd.recv(128) 
        time.sleep(0.1)
        data = connfd.recv(1024)
        #打包 请求类型和 数据
        data = st.unpack(ss,data)
        type_ = data[0].decode()
        msg = data[1].decode()
        return type_,msg
        


    def sign_up(self,connfd):    
        type_,msg = self.do_unpack(connfd)
        if type_ == "sing_up_username":
            sel ="select * from user where username = '%s'" %msg
            r = self.sqlh.all(sel)
            if len(r) == 0:
                connfd.send(b"OK")
                username = msg
                type_,msg = self.do_unpack(connfd)
                if type_ == "sign_up_password":
                    password = msg
                    connfd.send(b"OK") 
                    self.sqlh.zhixing("insert into user (username,password) values ('%s','%s')"%(username,password))
            else:
                connfd.send("用户名重复".encode())
                return
        else:
            connfd.send("error")
            return
            
    def sign_in(self,connfd):
        type_,msg = self.do_unpack(connfd)
        if type_ == "sing_in_username":
            sel ="select * from user where username = '%s'" %msg
            r = self.sqlh.all(sel)
            if len(r) != 1:
                connfd.send("没有这个用户".encode())
            elif len(r) == 1:
                connfd.send(b"OK")
                user = msg
                type_,msg = self.do_unpack(connfd)
                if type_ == "sign_in_password":
                    password = msg
                    #比对用户名密码
                    if r[0][0] == user and r[0][1] == password:
                        connfd.send(b"OK")
                    else:
                        connfd.send("密码错误".encode())


        








def main():
    #创建mysql对象
    sqlh = Mysqlpython("ElectricDict")
    #创建服务器
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    server = Server(sockfd,sqlh)
    
    server.serve_forever()     #启动服务器



if __name__ == "__main__":
    main()