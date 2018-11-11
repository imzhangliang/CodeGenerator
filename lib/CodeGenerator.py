#coding:utf-8

import json
import re
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
        self.configs = []   # 配置文件集合，支持批处理
        self.config = {}    # 配置文件。如果有多个配置文件，此为第一个配置文件
        self.models = []    # 数据模型集合，支持批处理
        self.model = {}     # 数据模型。如果有多个数据模型，此为第一个数据模型

        self.config = self.parseJsonFile(configFile)
        if type(self.config) == type([]):   # 配置json为列表
            self.configs = self.config
            self.config = self.configs[0]
        else:
            self.configs = [self.config]
        
        self.models = []
        for config in self.configs:
            self.models.append(self.configProcessor(config))

        self.model = self.models[0]

        
    def configProcessor(self, config):
        '''将配置转化为模型的方法，子类可进行重写'''
        # 将配置拷贝进model中，并删除以下划线开头的属性
        model = copy.deepcopy(config)
        for prop in model.keys():
            if (type(prop) == type('') or type(prop) == type(u'')) and prop.startswith('_'):
                del model[prop]
        return model

    def parseJsonFile(self, configFile):
        content = self._readFile(configFile)

        content = re.sub('"""((.|\n)*?)"""', lambda m: json.dumps(m.group(1)), content)   # 将"""包含的多行字符串转化为标准的json字符串

        return json.loads(content)

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
        '''由模版文件生成代码到目标文件。如果配置有多个（配置为列表），仅按第一个配置生成代码'''
        if os.path.isdir(self.tempFile) and os.path.isdir(self.outputFile):     # 模版和目标都为目录
            for parent, dirnames, filenames in os.walk(self.tempFile):     # 遍历目录下所有文件
                for filename in filenames:
                    if fnmatch.fnmatch(filename, fileFilter):
                        filename = os.path.join(parent, filename)
                        outFilename = filename.replace(self.tempFile, self.outputFile)
                        assert filename != outFilename  # 源目录不能等于目标目录，否则模板会被覆盖
                        print '-'*10, filename, outFilename, '-'*10
                        self._renderSingleFile(filename, outFilename)

        elif os.path.isfile(self.tempFile):   # 模板和目标都为文件
            assert self.tempFile != self.outputFile  # 源文件不能等于目标文件，否则模板会被覆盖
            if fnmatch.fnmatch(self.tempFile, fileFilter):
                self._renderSingleFile(self.tempFile, self.outputFile)
            else:
                print u'%s 文件不符合规则 %s' % (self.tempFile, fileFilter)

        else:
            if not os.path.exists(self.tempFile):
                print u'%s 不存在' % self.tempFile
            elif os.path.isdir(self.tempFile) and not os.path.isdir(self.outputFile):
                print u'%s是目录， 但 %s 不存在或不是目录' % (self.tempFile, self.outputFile)

            

            raise Exception('模版和目标必须都为目录或文件，且都存在')

    def startBatch(self, fileFilter = '*'):
        '''由模版文件生成代码到目标文件，批处理版本'''
        for model in self.models:
            self.model = model
            self.start(fileFilter=fileFilter)
        
        self.model = self.models[0] # 将self.model还原成第一个模型
            





if __name__ == '__main__':
    cg = CodeGenerator('config/config.json', '((TableName)).cs', '{{TableName}}.cs')
    cg.start()




