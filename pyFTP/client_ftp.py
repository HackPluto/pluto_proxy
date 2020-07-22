# coding:utf-8
from ctypes import *
import os
import sys
import ftplib


class myFtp:
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""

    def __init__(self, host, port=21):
        #self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)


    def UpLoadFile(self, LocalFile, RemoteFile):
        if os.path.isfile(LocalFile) == False:
            return False
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, 4096)
        file_handler.close()
        return True

    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            return False
        print("LocalDir:", LocalDir)
        LocalNames = os.listdir(LocalDir)
        print("list:", LocalNames)
        print(RemoteDir)
        self.ftp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                self.UpLoadFile(src, Local)

        self.ftp.cwd("..")
        return

    def DownLoadFile(self, LocalFile, RemoteFile):
        file_handler = open(LocalFile, 'wb')
        self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)
        file_handler.close()
        return True

    def DownLoadFileTree(self, LocalDir, RemoteDir):
        print("remoteDir:", RemoteDir)
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        print(self.ftp.nlst("/del1"))
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            if self.isDir(file):
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")
        if self.path in result and "<dir>" in result:
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()

def menu():
    a = '''
Pluto    Proxy     System
    [1] upload file
    [2] upload filetree
    [3] download file
    [4] download filetree
    [5] quit
    
[*]input index:
    '''
    print(a)
    index = input().strip()
    return  index

if __name__ == "__main__":
    ftp = myFtp('192.168.59.143')
    ftp.Login('lhh', 'liuhui1999')
    while True:
        key = menu()
        if '1' in key:
            local_file = input("[*]Input local file name ---->").strip()
            remote_file = input("[*]Input remote file name ---->").strip()
            ftp.UpLoadFile(local_file,remote_file)
            print("[*]Success!")

        elif '2' in key:
            local_file = input("[*]Input local filetree name ---->").strip()
            remote_file = input("[*]Input remote filetree name ---->").strip()
            ftp.UpLoadFileTree(local_file,remote_file)
            print("[*]Success!")

        elif '3' in key:
            local_file = input("[*]Input local file name ---->").strip()
            remote_file = input("[*]Input remote file name ---->").strip()
            ftp.DownLoadFile(local_file,remote_file)
            print("[*]Success!")

        elif '4' in key:
            local_file = input("[*]Input local filetree name ---->").strip()
            remote_file = input("[*]Input remote filetree name ---->").strip()
            ftp.DownLoadFileTree(local_file,remote_file)
            print("[*]Success!")

        elif '5' in key:
            print("Bye~")
            ftp.close()

        else:
            print("[*]Please input right index!")