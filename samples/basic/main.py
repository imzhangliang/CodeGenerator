#coding:utf-8
# 单个配置文件的测试： 一个模版文件只能生成一个目标文件

import sys
import os
sys.path.append('../..')

from lib.CodeGenerator import CodeGenerator


if __name__ == '__main__':
    # 通过单个配置文件生成代码
    # 'config/config.json'为配置文件
    # 'templates'为模版存放目录
    # 'output'为代码输出目录
    mcg = CodeGenerator('config/config.json', 'templates', 'output')
    mcg.start(fileFilter='*.html')
