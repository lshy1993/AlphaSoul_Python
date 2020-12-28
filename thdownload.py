import gzip
import os
import re
import requests
import time

# 下载下来的压缩包
ROOT = 'E:/MAJ/tenhou/'
# 解压后文件
UNZIP_PATH = 'E:/MAJ/tenhou/scc/'
# 牌谱存放
OUT_PATH = 'E:/MAJ/tenhou/log/'

RE_PATTERN = r'四鳳.*喰赤－'

def un_gz(file_name):
    # 获取文件的名称，去掉后缀名
    f_name = file_name.replace(".gz", "")
    # 开始解压
    g_file = gzip.GzipFile(ROOT+file_name)
    #读取解压后的文件，并写入去掉后缀名的同名文件（即得到解压后的文件）
    open(UNZIP_PATH + f_name, "wb+").write(g_file.read())
    g_file.close()

def unzipall():
    ''' 解压gz包
    '''
    for file in os.listdir(ROOT):
        fname = os.path.splitext(file)[0]
        extension = os.path.splitext(file)[1]
        if(extension == '.gz'):
            # 只选取天凤桌牌谱
            if file[:3] == 'scc':
                un_gz(file)

def download(id):
    url = 'http://tenhou.net/0/log/?'+id
    download_data = requests.get(url)
    content = download_data.content
    f = open(OUT_PATH + id,"wb+")
    f.write(content)
    f.close()
    
def analyse():
    ''' 读取文件 下载文件上记录的牌谱
    '''
    for file in os.listdir(UNZIP_PATH):
        with open(UNZIP_PATH+file,'r',encoding="UTF8") as f:
            for line in f:
                td = line.split('|')
                # 选取四人桌
                if re.search(RE_PATTERN,td[2]):
                    tt = re.search(r'log=([^">]*)',td[3])
                    id = tt.group(1)
                    download(id)
                    # 下载完成后等待
                    time.sleep(0.5)

def countDaily():
    ''' 统计每日牌谱数目
    '''
    count = 0
    for file in os.listdir(UNZIP_PATH):
        dcount = 0
        with open(UNZIP_PATH+file,'r',encoding="UTF8") as f:
            for line in f:
                td = line.split('|')
                # 选取四人桌
                if re.search(RE_PATTERN,td[2]):
                    dcount += 1
        print( '{}: {}'.format(file[:11], dcount) )
        count += dcount
    print( '合计: {}'.format(count) )


if __name__ == "__main__":
    countDaily()
    # unzipall()
    # analyse()
