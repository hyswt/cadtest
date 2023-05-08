import re


# INFO 读取qss文件
def read_qss(file_loc):
    with open(file_loc, 'r', encoding="utf-8") as f:
        return f.read()


# INFO 模糊搜索
def find_file_name(filter_name, filter_list):
    """用于文件的模糊搜索

    Parameters
    ----------
    filter_name : str
        搜索名称
    filter_list : list|tuple
        搜索列表（可迭代对象）

    Returns
    -------
    list|tuple
        返回一个可迭代列表
    """
    sugge = []
    pat = '.*'.join(filter_name)
    regex = re.compile(pat)
    for item in filter_list:
        match = regex.search(item)
        if match:
            sugge.append(item)
    return sugge
