import math
import pandas as pd
import numpy as np




def caculate(xinghao, d, D, alfa, item, bm):
    xilie = alfa
    alfa = np.deg2rad(alfa)
    str_xinghao = str(xinghao)
    zhijing = str_xinghao[1]

    columns = pd.MultiIndex.from_product([['100', '200'], ['min', 'max']])
    data = [[0.27, 0.32, 0, 0], [0.27, 0.32, 0.29, 0.33],
            [0.27, 0.32, 0.30, 0.335]]
    df = pd.DataFrame(data, columns=columns)

    if zhijing == '0':
        if xilie == 15 or xilie == 25:
            result1 = df.loc[0, ('100', 'min')]
            result2 = df.loc[0, ('100', 'max')]
        if xilie == 40:
            result1 = df.loc[0, ('200', 'min')]
            result2 = df.loc[0, ('200', 'max')]

    if zhijing == '2':
        if xilie == 15 or xilie == 25:
            result1 = df.loc[1, ('100', 'min')]
            result2 = df.loc[1, ('100', 'max')]
        if xilie == 40:
            result1 = df.loc[1, ('200', 'min')]
            result2 = df.loc[1, ('200', 'max')]

    if zhijing == '3':
        if xilie == 15 or xilie == 25:
            result1 = df.loc[2, ('100', 'min')]
            result2 = df.loc[2, ('100', 'max')]
        if xilie == 40:
            result1 = df.loc[2, ('200', 'min')]
            result2 = df.loc[2, ('200', 'max')]

    # print(result1)
    # print(result2)

    Dw_min = result1 * (D - d)
    Dw_max = result2 * (D - d)

    print('Kwmin = ', Dw_min)
    print('Kwmax = ', Dw_max)

    df = pd.read_excel('./钢球标准尺寸.xlsx', sheet_name='钢球标准尺寸')

    # list1是范围内的Dw
    list1 = [x for x in df['Dw'] if Dw_min <= x <= Dw_max]

    dpw_list = [x * (D + d) for x in list(np.arange(0.5, 0.51, 0.001))]

    list2 = []
    for num in list1:
        if num <= 15:
            kz = 1.01 + 1.5 / num
            zmax = (math.pi * dpw_list[5]) / (kz * num)
            zmax = math.floor(zmax)
            list2.append(zmax)

        if num > 15:
            kz = 1.11
            zmax = (math.pi * dpw_list[5]) / (kz * num)
            zmax = math.floor(zmax)
            list2.append(zmax)

    # print(list2)

    factor_list = [round(x, 2) for x in list(np.arange(0.01, 0.41, 0.01))]

    fc_list = [29.1, 35.8, 40.3, 43.8, 46.7,
               49.1, 51.1, 52.8, 54.3, 55.5,
               56.6, 57.5, 58.2, 58.8, 59.3,
               59.6, 59.8, 59.9, 60, 59.9,
               59.8, 59.6, 59.3, 59, 58.6,
               58.2, 57.7, 57.1, 56.6, 56,
               55.3, 54.6, 53.9, 53.2, 52.4,
               51.7, 50.9, 50, 49.2, 48.4]

    # 存放每次计算的最大Cr
    list4 = []

    # 存放 dpw值
    list6 = []
    for i in range(len(list1)):
        list3 = []
        if list1[i] <= 25.4:
            for j in range(len(dpw_list)):
                load = list1[i] * np.cos(alfa) / dpw_list[j]
                fc = np.interp(load, factor_list, fc_list)

                Cr = bm * fc * pow(item * np.cos(alfa), 0.7) * pow(list2[i], 2 / 3) * pow(list1[i], 1.8)
                list3.append(Cr)

            list3 = sorted(enumerate(list3), key=lambda x: x[1], reverse=True)
            sorted_indices = [x[0] for x in list3]
            sorted_values = [x[1] for x in list3]

            list4.append(sorted_values[0])

            list6.append(dpw_list[sorted_indices[0]])

        if list1[i] > 25.4:
            for j in range(len(dpw_list)):
                load = list1[i] * np.cos(0) / dpw_list[j]
                fc = np.interp(load, factor_list, fc_list)

                Cr = 3.647 * bm * fc * pow(item * np.cos(alfa), 0.7) * pow(list2[i], 2 / 3) * pow(list1[i], 1.4)
                list3.append(Cr)

            list3 = sorted(enumerate(list3), key=lambda x: x[1], reverse=True)
            sorted_indices = [x[0] for x in list3]
            sorted_values = [x[1] for x in list3]

            list4.append(sorted_values[0])

            list6.append(dpw_list[sorted_indices[0]])

    # 找出list4 的最大值
    # print('每个dw对应下不同dpw的Cr最大值 = ', list4)
    # print('每个Cr对应的dpw = ', list6)
    list4 = sorted(enumerate(list4), key=lambda x: x[1], reverse=True)
    sorted_indices = [x[0] for x in list4]
    sorted_values = [x[1] for x in list4]

    # print("dw = ", list1[sorted_indices[0]])
    # print('dpw = ', list6[sorted_indices[0]])
    # print('z = ', list2[sorted_indices[0]])
    # print('Cr = ', sorted_values[0])
    #

    dw = list1[sorted_indices[0]]
    dpw = list6[sorted_indices[0]]
    z = list2[sorted_indices[0]]
    Cr = sorted_values[0]
    print(dw)

    return dw, dpw, z, Cr


