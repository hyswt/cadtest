import pypyodbc
import collections
def func(accdb_file,tb_name:int, index: str, input_num: int) -> dict:
    """
    accdb_file:输入access文件
    tb_name:输入直径系列
    index:检索d还是dd
    input_num:输入d或者Dd
    """
    # file_path是access文件的绝对路径。
    file_path = r"./{}.accdb".format(accdb_file)
    # 链接数据库
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + file_path)
    # 创建游标
    tb_name1=str(tb_name)
    tb_name2=tb_name1[-3]

    cursor = conn.cursor()
    sql1=cursor.execute('''SELECT * FROM 直径系列{}  WHERE {}>={}'''.format(tb_name2,index, input_num))
    # 获取数据库中表的全部数据
    columns = [column[0] for column in sql1.description]
    values = [value for value in sql1.fetchone()]
    # print(values)
    dict_ = dict(zip(columns, values)) 
    ordered_dict = collections.OrderedDict(dict_) 
    last_key, last_value = ordered_dict.popitem() #获取最后一列的键值
    sql_='''SELECT * FROM 倒角 where r1smin={0} and dd超过<{1} and dd到>{1}'''.format(last_value,input_num)
    # print(sql_)
    cursor.execute(sql_)
    data=cursor.fetchone()
    columns1 = [column[0] for column in cursor.description]
    dict_1 = dict(zip(columns1, data))
    # #关闭游标和链接
    cursor.close()
    conn.close()
    return dict_1


if __name__ == "__main__":
    gbt=func("Data_角接触",7300, "d", 90)
    # down=gbt["r1smin"]
    print(gbt)
    pass
