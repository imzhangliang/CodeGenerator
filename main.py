#coding:utf-8

from lib.CodeGenerator import CodeGenerator

class MyCodeGenerator(CodeGenerator):
    def configProcessor(self, config):
        '''重写配置处理器'''
        model = super(MyCodeGenerator, self).configProcessor(config)

        ## 自定义更新model的代码
        ## ....
        ## ....

        return model

if __name__ == '__main__':
    # 通过单个配置文件生成代码
    # 'config/config.json'为配置文件
    # 'templates'为模版存放目录
    # 'output'为代码输出目录
    mcg = MyCodeGenerator('config/config.json', 'templates', 'output')
    mcg.start(fileFilter='*.html')

    # 通过多个配置文件审查代码
    # 'config/configBatch.json'为配置文件（其中是列表形式的）
    # 'templates'为模版存放目录
    # 'output'为代码输出目录
    mcgBatch = MyCodeGenerator('config/configBatch.json', 'templates', 'output')
    mcgBatch.startBatch(fileFilter='*.html')