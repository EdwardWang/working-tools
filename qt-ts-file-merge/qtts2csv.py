# _*_ encoding:utf-8 _*_

import codecs
import copy
from xml.parsers.expat import ParserCreate

class TsHandler(object):
    def __init__(self):
        super(TsHandler,self).__init__()
        self.alldict = {}
        self.pagedict = {}
        self.pageflag = 0
        self.pagename = None
        self.srcflag = 0
        self.srcname = None
        self.tsflag = 0
    
    def start_element(self,name,attrs):
        if name == 'name':
            self.pageflag = 1
        elif name == 'source':
            self.srcflag = 1
        elif name == 'translation':
            self.tsflag = 1

    def end_element(self,name):
        if name == 'context':
            self.alldict[self.pagename] = copy.deepcopy(self.pagedict)
            self.pagename = None
            self.pagedict.clear()
        elif name == 'name':
            self.pageflag = 0
        elif name == 'source':
            self.srcflag = 0
        elif name == 'translation':
            self.tsflag = 0

    def char_data(self,text):
        if self.pageflag == 1:
            self.pagename = text
        elif self.srcflag == 1:
            self.srcname = text
        elif self.tsflag == 1:    
            self.pagedict[self.srcname] = text
            self.srcname = None
            
    def result_dict(self):
        return self.alldict
            
def ts2xls(filename,fmt):
    handler = TsHandler()
    parser = ParserCreate()
    parser.returns_unicode = True
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    
    with codecs.open(filename, encoding=fmt) as f:
        for line in f.readlines():
            line = line.encode(fmt)
            parser.Parse(line)
            
    return handler.result_dict()


if __name__ == '__main__':

    args_zh = {'filename':'cn.ts',
               'fmt':'utf-8'
               }

    args_tw = {'filename':'cn_fanti.ts',
               'fmt':'utf-8'
               }
    
    zh = ts2xls(**args_zh)
    tw = ts2xls(**args_tw)

    with codecs.open('1.csv',mode='w',encoding='gbk') as f:
        for key in zh.iterkeys():
            if key:
                f.write(key)
            f.write(u'\n'.encode('gbk'))
            for subkey in zh[key].iterkeys():
                sstr = subkey
                if sstr:
                    if ',' in sstr:
                        sstr = sstr.replace(',',' ')
                    f.write(sstr)
                else:
                    continue
                f.write(u','.encode('gbk'))
                if zh[key].has_key(subkey):
                    zstr = zh[key][subkey]
                    if ','.encode('utf-8') in zstr:
                        zstr = zstr.replace(',',' ')
                    f.write(zstr)
                f.write(u','.encode('gbk'))
                if tw[key].has_key(subkey):
                    tstr = tw[key][subkey]
                    if ','.encode('utf-8') in tstr:
                        tstr = tstr.replace(',',' ')
                    f.write(tstr)
                f.write(u'\n'.encode('gbk'))
