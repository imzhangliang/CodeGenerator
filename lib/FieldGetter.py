#coding:utf-8

import pymssql
from pprint import pprint


#import uuid

class DBConfig:
    '''
    数据库配置类
    '''
    def __init__(self, host, username, password, dbname):
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname


class FieldGetter:
    '''
    从sql语句中获得每个字段的名称和类型
    '''
    def __init__(self, dbconfig, dbType):
        self.dbType = dbType.lower()    #  数据库类型

        if self.dbType == 'mssql':       # SQL server 数据库
            self.conn = pymssql.connect(
                dbconfig.host, 
                dbconfig.username,
                dbconfig.password,
                dbconfig.dbname
            )
            self.cur = self.conn.cursor()
            self.typeConvertTable = {}  # 转换表映射
            self._initTypeConvertTable()    # 初始化类型转换表

    def _initTypeConvertTable(self):
        '''
        初始化类型转换表
        '''
        self.typeConvertTable = {
            'python': {     # 因为基础类型就是python的类型，所以key和value一样
                'int': 'int',
                'decimal': 'decimal',
                'float': 'float',
                'unicode': 'unicode',
                'str': 'str',
                'bool': 'bool',
                'datetime': 'datetime',
                'uuid': 'uuid',
            },
            'c#': {
                'int': 'int',
                'decimal': 'decimal',
                'float': 'double',
                'unicode': 'string',
                'str': 'byte[]',
                'bool': 'bool',
                'datetime': 'DateTime',
                'uuid': 'Guid',
            },
        }

    def getFieldsFromSql(self, sql, language = 'python'):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        fieldDesc = self.cur.description

        fieldNames = [ item[0] for item in fieldDesc ]  # 获得所有列名

        # 获得所有列类型的代码 （这个代码是基本的代码，光靠这个还不知道实际类型）
        # 见：https://stackoverflow.com/questions/33335489/how-to-get-column-data-types-from-pymssql
        fieldTypeCodes = [ item[1] for item in fieldDesc]

        rowList = list(result[0])     # 用一行数据的数据类型进行解析类型

        for j in range(len(rowList)):
            if rowList[j] == None:      # 如果改列为None，则在下面的行中找到不为None的替换
                for i in range(1, len(result)):
                    if result[i][j] != None:
                        rowList[j] = result[i][j]

        
        fieldTypes = []
        for i in range(len(rowList)):
            item = rowList[i]
            code = fieldTypeCodes[i]

            # 先从列数据中推测类型，实在查不出，就按照typecode推测
            fieldType = type(item).__name__.lower()    # 类型一致用小些字母
            if fieldType == 'nonetype':
                fieldType = {
                    1: 'unicode',   # STRING
                    2: 'str',       # BINARY
                    3: 'float',     # NUMBER
                    4: 'datetime',  # DATETIME
                    5: 'str'        # ROWID
                }[code]

            fieldTypes.append(fieldType)

        language = language.lower()
        fieldTypes = [ self.typeConvertTable[language][t] for t in fieldTypes ] # 将基础类型转化为对应编程语言的类型
        

        result = [ (fieldNames[i], fieldTypes[i]) for i in range(len(fieldNames))]

        return result
    


if __name__ == "__main__":
    sql = '''
    --select 'zhang' name, 11 age, 'male' gender;
    select *, '123' [11你好] from [user]
    '''
    
    f = FieldGetter(DBConfig(
        '192.168.43.142',
        'sa',
        '123456',
        "testDB"
    ), 'mssql')
    fields = f.getFieldsFromSql(sql, 'c#')

    pprint(fields)

