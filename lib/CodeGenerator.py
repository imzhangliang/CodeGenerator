#coding:utf-8

import json
import os
from jinja2 import Template
import fnmatch
import copy

class CodeGenerator(object):
    def __init__(self, configFile, tempFile, outputFile, encoding='utf-8', renderOutFileName = True):
        self.configFile = configFile
        self.tempFile = tempFile
        self.outputFile = outputFile
        self.encoding = encoding
        self.renderOutFileName = renderOutFileName

        self.config = json.load(open(configFile, 'r'))
        self.model = self.configProcessor(self.config)
        
    def configProcessor(self, config):
        '''将配置转化为模型的方法，子类可进行重写'''
        # 将配置拷贝进model中，并删除以下划线开头的属性
        model = copy.deepcopy(config)
        for prop in model.keys():
            if (type(prop) == type('') or type(prop) == type(u'')) and prop.startswith('_'):
                del model[prop]
        print model
        return model


    def _writeFile(self, filePath, unicodeContent):
        '''将unicode内容写入文件filePath中'''
        with open(filePath, 'w') as f:
            f.write(unicodeContent.encode(self.encoding))
    
    def _readFile(self, filePath):
        '''读文件，返回unicode内容'''
        unicodeContent = u''
        with open(filePath, 'r') as f:
            unicodeContent = f.read().decode(self.encoding)
        return unicodeContent

    def renderStr(self, s):
        '''根据model渲染字符串s'''
        if type(s) == type(''):     # 如果不是unicode，先转化成unicode
            s = s.decode(self.encoding)
        
        t = Template(s)
        return t.render(self.model)

    
    def _renderSingleFile(self, srcFile, dstFile):
        '''把单个模版文件srcFile渲染成目标文件dstFile'''
        tempContent = self._readFile(srcFile)
        outContent = self.renderStr(tempContent)
        if self.renderOutFileName:
            outputFile = self.renderStr(dstFile)   # 将输出文件名也渲染了
        else:
            outputFile = self.outputFile

        # 创建不存在的目录
        basename = os.path.split(outputFile)[0]
        if not os.path.exists(basename):
            os.makedirs(basename)

        self._writeFile(outputFile, outContent)
            

    def start(self, fileFilter = '*'):
        '''由模版文件生成代码到目标文件'''
        if os.path.isdir(self.tempFile) and os.path.isdir(self.outputFile):
            for parent, dirnames, filenames in os.walk(self.tempFile):     # 遍历目录下所有文件
                for filename in filenames:
                    if fnmatch.fnmatch(filename, fileFilter):
                        filename = os.path.join(parent, filename)
                        outFilename = filename.replace(self.tempFile, self.outputFile)
                        assert filename != outFilename  # 源目录不能等于目标目录，否则会覆盖
                        print '-'*10, filename, outFilename, '-'*10
                        self._renderSingleFile(filename, outFilename)

        elif os.path.isfile(self.tempFile) and os.path.isfile(self.outputFile):
            self._renderSingleFile(self.tempFile, self.outputFile)
            





if __name__ == '__main__':
    cg = CodeGenerator('config/config.json', '((TableName)).cs', '{{TableName}}.cs')
    cg.start()




