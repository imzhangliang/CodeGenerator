#coding:utf-8

import sys
sys.path.append('../..')

from lib.CodeGenerator import CodeGenerator



if __name__ == '__main__':
    # 通过多个配置文件审查代码
    # 'config/configBatch.json'为配置文件（其中是列表形式的）
    # 'templates'为模版存放目录
    # 'output'为代码输出目录
    mcgBatch = CodeGenerator('config/configBatch.json', 'templates', 'output')
    mcgBatch.startBatch(fileFilter='*.html')