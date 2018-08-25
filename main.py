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
    mcg = MyCodeGenerator('config/config.json', 'templates', 'output')
    mcg.start(fileFilter='*.html')