def cacuklateACBB(d, D, B,alfa, xinghao, gongcha, item=1):
    coss = (math.cos(math.radians(alfa)))
    sinn = (math.sin(math.radians(alfa)))
    fc = 12.3
    bm = 1.3

    Dw, Dpw, Z, Cr = caculate(xinghao, d, D, alfa, item, bm)

    # 轴承额定负荷和额定寿命计算
    u8 = Dw*math.cos(math.radians(alfa))/Dpw
    u8 = round(u8, 2)
    df22 = pd.read_excel("./AC.xlsx", sheet_name='fc', index_col=0)
    fc = df22.loc[u8]
    Cor = fc*Z*Dw**2*coss
    # 轴承额定负荷和额定寿命计算
    # 套圈设计
    mk=0
    if Dw<=60:
        mk=Dw
    elif  Dw>60:
        mk=60 
    df20 = df = pd.read_excel("./AC.xlsx", sheet_name='rire', index_col=0)
    Ri, Re = df20.loc[mk]
    # print(Ri,Re)
    

    # 内外圈沟道曲率半径下式
    # di = Dpw-2*Ri+(2*Ri-Dw)*coss
    di = Dpw-2*Ri+(2*Ri-Dw)*coss
    # 书6
    De = Dpw+2*Re-(2*Re-Dw)*coss
    # 书6
    # print('di:', di)
    # print('De:', De)
    # 内外圈沟道曲率半径下式
    # 外圈沟道直径
    k2i=0
    k2e=0
    if alfa in [15, 25]:
        if xinghao in [7000]:
            k2i = 0.35
            k2e = 0.35
        elif xinghao in [7200, 7300]:
            if d <= 25:
                k2i = 0.35
                k2e = 0.35
            else:
                k2i = 0.40
                k2e = 0.40
    elif alfa in [40]:
        if xinghao in [7200, 7300]:
            k2i = 0.65
            k2e = 0.60
    d2 = di+k2i*Dw
    D2 = De-k2e*Dw

    # 内圈挡边直径
    # 内圈滚道中心至基准端面的距离ai、ae
    df = pd.DataFrame({
        'alfa': [15, 25, 40],
        'kai': [0.00388, 0.00634, 0.00964],
        'kae': [0.00647, 0.01057, 0.01607]
    })
    df2 = df.set_index('alfa')
    kae, kai = df2.loc[alfa]
    # print('kai', kai)
    # print('kae', kae)
    if 0 < d <= 10:
        u4 = 18
    elif 10 < d <= 18:
        u4 = 18
    elif 18 < d <= 30:
        u4 = 30
    elif 30 < d <= 50:
        u4 = 50
    elif 50 < d <= 80:
        u4 = 80
    elif 80 < d <= 120:
        u4 = 120
    elif 120 < d <= 180:
        u4 = 180
    elif 180 < d <= 250:
        u2 = 250
    elif 250 < d <= 315:
        u2 = 315
    df14 = pd.DataFrame({
        'd': [10, 18, 30, 50, 80, 120, 180, 250, 315],
        '': [0.015, 0.02, 0.025, 0.03, 0.04, 0.045, 0.05, 0.06, 0.065]
    })
    df15 = df14.set_index('d')
    dlta = df15.loc[u4]

    # else:
    if xinghao in [7000, 7200]:
        ai = 0.5 * B + (Ri-0.5 * Dw) * sinn-2 * dlta
        ae = 0.5 * B + (Re-0.5 * Dw) * sinn-2 * dlta
    else:
        ai = 0.5 * B + (Ri - 0.5 * Dw) * sinn - 2 * dlta
        ae = 0.5 * B + (Re - 0.5 * Dw) * sinn - 2 * dlta
    # print('ai:', ai)
    # print('ae:', ae)
    # 内圈滚道中心至基准端面的距离ai、ae
    # 装配锁口高度t 下式
    if 0 < d <= 30:
        u3 = 30
    elif 30 < d <= 80:
        u3 = 80
    elif 80 < d <= 1000:
        u3 = 1000
    df10 = pd.DataFrame({
        'd': [30, 80, 1000],
        '': [0.01, 0.02, 0.03]
    })
    df11 = df10.set_index(['d'])
    deltat = float(df11.loc[u3])
    if alfa == 15:
        if 4.5 < Dw <= 5:
            kt = 0.00206
        elif 5 < Dw <= 45:
            kt = 0.00196
    elif alfa == 25:
        if 4.5 < Dw <= 7:
            kt = 0.00468
        elif 7 < Dw <= 45:
            kt = 0.00436
    elif alfa == 40 and 7 < Dw <= 45:
        kt = 0.01074
    t1 = 0.00053*De + 0.5 * kt * Dw + deltat
    if 0.1 > t1:
        t = float('%.2f' % t1)
    elif 0.1 <= t1:
        t = float('%.2f' % t1)
    # print('t:', t)
    # 装配锁口高度t 上式
    if 0 < d <= 35:
        u = 35
    elif 35 < d <= 120:
        u = 120
    else:
        u = 240

    if 4.762 <= Dw <= 6:
        Rimax = Ri+0.03
        Remax = Re+0.03
    elif 6.1 <= Dw <= 10:
        Rimax = Ri + 0.04
        Remax = Re + 0.04
    elif 10.1 <= Dw <= 18:
        Rimax = Ri + 0.06
        Remax = Re + 0.06
    elif 18.1 <= Dw <= 24:
        Rimax = Ri + 0.09
        Remax = Re + 0.09
    elif 24.1 <= Dw <= 30:
        Rimax = Ri + 0.12
        Remax = Re + 0.12
    elif 30.1 <= Dw <= 40:
        Rimax = Ri + 0.14
        Remax = Re + 0.14
    elif 40.1 <= Dw <= 45:
        Rimax = Ri + 0.18
        Remax = Re + 0.18
    # if jingdu=P0:
    #     if Dw
    Rimin = Ri
    Remin = Re
    Dwmin = 0
    Dwmax = 0
    if gongcha == "P2":
        if 0 < Dw <= 18:
            Dwmax = Dw+0.0085
            Dwmin = Dw-0.0085
    elif 18 < Dw <= 30:
        Dwmax = Dw + 0.0105
        Dwmin = Dw - 0.0105
    elif gongcha == "P4":
        if 0 < Dw <= 18:
            Dwmax = Dw + 0.0105
            Dwmin = Dw - 0.0105
    elif 18 < Dw <= 30:
        Dwmax = Dw + 0.017
        Dwmin = Dw - 0.017
    elif gongcha == "P5":
        if 0 < Dw <= 30:
            Dwmax = Dw + 0.017
            Dwmin = Dw - 0.017
    elif 30 < Dw <= 50:
        Dwmax = Dw + 0.017
        Dwmin = Dw - 0.017
    elif gongcha in ["P6", "P0"]:
        if 0 < Dw <= 50:
            Dwmax = Dw + 0.017
            Dwmin = Dw - 0.017
    elif 50 < Dw <= 80:
        Dwmax = Dw + 0.022
        Dwmin = Dw - 0.022

    if alfa == 15 and 4.5 < Dw <= 5:
        u1 = 5
    elif alfa == 15 and 5 < Dw <= 45:
        u1 = 45
    elif alfa == 25 and 4.5 < Dw <= 7:
        u1 = 7
    elif alfa == 25 and 7 < Dw <= 45:
        u1 = 45
    elif alfa == 40 and 7 < Dw <= 45:
        u1 = 45
    df5 = pd.DataFrame({
        'alfa': [15, 15, 25, 25, 40, ],
        'dw': [5, 45, 7, 45, 45],
        '': [3.5, 3, 3, 2, 3],
    })
    df6 = df5.set_index(['alfa', 'dw'])
    # print(df6)
    df7 = pd.DataFrame({
        'alfa': [15, 15, 25, 25, 40],
        'dw': [5, 45, 7, 45, 45],
        '': [3.5, 3, 5, 4, 6],
    })
    df8 = df7.set_index(['alfa', 'dw'])
    alfamax = float(df6.loc[alfa, u1]+alfa)
    alfamin = float(alfa - df8.loc[alfa, u1])

    # print("alfamax", alfamax)
    # print("alfamin", alfamin)

    gmax = 2 * (Rimax+Remax-Dwmin) * (1-math.cos(math.radians(alfamax)))
    gmin = 2 * (Rimin+Remin-Dwmax) * (1-math.cos(math.radians(alfamin)))
    # 配套最小最大径向游隙上
    # 装配锁口高度的验算下式
    alfao = 0.0000118
    deltaT = 20
    if 0 < t <= 0.07:
        tmin = t-0.01
    elif 0.07 < t <= 0.1:
        tmin = t - 0.015
    elif 0.1 < t <= 0.2:
        tmin = t - 0.02
    elif 0.2 < t <= 0.29:
        tmin = t - 0.03
    elif 0.29 < t <= 0.39:
        tmin = t - 0.04
    elif 0.39 < t:
        tmin = t - 0.05
    # print('tmin', tmin)
    ymax = 2*t-gmin-alfao*deltaT*De
    ymin = 2*tmin-gmax
    # print('ymax:', ymax)
    # print('ymin:', ymin)
    # ymax=2*tmax-gmin-alfao*deltaT*De
    # ymin=2*tmin-gmax
    # 装配锁口高度的验算上式
    ti = 2*t
    # print('ti:', ti)
    # 非装配锁口高度ti
    # alfami = math.acos(1-gmin/(2*( Rimax + Remax - Dwmin)))
    # alfama = math.acos(1- gmax /(2*(Rimin+Remin-Dwmax)))
    #  接触角验算
    # # 装配高极限尺寸按下式确定
    # Tmax=aimax+aemax-(Rimin+Remin-Dw)*math.sin(math.radians(alfamin))
    # Tmax=aimax+aemax-(Rimin+Remin-Dw)*math.sin(math.radians(alfamin))
    Tmax = ai+ae-(Rimin+Remin-Dwmax)*math.sin(math.radians(alfamin))
    Tmin = ai+ae-(Rimax+Remax-Dwmin)*math.sin(math.radians(alfamax))
    # print('Tmax:', Tmax)
    # print('Tmin:', Tmin)
    # 装配高极限尺寸按上式确定
    # 实体保持架的设计
    # 保持架内径Dc1及外径Dc
    # 保持架旋转以内圈挡边引导时:
    if 0 < d2 <= 18:
        u2 = 18
    elif 18 < d2 <= 30:
        u2 = 30
    elif 30 < d2 <= 50:
        u2 = 50
    elif 50 < d2 <= 80:
        u2 = 80
    elif 80 < d2 <= 120:
        u2 = 120
    elif 120 < d2 <= 180:
        u2 = 180
    elif 180 < d2 <= 260:
        u2 = 260
    elif 260 < d2 <= 360:
        u2 = 360
    df9 = pd.DataFrame({
        'd2': [18, 30, 50, 80, 120, 180, 260, 360],
        '': [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55]
    })
    df10 = df9.set_index('d2')
    ibcti = df10.loc[u2]
    if D2 <= 18:
        u3 = 18
    elif 18 < D2 <= 30:
        u3 = 30
    elif 30 < D2 <= 50:
        u3 = 50
    elif 50 < D2 <= 80:
        u3 = 80
    elif 80 < D2 <= 120:
        u3 = 120
    elif 120 < D2 <= 180:
        u3 = 180
    elif 180 < D2 <= 260:
        u3 = 260
    elif 260 < D2 <= 360:
        u3 = 360
    df12 = pd.DataFrame({
        'D2': [18, 30, 50, 80, 120, 180, 260, 360],
        '': [0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.70, 0.80]
    })
    df13 = df12.set_index('D2')
    ibcte = df13.loc[u3]
    Dc1 = d2+ibcti
    Dc = Dc1+Dw
    # print('Dc1:', Dc1)
    # print('Dc:', Dc)
    Dc = D2-ibcti
    Dc1 = Dc-0.8*Dw
    # 保持架兜孔直径deltaC
    deltaC = 1.004*Dw+0.12
    # print('deltaC:', deltaC)
    # 保持架宽度Bc
    Bc = B-(0.06*Dw+0.5)
    # print('Bc:', Bc)
    # 保持架中心圆直径Dcp
    Dcp = Dpw
    # print('Dcp:', Dcp)
    # 直兜孔保持架外圆柱面上两兜孔中心径
    C = Dc*math.sin(math.radians(180/Z))
    # print('C:', C)
    # 直兜孔保持架间最小壁厚Sb
    Sb = Dc1*math.sin(math.radians(180/Z-math.asin(deltaC/Dc1)))
    # print('Sb:', Sb)
    # Sb必须满足以下验算值:
    # 7000c系列、7000ac系列，当d≤15时，Sb≥0.9
    # 当d＞15时，Sb≥0.1Dw≥1
    # 36200系列、46200系列，当d≤15时，Sb≥0.9
    # 当d＞15时，Sb≥0.08Dw≥1
    # S值满足上述要求可采用直兜孔，否则采用球形兜孔及
    # 其它形式，若仍采用直兜孔，保持架内径兜孔处应开一
    # 环形槽，槽宽0.75deltaC，槽深不超过0.1(Dc - Dc1)，
    # 环形槽倒角45°。
    # 槽宽:
    CK = 0.75*deltaC
    # print('CK:', CK)
    # 槽底径:
    Dck = Dc1+2*0.1*(Dc-Dc1)
    # print('Dck:', Dck)
    # 球兜孔保持架中心圆直径处两兜孔中心距
    C1 = Dcp*math.sin(math.radians(180/Z))
    # print('C1:', C1)
    # 球兜孔保持架的球面兜孔与内圆柱面相交的椭圆长轴
    J = math.sqrt(deltaC**2-((Dcp-Dc1))**2)
    # print('J:', J)
    # elif baochijia in [1]:
    # "C"型冲压保持架的设计
    # 保持架钢板厚度S
    S = float(('%.1f' % (0.08 * Dw)))
    # print('S:', S)
    # 保持架宽度Bc
    if xinghao == 7300:
        Ks = 2.5
    else:
        Ks = 3
    Bc = Dw + Ks * S
    # print('Bc:', Bc)
    # Ks:
    # 保持架小端面至只通过钢球中心的径向平面间的距离hc
    hc = 0.5*Dw+0.44*Ks*S
    # print('hc:', hc)
    # 保持架内球面曲率半径Rc
    Rc = (0.5+Bc-hc)/math.sin(math.radians(20))+0.14*Dw
    # 保持架中心圆直径
    Dcp = Dpw
    # 保持架小端面至内球面曲率中心延长线交点间的距离Bc1
    Bc1 = 0.5*Dcp*math.tan(math.radians(20))+hc
    # 保持架小端面内球面与平面交点处直径dc
    dc = 2*(math.sqrt(Rc**2-(Bc-S+0.5)**2)+(Bc1-Bc-0.5)/math.tan(math.radians(20)))
    # 保持架小端内径Dc1
    if Dw <= 18:
        ibct1 = 2.5
    elif 18 < Dw <= 28:
        ibct1 = 4
    elif 28 < Dw <= 42:
        ibct1 = 6
    Dc1 = di+2*ti+ibct1
    # 保持架大端内径Dc2
    Dc2 = Dcp-3*S
    # 保持架装配角beta
    beta = 20
    # 保持架小端弯边曲率半径r
    r = S
    # 保持架小端弯边曲率半径r1
    r1 = 2*S
    # 保持架压坡直径dc'
    if Dw <= 15:
        ibct2 = 0.2
    elif 15 < Dw <= 24:
        ibct2 = 0.26
    elif 24 < Dw <= 40:
        ibct2 = 0.32
    elif 40 < Dw <= 60:
        ibct2 = 0.40
    dca = Dw+ibct2
    # 保持架压坡深度S1
    S1 = 0.4*S
    # 保持架小端弯边高度
    hc2 = hc-0.5*math.sqrt(dca**2-(Dcp-(Dc1+1.5*S))**2)
    # 保持架小端弯边角
    fai1 = math.atan((hc2-(r+S))/((math.sqrt((Rc-r)**2-(Bc-(r+S)+0.5)**2))+(Bc1-Bc-0.5)/math.tan(math.radians(20))-((Dc1+1.5*S)/2))/(hc2-(r+S)))
    fai2 = math.asin(r*math.sin(math.radians(fai1)))
    beta2 = fai1+fai2
    # 保持架窗孔直径
    if 0 < Dw <= 15:
        ibct3 = 0.35
    elif 15 < Dw <= 25.4:
        ibct3 = 0.25
    elif 25.4 < Dw:
        ibct3 = 0.15

    Dwc = 2*math.sqrt(0.25*dca**2-(((2*(Rc+0.4*S)*math.sin(math.radians(20)))**2
                                    - (dca*math.sin(math.radians(20)))**2 - 4*(Bc-hc+0.5)**2)/(8*(Bc-hc+0.5)
                                                                                               * math.sin(math.radians(20))))**2)-ibct3
    # print('dwc:', Dwc)

    # 保持架窗孔底部至保持架底面的高度hc1
    # (压坡前尺寸,供制造模具用)
    hc1 = hc-(0.5*Dwc+(0.14*Dw-(Rc-math.sqrt(Rc**2-0.25*Dwc**2)))
              * math.tan(math.radians(20)))*math.cos(math.radians(20))
    # print('hc1', hc1)
    # 保持架外径
    Dc = 2*(r1+S+(Bc1-Bc-0.5)/math.tan(math.radians(20)
                                       + math.sqrt((Rc-r1)**2-(S+r1+0.5)**2))-0.2)
    return De, B, Re, ae, di, Ri, ai, d2, Dc1, Dcp, Bc, deltaC, D2, dc, hc2, Dc2, Dc, hc, Bc1, Rc, Dwc, dca, S, S1, Bc1, CK, C1, J, Dck


if __name__ == '__main__':
    d = 12
    D = 32
    B = 9
    T = 9
    alfa = 25
    xinghao = 7200
    c_list = cacuklateACBB(15, 32, 9, 15, 7000, "P2", 1)
    # print(c_list)

    baochijia = 1
    # 1实体保持架的设计 2"C"型冲压保持架的设计
    quanzhuan = 1
    # 1保持架旋转以内圈挡边引导时 2 保持架旋转以外圈挡边引导时
    gongcha = 0
    # 24560
    item = 1

    cacuklateACBB(d, D, B, alfa, xinghao, gongcha, item)
