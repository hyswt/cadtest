import pypyodbc
import re
def func(accdb_file,tb_name: str,roller_name:int,index: str, input_num: int) -> dict:
    """
    用于调用access数据库内容；\n
    使用方法
        1.将access文件放入到工作台根目录中；\n
        2.选择要使用的表格；\n
        3.输入数据进行模糊搜索。
    Args:
        accdb_file(str): 选取数据库
        tb_name (str): 所读表格的名字(P0、P2...)
        roller_name(int):轴承系列型号
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
    #NOTE 切片
    roller_name1=str(roller_name)
    roller_name2=roller_name1[-3]

    # 返回P级外圈字典
    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '外圈',index, input_num))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict_ = dict(zip(columns, values))
    list1=['vddp9','vddp01','vddp234','cir7891','cir234']
    regex = r'(?:vddp\d*|cir\d*)(?:%s|\d*$)' % roller_name2
    for num in list1:
        match = re.search(regex, num)
        if match:
            if match.group().startswith('vddp'):
                if roller_name2 in match.group():
                    dict_['vddp']=dict_[match.group()]
            elif match.group().startswith('cir'):
                if roller_name2 in match.group():
                    dict_['cir_dd']=dict_[match.group()]
                
    # 返回P级内圈字典
    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '内圈',index, input_num))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict1_ = dict(zip(columns, values))
    list2=['vdp9','vdp01','vdp234','cir7891','cir234']
    regex1 = r'(?:vdp\d*|cir\d*)(?:%s|\d*$)' % roller_name2
    for num in list2:
        match = re.search(regex1, num)
        if match:
            if match.group().startswith('vdp'):
                if roller_name2 in match.group():
                    dict1_['vdp']=dict1_[match.group()]
            elif match.group().startswith('cir'):
                if roller_name2 in match.group():
                    dict1_['cir_d']=dict1_[match.group()]

    # 返回P级总图内圈字典
    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '总图内圈',index, input_num))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict2_ = dict(zip(columns, values))
    list3=['zvdp89','zvdp01','zvdp234']
    regex2 = r'(?:zvdp\d*)(?:%s|\d*$)' % roller_name2
    for num in list3:
        match = re.search(regex2, num)
        if match:
            if match.group().startswith('zvdp'):
                if roller_name2 in match.group():
                    dict2_['zvdp']=dict2_[match.group()]

    # 返回P级总图外圈
    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '总图外圈',index, input_num))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict3_ = dict(zip(columns, values))
    list4=['zvddp89','zvddp01','zvddp234']
    regex3= r'(?:zvddp\d*)(?:%s|\d*$)' % roller_name2
    for num in list4:
        match = re.search(regex3, num)
        if match:
            if match.group().startswith('zvddp'):
                if roller_name2 in match.group():
                    dict3_['zvddp']=dict3_[match.group()]


    # 返回P级粗糙度字典
    cursor.execute('''SELECT * FROM {}级粗糙度表  WHERE {}>={}'''.format(tb_name,index, input_num))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict4_ = dict(zip(columns, values))
    "rsmin索引"
    '''rsmin=0.6,用dict_6.keys()获取,
       dict_6.valus()
    '''
    cursor.execute('''SELECT * FROM {}  WHERE {}>={}'''.format('非装配倒角尺寸','rsmin', 0.6))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict5_ = dict(zip(columns, values))
    "倒角返回字典"
    

    sql_='''SELECT * FROM 倒角 where rsmin={0} and dd超过<{1} and dd到>{1}'''.format(0.6,input_num)
    cursor.execute(sql_)
    data=cursor.fetchone()
    columns1 = [column[0] for column in cursor.description]
    dict_6 = dict(zip(columns1, data))
    dict_6['rs_a']=dict_6['rsmin']
    dict_6['rs_r']=dict_6['rsmin']
    dict_6['r1s_r']=dict_6['rsmin']
    

    # 合并字典
    def merge_dicts(*dict_args):
        result = {}
        for dictionary in dict_args:
            # TODO 
            result.update(dictionary)
        return result
    dict_7=merge_dicts(dict_,dict1_,dict2_,dict3_,dict4_,dict5_,dict_6)
   
    

    # #关闭游标和链接
    
    cursor.close()
    conn.close()
    return dict_7


if __name__ == "__main__":
    print(func("Data_深沟球","P6",7300, "d", 95))
    pass
