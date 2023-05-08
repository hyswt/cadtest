from typing import Union
import pandas as pd
import pythoncom
import win32com.client
import math


def behavioral_Tolerance(P: str, num: Union[int, float], name: str) -> dict:
    """
    用于查找上下行为公差

    Parameters
    ----------
    P : str
        `P0、P2...`公差等级
    num : int | float
        用于传入的数字，宽度or长度
    name : str
        轴承名，例如`'6206'...`


    Returns
    -------
    dict
        返回装有数值的字典
    """

    dict_data_all = {}
    for bearing in ('外圈', '内圈'):
        dict_data = {}
        sheet = bearing+P
        data = pd.read_excel('处理好的数据.xlsx', sheet_name=sheet, header=[0, 1], index_col=0)

        dsp = data['V_dsp'].columns

        for i in dsp:
            if name[-3] not in str(i):
                data = data.drop(labels=[('V_dsp', i)], axis=1, inplace=False)

        df_ref1 = data[(data.loc[:, ('d', '>')] < num) &
                       (data.loc[:, ('d', '<=')] >= num)]
        header1 = data.columns[2:]
        for j, k in header1:
            data3 = df_ref1.loc[:, (j, k)].values
            dict_data[j] = int(data3)/1000
        dict_data_all[bearing] = dict_data
    return dict_data_all


def cad_modu(scale_factor: Union[float, int], str1: str, str2: str, str3: str):
    """_summary_

    Parameters
    ----------
    scale_factor : Union[float, int]
        _description_
    str1 : str
        _description_
    """

    def vtpnt(x, y, z=0):
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))

    wincad = win32com.client.Dispatch("AutoCAD.Application")
    doc = wincad.ActiveDocument
    doc.Utility.Prompt("Hello! Autocad from pywin32com.\n")
    msp = doc.ModelSpace

    '''设置画线属性'''
    doc.preferences.LineweightDisplay = 1  # 显示线宽
# ........................
# 大外框
    p1 = vtpnt(-43.896, 114.7889)
    p2 = vtpnt(166.104, 114.7889)
    p3 = vtpnt(-43.896, -185.2111)
    p4 = vtpnt(166.104, -185.2111)
    line1 = msp.AddLine(p1, p2)
    line2 = msp.AddLine(p1, p3)
    line3 = msp.AddLine(p2, p4)
    line4 = msp.AddLine(p3, p4)
    line1.Lineweight = 0.0
    line2.Lineweight = 0.0
    line3.Lineweight = 0.0
    line4.Lineweight = 0.0
    # ......................
# 内框
    p5 = vtpnt(-18.896, 109.7889)
    p6 = vtpnt(161.104, 109.7889)
    p7 = vtpnt(-18.896, -180.2111)
    p8 = vtpnt(161.104, -180.2111)
    line5 = msp.AddLine(p5, p6)
    line6 = msp.AddLine(p5, p7)
    line7 = msp.AddLine(p6, p8)
    line8 = msp.AddLine(p7, p8)
    line5.Lineweight = 50
    line6.Lineweight = 50
    line7.Lineweight = 50
    line8.Lineweight = 50

    # 左上小内框
    p9 = vtpnt(41.104, 109.7889)
    p10 = vtpnt(-18.896, 97.7889)
    p11 = vtpnt(41.104, 97.7889)
    line9 = msp.AddLine(p9, p11)
    line10 = msp.AddLine(p10, p11)
    line9.Lineweight = 50
    line10.Lineweight = 50

    # 下方大框
    p12 = vtpnt(-18.896, -130.2111)
    p13 = vtpnt(161.104, -130.2111)
    p14 = vtpnt(-18.896, -180.2111)
    p15 = vtpnt(161.104, -180.2111)
    p16 = vtpnt(-43.896, -180.2111)
    p17 = vtpnt(-18.896, -130.2111)

    line11 = msp.AddLine(p12, p13)
    line12 = msp.AddLine(p12, p14)
    line13 = msp.AddLine(p13, p15)
    line14 = msp.AddLine(p15, p16)
    line15 = msp.AddLine(p13, p17)

    line11.Lineweight = 50
    line12.Lineweight = 50
    line13.Lineweight = 50
    line14.Lineweight = 50
    line15.Lineweight = 50
    # 小框
    p18 = vtpnt(-43.896, -145.2111)
    p19 = vtpnt(-18.896, -145.2111)
    p20 = vtpnt(-43.896, -160.2111)
    p21 = vtpnt(-18.896, -160.2111)
    p22 = vtpnt(-43.896, -175.2111)
    p23 = vtpnt(-18.896, -175.2111)

    line16 = msp.AddLine(p18, p19)
    line17 = msp.AddLine(p20, p21)
    line18 = msp.AddLine(p22, p23)
    line16.Lineweight = 50
    line17.Lineweight = 50
    line18.Lineweight = 50
    #
