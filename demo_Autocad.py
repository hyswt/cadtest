from pyautocad import Autocad
import win32com.client
from tool import load_accdb, load_roughness, load_chamfer

acad = Autocad(create_if_not_exists=True)
dict_ = load_accdb.func("Data_深沟球", "P6", 7300, "d", 30)


for text in acad.iter_objects_fast(['Text', "MText", 'Aligned', 'Rotated', "Linear"]):
    layer_=text.Layer
    match layer_:
        case "Bstart":
            try:
                name_ = text.TextString
                text.TextString = dict_.get(name_, f"{name_}未找到")
            except:
                pass
        case "d":
            text.TextOverride = "\A1;{}{{\H0.5X;\S{}^{};}}".format(
                dict_['d'], 0, dict_['δdmp'])
        case "dd":
            text.TextOverride = "\A1;{}{{\H0.5X;\S{}^{};}}".format(20, 0, dict_['dmp'])
        case "rs_a":
            upper = round(dict_["轴向"]-dict_['rsmin'], 3)
            downer = 0
            text.TextOverride = "\A1;{}{{\H0.5X;\S{}^{};}}".format(dict_['rs_a'], upper, 0)
        case "rs_r":
            upper = round(dict_["径向"]-dict_['rsmin'], 3)
            downer = 0
            text.TextOverride = "\A1;{}{{\H0.5X;\S{}^{};}}".format(dict_['rs_r'], upper, 0)
        case "r1s_r":
            upper = round(dict_["径向"]-dict_['rsmin'], 3)
            downer = 0
            text.TextOverride = "\A1;{}{{\H0.5X;\S{}^{};}}".format(dict_['r1s_r'], upper, 0)
        case "r3":
            text.TextOverride = "\A1;{}{{\H0.5X;\S{}^{};}}".format(dict_['r3'], dict_['r3_h'], dict_['r3_l'])
        case "r8":
            text.TextOverride = "\A1;{}{{\H0.5X;\S{}^{};}}".format(dict_['r8'], dict_['r8_h'], dict_['r8_l'])

                
        
    


# var = "d_2"
# var_1 = f"D{var}"
# pass
