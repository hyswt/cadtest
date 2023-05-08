import math

import pandas as pd
import numpy as np


def dgbbcaculate(xinghao, d, D, item, bm):

    str_xinghao = str(xinghao)
    zhijing = str_xinghao[-3]
    # xilie = str_xinghao[0] + '000'
    alfa = 0

    columns = pd.MultiIndex.from_product([['100', '200', '300', '400'], ['min', 'max']])
    data = [[0.24, 0.30, 0.24, 0.31, 0.25, 0.32, 0.28, 0.32], [0.30, 0.32, 0.30, 0.32, 0.30, 0.33, 0.30, 0.32],
            [0.29, 0.32, 0.28, 0.32, 0.29, 0.32, 0.25, 0.30]]
    df = pd.DataFrame(data, columns=columns)
    # print(df)

    if d <= 35:
        if zhijing == '0':
            result1 = df.loc[0, ('100', 'min')]
            result2 = df.loc[0, ('100', 'max')]
        if zhijing == '2':
            result1 = df.loc[0, ('200', 'min')]
            result2 = df.loc[0, ('200', 'max')]
        if zhijing == '3':
            result1 = df.loc[0, ('300', 'min')]
            result2 = df.loc[0, ('300', 'max')]
        if zhijing == '4':
            result1 = df.loc[0, ('400', 'min')]
            result2 = df.loc[0, ('400', 'max')]
    if d > 35 and d <= 120:
        if zhijing == '0':
            result1 = df.loc[1, ('100', 'min')]
            result2 = df.loc[1, ('100', 'max')]
        if zhijing == '2':
            result1 = df.loc[1, ('200', 'min')]
            result2 = df.loc[1, ('200', 'max')]
        if zhijing == '3':
            result1 = df.loc[1, ('300', 'min')]
            result2 = df.loc[1, ('300', 'max')]
        if zhijing == '4':
            result1 = df.loc[1, ('400', 'min')]
            result2 = df.loc[1, ('400', 'max')]
    if d > 120 and d <= 240:
        if zhijing == '0':
            result1 = df.loc[2, ('100', 'min')]
            result2 = df.loc[2, ('100', 'max')]
        if zhijing == '2':
            result1 = df.loc[2, ('200', 'min')]
            result2 = df.loc[2, ('200', 'max')]
        if zhijing == '3':
            result1 = df.loc[2, ('300', 'min')]
            result2 = df.loc[2, ('300', 'max')]
        if zhijing == '4':
            result1 = df.loc[2, ('400', 'min')]
            result2 = df.loc[2, ('400', 'max')]

    print(result1)
    print(result2)

    Dw_min = result1 * (D - d)
    Dw_max = result2 * (D - d)

    print('Kwmin = ', Dw_min)
    print('Kwmax = ', Dw_max)

    df = pd.read_excel('./钢球标准尺寸.xlsx', sheet_name='钢球标准尺寸')
    # 选择需要的列，比如第一列
    column_data = df.iloc[:, 0]
    # 将选定列的数据转换成 Python 的列表或数组
    column_values = column_data.values.tolist()  # 转换成列表

    column_values = [x for x in column_values if Dw_min < x < Dw_max]
    print('dw范围 = ', column_values)

    xinghao_dict = {'0': 195, '2': 194, '3': 193, '4': 192}

    fai = xinghao_dict[zhijing]

    dpw_list = [x * (D + d) for x in list(np.arange(0.5, 0.515, 0.001))]

    print("dpw范围 = ", dpw_list)

    list1 = []
    list2 = []
    for num in column_values:
        zmax = (fai / (2 * math.degrees(math.asin(num / dpw_list[15])))) + 1

        zmax = math.floor(zmax)
        list1.append(zmax)

        zmin = (180 / (2 * math.degrees(math.asin(num / dpw_list[0])))) + 1
        zmin = math.ceil(zmin)
        list2.append(zmin)

    print('对应范围内的滚珠数 = ', list1)

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
    for i in range(len(column_values)):
        list3 = []
        if column_values[i] <= 25.4:
            for j in range(len(dpw_list)):
                load = column_values[i] * np.cos(alfa) / dpw_list[j]
                fc = np.interp(load, factor_list, fc_list)

                Cr = bm * fc * pow(item * np.cos(alfa), 0.7) * pow(list1[i], 2 / 3) * pow(column_values[i], 1.8)
                list3.append(Cr)

            list3 = sorted(enumerate(list3), key=lambda x: x[1], reverse=True)
            sorted_indices = [x[0] for x in list3]
            sorted_values = [x[1] for x in list3]

            list4.append(sorted_values[0])

            list6.append(dpw_list[sorted_indices[0]])

        if column_values[i] > 25.4:
            for j in range(len(dpw_list)):
                load = column_values[i] * np.cos(0) / dpw_list[j]
                fc = np.interp(load, factor_list, fc_list)

                Cr = 3.647 * bm * fc * pow(item * np.cos(alfa), 0.7) * pow(list1[i], 2 / 3) * pow(column_values[i], 1.4)
                list3.append(Cr)

            list3 = sorted(enumerate(list3), key=lambda x: x[1], reverse=True)
            sorted_indices = [x[0] for x in list3]
            sorted_values = [x[1] for x in list3]

            list4.append(sorted_values[0])

            list6.append(dpw_list[sorted_indices[0]])

    # 找出list4 的最大值
    print('每个dw对应下不同dpw的Cr最大值 = ', list4)
    print('每个Cr对应的dpw = ', list6)
    list4 = sorted(enumerate(list4), key=lambda x: x[1], reverse=True)
    sorted_indices = [x[0] for x in list4]
    sorted_values = [x[1] for x in list4]

    print("dw = ", column_values[sorted_indices[0]])
    print('dpw = ', list6[sorted_indices[0]])
    print('z = ', list1[sorted_indices[0]])
    print('Cr = ', sorted_values[0])
    dw = column_values[sorted_indices[0]]
    dpw = list6[sorted_indices[0]]
    z = list1[sorted_indices[0]]
    cr = sorted_values[0]
    return dw, dpw, z


