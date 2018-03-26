# -*- coding: cp936 -*-
#��https://papers.nips.cc/��ַ���߳������������Ľű�
import urllib#����ַʹ��
import threading#���߳�ʹ��
import os#������ʱ�ļ�ʹ��

currentnum=0#������ʾ��ǰ�������Ŀ���

def readfile(readfilename):#�ļ�Ԥ����ÿ100����Ŀ����һ��С�ļ�
    try:
        f_read=open(readfilename,'r')
        filenum=0#�ļ�����
        totalnum=0#���������Ŀ����
        itemnum=0#ÿһ���ļ��ڵĵ�ǰ��Ŀ��(0-99)��ÿ���ļ�����100����Ŀ
        for line in f_read:#ֱ��ʹ��readlines���߽����д���ڴ�ʱ���������ݹ��󣬳���ʱ������Ӧ�����Բ��õ���һ��һ�ж�ȡ���ݲ�д���ļ���
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
            f_write.close()#�ر����һ���ļ�
    except KeyboardInterrupt,e:
        f_read.close()
        return filenum,totalnum
    except Exception,e:
        print repr(type(e))+':'+repr(e)
    finally:
        f_read.close()
        return filenum,totalnum

def rules1(line):#��һ����ȡ�ؼ��ֹ���
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

def rules2(line):#�ڶ�����ȡ�ؼ��ֹ���
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

def download(readfilenumber):#���߳����غ���
    try:
        global currentnum#����Ϊȫ�ֱ���
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
                        tempstring=repr(currentnum)+':'+repr(result2)+'\n'#������̹߳����и��ַ�����ʾʱ����
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

__metaclass__=type#ʹ����ʽ��

class MultiThreadDownload(threading.Thread):#���߳���
    def __init__(self,filenumber):
        super(MultiThreadDownload,self).__init__()
        #threading.Thread.__init__(self)
        self.filenumber=filenumber
    def run(self):
        download(self.filenumber)

def downloadBegin(filenum):#ʹ�ö��߳�����
    allthread=[]#���ڴ洢���е��̣߳��Ա��Ժ��ж��Ƿ����е��߳�ȫ������
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
            while(thread.is_alive()==True):pass#�ȴ������߳̽���
    except KeyboardInterrupt,e:
        return False
    except Exception,e:
        print repr(type(e))+':'+repr(e)
        return False
    return True

def combine(filenum):#�����������̲߳�����txt�ļ��ϲ���һ��
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

def cleanup(filenum):#ɾ���������й����в�������ʱ�ļ�
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

def main(readfilename):#������
    try:
        totalnum=0#��ֹreadfileδ����ǰ�˳�ʱ�ñ���û��ֵ��print�����������쳣
        realtotalnum=0#��ֹcombineδ����ǰ�˳�ʱ�ñ���û��ֵ��print�����������쳣
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

    
