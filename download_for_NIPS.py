# -*- coding: cp936 -*-
#从https://papers.nips.cc/网址多线程批量下载论文脚本
import urllib#打开网址使用
import threading#多线程使用
import os#清理临时文件使用

currentnum=0#用于显示当前输出的项目标号

def readfile(readfilename):#文件预处理，每100个项目生成一个小文件
    try:
        f_read=open(readfilename,'r')
        filenum=0#文件总数
        totalnum=0#待处理的项目总数
        itemnum=0#每一个文件内的当前项目数(0-99)，每个文件含有100条项目
        for line in f_read:#直接使用readlines或者将结果写入内存时会由于数据过大，程序长时间无响应。所以采用迭代一行一行读取数据并写入文件中
            line=line.strip()
            if line!='':
                if itemnum==0:
                    filenum+=1
                    f_write=open('in_'+repr(filenum)+'.txt','w')
                f_write.write(line+'\n')
                itemnum+=1
                totalnum+=1
                if itemnum==100:
                    f_write.close()
                    itemnum=0
        if itemnum!=100:
            f_write.close()#关闭最后一个文件
    except KeyboardInterrupt,e:
        f_read.close()
        return filenum,totalnum
    except Exception,e:
        print repr(type(e))+':'+repr(e)
    finally:
        f_read.close()
        return filenum,totalnum

def rules1(line):#第一层提取关键字规则
    try:
        info1='\"'
        info2='\"'
        index1=line.find(info1,0)
        index2=line.find(info2,index1+1)
        if index1==-1 or index2==-1:return None
        return line[index1+1:index2]
    except KeyboardInterrupt,e:
        return None
    except Exception,e:
        print repr(type(e))+':'+repr(e)
        return None

def rules2(line):#第二层提取关键字规则
    try:
        info1='\"'
        info2='\"'
        if 'citation_pdf_url' in line.strip():
            index1=line.find(info1,39)
            index2=line.find(info2,index1+1)
            if index1==-1 or index2==-1:return None
            return line[index1+1:index2]
    except KeyboardInterrupt,e:
        return None
    except Exception,e:
        print repr(type(e))+':'+repr(e)
        return None

def download(readfilenumber):#单线程下载函数
    try:
        global currentnum#声明为全局变量
        f_read=open('in_'+repr(readfilenumber)+'.txt','r')
        f_write=open('out_'+repr(readfilenumber)+'.txt','w')
        for line1 in f_read:
            result1=rules1(line1)
            if result1!=None:
                for line2 in urllib.urlopen(result1):
                    result2=rules2(line2)
                    if result2!=None:
                        f_write.write(result2+'\n')
                        currentnum+=1
                        tempstring=repr(currentnum)+':'+repr(result2)+'\n'#避免多线程过程中该字符串显示时混乱
                        print tempstring
                        break
    except KeyboardInterrupt,e:
        f_read.close()
        f_write.close()
        return
    except Exception,e:
        print repr(type(e))+':'+repr(e)
    finally:
        f_read.close()
        f_write.close()
        return

__metaclass__=type#使用新式类

class MultiThreadDownload(threading.Thread):#多线程类
    def __init__(self,filenumber):
        super(MultiThreadDownload,self).__init__()
        #threading.Thread.__init__(self)
        self.filenumber=filenumber
    def run(self):
        download(self.filenumber)

def downloadBegin(filenum):#使用多线程下载
    allthread=[]#用于存储所有的线程，以便以后判断是否所有的线程全部结束
    for num in range(filenum):
        try:
            tempthread=MultiThreadDownload(num+1)
            allthread.append(tempthread)
            tempthread.start()
        except KeyboardInterrupt,e:
            return False
        except Exception,e:
            print repr(type(e))+':'+repr(e)
    try:
        for thread in allthread:
            while(thread.is_alive()==True):pass#等待所有线程结束
    except KeyboardInterrupt,e:
        return False
    except Exception,e:
        print repr(type(e))+':'+repr(e)
        return False
    return True

def combine(filenum):#将最终所有线程产生的txt文件合并在一起
    try:
        realtotalnum=0
        f_write=open('out.txt','w')
        for num in range(filenum):
            f_read=open('out_'+repr(num+1)+'.txt','r')
            for line in f_read:
                line=line.strip()
                if line!='':
                    f_write.write(line+'\n')
                    realtotalnum+=1
            f_read.close()
    except KeyboardInterrupt,e:
        f_write.close()
        return realtotalnum
    except Exception,e:
        print repr(type(e))+':'+repr(e)
    finally:
        f_write.close()
        return realtotalnum

def cleanup(filenum):#删除程序运行过程中产生的临时文件
    try:
        for num in range(filenum):
            if os.path.exists('in_'+repr(num+1)+'.txt'):
                os.remove('in_'+repr(num+1)+'.txt')
            if os.path.exists('out_'+repr(num+1)+'.txt'):
                os.remove('out_'+repr(num+1)+'.txt')
    except KeyboardInterrupt,e:
        return
    except Exception,e:
        print repr(type(e))+':'+repr(e)
    finally:
        return

def main(readfilename):#主程序
    try:
        totalnum=0#防止readfile未调用前退出时该变量没有值在print过程中引发异常
        realtotalnum=0#防止combine未调用前退出时该变量没有值在print过程中引发异常
        (filenum,totalnum)=readfile(readfilename)
        print 'file num is:'+repr(filenum)
        print 'total num is:'+repr(totalnum)
        downloadBegin(filenum)
        realtotalnum=combine(filenum)
        cleanup(filenum)
    except KeyboardInterrupt,e:
        print 'all is finish:'
        print 'except total num is:'+repr(totalnum)
        print 'real total num is:'+repr(realtotalnum)
        return
    except Exception,e:
        print repr(type(e))+':'+repr(e)
    finally:
        print 'all is finish:'
        print 'except total num is:'+repr(totalnum)
        print 'real total num is:'+repr(realtotalnum)
        return

if __name__=='__main__':
    main('in.txt')

    
