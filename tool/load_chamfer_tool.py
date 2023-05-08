import pypyodbc
# file_path是access文件的绝对路径。
def functool(accdb_file,num:int,num1: int) -> dict:
    file_path = r"./{}.accdb".format(accdb_file)
    # 链接数据库
    conn = pypyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+ file_path)
    # 创建游标
    cursor = conn.cursor()
    sql_='''SELECT * FROM 角接触球轴承 where r1smin={0} and dd超过<{1} and dd到>{1}'''.format(num,num1)
    # print(sql_)
    cursor.execute(sql_)
    # 获取数据库中表的全部数据
    data=cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    dict_ = dict(zip(columns, data))
    cursor.close()
    conn.close()
    return dict_
if __name__ == "__main__":
    gbt=functool("Data_角接触",0.6,35 )
    print(gbt)
    pass


