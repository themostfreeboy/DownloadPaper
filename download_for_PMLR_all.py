# -*- coding: cp936 -*-
#从http://proceedings.mlr.press/index.html网址批量下论文脚本(全部版)
import urllib
info1='[<a href="http://'
info2='">'
try:
    webpage1=urllib.urlopen('http://proceedings.mlr.press/index.html')
    for line1 in webpage1:
        index1=line1.find('<a href="/',0)
        index2=line1.find('</b></a>',index1+1)
        if index1!=-1 and index2!=-1:
            index3=line1.find('">',index1+1)
            nexturl='http://proceedings.mlr.press'+line1[index1+9:index3]
            print 'url is:',nexturl
            filename=line1[index3+5:index2]
            f_write=open(filename+'.txt','w')
            webpage2=urllib.urlopen(nexturl)
            for line2 in webpage2:
                index4=line2.find('[<a href="http://',0)
                index5=line2.find('">',index4+1)
                if index4!=-1 and index5!=-1:
                    tempstring=line2[index4+10:index5]
                    if tempstring[-1]=='f':
                        print tempstring
                        f_write.write(tempstring+'\n')
            f_write.close()
except Exception,e:
    print type(e),':',e
finally:
    pass
