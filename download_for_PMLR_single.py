# -*- coding: cp936 -*-
#从http://proceedings.mlr.press/index.html网址批量下论文脚本
info1='[<a href="http://'
info2='">'
try:
    f_read=open('in.txt','r')
    f_write=open('out.txt','w')
    for line in f_read:
        index1=line.find(info1,0)
        index2=line.find(info2,index1+1)
        if index1!=-1 and index2!=-1:
            tempstring=line[index1+10:index2]
            if tempstring[-1]=='f':
                print tempstring
                f_write.write(tempstring+'\n')
except Exception,e:
    print type(e),':',e
finally:
    f_read.close()
    f_write.close()