#p24 = vtpnt(-43.896, -135.2111)
#p25 = vtpnt(-18.896, -135.2111)
    p26 = vtpnt(-43.896, -140.2111)
    p27 = vtpnt(-18.896, -140.2111)
    #line19 = msp.AddLine(p24, p25)
    line20 = msp.AddLine(p26, p27)
    #line19.Lineweight = 50
    line20.Lineweight = 50
    #

    p28 = vtpnt(-18.896, -150.2111)
    p29 = vtpnt(46.104, -150.2111)
    line21 = msp.AddLine(p28, p29)
    line21.Lineweight = 50
    #

    p30 = vtpnt(-43.896, -155.2111)
    p31 = vtpnt(-18.896, -155.2111)
    #p32 = vtpnt(-43.896, -165.2111)
#p33 = vtpnt(-18.896, -165.2111)
    p34 = vtpnt(-43.896, -170.2111)
    p35 = vtpnt(-18.896, -170.2111)
    line22 = msp.AddLine(p30, p31)
    #line23 = msp.AddLine(p32, p33)
    line24 = msp.AddLine(p34, p35)
    line22.Lineweight = 50
    #line23.线宽= 50
    line24.Lineweight = 50

    p36 = vtpnt(-31.396, -170.2111)
    p37 = vtpnt(-31.396, -180.2111)
    line25 = msp.AddLine(p36, p37)
    line25.Lineweight = 50

    p38 = vtpnt(-10.896, -130.2111)
    p39 = vtpnt(-10.896, -150.2111)
    p40 = vtpnt(-2.896, -130.2111)
    p41 = vtpnt(-2.896, -150.2111)
    p42 = vtpnt(13.104, -130.2111)
    p43 = vtpnt(13.104, -150.2111)
    p44 = vtpnt(29.104, -130.2111)
    p45 = vtpnt(29.104, -180.2111)
    line26 = msp.AddLine(p38, p39)
    line27 = msp.AddLine(p40, p41)
    line28 = msp.AddLine(p42, p43)
    line29 = msp.AddLine(p44, p45)
    line26.Lineweight = 50
    line27.Lineweight = 50
    line28.Lineweight = 50
    line29.Lineweight = 50

    p46 = vtpnt(46.104, -130.2111)
    p47 = vtpnt(46.104, -180.2111)
    line30 = msp.AddLine(p46, p47)
    line30.Lineweight = 50

    p48 = vtpnt(5.104, -150.2111)
    p49 = vtpnt(5.104, -180.2111)
    line31 = msp.AddLine(p48, p49)
    line31.Lineweight = 50

    p50 = vtpnt(46.104, -165.2111)
    p51 = vtpnt(161.104, -165.2111)
    line32 = msp.AddLine(p50, p51)
    line32.Lineweight = 50

    p52 = vtpnt(101.104, -130.2111)
    p53 = vtpnt(101.104, -180.2111)
    line33 = msp.AddLine(p52, p53)
    line33.Lineweight = 50

    p54 = vtpnt(101.104, -145.2111)
    p55 = vtpnt(161.104, -145.2111)
    p56 = vtpnt(101.104, -150.2111)
    p57 = vtpnt(161.104, -150.104)
    p58 = vtpnt(101.104, -160.2111)
    p59 = vtpnt(161.104, -160.2111)
    line34 = msp.AddLine(p54, p55)
    line35 = msp.AddLine(p56, p57)
    line36 = msp.AddLine(p58, p59)
    line34.Lineweight = 50
    line35.Lineweight = 50
    line36.Lineweight = 50

    p60 = vtpnt(111.104, -150.2111)
    p61 = vtpnt(111.104, -160.2111)
    p62 = vtpnt(121.104, -150.2111)
    p63 = vtpnt(121.104, -160.2111)
    p64 = vtpnt(131.104, -145.2111)
    p65 = vtpnt(131.104, -165.2111)
    p66 = vtpnt(146.104, -145.2111)
    p67 = vtpnt(146.104, -160.2111)
    line37 = msp.AddLine(p60, p61)
    line38 = msp.AddLine(p62, p63)
    line39 = msp.AddLine(p64, p65)
    line40 = msp.AddLine(p66, p67)
    line37.Lineweight = 50
    line38.Lineweight = 50
    line39.Lineweight = 50
    line40.Lineweight = 50
    #

    p68 = vtpnt(-18.896, -135.2111)
    p69 = vtpnt(46.104, -135.2111)
    p70 = vtpnt(-18.896, -140.2111)
    p71 = vtpnt(46.104, -140.2111)
    p72 = vtpnt(-18.896, -145.2111)
    p73 = vtpnt(46.104, -145.2111)
    line41 = msp.AddLine(p68, p69)
    line42 = msp.AddLine(p70, p71)
    line43 = msp.AddLine(p72, p73)
    line41.Lineweight = 0.0
    line42.Lineweight = 0.0
    line43.Lineweight = 0.0
    #

    p74 = vtpnt(-18.896, -155.2111)
    p75 = vtpnt(46.104, -155.2111)
    p76 = vtpnt(-18.896, -160.2111)
    p77 = vtpnt(46.104, -160.2111)
    p78 = vtpnt(-18.896, -165.2111)
    p79 = vtpnt(46.104, -165.2111)
    p80 = vtpnt(-18.896, -170.2111)
    p81 = vtpnt(46.104, -170.2111)
    p82 = vtpnt(-18.896, -175.2111)
    p83 = vtpnt(46.104, -175.2111)
    line44 = msp.AddLine(p74, p75)
    line45 = msp.AddLine(p76, p77)
    line46 = msp.AddLine(p78, p79)
    line47 = msp.AddLine(p80, p81)
    line48 = msp.AddLine(p82, p83)
    line44.Lineweight = 0.0
    line45.Lineweight = 0.0
    line46.Lineweight = 0.0
    line47.Lineweight = 0.0
    line48.Lineweight = 0.0

    p84 = vtpnt(124.3448, 100.6996)
    p85 = vtpnt(128.3723, 100.6996)
    p86 = vtpnt(126.3541, 97.2355)
    line49 = msp.AddLine(p84, p85)
    line50 = msp.AddLine(p84, p86)
    line51 = msp.AddLine(p85, p86)
    line49.Lineweight = 0.0
    line50.Lineweight = 0.0
    line51.Lineweight = 0.0

    p87 = vtpnt(130.3813, 104.1479)
    p88 = vtpnt(137.4146, 104.1479)
    line52 = msp.AddLine(p87, p88)
    line53 = msp.AddLine(p85, p87)

    '''添加字体'''

    retVal2 = msp.AddText('浙江天马轴承集团有限公司', vtpnt(0, 0), 3.4)
    retVal2.Alignment = 10
    retVal2.TextAlignmentPoint = vtpnt(131.104, -172.711)

    retVal4 = msp.AddText('标记', vtpnt(0, 0), 2.0)
    retVal4.Alignment = 10
    #retVal4.Rotation = np.radians(180)
    retVal4.TextAlignmentPoint = vtpnt(-14.896, -147.7111)

    retVal5 = msp.AddText('处数', vtpnt(0, 0), 2.0)
    retVal5.Alignment = 10
    #retVal5.Rotation = np.radians(180)
    retVal5.TextAlignmentPoint = vtpnt(-6.896, -147.7111)

    retVal6 = msp.AddText('更改文件号', vtpnt(0, 0), 2.0)
    retVal6.Alignment = 10
    #retVal6.Rotation = np.radians(180)
    retVal6.TextAlignmentPoint = vtpnt(5.104, -147.7111)

    retVal7 = msp.AddText('签        字', vtpnt(0, 0), 2.0)
    retVal7.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal7.TextAlignmentPoint = vtpnt(21.104, -147.7111)

    retVal8 = msp.AddText('日        期', vtpnt(0, 0), 2.0)
    retVal8.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal8.TextAlignmentPoint = vtpnt(37.604, -147.7111)

    retVal9 = msp.AddText('设        计', vtpnt(0, 0), 2.0)
    retVal9.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal9.TextAlignmentPoint = vtpnt(-6.896, -152.7111)

    retVal10 = msp.AddText('校        对', vtpnt(0, 0), 2.0)
    retVal10.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal10.TextAlignmentPoint = vtpnt(-6.896, -157.7111)

    retVal11 = msp.AddText('标准化审查', vtpnt(0, 0), 2.0)
    retVal11.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal11.TextAlignmentPoint = vtpnt(-6.896, -162.7111)

    retVal12 = msp.AddText('工艺会签', vtpnt(0, 0), 2.0)
    retVal12.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal12.TextAlignmentPoint = vtpnt(-6.896, -167.7111)

    retVal13 = msp.AddText('审         核', vtpnt(0, 0), 2.0)
    retVal13.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal13.TextAlignmentPoint = vtpnt(-6.896, -172.7111)

    retVal14 = msp.AddText('批        准', vtpnt(0, 0), 2.0)
    retVal14.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal14.TextAlignmentPoint = vtpnt(-6.896, -177.7111)

    retVal15 = msp.AddText('图样标记', vtpnt(0, 0), 2.0)
    retVal15.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal15.TextAlignmentPoint = vtpnt(116.104, -147.6843)

    retVal16 = msp.AddText('质量(kg)', vtpnt(0, 0), 2.0)
    retVal16.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal16.TextAlignmentPoint = vtpnt(138.604, -147.6709)

    retVal17 = msp.AddText('比例', vtpnt(0, 0), 2.0)
    retVal17.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal17.TextAlignmentPoint = vtpnt(153.604, -147.6576)

    retVal18 = msp.AddText('其余', vtpnt(0, 0), 3.0)
    retVal18.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal18.TextAlignmentPoint = vtpnt(119.5633, 97.8533)

    retVal19 = msp.AddText('Ra', vtpnt(0, 0), 3.0)
    retVal19.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal19.TextAlignmentPoint = vtpnt(132.4185, 101.0174)

    retVal20 = msp.AddText('更(改)换通知号', vtpnt(0, 0), 2.0)
    retVal20.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal20.TextAlignmentPoint = vtpnt(-31.396, -142.7111)

    retVal21 = msp.AddText('版本号', vtpnt(0, 0), 2.0)
    retVal21.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal21.TextAlignmentPoint = vtpnt(-31.396, -157.7111)

    retVal22 = msp.AddText('A0', vtpnt(0, 0), 5.0)
    retVal22.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal22.TextAlignmentPoint = vtpnt(-31.396, -165.7111)

    retVal23 = msp.AddText('签字', vtpnt(0, 0), 2.0)
    retVal23.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal23.TextAlignmentPoint = vtpnt(-37.646, -172.7111)

    retVal24 = msp.AddText('日期', vtpnt(0, 0), 2.0)
    retVal24.Alignment = 10
    #retVal7.Rotation = np.radians(180)
    retVal24.TextAlignmentPoint = vtpnt(-37.646, -177.7111)

    retVal25 = msp.AddText('1:1', vtpnt(0, 0), 2.0)
    retVal25.Alignment = 10

    retVal25.TextAlignmentPoint = vtpnt(153.5941, -155.1643)

    # TAG 自定义输入
    retVal26 = msp.AddText(str1, vtpnt(0, 0), 5.0)
    retVal26.Alignment = 10
    retVal26.TextAlignmentPoint = vtpnt(73.604, -147.7111)

    retVal27 = msp.AddText(str2, vtpnt(0, 0), 3.0)
    retVal27.Alignment = 10
    retVal27.TextAlignmentPoint = vtpnt(131.104, -137.7111)

    retVal28 = msp.AddText(str3, vtpnt(0, 0), 3.0)
    retVal28.Alignment = 10
    retVal28.TextAlignmentPoint = vtpnt(73.604, -172.7111)

    retVal29 = msp.AddText(str2, vtpnt(0, 0), 3.0)
    retVal29.Alignment = 10
    retVal29.Rotation = math.radians(180)
    retVal29.TextAlignmentPoint = vtpnt(11.104, 103.7889)

    scale_list = [line1, line2, line3, line4, line5, line6, line7, line8, line9, line10, line11, line12, line13, line14,
                  line15, line16, line17, line18,  line20, line21, line22,  line24, line25, line26, line27,
                  line28, line29, line30, line31, line32, line33, line34, line35, line36, line37, line38, line39, line40,
                  line41, line42, line43, line44, line45, line46, line47, line48, line49, line50, line51, line52, line53,
                  retVal2,  retVal4, retVal5, retVal6, retVal7, retVal8, retVal9, retVal10, retVal11,
                  retVal12, retVal13, retVal14, retVal15, retVal16, retVal17, retVal18, retVal19, retVal20, retVal21,
                  retVal22, retVal23, retVal24, retVal25, retVal26, retVal27, retVal28, retVal29]
    # INFO 缩放功能
    for i in scale_list:
        i.ScaleEntity(vtpnt(0, 0), scale_factor)


# TEST 测试
if __name__ == '__main__':
    cad_modu(1, '保  持  架', 'E6206 TVP5-2RSL·46', 'PA46-GF30')
