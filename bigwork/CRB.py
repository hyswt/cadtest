import pypyodbc
import re
def CRB(accdb_file,tb_name: str,roller_name:int,index: str, input_num: int,rsmin:float,r1smin:float) -> dict:
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
    list1=['vddp9','vddp01','vddp234']
    regex = r'(?:vddp\d*|cir\d*)(?:%s|\d*$)' % roller_name2
    for num in list1:
        match = re.search(regex, num)
        if match:
            if match.group().startswith('vddp'):
                if roller_name2 in match.group():
                    dict_['vddp']=dict_[match.group()]
            
                
    # 返回P级内圈字典
    cursor.execute('''SELECT * FROM {}级{}技术条件  WHERE {}>={}'''.format(tb_name, '内圈',index, input_num))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict1_ = dict(zip(columns, values))
    list2=['vdp9','vdp01','vdp234']
    regex1 = r'(?:vdp\d*|cir\d*)(?:%s|\d*$)' % roller_name2
    for num in list2:
        match = re.search(regex1, num)
        if match:
            if match.group().startswith('vdp'):
                if roller_name2 in match.group():
                    dict1_['vdp']=dict1_[match.group()]
            

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
    cursor.execute('''SELECT * FROM {}  WHERE {}>={}'''.format('非装配倒角尺寸',"rsmin", rsmin))
    columns = [column[0] for column in cursor.description]
    values = [str(value) for value in cursor.fetchone()]
    dict5_ = dict(zip(columns, values))

    
    "倒角返回字典"
    sql_ = '''SELECT * FROM 倒角 where rsmin={0} and dd超过<{1} and dd到>{1}'''.format(rsmin,input_num)
    cursor.execute(sql_)
    data=cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    dict_6 = dict(zip(columns, data))
    dict_6['rs_a']=dict_6['rsmin']
    dict_6['rs_r']=dict_6['rsmin']
    

    "窄端面"  
    sql_ = '''SELECT * FROM 窄端面 where r1smin={0} and dd超过<{1} and dd到>{1}'''.format(r1smin,input_num)
    cursor.execute(sql_)
    data=cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    dict_6_1 = dict(zip(columns, data))
    dict_6_1['r1s_r']=dict_6_1['r1smin']
    dict_6_1['r1s_a']=dict_6_1['r1smin']


    

    # 合并字典
    def merge_dicts(*dict_args):
        result = {}
        for dictionary in dict_args:
            # TODO 
            result.update(dictionary)
        return result
    dict_9={'De': 23.380612286851935, 'B': 8, 'Re': 2.61, 'ae': 4.006488008791477, 'di': 13.348756934444397, 'Ri': 2.56, 'ai': 3.985357095704442, 'd2': 13.348756934444397, 'Dc1': 15.968756934444396, 'Dcp': 18.36, 'Bc': 7.1, 'deltaC': 5.14, 'D2': 23.380612286851935, 'dc': 17.235361900044015, 'hc2': 0.9119755654502972, 'Dc2': 16.259999999999998, 'Dc': 4.860214132850264, 'hc': 3.424, 'Bc1': 6.765246750563737, 'Rc': 12.909807175081053, 'Dwc': 4.633448684632123, 'dca': 5.2, 'S': 0.7, 'S1': 0.27999999999999997, 'CK': 3.8549999999999995, 'C1': 7.026067818223048, 'J': 5.089235495832161, 'Dck': 19.880612286851935, 't': 0.03,'pdmin':7,'pdmax':6,'CrD':8,'CorD':9,'D':5,'ai':3.14,'B':3.14,'ae':3,'L1': 3.886452541223238, 'S': 0.6, 'Rc': 3.08, 'rc': -0.8073235064096858, 'K': 3.04, 'Dcw': 25.64, 'Dc': 25.54, 'Dcp': 22.66, 'Dc1': 19.78, 'C': 9.831805528403867, 'C1': 5.042324363450084, 'DF2': 32.6, 'DF3': 29.0, 'BF1': 1.8000000000000003, 'DF1': 32.199999999999996, 'DF': 35.8, 'dF': 19.7, 'BF2': 1.4000000000000001, 'SF': 0.4, 'RF': 0.4999999999999999, 'alfaF': 51.21463691560988, 'RF1': 0.8, 'BF': 2.76, 'Dm1': 37.059999999999995, 'Dm2': 35.5, 'Dm3': 32.2, 'Dm4': 30.200000000000003, 'Bm4': 0.2, 'dm1': 19.7, 'dm2': 20.078911580341916, 'dm3': 20.778911580341916, 'Bm5': 0.5683673705128764, 'Bm6': 0.18945579017095882, 'Bm1': 2.2, 'Bm2': 1.2, 'Bm3': 0.6, 'Rm1': 0.35, 'Rm2': 0.02, 'DH': 32.2, 'dH': 22.578911580341916, 'SH': 0.8, 'dma': 2.5, 'Bc': 2.88, 'L': 6.7, 'H': 2.0, 'De': 34.684, 'di': 16.66, 'rmax': 0.2, 'Dm': 4.0, 'dm': 2.5, 'D2': 33, 'd2': 19, 'Ri': 3.08, 'Re': 3.14, 'e': 3.0, 'd1': 2.37}
    dict_7=merge_dicts(dict_,dict1_,dict2_,dict3_,dict4_,dict5_,dict_6,dict_6_1,dict_9)
    

    

    # #关闭游标和链接
    
    cursor.close()
    conn.close()
    return dict_7


if __name__ == "__main__":
    print(CRB("Data_圆柱滚子","P6",7300, "d", 95,0.3,1))
    pass
