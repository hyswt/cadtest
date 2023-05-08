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
        index(str): 索引标题,套圈直径
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
    cursor.execute('''SELECT * FROM {}级粗糙度表  WHERE {}>={}'''.format(tb_name,index, input_num))
    # 获取数据库中表的全部数据
    columns = [column[0] for column in cursor.description]
    values = [value for value in cursor.fetchone()]
    dict_ = dict(zip(columns, values))
    # #关闭游标和链接
    cursor.close()
    conn.close()
    return dict_


if __name__ == "__main__":
    gbt=func("Data_轻系列","P6", "d", 95)
    # down=gbt["@dds"]
    print(gbt)
    pass
