import pypyodbc

dict_1={'a':1,'b':2,'c':3}
dict_2={'a':4,'e':5,'g':6}
dict_3={'u':7,'l':0,'p':8}
common_keys = set(dict_1.keys()) & set(dict_2.keys())
for key in common_keys:
    print("相同的键：", key)
# def Merge(dict1, dict2): 
#     res = {**dict1, **dict2} 
#     return res 
# dict3=Merge(dict_1, dict_2)
# print(dict3)
# dict3=dict_1|dict_2|dict_3
# print(dict3)

import pypyodbc


def func(accdb_file,tb_name: str, index: str, input_num: int) -> dict:
    """
    用于调用access数据库内容；\n
    使用方法
        1.将access文件放入到工作台根目录中；\n
        2.选择要使用的表格；\n
        3.输入数据进行模糊搜索。

    Args:
        accdb_file(str): 选取数据库
        tb_name (str): 所读表格的名字(P0、P2...)
        out_in(str): 内圈、外圈
        index(str): 索引标题
        input_num (int): 输入参数
        

    Returns:
        dict: 返回列名为key，所选行内容为value的字典
    """
    # file_path是access文件的绝对路径。
    file_path = r"./{}.accdb".format(accdb_file)
    # 链接数据库
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + file_path)
    # 创建游标
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '外圈',index, input_num))
    # 获取数据库中表的全部数据
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict_ = dict(zip(columns, values))
    
     
    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '内圈',index, input_num))
    # 获取数据库中表的全部数据
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict1_ = dict(zip(columns, values))

    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '总图内圈',index, input_num))
    # 获取数据库中表的全部数据
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict2_ = dict(zip(columns, values))

    cursor.execute('''SELECT * FROM {}级粗糙度表  WHERE {}>={}'''.format(tb_name,index, input_num))
    # 获取数据库中表的全部数据
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict3_ = dict(zip(columns, values))

    
    def merge_dicts(*dict_args):
        result = {}
        for dictionary in dict_args:
            # TODO 
            result.update(dictionary)
        return result
    dict_4=merge_dicts(dict_,dict1_,dict2_,dict3_)

    # #关闭游标和链接
    
    cursor.close()
    conn.close()
    return dict_4


if __name__ == "__main__":
    print(func("Data_轻系列","P6", "d", 95))
    pass

