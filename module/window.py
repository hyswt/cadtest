from ui import Ui_window
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from tool import tool
from pyautocad import Autocad, APoint
import os
import fnmatch
from tool import load_accdb, load_roughness, load_chamfer, acbb_caculate, dgbb_caculate
import shutil
import win32com.client

class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # TAG 窗口对象
        self.ui = Ui_window.Ui_MainWindow()
        self.cad = MainPro()
        self.ui.setupUi(self)
        # TAG 控件属性
        self.ui.lineEdit.setReadOnly(True)
        self.show_acbb(False)
        # TAG (菜单)槽函数连接
        self.ui.action1_2.triggered.connect(lambda: self.show_cad_list(self.ui.action1_2.text(), "Data_角接触"))
        self.ui.action3.triggered.connect(lambda: self.show_cad_list(self.ui.action3.text()))
        self.ui.action4.triggered.connect(lambda: self.show_cad_list(self.ui.action4.text()))
        self.ui.action1_3.triggered.connect(lambda: self.show_cad_list(self.ui.menu_2.title()+"/"+self.ui.action1_3.text(), "Data_轻系列"))
        self.ui.action2_2.triggered.connect(lambda: self.show_cad_list(self.ui.menu_2.title()+"/"+self.ui.action2_2.text(), "Data_深沟球"))
        # TAG (列表)槽函数连接
        self.ui.listWidget.doubleClicked.connect(self.select_items)
        # TAG (单行文本)槽函数连接
        self.ui.lineEdit.textChanged.connect(self.filter_cad_list)
        # TAG (按钮)槽函数连接
        self.ui.pushButton.clicked.connect(self.change_text)
        self.ui.pushButton_2.clicked.connect(self.save_dwg)
        # TAG sheetstyle
        self.setStyleSheet(tool.read_qss("./qss/window.qss"))
        # TAG 信号重载
        self.cad.sign_str.connect(self.show_error_msg)
        pass

    def change_accdb_file(self, accdb_name):
        self.cad.accdb_file = accdb_name

    def show_cad_list(self, action_name, accdb_name):
        # INFO lineWidget更新
        """根据菜单名刷新lineWidget列表
        Parameters
        ----------
        action_name : str
            菜单名
        """
        self.change_accdb_file(accdb_name)
        self.action_name = action_name
        if action_name == "角接触球轴承":
            self.show_acbb(True)
        else:
            self.show_acbb(False)
        self.cad_list = fnmatch.filter(os.listdir("./TMB  图纸/"+action_name), "*.dwg")
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(self.cad_list)
        self.ui.lineEdit.setReadOnly(False)
        pass

    def filter_cad_list(self):
        # INFO 刷新轴承列表
        filter_name = self.ui.lineEdit.text()
        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(tool.find_file_name(filter_name, self.cad_list))
        pass

    def select_items(self):
        # INFO 打开对应的CAD文件
        try:
            cad_name = self.ui.listWidget.selectionModel().selectedIndexes()[0].data()
            if "00" in cad_name:
                self.cad.assemble = True
            else:
                self.cad.assemble = False
            # 复制CAD文件到一个临时文件夹
            open_cad_name = "TMB  图纸\\"+self.action_name+"\\"+cad_name
            shutil.copyfile(open_cad_name, f"temp\\{cad_name}")
            open_cad_name = f"temp\\{cad_name}"
            # 启动CAD文件
            os.startfile(open_cad_name)
        except IndexError:
            QMessageBox.warning(self, "警告", "请从列表中选择一个CAD文件")
            pass

    def change_text(self):
        # INFO 修改CAD图上对应内容
        # BUG 当使用线程以后，会报错
        roller_name = self.ui.lineEdit_7.text()
        d = float(self.ui.lineEdit_2.text())
        Dd = float(self.ui.lineEdit_3.text())
        B = float(self.ui.lineEdit_6.text())
        alpha = float(self.ui.lineEdit_5.text())
        precision = self.ui.comboBox.currentText()
        self.cad.change_text(roller_name, d, Dd, B, alpha,  P=precision)
        pass

    def show_error_msg(self, error_msg):
        # INFO 子线程报错窗口
        QMessageBox.critical(self, "警告", error_msg)
        pass

    def save_dwg(self):
        # INFO 保存CAD文件
        cad_file, fit = QFileDialog.getSaveFileName(self, "保存CAD", "./", "CAD(*.dwg)")
        self.cad.save_file(cad_file)
        pass

    def show_acbb(self, show_: bool):
        # INFO 显示隐藏接触角控件
        self.ui.label_6.setVisible(show_)
        self.ui.lineEdit_5.setVisible(show_)
        pass