def dgbb_design(d, D, B, xinghao):

    str_xinghao = str(xinghao)
    zhijing = int(str_xinghao[-3])

    Dw, Dpw, Z = dgbbcaculate(xinghao=xinghao, d=d, D=D, item=1, bm=1.3)

    u30 = Dw / Dpw
    u30 = round(u30, 2)
    df22 = pd.read_excel("./AC.xlsx", sheet_name='fc', index_col=0)
    fc = df22.loc[u30]
    Cor = fc * Z * Dw ** 2
    print('cor', Cor)
    mk=0
    if Dw<=60:
        mk=Dw
    elif  Dw>60:
        mk=60    
    df30 = pd.read_excel('./AC.xlsx', sheet_name='srire', index_col=0)
    Ri, Re, Rc, K = df30.loc[mk]
    if 2 < d <= 6:
        u6 = 6
    elif 6 < d <= 10:
        u6 = 10
    elif 10 < d <= 18:
        u6 = 18
    elif 18 < d <= 24:
        u6 = 24
    elif 24 < d <= 30:
        u6 = 30
    elif 30 < d <= 40:
        u6 = 40
    elif 40 < d <= 50:
        u6 = 50
    elif 50 < d <= 65:
        u6 = 65
    elif 65 < d <= 80:
        u6 = 80
    elif 80 < d <= 100:
        u6 = 100
    elif 100 < d <= 120:
        u6 = 120
    elif 120 < d <= 140:
        u6 = 140
    elif 140 < d <= 160:
        u6 = 160
    elif 160 < d <= 180:
        u6 = 180
    elif 180 < d <= 200:
        u6 = 200
    df21 = pd.DataFrame({
        'd': [6, 10, 18, 24, 30, 40, 50, 65, 80, 100, 120, 140, 160, 180, 200],
        'umin': [0.002, 0.002, 0.003, 0.005, 0.005, 0.006, 0.006, 0.008, 0.010, 0.012, 0.015, 0.018, 0.018, 0.020,
                 0.025],
        'umax': [0.013, 0.013, 0.018, 0.020, 0.020, 0.020, 0.023, 0.028, 0.030, 0.036, 0.041, 0.048, 0.053, 0.061,
                 0.071]

    })
    df22 = df21.set_index('d')
    umin, umax = df22.loc[u6]
    print('umin', umin)
    print('umax', umax)
    u = (umin + umax) / 2
    di = Dpw - Dw
    De = Dpw + 2 * Dw + u
    print('u', u)
    print('di:', di)
    print('De:', De)
    # 内外圈沟道曲率半径下式
    a = B / 2  # 沟位置
    ai = a
    ae = a
    print('ai:', ai)
    print('ae:', ae)
    # 外圈沟道直径# print('ai:', ai)
    # # print('ae:', ae)
    kd=0
    if xinghao in [6000]:
        kd = 0.35
    elif xinghao in [6200, 6300]:
        if d <= 25:
            kd = 0.35
        else:
            kd = 0.40
    elif xinghao in [6400]:
        kd = 0.40
    d2 = di + kd * Dw
    D2 = De - kd * Dw
    print('d2:', d2)
    print('D2:', D2)
    # 保持架钢板厚度
    if zhijing in [0] and 4 < Dw <= 35:
        S = math.sqrt((Dw / 3.174) + (1.25) ** 2) - 1.25
    if zhijing in [2] and 4 < Dw <= 45:
        S = math.sqrt((Dw / 6.3) - 0.5) - 0.04
    if zhijing in [3, 4]:
        if 5 < Dw <= 45:
            S = math.sqrt((Dw / 8.5) - 0.5) + 0.15
        elif 45 < Dw <= 55:
            S = math.sqrt((Dw / 8.5) - 0.5) + 0.4
    # 保持架钢板厚度上
    # 保持架宽度下
    if 0 <= S <= 1.0:
        S = round(S, 1)
    elif 1 < S <= 1.1:
        S = 1
    elif 1 < S <= 1.3:
        S = 1.2
    elif 1.3 < S <= 1.75:
        S = 1.5
    elif 1.75 < S <= 2.25:
        S = 2
    elif 2.25 < S <= 2.75:
        S = 2.5
    elif 2.75 < S <= 3.25:
        S = 3
    elif 3.25 < S:
        S = 3.5
    print('s', S)
    if zhijing in [0]:
        kc = 0.48
    elif zhijing in [2, 3, 4]:
        kc = 0.45
    Bc = kc * Dw
    print('bc', Bc)
    # 保持架宽度上
    # 保持架外径
    Dc = Dpw + Bc
    print('dc', Dc)
    # 保持架内径
    Dc1 = Dpw - Bc
    print('Dc1', Dc1)
    Dcp = Dpw
    # 保持架兜孔深度K
    df23 = pd.DataFrame({
        'Dw': [6, 10, 14, 18, 24, 32, 40, 50, 60],
        'Epc': [0.04, 0.05, 0.06, 0.07, 0.08, 0.10, 0.1, 0.12, 0.14],
        'kmax': [0.04, 0.05, 0.06, 0.07, 0.08, 0.10, 0.10, 0.12, 0.14]
    })
    if 0 < Dw <= 6:
        u7 = 6
    elif 6 < Dw <= 10:
        u7 = 10
    elif 10 < Dw <= 14:
        u7 = 14
    elif 14 < Dw <= 18:
        u7 = 18
    elif 18 < Dw <= 24:
        u7 = 24
    elif 24 < Dw <= 32:
        u7 = 32
    elif 32 < Dw <= 40:
        u7 = 40
    elif 40 < Dw <= 50:
        u7 = 50
    elif 50 < Dw <= 60:
        u7 = 60
    df24 = df23.set_index('Dw')
    Epc, km = df24.loc[u7]
    # K = 0.5 * Dw + Epc
    print('k', K)
    # 保持架球兜内球面半径Rc
    # Kmax= K+km
    # Rc = Kmax
    print('RC:', Rc)
    # 保持架钢球径向游动量
    Ep = 0.85 * Bc - Dw * math.sin(math.acos((2 * (Rc * math.cos(math.asin((0.85 * Bc) / (2 * Rc))) - Rc + K)) / Dw))
    print('ep', Ep)

    # 计算Epmin时, Rc, Hc取最小值
    # Epmin:
    # 计算Epmax时, Rc, Hc取最大值
    # Epmax:
    # 相邻两球兜或铆钉孔中心距
    C0 = Dcp * math.sin(math.radians(180 / Z))
    print('C0:', C0)
    # 兜孔中心与相邻铆钉孔中心距
    C1 = Dcp * math.sin(math.radians(90 / Z))
    print('C1:', C1)
    # 保持架兜孔之间的平面与球兜相交的圆角半径
    df5 = pd.DataFrame({
        'd': [10, 18, 30, 50, 80, 120, 180, 250, 315, 400, 500],
        'Ddm': [1.2, 1.6, 1.9, 2.4, 3.2, 4, 4.8, 5.6, 6.4, 7.2, 8],
        'dm': [0.8, 1, 1.2, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],
        'L': [2.8, 3.2, 4, 4.2, 4.8, 6.7, 7.3, 8.8, 9, 11, 14.5],
        'H': [0.6, 0.8, 0.95, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6, 4],
        'dma': [0.8, 1, 1.2, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    })
    if 0 < d <= 10:
        u9 = 10
    elif 10 < d <= 18:
        u9 = 18
    elif 18 < d <= 30:
        u9 = 18
    elif 30 < d <= 50:
        u9 = 50
    elif 50 < d <= 80:
        u9 = 80
    elif 80 < d <= 120:
        u9 = 120
    elif 120 < d <= 180:
        u9 = 180
    elif 180 < d <= 250:
        u9 = 250
    elif 250 < d <= 315:
        u9 = 315
    elif 315 < d <= 400:
        u9 = 400
    elif 400 < d <= 500:
        u9 = 500
    df6 = df5.set_index('d')
    Ddm, dm, L, H, dma = df6.loc[u9]
    # 铆钉尺寸
    rc = Dcp * math.sin(math.radians(90 / Z)) - (Dw / 2 + S) * math.cos(math.asin(S / (0.5 * Dw + S))) - Ddm / 2 - 0.3
    print('rc:', rc)
    if 0.8 <= dm <= 3:
        rmax = 0.2
    elif 3.5 <= dm <= 5:
        rmax = 0.3
    # print('rc',rc)
    if 0 < D <= 30:
        u8 = 30
    elif 30 < D <= 50:
        u8 = 50
    elif 50 < D <= 80:
        u8 = 80
    elif 80 < D <= 120:
        u8 = 120
    elif 120 < D <= 500:
        u8 = 180
    df1 = pd.DataFrame({
        'D': [20, 30, 50, 80, 120, 180],
        'b1': [0.7, 0.7, 0.8, 0.9, 1, 1.2],
        'sh': [0.2, 0.4, 0.5, 0.6, 0.7, 0.8],
        'm1': [0.1, 0.2, 0.2, 0.3, 0.3, 0.5],
        'm2': [0.1, 0.1, 0.2, 0.2, 0.2, 0.2],
        'k': [1, 1, 1, 1.2, 1.4, 1.6],
        'R1': [0.3, 0.3, 0.3, 0.3, 0.4, 0.5],
        'm3': [0.03, 0.08, 0.1, 0.12, 0.14, 0.16],
        'Rm1': [0.15, 0.2, 0.25, 0.25, 0.3, 0.35]
    })
    df2 = df1.set_index('D')
    b1, SH, m1, m2, k, R1, m3, Rm1 = df2.loc[u8]
    print(b1, SH, m1, m2, k, R1, m3, Rm1)
    b = b1 + SH + m1 + m2
    print('b', b)
    D3 = D2 + 2 * m2 + SH + k
    print('D3', D3)
    if 12 < D <= 30:
        D4 = D3 + b1
    elif D > 30:
        D4 = D3 + b1 - 0.1
    print('D4', D4)
    # 密封设计
    # 保持架中心圆直径Dcp及铆钉中心圆直径Dkp的计算
    Dkp = math.sqrt(Ddm * dm)
    print('Dkp:', Dkp)
    # 外圈密封槽尺寸设计
    # 外圈密封槽顶宽上式有
    # 外圈密封槽位置
    b = b1 + SH + m1 + m2
    print('b:', b)
    # 外圈密封槽止口直径
    D3 = D2 + 2 * m2 + SH + k
    print('D3:', D3)
    # 外圈密封槽底直径
    if 12 < D <= 30:
        D4 = D3 + b1
    elif D > 30:
        D4 = D3 + b1 - 0.1
    print('D4:', D4)
    # 外圈密封槽压坡角
    α = 45
    # 密封槽顶圆弧半径R1 上边有
    # 密封圈设计
    # 密封圈外径
    Dm1 = D4 + m3
    print('dm1:', Dm1)
    # 密封圈装配引导直径
    Dm2 = D3 - 0.3
    print('dm2:', Dm2)
    # 密封圈骨架定位直径
    Dm3 = D2 - SH
    print('dm3:', Dm3)
    # 密封圈骨架定位面挂胶直径
    Dm4 = Dm3 - 2 * (SH + m2)
    print('dm4:', Dm4)
    # 密封圈装配减压槽圆弧半径df1
    # Rm1:
    # 密封圈台肩圆弧半径P21
    Rm2 = 0.02
    print('Rm2:', Rm2)
    # 密封圈总厚度
    Bm1 = b1 + SH + m2
    print('Bm1:', Bm1)
    # 密封圈外径唇部厚度
    Bm2 = b1
    print('Bm2:', Bm2)
    # 密封圈外径唇部厚度
    Bm3 = 0.5 * Bm2
    print('Bm3:', Bm3)
    # 密封圈骨架挂胶厚度
    Bm4 = m2
    print('Bm4:', Bm4)
    # 密封圈内径
    if 0 < d <= 9:
        u10 = 9
    elif 9 < d <= 18:
        u10 = 18
    elif 18 < d <= 30:
        u10 = 18
    elif 30 < d <= 50:
        u10 = 50
    elif 50 < d <= 80:
        u10 = 80
    elif 80 < d <= 120:
        u10 = 120
    df8 = pd.DataFrame({
        'd': [9, 18, 30, 50, 80, 120],
        'm4': [0.1, 0.1, 0.2, 0.3, 0.4, 0.5],
        'm5': [0.2, 0.3, 0.1, 0.2, 0.6, 0.7],
        'm6': [1, 1.2, 1.5, 1.8, 2, 2.5],
        'k1': [0.012, 0.01, 0.009, 0.008, 0.007, 0.006],
        'keci1': [0.7, 0.7, 0.9, 1.1, 1.4, 1.7]
    })
    df9 = df8.set_index('d')
    m4, m5, m6, k1, keci1 = df9.loc[u10]
    dm1 = d2 + 0.2 + m4
    print('dm1', dm1)
    # 密封圈内径处唇厚P21
    Bm5 = Bm1
    print('bm5', Bm5)
    dm3 = d2 + 2 / 3 * Bm5 + keci1
    print('dm3', dm3)
    delt = (B / 2 - Bm1 - m1) - math.sqrt((K + S) ** 2 - ((dm3 - Dpw) / 2) ** 2)
    if delt >= 0.3:
        Bm5 = Bm1
    elif delt < 0.3:
        Bm5 = B / 2 - m1 - math.sqrt((K + S) ** 2 - ((dm3 - Dpw) / 2) ** 2) - 0.3
    print('Bm5', Bm5)
    # 密封圈内径处内唇，外唇
    Bm6 = Bm7 = Bm5 / 3
    print('Bm5', Bm5)
    # 密封圈内径处减压槽直径
    dm2 = dm1 + 2 * Bm5 / 3
    print('dm2', dm2)
    # 密封圈内径处润滑脂引导斜坡直径
    dm3 = dm2 + m5
    print('dm3', dm3)
    # 密封圈内径处润滑脂引导斜坡角度
    β = 45
    # 密封圈接触唇内径
    dm4 = d2 / (1 + k1)
    print('dm4', dm4)
    # 密封圈接触唇减压圆弧半径
    Rm3 = (dm2 - dm4) / 8
    print('Rm3', Rm3)
    # k:接触唇压缩量参数
    # 密封圈骨架设计
    # 骨架定位尺寸
    DH = Dm3
    print('DH', DH)
    # 钢骨架钢板厚度
    # 钢骨架总厚度
    # H=2*SH
    # 钢骨架内径尺寸
    dH = dm2 + m6
    print('dH', dH)
    # 保持架弯爪内径
    Dcw = Dc + 0.1
    print('Dcw', Dcw)
    # 保持架弯爪长度
    # L=0.75*Bc+2*S+q1
    # q1:
    # 保持架弯爪根部宽度
    if Dw <= 2.5:
        a1 = 0.1
    elif Dw > 2.5:
        a1 = 0.2
    L1 = C0 - 2 * (Rc + S + rc) - a1
    print('L1', L1)
    # 保持架弯爪圆头半径
    r1 = (C0 - 2 * math.sqrt(K * (2 * Rc + 2 * S - K))) / 3
    print('r1', r1)
    # 保持架弯爪弯曲圆弧半径
    # r3:
    # # 弯爪头部打薄尺寸
    # S2:
    # S1:
    # 装配时弯爪弯曲后不应与外圈相碰
    # εL=D2min85-(Dcmax+2*S+0.1)
    # 计算后的εL必须满足εL>0.2
    # 防尘盖的设计
    # 防尘盖外径尺寸DF
    DF = D3
    print('DF', DF)
    # 防尘盖内径尺寸dF
    dF = d2 + 0.2 + m4
    print('dF', dF)
    # 防尘盖钢板厚SF
    if 10 < D <= 24:
        u99 = 24
    elif 24 < D <= 50:
        u99 = 50
    elif 50 < D <= 80:
        u99 = 80
    elif 80 < D <= 120:
        u99 = 120
    elif 120 < D <= 500:
        u99 = 180
    df11 = pd.DataFrame({
        'd': [24, 50, 80, 120, 180],
        'SF': [0.15, 0.2, 0.3, 0.3, 0.4]
    })
    df12 = df11.set_index('d')
    SF = float(df12.loc[u99])
    print('SF', SF)
    # 防尘盖卷边圆弧半径RF
    RF = 0.75 * b1 - SF
    print('RF', RF)
    # 防尘盖卷边宽度BF
    BF = 2.3 * b1
    print('BF', BF)
    # 防尘盖尺寸BF1
    BF1 = b - SF - m1
    print('BF1', BF1)
    # 防尘盖翻边尺寸BF2
    BF2 = 3.5 * SF
    print('BF2', BF2)
    # 防尘盖尺寸DF1
    DF1 = DF - 4 * (RF + SF)
    print('DF1', DF1)
    # 防尘盖尺寸DF2
    DF2 = D2 - SF
    print('DF2', DF2)
    # 防尘盖尺寸DF3
    DF3 = DF2 - 2 * BF1
    print('DF3', DF3)
    # 防尘盖卷边圆周等分开槽数NF(计算后按奇数圆整)
    NF = 3.14156 * DF / 16
    print('NF', NF)
    # 防尘盖卷边圆周等分开槽宽度hF
    hF = 4 * SF
    print('hF', hF)
    # 防尘盖卷边圆周等分开槽角度
    alfaF = 360 / NF
    print('alfaF', alfaF)
    # 防尘盖卷边圆周等分开槽圆弧半径RF1
    RF1 = hF / 2
    print('RF1', RF1)
    # 标志圆中心直径Dkb1
    Dk = ((DF2 - 2 * BF) + dF) / 2
    print('Dk', Dk)
    # 标志面宽度hw
    hw = (DF3 - dF) / 2
    print('hw', hw)
    # 保持架兜孔中心至其基准端面的距离与S的计算
    SB = 0.5 * Bc
    print('SB', SB)
    print('Ddm', Ddm)
    print('dm', dm)
    return L1, S, Rc, rc, K, Dcw, Dc, Dcp, Dc1, C0, DF2, DF3, BF1, DF1, DF, dF, BF2, SF, RF, alfaF, RF1, BF, Dm1, Dm2, Dm3, Dm4, Bm4, dm1, dm2, dm3, Bm5, Bm6, Bm1, Bm2, Bm3, Rm1, Rm2, DH, dH, SH, Dc1, Dc, dma, Bc, C0, L, H, rmax, Ddm, dm


if __name__ == '__main__':
    a_list = dgbbcaculate(6200, 12, 32, 1, 1.3)
    Dw = 5.953
    Dpw = 22.2
    d = 90
    D = 190
    B = 10
    xinghao = 6000
    dgbb_design(d=d, D=D, B=B, xinghao=xinghao)