class MainPro(QObject):

    sign_str = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.acad = Autocad(create_if_not_exists=True)
        self.accdb_file = None
        self.assemble = None
        pass

    def create_mtext(self, text, context):
        """用于创建CAD多行文本 

        Parameters
        ----------
        text : CAD.obj
            CAD中的text对象
        context : str
            多行文字内容
        """
        inser_p = APoint(text.InsertionPoint)  # 多行文字插入点
        width = 10
        mtext = self.acad.model.AddMText(inser_p, width, context)
        mtext.AttachmentPoint = 7
        mtext.InsertionPoint = inser_p
        mtext.LineSpacingFactor = 1  # 设置行间距，输入值在0.24-4之间
        mtext.Height = 3  # 文字高度
        mtext.Rotate(inser_p, text.Rotation)
        pass

    def change_text(self, roller_name: str, d: str, Dd: str, B: str,  alpha: str,  P: str = "P0"):
        # INFO 将CAD标志符替换成所需要的内容
        """将CAD中标志符替换成所需要的内容 

        Parameters
        ----------
        roller_name : str
            轴承名
        d : str
            装配图内径
        Dd : str
            装配图外径
        B : str
            轴承宽度
        P : str
            轴承精度等级, by default "P0"
        """
        # 参考资料：https://zhuanlan.zhihu.com/p/407965654
        # TODO 创建的变量(var)
        # dict_ = {"alpha": "15°", "Bstart": "sspu"}
        acad = win32com.client.Dispatch("AutoCAD.Application")
        doc = acad.ActiveDocument

        # for obj in doc.ModelSpace:
        #     if obj.ObjectName == "AcDbLine":
        #         length = obj.Length
        #         print("Line length: ", length)
        dict_=load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        dict_1=load_roughness.func('Data_角接触',P, "套圈直径", d)
        
        # NOTE 对cad图层进行迭代，获取不同图层的数值，以后进行不同图层的更改
        print(dict_)
        for text in self.acad.iter_objects(['rotated', 'angular']):
          if text.Layer == "Bstart":
                name_=text.TextOverride
                print(dict_.get(name_))
                text.TextOverride=dict_.get(name_,f"{name_}未找到")
                pass

        # "角接触返回值"
        # a_list = dgbb_caculate.dgbb_design(d, Dd, B, roller_name)
        # # a_list =[]*50
        # c_list = acbb_caculate.cacuklateACBB(d, Dd, B, alpha, roller_name, P)
        # print(c_list)
        # De = round(c_list[0], 3)
        # # B = round(c_list[1], 3) 
        # Re = round(c_list[2], 3)
        # ae = round(c_list[3], 3)
        # di = round(c_list[4], 3)
        # Ri = round(c_list[5], 3)
        # ai = round(c_list[6], 3)
        # d2 = round(c_list[7], 3)
        # Dc1 = round(c_list[8], 3)
        # Dcp = round(c_list[9], 3)
        # Bc = round(c_list[10], 3)
        # deltaC = round(c_list[11], 3)
        # D2 = round(c_list[12], 3)
        # dc = round(c_list[13], 3)
        # hc2 = round(c_list[14], 3)
        # Dc2 = round(c_list[15], 3)
        # Dc = round(c_list[16], 3)
        # hc = round(c_list[17], 3)
        # Bc1 = round(c_list[18], 3)
        # Rc = round(c_list[19], 3)
        # Dwc = round(c_list[20], 3)
        # dca = round(c_list[21], 3)
        # S = round(c_list[22], 3)
        # S1 = round(c_list[23], 3)
        # Bc1 = round(c_list[24], 3)
        # CK = round(c_list[25], 3)
        # C1 = round(c_list[26], 3)
        # J = round(c_list[27], 3)
        # Dck = round(c_list[28], 3)
        # "深沟球参数浪形保持架"
        # L1 = round(a_list[0], 3)
        # S = round(a_list[1], 3)
        # Rc = round(a_list[2], 3)
        # rc = round(a_list[3], 3)
        # K = round(a_list[4], 3)
        # Dcw = round(a_list[5], 3)
        # Dc = round(a_list[6], 3)
        # Dcp = round(a_list[7], 3)
        # Dc1 = round(a_list[8], 3)
        # C = round(a_list[9], 3)
        # DF2 = round(a_list[10], 3)
        # DF3 = round(a_list[11], 3)
        # BF1 = round(a_list[12], 3)
        # DF1 = round(a_list[13], 3)
        # DF = round(a_list[14], 3)
        # dF = round(a_list[15], 3)
        # BF2 = round(a_list[16], 3)
        # SF = round(a_list[17], 3)
        # RF = round(a_list[18], 3)
        # alfaF = round(a_list[19], 3)
        # RF1 = round(a_list[20], 3)
        # BF = round(a_list[21], 3)
        # Dm1 = round(a_list[22], 3)
        # Dm2 = round(a_list[23], 3)
        # Dm3 = round(a_list[24], 3)
        # Dm4 = round(a_list[25], 3)
        # Bm4 = round(a_list[26], 3)
        # dm1 = round(a_list[27], 3)
        # dm2 = round(a_list[28], 3)
        # dm3 = round(a_list[29], 3)
        # Bm5 = round(a_list[30], 3)
        # Bm6 = round(a_list[31], 3)
        # Bm1 = round(a_list[32], 3)
        # Bm2 = round(a_list[33], 3)
        # Bm3 = round(a_list[34], 3)
        # Rm1 = round(a_list[35], 3)
        # Rm2 = round(a_list[36], 3)
        # DH = round(a_list[37], 3)
        # dH = round(a_list[38], 3)
        # SH = round(a_list[39], 3)
        # Dc1 = round(a_list[40], 3)
        # Dc = round(a_list[41], 3)
        # dma = round(a_list[42], 3)
        # Bc = round(a_list[43], 3)
        # C = round(a_list[44], 3)
        # L = round(a_list[45], 3)
        # H = round(a_list[46], 3)
        # rmax = round(a_list[47], 3)
        # Ddm = round(a_list[48], 3)
        # dm = round(a_list[49], 3)

        # try:
        # for text in self.acad.iter_objects(['rotated', 'angular']):
        #     if text.Layer == "Bstart":
        #         if 'd' == text.TextString:  # d是需要修改的内容
        #             text.TextString = ""
        #             size = d
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图内圈", "d", d)
        #                 downer = gbt["d_l"]
        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #                 downer = gbt["δDMP"]
        #             context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)

        #         if 'Dd' == text.TextString:  # d是需要修改的内容
        #             text.TextString = ""
                    
        #             size = Dd
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)

        #                 downer = gbt["dd_l"]
        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 downer = gbt["δDMP"]
        #             context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'D' == text.TextString:  # d是需要修改的内容
        #             text.TextString = ""
                    
        #             size = Dd
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)

        #                 downer = gbt["dd_l"]
        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 downer = gbt["δDMP"]
        #             context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'rs_a' == text.TextString:
        #             text.TextString = ""
                    
        #             gbt = load_chamfer.func(self.accdb_file, roller_name, "d", d)
        #             size = gbt["r1smin"]
        #             upper = round(gbt["轴向"]-size, 3)
        #             downer = 0
        #             context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'rs_r' == text.TextString:
        #             text.TextString = ""
                    
        #             gbt = load_chamfer.func(self.accdb_file, roller_name, "d", d)
        #             size = gbt["r1smin"]
        #             upper = round(gbt["径向"]-size,3)
        #             downer = 0
        #             context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'r1s_r' == text.TextString:
                    
        #             text.TextString = ""
        #             gbt = load_chamfer.func(self.accdb_file, roller_name, "d", d)
        #             size = gbt["r1smin"]
        #             upper = round(gbt["径向"]-size,3)
        #             downer = 0
        #             context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZSea' == text.TextString:
        #             text.TextString = ""
                    
        #             #size = ZSea
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)
        #                 ZSea = gbt["zsea"]
        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 ZSea = gbt["zsea"]
        #             ZSea = gbt["zsea"]
        #             context = "{}".format(ZSea)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZVBs' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图内圈", "d", d)
        #                 ZVBs = gbt["zvbs"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #                 ZVBs = gbt["zvbs"]

        #             ZVBs = gbt["zvbs"]
        #             context = "{}".format(ZVBs)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZVCs' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)
        #                 ZVCs = gbt["zvcs"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 ZVCs = gbt["zvcs"]

        #             ZVCs = gbt["zvcs"]
        #             context = "{}".format(ZVCs)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZVDdp' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)
        #                 ZVDdp = gbt["zvddp01"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 ZVDdp = gbt["zvddp01"]

        #             ZVDdp = gbt["zvddp01"]
        #             context = "{}".format(ZVDdp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZVdmp' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图内圈", "d", d)
        #                 ZVdmp = gbt["zvdmp"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #                 ZVdmp = gbt["zvdmp"]

        #             ZVdmp = gbt["zvdmp"]
        #             context = "{}".format(ZVdmp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZKia' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图内圈", "d", d)
        #                 ZKia = gbt["zkia"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #                 ZKia = gbt["zkia"]

        #             ZKia = gbt["zkia"]
        #             context = "{}".format(ZKia)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZSd' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图内圈", "d", d)
        #                 ZSd = gbt["zsd"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #                 ZSd = gbt["zsd"]

        #             ZSd = gbt["zsd"]
        #             context = "{}".format(ZSd)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZSia' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图内圈", "d", d)
        #                 ZSia = gbt["zsia"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #                 ZSia = gbt["zsia"]

        #             ZSia = gbt["zsia"]
        #             context = "{}".format(ZSia)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZVDdmp' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)
        #                 ZVDdmp = gbt["zvddmp"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 ZVDdmp = gbt["zvddmp"]

        #             ZVDdmp = gbt["zvddmp"]
        #             context = "{}".format(ZVDdmp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZKea' == text.TextString:
        #             text.TextString = ""
                    
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)
        #                 ZKea = gbt["zkea"]

        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 ZKea = gbt["zkea"]

        #             ZKea = gbt["zkea"]
        #             context = "{}".format(ZKea)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZSDd' == text.TextString:
        #             text.TextString = ""
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)
        #                 ZSDd = gbt["zsdd"]
        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 ZSDd = gbt["zsdd"]
        #             ZSDd = gbt["zsdd"]
        #             context = "{}".format(ZSDd)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'ZVdp' == text.TextString:
        #             text.TextString = ""
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图内圈", "d", d)
        #                 ZVdp = gbt["zvdp01"]
        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #                 ZVdp = gbt["zvdp01"]
        #             ZVdp = gbt["zvdp01"]
        #             context = "{}".format(ZVdp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'alfa' == text.TextString:
        #             text.TextString = ""
        #             size = Dd
        #             upper = 0
        #             if self.accdb_file:
        #                 gbt = load_accdb.func(self.accdb_file, P, "总图外圈", "d", Dd)

        #                 downer = gbt["dd_l"]
        #             else:
        #                 gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #                 downer = gbt["δDMP"]
        #             context = "{}".format("alfa_")  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'r1s_a' == text.TextString:
        #             text.TextString = ""
                    
        #             gbt = load_chamfer.func(self.accdb_file, roller_name, "d", d)
        #             size = gbt["r1smin"]
        #             upper = round(gbt["轴向"]-size, 3)
        #             downer = 0
        #             context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'VCs' == text.TextString:
        #             text.TextString = ""
                    
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             VCs = gbt["vcs"]
        #             context = "{}".format(VCs)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Se' == text.TextString:
        #             text.TextString = ""
                    
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             Se = gbt["se"]
        #             context = "{}".format(Se)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'VDdp' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             VDdp = gbt["vdp01"]
        #             context = "{}".format(VDdp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'VDdmp' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             VDdmp = gbt["vdmp"]
        #             context = "{}".format(VDdmp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'SDd' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             SDd = gbt["sd"]
        #             context = "{}".format(SDd)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Ke' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             Ke = gbt["ke"]
        #             context = "{}".format(Ke)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Cir_Dd' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             Cir_Dd = gbt["deltacir234"]
        #             context = "{}".format(Cir_Dd)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Cur_Dd' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "外圈", "d", Dd)
        #             Cur_Dd = gbt["deltacur"]
        #             context = "{}".format(Cur_Dd)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if '@ds' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", Dd)
        #             ds = gbt["@ds"]
        #             context = "{}".format(ds)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if '@Ds' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", Dd)
        #             Ds = gbt["@ds"]
        #             context = "{}".format(Ds)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if '@Dds' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", Dd)
        #             Dds = gbt["@dds"]
        #             context = "{}".format(Dds)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if '@Dd2' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", Dd)
        #             dd2 = gbt["@dd2"]
        #             context = "{}".format(dd2)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)

        #         if '@Dde' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", Dd)
        #             Dde = gbt["@dde"]
        #             context = "{}".format(Dde)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if '@Dd' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", Dd)
        #             Dd_1 = gbt["@dd"]  
        #             context = "{}".format(Dd_1)  #
        #             self.create_mtext(text, context)
        #         if 'De' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(De)  #
        #             self.create_mtext(text, context)
        #         if 'Dd2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(D2)  #
        #             self.create_mtext(text, context)
        #         if 'B' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(B)  #
        #             self.create_mtext(text, context)
        #         if 'Re' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Re)  #
        #             self.create_mtext(text, context)
        #         if 'r3' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(5)  #
        #             self.create_mtext(text, context)
        #         if 'ae' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(ae)  #
        #             self.create_mtext(text, context)
        #         if 'Vdp' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             Vdp = gbt["vdp01"]
        #             context = "{}".format(Vdp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Vdmp' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             Vdmp = gbt["vdmp"]
        #             context = "{}".format(Vdmp)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Cur_d' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             Cur_d = gbt["deltacur"]
        #             context = "{}".format(Cur_d)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Cir_d' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             Cir_d = gbt["deltacir234"]
        #             context = "{}".format(Cir_d)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Ki' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             Ki = gbt["ki"]
        #             context = "{}".format(Ki)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'VBs' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             VBs = gbt["vbs"]
        #             context = "{}".format(VBs)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Si' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             Si = gbt["si"]
        #             context = "{}".format(Si)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         if 'Sd' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_accdb.func(self.accdb_file, P, "内圈", "d", d)
        #             Sd = gbt["sd"]
        #             context = "{}".format(Sd)  # 多行文字标注上下差格式
        #             self.create_mtext(text, context)
        #         # if 'd' == text.TextString:  # d是需要修改的内容
        #         #     text.TextString = ""
        #         #     
        #         #     size = d
        #         #     upper = 0
        #         #     if self.accdb_file:
        #         #         gbt=load_accdb.func(self.accdb_file,P,"总图内圈","d",d)
        #         #         downer = gbt["d_l"]
        #         #     else:
        #         #         gbt=load_accdb.func(self.accdb_file,P,"内圈","d",d)
        #         #         downer=gbt["δDMP"]
        #         #     context = "\A1;{}{{\H0.5X;\S{}^{};}}".format(size, upper, downer)  # 多行文字标注上下差格式
        #         #     self.create_mtext(text, context)
        #         if '@di' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", d)
        #             di = gbt["@di"]  
        #             context = "{}".format(di)  #
        #             self.create_mtext(text, context)
        #         if '@d' == text.TextString:
        #             text.TextString = ""
        #             gbt = load_roughness.func(self.accdb_file, P, "套圈直径", d)
        #             d_1 = gbt["@d"]  
        #             context = "{}".format(d_1)  #
        #             self.create_mtext(text, context)
        #         if 'di' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(di)  #
        #             self.create_mtext(text, context)
        #         if 'Ri' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Ri)  #
        #             self.create_mtext(text, context)
        #         if 'ai' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(ai)  #
        #             self.create_mtext(text, context)
        #         if 'd2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(d2)  #
        #             self.create_mtext(text, context)
        #         if 'r8' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(2)  #
        #             self.create_mtext(text, context)
        #         if 'dc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dc)  #
        #             self.create_mtext(text, context)
        #         if 'Dc1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dc1)  #
        #             self.create_mtext(text, context)
        #         if 'hc2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(hc2)  #
        #             self.create_mtext(text, context)
        #         if 'Dc2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dc2)  #
        #             self.create_mtext(text, context)
        #         if 'Dcp' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dcp)  #
        #             self.create_mtext(text, context)
        #         if 'Ddc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dc)  #
        #             self.create_mtext(text, context)
        #         if 'hc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(hc)  #
        #             self.create_mtext(text, context)
        #         if 'Bc1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bc1)  #
        #             self.create_mtext(text, context)
        #         if 'Bc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bc)  #
        #             self.create_mtext(text, context)
        #         if 'Rc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Rc)  #
        #             self.create_mtext(text, context)
        #         if 'Dwc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dwc)  #
        #             self.create_mtext(text, context)
        #         if 'dca' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dca)  #
        #             self.create_mtext(text, context)
        #         if 'S' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(S)  #
        #             self.create_mtext(text, context)
        #         if 'S1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(S1)  #
        #             self.create_mtext(text, context)
        #         if 'Deltac' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(deltaC)  #
        #             self.create_mtext(text, context)
        #         if 'Bca' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bc1)  #
        #             self.create_mtext(text, context)
        #         if 'ck' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(CK)  #
        #             self.create_mtext(text, context)
        #         if 'C1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(C1)  #
        #             self.create_mtext(text, context)
        #         if 'J' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(J)  #
        #             self.create_mtext(text, context)
        #         if 'Dck' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dck)  #
        #             self.create_mtext(text, context)
        #         if 'L1Z' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(L1)  #
        #             self.create_mtext(text, context)
        #         if 'L' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(L)  #
        #             self.create_mtext(text, context)

        #         if 'S' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(S)  #
        #             self.create_mtext(text, context)

        #         if 'Rc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Rc)  #
        #             self.create_mtext(text, context)
        #         if 'rrc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(rc)  #
        #             self.create_mtext(text, context)
        #         if 'K' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(K)  #
        #             self.create_mtext(text, context)
        #         if 'Dcw' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dcw)  #
        #             self.create_mtext(text, context)

        #         if 'Dc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dc)  #
        #             self.create_mtext(text, context)
        #         if 'Dcp' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dcp)  #
        #             self.create_mtext(text, context)
        #         if 'Dc1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Rc)  #
        #             self.create_mtext(text, context)
        #         if 'C' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(C)  #
        #             self.create_mtext(text, context)
        #         if 'DdF2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(DF2)  #
        #             self.create_mtext(text, context)
        #         if 'DdF3' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(DF3)  #
        #             self.create_mtext(text, context)
        #         if 'BF1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(BF1)  #
        #             self.create_mtext(text, context)
        #         if 'DdF1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(DF1)  #
        #             self.create_mtext(text, context)
        #         if 'DdF' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(DF)  #
        #             self.create_mtext(text, context)
        #         if 'dF' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dF)  #
        #             self.create_mtext(text, context)
        #         if 'BF2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(BF2)  #
        #             self.create_mtext(text, context)
        #         if 'SF' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(SF)  #
        #             self.create_mtext(text, context)
        #         if 'RF' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(RF)  #
        #             self.create_mtext(text, context)
        #         if 'alfaF' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(alfaF)  #
        #             self.create_mtext(text, context)
        #         if 'RF1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(RF1)  #
        #             self.create_mtext(text, context)
        #         if 'BF' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(BF)  #
        #             self.create_mtext(text, context)
        #         if 'Ddm1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dm1)  #
        #             self.create_mtext(text, context)
        #         if 'Ddm2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dm2)  #
        #             self.create_mtext(text, context)
        #         if 'Ddm3' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dm3)  #
        #             self.create_mtext(text, context)
        #         if 'Ddm4' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dm4)  #
        #             self.create_mtext(text, context)
        #         if 'Bm4' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bm4)  #
        #             self.create_mtext(text, context)
        #         if 'dm1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dm1)  #
        #             self.create_mtext(text, context)
        #         if 'dm2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dm2)  #
        #             self.create_mtext(text, context)
        #         if 'dm3' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dm3)  #
        #             self.create_mtext(text, context)
        #         if 'Bm4' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bm4)  #
        #             self.create_mtext(text, context)
        #         if 'Bm5' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bm5)  #
        #             self.create_mtext(text, context)
        #         if 'Bm6' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bm6)  #
        #             self.create_mtext(text, context)
        #         if 'Bm1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bm1)  #
        #             self.create_mtext(text, context)
        #         if 'Bm2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bm2)  #
        #             self.create_mtext(text, context)
        #         if 'Bm3' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bm3)  #
        #             self.create_mtext(text, context)
        #         if 'Rm1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Rm1)  #
        #             self.create_mtext(text, context)
        #         if 'Rm2' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Rm2)  #
        #             self.create_mtext(text, context)
        #         if 'DdH' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(DH)  #
        #             self.create_mtext(text, context)
        #         if 'dH' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dH)  #
        #             self.create_mtext(text, context)
        #         if 'SH' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(SH)  #
        #             self.create_mtext(text, context)
        #         if 'DdF1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(DF1)  #
        #             self.create_mtext(text, context)

        #         if 'Dc1' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dc1)  #
        #             self.create_mtext(text, context)
        #         if 'Dc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Dc)  #
        #             self.create_mtext(text, context)
        #         if 'dma' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dma)  #
        #             self.create_mtext(text, context)
        #         if 'Bc' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(Bc)  #
        #             self.create_mtext(text, context)
        #         if 'deltaC' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(deltaC)  #
        #             self.create_mtext(text, context)
        #         if 'L' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(L)  #
        #             self.create_mtext(text, context)
        #         if 'H' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(H)  #
        #             self.create_mtext(text, context)
        #         if 'rmax' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(rmax)  #
        #             self.create_mtext(text, context)
        #         if 'dm' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(dm)  #
        #             self.create_mtext(text, context)
        #         if 'lm' == text.TextString:
        #             text.TextString = ""  
        #             # gbt=load_roughness.func(self.accdb_file,P,"套圈直径",Dd)
        #             # Dd_1=gbt["@dd"]
        #             context = "{}".format(L)  #
        #             self.create_mtext(text, context)

        # except Exception as e:
        #     self.sign_str.emit(str(e))
        pass

    def save_file(self, dwg_loc):
        self.acad.ActiveDocument.SaveAs(dwg_loc)
        pass
