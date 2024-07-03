import codecs
import os
import os.path
import re
import sys
from collections import OrderedDict
from csv import writer, QUOTE_MINIMAL
from filecmp import cmp
from functools import partial, wraps
from getpass import getuser
from hashlib import md5
from locale import getdefaultlocale
from os.path import abspath, dirname, exists, expanduser, getsize, isfile, normpath
from pathlib import Path
from platform import machine, processor, python_version, system, uname
from pprint import pprint
from re import I, IGNORECASE, escape, findall, match
from shutil import copy2
from subprocess import Popen
from time import strftime, time
from traceback import print_exc
from unicodedata import normalize
from uuid import getnode

import yaml
from PIL import Image
from PyQt6.QtCore import QEventLoop, QTimer, QItemSelectionModel, QSize, Qt, pyqtSignal, QTranslator, QPoint
from PyQt6.QtGui import QAction, QActionGroup, QBrush, QDoubleValidator, QFont, QIcon, QImage, \
    QKeySequence, QPainter, QPixmap, QStandardItemModel, QColor, QPen, QStandardItem
from PyQt6.QtWidgets import QAbstractItemView, QApplication, QDockWidget, QFileDialog, QGraphicsSceneMouseEvent, \
    QGraphicsScene, QGraphicsView, QHBoxLayout, QLabel, QLineEdit, QListView, \
    QListWidget, QListWidgetItem, QMainWindow, QMenu, QStatusBar, \
    QTabWidget, QToolBar, QToolButton, QVBoxLayout, QWidget, QFrame, QHeaderView, QPlainTextEdit, QSizePolicy, \
    QTableView, QGraphicsTextItem, QGraphicsEllipseItem, QGraphicsItem, QGraphicsItemGroup, QStyledItemDelegate
from cv2 import COLOR_BGR2RGB, COLOR_BGRA2BGR, COLOR_GRAY2BGR, COLOR_RGB2BGR, cvtColor, imdecode, imencode
from loguru import logger
from matplotlib import colormaps
from natsort import natsorted
from numpy import array, clip, fromfile, ndarray, ones, uint8
from prettytable import PrettyTable
from psutil import virtual_memory
from qtawesome import icon as qicon

python_ver = python_version()


# ================================参数区================================
def a1_const():
    return


# Platforms
SYSTEM = ''
platform_system = system()
platform_uname = uname()
os_kernal = platform_uname.machine
if os_kernal in ['x86_64', 'AMD64']:
    if platform_system == 'Windows':
        SYSTEM = 'WINDOWS'
    elif platform_system == 'Linux':
        SYSTEM = 'LINUX'
    else:  # 'Darwin'
        SYSTEM = 'MAC'
else:  # os_kernal = 'arm64'
    if platform_system == 'Windows':
        SYSTEM = 'WINDOWS'
    elif platform_system == 'Darwin':
        SYSTEM = 'M1'
    else:
        SYSTEM = 'PI'

locale_tup = getdefaultlocale()
lang_code = locale_tup[0]

username = getuser()
homedir = expanduser("~")
homedir = Path(homedir)
DOWNLOADS = homedir / 'Downloads'
DOCUMENTS = homedir / 'Documents'

mac_address = ':'.join(findall('..', '%012x' % getnode()))
node_name = platform_uname.node

current_dir = dirname(abspath(__file__))
current_dir = Path(current_dir)

dirpath = os.getcwd()
ProgramFolder = Path(dirpath)
UserDataFolder = ProgramFolder / 'MomoHanhuaUserData'

python_vs = f"{sys.version_info.major}.{sys.version_info.minor}"

APP_NAME = 'MomoTranslator'
MAJOR_VERSION = 2
MINOR_VERSION = 0
PATCH_VERSION = 0
APP_VERSION = f'v{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}'

APP_AUTHOR = '墨问非名'

if SYSTEM == 'WINDOWS':
    encoding = 'gbk'
    line_feed = '\n'
    cmct = 'ctrl'
else:
    encoding = 'utf-8'
    line_feed = '\n'
    cmct = 'command'

if SYSTEM in ['MAC', 'M1']:

    processor_name = processor()
else:
    processor_name = machine()

if SYSTEM == 'WINDOWS':
    import pytesseract

    # 如果PATH中没有tesseract可执行文件，请指定tesseract路径
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

line_feeds = line_feed * 2

lf = line_feed
lfs = line_feeds

ignores = ('~$', '._')

type_dic = {
    'xlsx': '.xlsx',
    'csv': '.csv',
    'pr': '.prproj',
    'psd': '.psd',
    'tor': '.torrent',
    'xml': '.xml',
    'audio': ('.aif', '.mp3', '.wav', '.flac', '.m4a', '.ogg'),
    'video': ('.mp4', '.mkv', '.avi', '.flv', '.mov', '.wmv'),
    'compressed': ('.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'),
    'font': ('.ttc', '.ttf', '.otf'),
    'comic': ('.cbr', '.cbz', '.rar', '.zip', '.pdf', '.txt'),
    'pic': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'),
    'log': '.log',
    'json': '.json',
    'pickle': '.pkl',
    'python': '.py',
    'txt': '.txt',
    'doc': ('.doc', '.docx'),
    'ppt': ('.ppt', '.pptx'),
    'pdf': '.pdf',
    'html': ('.html', '.htm'),
    'css': '.css',
    'js': '.js',
    'markdown': ('.md', '.markdown'),
    'yml': ('.yml', '.yaml'),
}

ram = str(round(virtual_memory().total / (1024.0 ** 3)))

video_width = 1920
video_height = 1080
video_size = (video_width, video_height)

pylupdate = 'pylupdate6'
lrelease = 'lrelease'

window_title_prefix = f'{APP_NAME} {APP_VERSION}'

py_path = Path(__file__).resolve()

google_max_chars = 5000

pictures_exclude = '加框,分框,框,涂白,填字,修图,-,copy,副本,拷贝,顺序,打码,测试,标注,边缘,标志,伪造'
pic_tuple = tuple(pictures_exclude.split(','))

pre_tuple = (
    'zzz,'
)

scan_tuple = (
    'zSoU-Nerd',
    'zWater',
    'ZZZZZ',
    'zzzDQzzz',
    'zzz DQ zzz',
    'zzz LDK6 zzz',
    'zzz-mephisto',
    'zzz MollK6 zzz',
    'z',
    'zzz empire',
    'zzdelirium_dargh',
    'zzTLK',
    'zzz6 (Darkness-Empire)',
    'zfire',
)

color_blue = (255, 0, 0)
color_green = (0, 255, 0)
color_red = (0, 0, 255)
color_white = (255, 255, 255)
color_black = (0, 0, 0)

color_yellow = (0, 255, 255)  # 黄色
color_cyan = (255, 255, 0)  # 青色
color_magenta = (255, 0, 255)  # 洋红色
color_silver = (192, 192, 192)  # 银色
color_gray = (128, 128, 128)  # 灰色
color_maroon = (0, 0, 128)  # 褐红色
color_olive = (0, 128, 128)  # 橄榄色
color_purple = (128, 0, 128)  # 紫色
color_teal = (128, 128, 0)  # 蓝绿色
color_navy = (128, 0, 0)  # 海军蓝色
color_orange = (0, 165, 255)  # 橙色
color_pink = (203, 192, 255)  # 粉色
color_brown = (42, 42, 165)  # 棕色
color_gold = (0, 215, 255)  # 金色
color_lavender = (250, 230, 230)  # 薰衣草色
color_beige = (220, 245, 245)  # 米色
color_mint_green = (189, 255, 172)  # 薄荷绿
color_turquoise = (208, 224, 64)  # 绿松石色
color_indigo = (130, 0, 75)  # 靛蓝色
color_coral = (80, 127, 255)  # 珊瑚色
color_salmon = (114, 128, 250)  # 鲑鱼色
color_chocolate = (30, 105, 210)  # 巧克力色
color_tomato = (71, 99, 255)  # 番茄色
color_violet = (226, 43, 138)  # 紫罗兰色
color_goldenrod = (32, 165, 218)  # 金菊色
color_fuchsia = (255, 0, 255)  # 紫红色
color_crimson = (60, 20, 220)  # 深红色
color_dark_orchid = (204, 50, 153)  # 暗兰花色
color_slate_blue = (205, 90, 106)  # 石板蓝色
color_medium_sea_green = (113, 179, 60)  # 中等海洋绿色

rgba_white = (255, 255, 255, 255)
rgba_zero = (0, 0, 0, 0)
rgba_black = (0, 0, 0, 255)

index_color = (0, 0, 255, 255)

trans_red = (255, 0, 0, 128)  # 半透明红色
trans_green = (0, 255, 0, 128)  # 半透明绿色
trans_purple = (128, 0, 128, 168)  # 半透明紫色
trans_yellow = (255, 255, 0, 128)  # 半透明黄色
trans_blue = (0, 255, 255, 128)  # 半透明蓝色
trans_olive = (0, 128, 128, 128)  # 半透明橄榄色

red_color = QColor('red')
purple_color = QColor('purple')

mark_px = [0, 0, 0, 1]

pad = 5

punc_table_full = str.maketrans(r'：；，。！？“”‘’（）', r""":;,.!?""''()""")
punc_table_simple = str.maketrans(r'：；，。！？（）', r""":;,.!?()""")

language_tuples = [
    # ================支持的语言================
    ('zh_CN', 'Simplified Chinese', '简体中文', '简体中文'),
    ('zh_TW', 'Traditional Chinese', '繁体中文', '繁體中文'),
    ('en_US', 'English', '英语', 'English'),
    ('ja_JP', 'Japanese', '日语', '日本語'),
    ('ko_KR', 'Korean', '韩语', '한국어'),
    # ================未来支持的语言================
    # ('es_ES', 'Spanish', '西班牙语', 'Español'),
    # ('fr_FR', 'French', '法语', 'Français'),
    # ('de_DE', 'German', '德语', 'Deutsch'),
    # ('it_IT', 'Italian', '意大利语', 'Italiano'),
    # ('pt_PT', 'Portuguese', '葡萄牙语', 'Português'),
    # ('ru_RU', 'Russian', '俄语', 'Русский'),
    # ('ar_AR', 'Arabic', '阿拉伯语', 'العربية'),
    # ('nl_NL', 'Dutch', '荷兰语', 'Nederlands'),
    # ('sv_SE', 'Swedish', '瑞典语', 'Svenska'),
    # ('tr_TR', 'Turkish', '土耳其语', 'Türkçe'),
    # ('pl_PL', 'Polish', '波兰语', 'Polski'),
    # ('he_IL', 'Hebrew', '希伯来语', 'עברית'),
    # ('da_DK', 'Danish', '丹麦语', 'Dansk'),
    # ('fi_FI', 'Finnish', '芬兰语', 'Suomi'),
    # ('no_NO', 'Norwegian', '挪威语', 'Norsk'),
    # ('hu_HU', 'Hungarian', '匈牙利语', 'Magyar'),
    # ('cs_CZ', 'Czech', '捷克语', 'Čeština'),
    # ('ro_RO', 'Romanian', '罗马尼亚语', 'Română'),
    # ('el_GR', 'Greek', '希腊语', 'Ελληνικά'),
    # ('id_ID', 'Indonesian', '印度尼西亚语', 'Bahasa Indonesia'),
    # ('th_TH', 'Thai', '泰语', 'ภาษาไทย'),
]

p_zh_char = re.compile(r'[^\u4e00-\u9fffA-Za-z，。、,\. ]')
p_zh = re.compile(r'[\u4e00-\u9fff]')
p_en = re.compile(r'\b[A-Za-z]+\b')
p_color = re.compile(r'([a-fA-F0-9]{6})-?(\d{0,3})', I)
p_issue_w_dot = re.compile(r'(.+?)(?!\d) (\d{2,5})', I)
p_num_chara = re.compile(r'(\d+)(\D+)')
p_comment = re.compile(r'^(\*|[①-⑨])')
p_lp_coor = re.compile(r'----------------\[(\d+)\]----------------\[(\d+\.\d+),(\d+\.\d+),(\d+)\]', I)

# 使用matplotlib的tab20颜色映射
colormap_tab20 = colormaps['tab20']


# ================================基础函数区================================
def a2_base():
    return


def kernel(size):
    return ones((size, size), uint8)


def kernel_hw(h, w):
    return ones((h, w), uint8)


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        elapsed_time = time() - start_time

        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)

        if hours > 0:
            show_run_time = f"{int(hours)}时{int(minutes)}分{seconds:.2f}秒"
        elif minutes > 0:
            show_run_time = f"{int(minutes)}分{seconds:.2f}秒"
        else:
            show_run_time = f"{seconds:.2f}秒"

        logger.debug(f"{func.__name__} took: {show_run_time}")
        return result

    return wrapper


def is_decimal_or_comma(s):
    pattern = r'^\d*\.?\d*$|^\d*[,]?\d*$'
    return bool(match(pattern, s))


def is_valid_file(file_path, suffixes):
    if not file_path.is_file():
        return False
    if not file_path.stem.startswith(ignores):
        if suffixes:
            return file_path.suffix.lower() in suffixes
        else:
            return True
    return False


def printe(e):
    print(e)
    logger.error(e)
    print_exc()


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def reduce_list(input_list):
    try:
        # 尝试使用dict.fromkeys方法
        output_list = list(OrderedDict.fromkeys(input_list))
    except TypeError:
        # 如果发生TypeError（可能是因为列表包含不可哈希的对象），
        # 则改用更慢的方法
        output_list = []
        for input in input_list:
            if input not in output_list:
                output_list.append(input)
    return output_list


# ================创建目录================
def make_dir(file_path):
    if not exists(file_path):
        try:
            os.makedirs(file_path)
        except BaseException as e:
            print(e)


# ================获取文件夹列表================
def get_dirs(rootdir):
    dirs_list = []
    if rootdir and rootdir.exists():
        # 列出目录下的所有文件和目录
        lines = os.listdir(rootdir)
        for line in lines:
            filepath = Path(rootdir) / line
            if filepath.is_dir():
                dirs_list.append(filepath)
    dirs_list.sort()
    return dirs_list


def get_files(rootdir, file_type=None, direct=False):
    rootdir = Path(rootdir)
    file_paths = []

    # 获取文件类型的后缀
    # 默认为所有文件
    suffixes = type_dic.get(file_type, file_type)
    if isinstance(suffixes, str):
        suffixes = (suffixes,)

    # 如果根目录存在
    if rootdir and rootdir.exists():
        # 只读取当前文件夹下的文件
        if direct:
            files = os.listdir(rootdir)
            for file in files:
                file_path = Path(rootdir) / file
                if is_valid_file(file_path, suffixes):
                    file_paths.append(file_path)
        # 读取所有文件
        else:
            for root, dirs, files in os.walk(rootdir):
                for file in files:
                    file_path = Path(root) / file
                    if is_valid_file(file_path, suffixes):
                        file_paths.append(file_path)

    # 使用natsorted()进行自然排序，
    # 使列表中的字符串按照数字顺序进行排序
    file_paths = natsorted(file_paths)
    return file_paths


def filter_items(old_list, prefix=pre_tuple, infix=scan_tuple, suffix=pic_tuple, item_attr='stem'):
    """
    这个函数用于过滤一个列表，根据指定的前缀、中缀和后缀来排除不需要的元素。
    可以根据文件的全名或者文件名（不包括扩展名）来进行过滤。

    :param old_list: 原始列表。
    :param prefix: 要排除的前缀元组。
    :param infix: 要排除的中间文本元组。
    :param suffix: 要排除的后缀元组。
    :param item_attr: 'name' 或 'stem'，基于文件全名或仅基于文件主名进行过滤。
    :return: 过滤后的新列表，不包含任何匹配前缀、中缀或后缀的元素。
    """

    # 定义一个内部函数来判断一个元素是否应该被排除
    def is_excluded(item):
        # 检查元素是否以任何给定的前缀开始
        for p in prefix:
            if item.startswith(p):
                return True
        # 检查元素的名字是否包含任何给定的中缀
        for i in infix:
            if i == item:
                return True
        # 检查元素是否以任何给定的后缀结束
        for s in suffix:
            if item.endswith(s):
                return True
        # 如果元素不匹配任何排除规则，则不应该排除
        return False

    # 使用列表推导式来过滤原始列表
    # 对于列表中的每一个元素，我们先获取其指定的属性（'name'或'stem'），然后检查是否应该排除
    filtered_list = [item for item in old_list if not is_excluded(getattr(item, item_attr))]

    return filtered_list


@logger.catch
def get_valid_imgs(rootdir, vmode='raw'):
    all_pics = get_files(rootdir, 'pic', True)
    jpgs = [x for x in all_pics if x.suffix.lower() in ('.jpg', '.jpeg')]
    pngs = [x for x in all_pics if x.suffix.lower() == '.png']

    all_masks = [x for x in pngs if '-Mask-' in x.stem]
    all_Whitens = [x for x in pngs if x.stem.endswith('-Whiten')]
    exclude_pngs = all_masks + all_Whitens
    no_masks = [x for x in pngs if '-Mask-' not in x.stem]

    valid_jpgs = filter_items(jpgs)
    valid_pngs = filter_items(no_masks)

    valid_img_list = [x for x in all_pics if x not in exclude_pngs]
    valid_img_list = filter_items(valid_img_list)

    if vmode == 'raw':
        valid_imgs = valid_img_list
    else:
        valid_imgs = all_masks
    return valid_imgs


# ================读取文本================
def read_txt(file_path, encoding='utf-8'):
    """
    读取指定文件路径的文本内容。

    :param file_path: 文件路径
    :param encoding: 文件编码，默认为'utf-8'
    :return: 返回读取到的文件内容，如果文件不存在则返回None
    """
    file_content = None
    if file_path.exists():
        with open(file_path, mode='r', encoding=encoding) as file_object:
            file_content = file_object.read()
    return file_content


# ================写入文件================
def write_txt(file_path, text_input, encoding='utf-8', ignore_empty=True):
    """
    将文本内容写入指定的文件路径。

    :param file_path: 文件路径
    :param text_input: 要写入的文本内容，可以是字符串或字符串列表
    :param encoding: 文件编码，默认为'utf-8'
    :param ignore_empty: 是否忽略空内容，默认为True
    """
    if text_input:
        save_text = True
        if isinstance(text_input, list):
            otext = lf.join(text_input)
        else:
            otext = text_input
        file_content = read_txt(file_path, encoding)
        if file_content == otext or (ignore_empty and otext == ''):
            save_text = False
        if save_text:
            with open(file_path, mode='w', encoding=encoding, errors='ignore') as f:
                f.write(otext)


def generate_md5(img_array):
    img_data = imencode('.png', img_array)[1].tostring()
    file_hash = md5()
    file_hash.update(img_data)
    return file_hash.hexdigest()


# ================对文件算MD5================
def md5_w_size(path, blksize=2 ** 20):
    if isfile(path) and exists(path):  # 判断目标是否文件,及是否存在
        file_size = getsize(path)
        if file_size <= 256 * 1024 * 1024:  # 512MB
            with open(path, 'rb') as f:
                cont = f.read()
            hash_object = md5(cont)
            t_md5 = hash_object.hexdigest()
            return t_md5, file_size
        else:
            m = md5()
            with open(path, 'rb') as f:
                while True:
                    buf = f.read(blksize)
                    if not buf:
                        break
                    m.update(buf)
            t_md5 = m.hexdigest()
            return t_md5, file_size
    else:
        return None


def write_csv(csv_path, data_input, headers=None):
    temp_csv = csv_path.parent / 'temp.csv'

    try:
        if isinstance(data_input, list):
            if len(data_input) >= 1:
                if csv_path.exists():
                    with codecs.open(temp_csv, 'w', 'utf_8_sig') as f:
                        f_csv = writer(f, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL, escapechar='\\')
                        if headers:
                            f_csv.writerow(headers)
                        f_csv.writerows(data_input)
                    if md5_w_size(temp_csv) != md5_w_size(csv_path):
                        copy2(temp_csv, csv_path)
                    if temp_csv.exists():
                        os.remove(temp_csv)
                else:
                    with codecs.open(csv_path, 'w', 'utf_8_sig') as f:
                        f_csv = writer(f, delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL, escapechar='\\')
                        if headers:
                            f_csv.writerow(headers)
                        f_csv.writerows(data_input)
        else:  # DataFrame
            if csv_path.exists():
                data_input.to_csv(temp_csv, encoding='utf-8', index=False)
                if md5_w_size(temp_csv) != md5_w_size(csv_path):
                    copy2(temp_csv, csv_path)
                if temp_csv.exists():
                    os.remove(temp_csv)
            else:
                data_input.to_csv(csv_path, encoding='utf-8', index=False)
    except BaseException as e:
        printe(e)


def conv_img(img, target_format='PIL'):
    """
    将图像转换为指定的格式。

    :param img: 输入图像，可以是 NumPy 数组或 PIL 图像。
    :param target_format: 目标格式，可以是 'PIL' 或 'CV'。
    :return: 转换后的图像。
    """
    if target_format == 'PIL':
        if isinstance(img, ndarray):
            # 转换 NumPy 数组为 PIL 图像
            if len(img.shape) == 2:  # 灰度或黑白图像
                cimg = Image.fromarray(img, 'L')
            else:  # if len(img.shape) == 3:  # 彩色图像
                cimg = Image.fromarray(img, 'RGB')
        else:  # isinstance(img, Image.Image)
            cimg = img
    else:
        # 如果是PIL图像，转换为NumPy数组
        if isinstance(img, Image.Image):
            cimg = array(img)
            # 如果图像有三个维度，并且颜色为三通道，则进行颜色空间的转换
            if cimg.ndim == 3 and cimg.shape[2] == 3:
                cimg = cvtColor(cimg, COLOR_RGB2BGR)
        else:  # isinstance(img, ndarray)
            cimg = img
    return cimg


@logger.catch
def write_pic(pic_path, picimg):
    pic_path = Path(pic_path)
    ext = pic_path.suffix
    temp_pic = pic_path.parent / f'{pic_path.stem}-temp{ext}'

    # 检查输入图像的类型
    if isinstance(picimg, bytes):
        # 如果是字节对象，直接写入文件
        with open(temp_pic, 'wb') as f:
            f.write(picimg)
    else:
        # 如果是PIL图像，转换为NumPy数组
        if isinstance(picimg, Image.Image):
            picimg = array(picimg)

            # 如果图像有三个维度，并且颜色为三通道，则进行颜色空间的转换
            if picimg.ndim == 3 and picimg.shape[2] == 3:
                picimg = cvtColor(picimg, COLOR_RGB2BGR)

        # 检查图像是否为空
        if picimg is None or picimg.size == 0:
            logger.error(f'{pic_path=}')
            # raise ValueError("The input image is empty.")
            return pic_path

        # 保存临时图像
        imencode(ext, picimg)[1].tofile(temp_pic)
    # 检查临时图像和目标图像的md5哈希和大小是否相同
    if not pic_path.exists() or md5_w_size(temp_pic) != md5_w_size(pic_path):
        copy2(temp_pic, pic_path)
    # 删除临时图像
    if temp_pic.exists():
        os.remove(temp_pic)
    return pic_path


# #@logger.catch
def write_docx(docx_path, docu):
    temp_docx = docx_path.parent / 'temp.docx'
    if docx_path.exists():
        docu.save(temp_docx)
        if md5_w_size(temp_docx) != md5_w_size(docx_path):
            copy2(temp_docx, docx_path)
        if temp_docx.exists():
            os.remove(temp_docx)
    else:
        docu.save(docx_path)


def write_yml(yml_path, data):
    temp_yml = yml_path.parent / 'temp.yml'
    if yml_path.exists():
        with open(temp_yml, 'w', encoding='utf-8') as temp_file:
            yaml.dump(data, temp_file, default_flow_style=False, allow_unicode=True)
        if not cmp(temp_yml, yml_path):
            copy2(temp_yml, yml_path)
        if temp_yml.exists():
            os.remove(temp_yml)
    else:
        with open(yml_path, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(data, yaml_file, default_flow_style=False, allow_unicode=True)


def common_prefix(strings):
    """
    返回字符串列表中的共同前缀。

    :param strings: 字符串列表
    :return: 共同前缀
    """
    # pprint(strings)
    if not strings:
        return ""
    common_prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(common_prefix):
            common_prefix = common_prefix[:-1]
            if not common_prefix:
                return ""
    return common_prefix


def common_suffix(strings):
    """
    返回字符串列表中的共同后缀。

    :param strings: 字符串列表
    :return: 共同后缀
    """
    if not strings:
        return ""
    common_suffix = strings[0]
    for s in strings[1:]:
        while not s.endswith(common_suffix):
            common_suffix = common_suffix[1:]
            if not common_suffix:
                return ""
    return common_suffix


# ================================基础图像函数区================================
def a3_pic():
    return


def rect2poly(x, y, w, h):
    # 四个顶点为：左上，左下，右下，右上
    points = [
        (x, y),  # 左上
        (x, y + h),  # 左下
        (x + w, y + h),  # 右下
        (x + w, y),  # 右上
    ]
    return points


def hex2int(hex_num):
    hex_num = f'0x{hex_num}'
    int_num = int(hex_num, 16)
    return int_num


def rgb2str(rgb_tuple):
    r, g, b = rgb_tuple
    color_str = f'{r:02x}{g:02x}{b:02x}'
    return color_str


def toBGR(img_raw):
    # 检查图像的维度（颜色通道数）
    if len(img_raw.shape) == 2:
        # 图像是灰度图（只有一个颜色通道），将其转换为BGR
        img_raw = cvtColor(img_raw, COLOR_GRAY2BGR)
    elif img_raw.shape[2] == 3:
        # 图像已经是BGR格式（有三个颜色通道），不需要转换
        pass
    elif img_raw.shape[2] == 4:
        # 图像是BGRA格式（有四个颜色通道），将其转换为BGR，移除Alpha通道
        img_raw = cvtColor(img_raw, COLOR_BGRA2BGR)
    return img_raw


def pt2tup(point):
    return (int(point.x), int(point.y))


def crop_img(src_img, br, pad=0):
    # 输入参数:
    # src_img: 原始图像(numpy array)
    # br: 裁剪矩形(x, y, w, h)，分别代表左上角坐标(x, y)以及宽度和高度
    # pad: 额外填充，默认值为0

    x, y, w, h = br
    ih, iw = src_img.shape[0:2]

    # 计算裁剪区域的边界坐标，并确保它们不超过图像范围
    y_min = clip(y - pad, 0, ih - 1)
    y_max = clip(y + h + pad, 0, ih - 1)
    x_min = clip(x - pad, 0, iw - 1)
    x_max = clip(x + w + pad, 0, iw - 1)

    # 使用numpy的切片功能对图像进行裁剪
    cropped = src_img[y_min:y_max, x_min:x_max]
    return cropped


# ================================图像函数区================================
def a5_frame():
    return


# ================================qt函数区================================
def a6_pyqt():
    return


def copy2clipboard(text):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)


def iact(text, icon=None, shortcut=None, checkable=False, toggled_func=None, trig=None):
    """创建并返回一个QAction对象"""
    action = QAction(text)
    if icon:  # 检查icon_name是否不为None
        action.setIcon(qicon(icon))
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    if checkable:
        action.setCheckable(True)
    if toggled_func:
        action.toggled.connect(toggled_func)
    if trig:
        action.triggered.connect(trig)
    return action


def ibut(text, icon):
    button = QToolButton()
    button.setIcon(qicon(icon))
    button.setCheckable(True)
    button.setText(text)
    button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
    return button


def get_search_regex(search_text, case_sensitive, whole_word, use_regex):
    """根据搜索条件，返回对应的正则表达式模式对象。"""

    # 如果不区分大小写，设置正则标志为忽略大小写
    flags = IGNORECASE if not case_sensitive else 0

    # 如果不使用正则表达式，对搜索文本进行转义，避免特殊字符影响匹配
    if not use_regex:
        search_text = escape(search_text)

    # 如果选择全词匹配，为搜索文本添加边界匹配符
    if whole_word:
        search_text = fr"\b{search_text}\b"

    # 尝试编译正则表达式，如果失败返回None
    try:
        return re.compile(search_text, flags)
    except re.error:
        return None


# ================================图像函数区================================
def a9_dev():
    return


def open_in_viewer(file_path):
    if sys.platform == 'win32':
        os.startfile(normpath(file_path))
    elif sys.platform == 'darwin':
        Popen(['open', file_path])
    else:
        Popen(['xdg-open', file_path])


def open_in_explorer(file_path):
    folder_path = dirname(file_path)
    if sys.platform == 'win32':
        Popen(f'explorer /select,"{normpath(file_path)}"')
    elif sys.platform == 'darwin':
        Popen(['open', '-R', file_path])
    else:
        Popen(['xdg-open', folder_path])


def open_in_ps(file_path):
    if sys.platform == 'win32':
        photoshop_executable_path = "C:/Program Files/Adobe/Adobe Photoshop CC 2019/Photoshop.exe"  # 请根据您的Photoshop安装路径进行修改
        Popen([photoshop_executable_path, file_path])
    elif sys.platform == 'darwin':
        photoshop_executable_path = "/Applications/Adobe Photoshop 2021/Adobe Photoshop 2021.app"  # 修改此行
        Popen(['open', '-a', photoshop_executable_path, file_path])
    else:
        logger.warning("This feature is not supported on this platform.")


def get_paint_colors(group):
    # 根据group选择颜色
    if group == 1:
        dot_color = QColor('red')
        text_color = QColor('purple')
    elif group == 2:
        dot_color = QColor('blue')
        text_color = QColor('navy')
    else:
        dot_color = QColor('green')
        text_color = QColor('maroon')
    return dot_color, text_color


@logger.catch
def get_formatted_stem(file_stem, format='txt'):
    if format == 'doc':
        formatted_stem = file_stem
    elif format == 'html':
        formatted_stem = f'<p>{file_stem}</p>'
    else:  # format == 'txt':
        formatted_stem = f'>>>>>>>>[{file_stem.name}]<<<<<<<<'
    formatted_stem = normalize('NFC', formatted_stem)
    # logger.debug(f'{formatted_stem=}')
    return formatted_stem


@logger.catch
def create_index_dict(file_stems, full_paragraphs, format='doc'):
    """根据图片文件名（不包括扩展名）和段落列表创建索引字典和索引列表"""
    full_paragraphs_normalized = [normalize('NFC', paragraph) for paragraph in full_paragraphs]
    index_dict = {}
    last_ind = 0
    indexes = []
    for i, file_stem in enumerate(file_stems):
        formatted_stem = get_formatted_stem(file_stem, format)
        if formatted_stem in full_paragraphs[last_ind:]:
            ind = full_paragraphs[last_ind:].index(formatted_stem) + last_ind
            index_dict[formatted_stem] = ind
            indexes.append(ind)
            last_ind = ind
    indexes.append(len(full_paragraphs))
    return index_dict, indexes


@logger.catch
def find_bubbles(text_input):
    bubbles = []
    if isinstance(text_input, str):
        textlines = text_input.splitlines()
    else:
        textlines = text_input
    coor_inds = []
    for t in range(len(textlines)):
        textline = textlines[t]
        m_lp_coor = p_lp_coor.match(textline)
        if m_lp_coor:
            coor_inds.append(t)
    coor_inds.append(len(textlines) - 1)

    for c in range(len(coor_inds) - 1):
        coor_ind = coor_inds[c]
        next_coor_ind = coor_inds[c + 1]
        textline = textlines[coor_ind]
        m_lp_coor = p_lp_coor.match(textline)
        if m_lp_coor:
            bubble_id = int(m_lp_coor.group(1))
            coor_x = float(m_lp_coor.group(2))
            coor_y = float(m_lp_coor.group(3))
            group = int(m_lp_coor.group(4))
            content_lines = textlines[coor_ind + 1:next_coor_ind - 1]
            content = lf.join(content_lines)
            bubble = {
                'id': bubble_id,
                'coor_x': coor_x,
                'coor_y': coor_y,
                'group': group,
                'content': content
            }
            bubbles.append(bubble)
    return bubbles


@timer_decorator
def create_para_dic(file_stems, index_dict, indexes, lines, format='doc'):
    """根据图片文件名、索引字典、索引列表和行列表创建段落字典"""
    pin = 0
    para_dic = {}
    start_inds = []
    # 初始化'head'部分
    if indexes:
        start_ind = 0
        end_ind = indexes[0]
        if end_ind > 0:
            stem_text_list = lines[start_ind:end_ind]
            para_dic['head'] = stem_text_list
    for file_stem in file_stems:
        formatted_stem = get_formatted_stem(file_stem, format)
        if formatted_stem in index_dict:
            start_ind = indexes[pin] + 1
            start_inds.append(start_ind)
            end_ind = indexes[pin + 1]
            pin += 1
            stem_text_list = lines[start_ind:end_ind]
            if format == 'txt':
                rlp_pic_bubbles = find_bubbles(stem_text_list)
                para_dic[formatted_stem] = rlp_pic_bubbles
            else:
                para_dic[formatted_stem] = stem_text_list
    return para_dic


lp_head = """
1,0
-
框内
框外
-
Default Comment
You can edit me
"""


@logger.catch
def read_rlp(rlp_txt, img_list):
    if rlp_txt.exists():
        rlp_text = read_txt(rlp_txt, encoding='utf-8-sig')
        rlp_lines = rlp_text.splitlines()
        rlp_index_dict, rlp_inds = create_index_dict(img_list, rlp_lines, 'txt')
        rlp_para_dic = create_para_dic(img_list, rlp_index_dict, rlp_inds, rlp_lines, 'txt')
    else:
        rlp_para_dic = {}
        head = lp_head.strip().splitlines()
        head += ['', '']
        rlp_para_dic['head'] = head
        for i in range(len(img_list)):
            img_file = img_list[i]
            formatted_stem = get_formatted_stem(img_file)
            rlp_para_dic[formatted_stem] = []
    return rlp_para_dic


@logger.catch
def save_rlp(rlp_txt, rlp_para_dic, img_list):
    rlp_lines = []
    rlp_lines += rlp_para_dic['head']
    for i in range(len(img_list)):
        img_file = img_list[i]
        formatted_stem = get_formatted_stem(img_file)
        rlp_lines.append(formatted_stem)
        rlp_pic_bubbles = rlp_para_dic.get(formatted_stem, [])
        for r in range(len(rlp_pic_bubbles)):
            # ================针对每一个气泡================
            rlp_pic_bubble = rlp_pic_bubbles[r]
            id = rlp_pic_bubble['id']
            coor_x = rlp_pic_bubble['coor_x']
            coor_y = rlp_pic_bubble['coor_y']
            group = rlp_pic_bubble['group']
            content = rlp_pic_bubble['content']
            meta_line = f'----------------[{id}]----------------[{coor_x:.3f},{coor_y:.3f},{group}]'
            rlp_lines.append(meta_line)
            rlp_lines.extend(content.splitlines())
            rlp_lines.append('')
        rlp_lines.append('')
    rlp_text = lf.join(rlp_lines)
    write_txt(rlp_txt, rlp_text)


class SearchLine(QLineEdit):
    def __init__(self, parent=None):
        super(SearchLine, self).__init__(parent)

        self.type = self.__class__.__name__
        self.parent_window = parent
        # 区分大小写按钮
        self.case_sensitive_button = ibut(self.tr('Case Sensitive'), 'msc.case-sensitive')
        # 全词匹配按钮
        self.whole_word_button = ibut(self.tr('Whole Word'), 'msc.whole-word')
        # 正则表达式按钮
        self.regex_button = ibut(self.tr('Use Regex'), 'mdi.regex')

        # 创建水平布局，用于将三个按钮放在一行
        self.hb_search_bar = QHBoxLayout()
        self.hb_search_bar.setContentsMargins(0, 0, 0, 0)
        self.hb_search_bar.setSpacing(2)
        self.hb_search_bar.addStretch()
        self.hb_search_bar.addWidget(self.case_sensitive_button)
        self.hb_search_bar.addWidget(self.whole_word_button)
        self.hb_search_bar.addWidget(self.regex_button)

        self.case_sensitive_button.clicked.connect(lambda: self.parent_window.filter_imgs(self.text()))
        self.whole_word_button.clicked.connect(lambda: self.parent_window.filter_imgs(self.text()))
        self.regex_button.clicked.connect(lambda: self.parent_window.filter_imgs(self.text()))
        self.textChanged.connect(self.parent_window.filter_imgs)

        # 设置占位符文本
        self.setPlaceholderText(self.tr('Search'))
        # 将按钮添加到 QLineEdit 的右侧
        self.setLayout(self.hb_search_bar)


class CustImageList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.type = self.__class__.__name__
        self.parent_window = parent
        self.display_mode = 0
        self.font = QFont()
        self.font.setWordSpacing(0)
        # 设置图标模式
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(thumb_size, thumb_size))  # 设置图标大小
        self.setResizeMode(QListView.ResizeMode.Adjust)  # 设置自动调整大小
        self.setSpacing(5)  # 设置间距
        self.setWordWrap(True)  # 开启单词换行
        self.setWrapping(False)  # 关闭自动换行
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # 设置单选模式
        self.setFlow(QListView.Flow.TopToBottom)  # 设置从上到下排列
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # 设置自定义右键菜单
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.itemSelectionChanged.connect(self.on_img_selected)
        self.load_img_list()

    def load_img_list(self):
        # 加载图片列表
        self.clear()
        for i in range(len(self.parent_window.img_list)):
            img = self.parent_window.img_list[i]
            pixmap = QPixmap(str(img)).scaled(thumb_size, thumb_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            item = QListWidgetItem(QIcon(pixmap), img.name)
            item.setFont(self.font)
            item.setData(Qt.ItemDataRole.UserRole, img)
            item.setTextAlignment(Qt.AlignBottom | Qt.AlignHCenter)
            self.addItem(item)

    def on_img_selected(self):
        # 通过键鼠点击获取的数据是真实序数img_ind
        selected_items = self.selectedItems()
        if selected_items:
            current_item = selected_items[0]
            img_ind = self.row(current_item)
            if img_ind != self.parent_window.img_ind:
                img_file = current_item.data(Qt.ItemDataRole.UserRole)
                self.parent_window.open_img_by_path(img_file)

    def set_display_mode(self, display_mode):
        self.display_mode = display_mode
        self.setUpdatesEnabled(False)
        for index in range(self.count()):
            item = self.item(index)
            data = item.data(Qt.ItemDataRole.UserRole)
            if self.display_mode == 0:  # 仅显示缩略图
                item.setIcon(QIcon(data.as_posix()))
                item.setText('')
                self.setWordWrap(False)
            elif self.display_mode == 1:  # 仅显示文件名
                item.setIcon(QIcon())  # 清除图标
                item.setText(data.name)
                self.setWordWrap(False)  # 确保文件名不换行
            elif self.display_mode == 2:  # 同时显示缩略图和文件名
                item.setIcon(QIcon(data.as_posix()))
                item.setText(data.name)
                self.setWordWrap(True)

        self.setIconSize(QSize(thumb_size, thumb_size))  # 设置图标大小
        if self.display_mode == 1:  # 仅显示文件名
            self.setGridSize(QSize(-1, -1))  # 使用默认大小的网格
        else:
            # 为缩略图和两种模式设置网格大小
            # 为文件名和间距增加额外的宽度
            self.setGridSize(QSize(thumb_size + 30, -1))

        self.setUpdatesEnabled(True)

    def show_context_menu(self, point):
        item = self.itemAt(point)
        if item:
            context_menu = QMenu(self)
            # 创建并添加菜单项
            open_file_action = QAction(self.tr('Open in Explorer'), self)
            open_img_action = QAction(self.tr('Open in Preview'), self)
            open_with_ps = QAction(self.tr('Photoshop'), self)
            # 添加拷贝图片路径、拷贝图片名的选项
            copy_img_path = QAction(self.tr('Copy Image Path'), self)
            copy_img_name = QAction(self.tr('Copy Image Name'), self)

            context_menu.addAction(open_file_action)
            context_menu.addAction(open_img_action)
            # 添加一个打开方式子菜单
            open_with_menu = context_menu.addMenu(self.tr('Open with'))
            open_with_menu.addAction(open_with_ps)
            context_menu.addAction(copy_img_path)
            context_menu.addAction(copy_img_name)

            open_file_action.triggered.connect(lambda: open_in_explorer(item.data(Qt.ItemDataRole.UserRole)))
            open_img_action.triggered.connect(lambda: open_in_viewer(item.data(Qt.ItemDataRole.UserRole)))
            open_with_ps.triggered.connect(lambda: open_in_ps(item.data(Qt.ItemDataRole.UserRole)))
            copy_img_path.triggered.connect(lambda: copy2clipboard(item.data(Qt.ItemDataRole.UserRole).as_posix()))
            copy_img_name.triggered.connect(lambda: copy2clipboard(item.text()))

            context_menu.exec(self.mapToGlobal(point))


class CustGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type = self.__class__.__name__
        self.parent = parent
        self.img_file = None

    def load_qimg(self, img_data, img_file=None):
        self.img_file = img_file
        # 如果输入是Pillow图像，将其转换为NumPy数组
        if isinstance(img_data, Image.Image):
            img_data = array(img_data)

        # 确保输入数据是NumPy数组
        if isinstance(img_data, ndarray):
            # 检查图像是否是灰度图
            if len(img_data.shape) == 2:  # 灰度图，只有高度和宽度
                height, width = img_data.shape
                bytes_per_line = width  # 灰度图像的每行字节数
                qimg_format = QImage.Format_Grayscale8  # 灰度图像格式
                # 将NumPy数组转换为QImage
                qimage = QImage(img_data.data, width, height, bytes_per_line, qimg_format)
            else:  # 彩色图像
                height, width, channel = img_data.shape
                bytes_per_line = channel * width
                if channel == 4:
                    # 如果输入图像有4个通道（带有Alpha通道）
                    qimg_format = QImage.Format_ARGB32
                elif channel == 3:
                    # 如果输入图像有3个通道
                    # 如果输入图像使用BGR顺序，交换颜色通道以获得正确的RGB顺序
                    img_data = cvtColor(img_data, COLOR_BGR2RGB)
                    qimg_format = QImage.Format_RGB888
                # 将NumPy数组转换为QImage
                qimage = QImage(img_data.data, width, height, bytes_per_line, qimg_format)
            # 将QImage转换为QPixmap
            pixmap = QPixmap.fromImage(qimage)
            # ================清除之前的图像================
            self.clear()
            # ================显示新图片================
            self.addPixmap(pixmap)
            # 将视图大小设置为 pixmap 的大小，并将图像放入视图中
            self.setSceneRect(pixmap.rect().toRectF())

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            x = int(event.scenePos().x())
            y = int(event.scenePos().y())
            self.parent.on_create(x, y)
        super().mousePressEvent(event)


class CustGraphicsView(QGraphicsView):
    zoomChanged = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.type = self.__class__.__name__
        self.parent_window = parent
        # 默认缩放级别，表示原始大小
        self.zoom_level = scaling_factor_reci
        self.start_pt = None
        self.selected_contours = []
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setInteractive(True)
        self.setMouseTracking(True)
        # 设置渲染、优化和视口更新模式
        # 设置渲染抗锯齿
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        # 设置优化标志以便不为抗锯齿调整
        self.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing, True)
        # 设置优化标志以便不保存画家状态
        self.setOptimizationFlag(QGraphicsView.OptimizationFlag.DontSavePainterState, True)
        # 设置视口更新模式为完整视口更新
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        # 设置渲染提示为平滑图像变换，以提高图像的显示质量
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setBackgroundBrush(QBrush(Qt.GlobalColor.lightGray))

    def cust_zoom(self, factor):
        self.scale(factor, factor)
        self.zoom_level *= factor
        # 在主窗口中更新缩放输入
        self.parent_window.update_zoom_label()
        self.zoomChanged.emit(self.zoom_level)

    def cust_zoom_in(self):
        self.cust_zoom(1.25)

    def cust_zoom_out(self):
        self.cust_zoom(0.8)

    def fit2view(self, fmode):
        rect = self.scene().itemsBoundingRect()
        view_rect = self.viewport().rect()
        scale_factor_x = view_rect.width() / rect.width()
        scale_factor_y = view_rect.height() / rect.height()
        if fmode == 'width':
            scale_factor = scale_factor_x
        elif fmode == 'height':
            scale_factor = scale_factor_y
        elif fmode == 'screen':
            scale_factor = min(scale_factor_x, scale_factor_y)
        elif fmode == 'original':
            scale_factor = scaling_factor_reci
        self.zoom_level = scale_factor
        self.resetTransform()
        self.scale(scale_factor, scale_factor)
        self.zoomChanged.emit(self.zoom_level)


class ColorTextItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        # 设置画笔颜色基于单元格内容
        text = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if text == "G1框内":
            painter.setPen(QPen(QColor("red")))
        elif text == "G2框外":
            painter.setPen(QPen(QColor("blue")))
        else:
            painter.setPen(QPen(QColor("black")))  # 默认颜色

        # 绘制文本
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)


class CustTableView(QTableView):
    def __init__(self, parent=None):
        super(CustTableView, self).__init__(parent)
        self.parent = parent

        self.setItemDelegateForColumn(2, ColorTextItemDelegate(self))  # 假设你想在第三列应用颜色
        # 设置表格为不可编辑状态
        self.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # 设置选择模式和选择行为
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        # 表格宽度的自适应调整
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.horizontalHeader().setStretchLastSection(True)

        # 自定义右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

        # self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改

        # 水平方向，表格大小拓展到适当的尺寸
        self.setSelectionMode(QAbstractItemView.SingleSelection)  # 单选
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # 单元格选择
        self.setFrameShape(QFrame.NoFrame)  # 设置无表格的外框

        self.setStyleSheet("""
        QTableView {
            selection-background-color: lightblue;
            selection-color: black;
        }
        """)

    def onContextMenu(self, point: QPoint):
        contextMenu = QMenu(self)
        contextMenu.addAction(self.parent.group1Action)
        contextMenu.addAction(self.parent.group2Action)
        contextMenu.addAction(self.parent.deleteAction)
        contextMenu.exec(self.mapToGlobal(point))


class DraggableGroup(QGraphicsItemGroup):
    def __init__(self, x, y, id, group, parent=None):
        super().__init__()
        # 创建椭圆
        self.id = int(id)
        self.group = int(group)
        diameter = 20
        dot_color, text_color = get_paint_colors(group)
        self.ellipse = QGraphicsEllipseItem(x - diameter / 2, y - diameter / 2, diameter, diameter, self)
        self.ellipse.setBrush(QBrush(dot_color))
        self.ellipse.setPen(QPen(Qt.NoPen))

        # 创建文本
        self.text_item = QGraphicsTextItem(str(self.id), self)
        self.text_item.setDefaultTextColor(text_color)
        self.text_item.setFont(QFont('Arial', 100, QFont.Weight.Normal))
        self.text_item.setPos(x, y)  # 相对于组的位置

        # 设置组的拖动属性
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)
        # 连接父窗口
        self.parent = parent

    def change_id(self, id):
        self.id = id
        self.text_item.setPlainText(str(self.id))

    def change_group(self, group):
        self.group = group
        dot_color, text_color = get_paint_colors(group)
        self.ellipse.setBrush(QBrush(dot_color))
        self.text_item.setDefaultTextColor(text_color)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            # 获取椭圆在场景中的新位置
            new_scene_pos = self.ellipse.mapToScene(self.ellipse.rect().center())
            new_x = int(new_scene_pos.x())
            new_y = int(new_scene_pos.y())
            # 更新表格坐标
            # logger.debug(f'{new_x},{new_y}')
            self.parent.update_coordinates(self, new_x, new_y)
        return super().itemChange(change, value)


class CustTableModel(QStandardItemModel):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns, parent)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            text = super().data(index, role)
            if text is not None:
                return text.replace('\n', ' ')  # 将换行替换为空格用于显示
        return super().data(index, role)

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            # 存储原始多行文本
            return super().setData(index, value, role)
        return False

    def addData(self, row, column, value):
        item = QStandardItem(value)
        self.setItem(row, column, item)


class LabelPlusWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.type = self.__class__.__name__
        self.a0_para()
        self.a1_initialize()
        self.a2_status_bar()
        self.a3_docks()
        self.a4_actions()
        self.a5_menubar()
        self.a6_toolbar()
        self.a9_setting()

    def b1_window(self):
        return

    def a0_para(self):
        # ================初始化变量================
        self.screen_icon = qicon('ei.screen')
        self.setWindowIcon(self.screen_icon)
        self.cgs = CustGraphicsScene(self)
        self.cgv = CustGraphicsView(self)
        self.cgv.setScene(self.cgs)
        self.cgv.zoomChanged.connect(self.update_zoom_label)
        self.resize(window_w, window_h)

    def a1_initialize(self):
        # ================图片列表================
        self.img_folder = img_folder
        self.auto_subdir = Auto / self.img_folder.name
        make_dir(self.auto_subdir)
        self.img_list = get_valid_imgs(self.img_folder)
        self.rlp_txt = self.img_folder.parent / f'{self.img_folder.name}翻译_0.txt'
        self.rlp_para_dic = read_rlp(self.rlp_txt, self.img_list)
        self.filter_img_list = self.img_list
        self.img_ind = clamp(img_ind, 0, len(self.img_list) - 1)
        self.bubble_ellipses = []
        if self.img_ind < len(self.img_list):
            self.img_file = self.img_list[self.img_ind]
            self.setWindowTitle(self.img_file.name)
        else:
            self.img_file = None

    def a2_status_bar(self):
        # ================状态栏================
        self.status_bar = QStatusBar()
        # 设置状态栏，类似布局设置
        self.setStatusBar(self.status_bar)

    def a3_docks(self):
        self.nav_tab = QTabWidget(self)
        self.cil = CustImageList(self)
        self.nav_tab.addTab(self.cil, self.tr('Thumbnails'))

        self.search_line = SearchLine(self)

        # 构建Model/View
        table_header = [self.tr('ID'), self.tr('Content'), self.tr('Group'), self.tr('Coordinates'), ]
        self.plus_tv_im = CustTableModel(10, 4, self)  # 数据模型,10行4列
        self.plus_tv_im.setHorizontalHeaderLabels(table_header)
        self.plus_tv_sm = QItemSelectionModel(self.plus_tv_im)  # Item选择模型
        self.plus_tv_sm.selectionChanged.connect(self.update_plus_pte)

        # 设置表格属性
        self.plus_tv = CustTableView(self)
        self.plus_tv.setModel(self.plus_tv_im)  # 设置数据模型
        self.plus_tv.setSelectionModel(self.plus_tv_sm)  # 设置选择模型
        if hide_extra:
            self.plus_tv.setColumnHidden(0, True)  # ID
            self.plus_tv.setColumnHidden(2, True)  # 组别
            self.plus_tv.setColumnHidden(3, True)  # 坐标

        self.plus_pte = QPlainTextEdit()
        self.plus_pte.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.plus_pte.setObjectName("plainTextEdit")
        self.plus_pte.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.plus_pte.textChanged.connect(self.on_text_changed)

        self.pics_widget = QWidget()
        self.vb_search_nav = QVBoxLayout(self)
        self.vb_search_nav.addWidget(self.search_line)
        self.vb_search_nav.addWidget(self.nav_tab)
        self.pics_widget.setLayout(self.vb_search_nav)

        self.lp_widget = QWidget()
        self.lp_vb = QVBoxLayout(self)
        self.lp_vb.addWidget(self.plus_tv)
        self.lp_vb.addWidget(self.plus_pte)
        self.lp_widget.setLayout(self.lp_vb)

        self.pics_dock = QDockWidget(self.tr('Image List'), self)
        self.pics_dock.setObjectName("PicsDock")
        self.pics_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.pics_dock.setWidget(self.pics_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.pics_dock)

        self.lp_dock = QDockWidget(self.tr('LabelPlus'), self)
        self.lp_dock.setObjectName("LabelplusDock")
        self.lp_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.lp_dock.setWidget(self.lp_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.lp_dock)

    def a4_actions(self):
        self.le_scale_percent = QLineEdit(self)
        self.le_scale_percent.setFixedWidth(50)
        self.le_scale_percent.setValidator(QDoubleValidator(1, 1000, 2))

        self.open_folder_action = iact(self.tr('Open Folder'), 'ei.folder', QKeySequence.StandardKey.Open,
                                       trig=self.open_folder_by_dialog)
        self.zoom_in_action = iact(self.tr('Zoom In'), 'ei.zoom-in', QKeySequence.StandardKey.ZoomIn,
                                   trig=self.cgv.cust_zoom_in)
        self.zoom_out_action = iact(self.tr('Zoom Out'), 'ei.zoom-out', QKeySequence.StandardKey.ZoomOut,
                                    trig=self.cgv.cust_zoom_out)
        self.fit2screen_action = iact(self.tr('Fit to Screen'), 'mdi6.fit-to-screen-outline', "Alt+F",
                                      trig=lambda: self.cgv.fit2view("screen"))
        self.fit2width_action = iact(self.tr('Fit to Width'), 'ei.resize-horizontal', "Alt+W",
                                     trig=lambda: self.cgv.fit2view("width"))
        self.fit2height_action = iact(self.tr('Fit to Height'), 'ei.resize-vertical', "Alt+H",
                                      trig=lambda: self.cgv.fit2view("height"))
        self.reset_zoom_action = iact(self.tr('Reset Zoom'), 'mdi6.backup-restore', "Ctrl+0",
                                      trig=lambda: self.cgv.fit2view("original"))
        self.prev_img_action = iact(self.tr('Previous Image'), 'ei.arrow-left', "Ctrl+Left",
                                    trig=lambda: self.nav_img(-1))
        self.next_img_action = iact(self.tr('Next Image'), 'ei.arrow-right', "Ctrl+Right",
                                    trig=lambda: self.nav_img(1))
        self.first_img_action = iact(self.tr('First Image'), 'ei.step-backward', "Ctrl+Home",
                                     trig=lambda: self.nav_img("first"))
        self.last_img_action = iact(self.tr('Last Image'), 'ei.step-forward', "Ctrl+End",
                                    trig=lambda: self.nav_img("last"))

        self.deleteAction = iact(self.tr('Delete'), 'ri.delete-bin-7-line', QKeySequence.StandardKey.Delete,
                                 trig=self.on_delete)
        self.group1Action = iact(self.tr('Inside'), 'ph.number-circle-one-fill', "Ctrl+1",
                                 trig=partial(self.on_group, 1))
        self.group2Action = iact(self.tr('Outside'), 'ph.number-circle-two-fill', "Ctrl+2",
                                 trig=partial(self.on_group, 2))
        self.up_action = iact(self.tr('Up'), 'ei.chevron-up', "Ctrl+Up", trig=partial(self.on_move, -1))
        self.down_action = iact(self.tr('Down'), 'ei.chevron-down', "Ctrl+Down", trig=partial(self.on_move, 1))
        self.top_action = iact(self.tr('Top'), 'mdi.arrow-collapse-up', "Alt+Up", trig=partial(self.on_move, '1'))
        self.bottom_action = iact(self.tr('Bottom'), 'mdi.arrow-collapse-down', "Alt+Down",
                                  trig=partial(self.on_move, '-1'))
        self.undo_action = iact(self.tr('Undo'), 'fa5s.undo', QKeySequence.StandardKey.Undo, trig=self.undo)
        self.redo_action = iact(self.tr('Redo'), 'fa5s.redo', QKeySequence.StandardKey.Redo, trig=self.redo)
        self.save_action = iact(self.tr('Save'), 'msc.save', QKeySequence.StandardKey.Save, trig=self.save2lp)

        self.undo_action.setEnabled(False)
        self.redo_action.setEnabled(False)

        self.le_scale_percent.editingFinished.connect(self.scale_by_percent)
        self.update_zoom_label()

    def a5_menubar(self):
        # 文件菜单
        self.file_menu = self.menuBar().addMenu(self.tr('File'))
        self.file_menu.addAction(self.open_folder_action)

        # 显示菜单
        self.view_menu = self.menuBar().addMenu(self.tr('View'))
        # 视图菜单选项
        self.view_menu.addAction(self.pics_dock.toggleViewAction())
        self.view_menu.addSeparator()
        # 缩放选项
        self.view_menu.addAction(self.zoom_in_action)
        self.view_menu.addAction(self.zoom_out_action)
        self.view_menu.addAction(self.fit2screen_action)
        self.view_menu.addAction(self.fit2width_action)
        self.view_menu.addAction(self.fit2height_action)
        self.view_menu.addAction(self.reset_zoom_action)
        self.view_menu.addSeparator()

        # 显示选项
        self.display_modes = [(self.tr('Show Thumbnails'), 0),
                              (self.tr('Show Filenames'), 1),
                              (self.tr('Show Both'), 2)]
        self.display_mode_group = QActionGroup(self)
        for display_mode in self.display_modes:
            action = QAction(display_mode[0], self, checkable=True)
            action.triggered.connect(lambda _, dmode=display_mode[1]: self.cil.set_display_mode(dmode))
            self.view_menu.addAction(action)
            self.display_mode_group.addAction(action)

        # 默认选中 Show Both 选项
        self.display_mode_group.actions()[2].setChecked(True)

        # 导航菜单
        self.nav_menu = self.menuBar().addMenu(self.tr('Navigate'))
        self.nav_menu.addAction(self.prev_img_action)
        self.nav_menu.addAction(self.next_img_action)
        self.nav_menu.addAction(self.first_img_action)
        self.nav_menu.addAction(self.last_img_action)

        # 编辑菜单
        self.edit_menu = self.menuBar().addMenu(self.tr('Edit'))
        self.edit_menu.addAction(self.deleteAction)
        self.edit_menu.addAction(self.group1Action)
        self.edit_menu.addAction(self.group2Action)
        self.edit_menu.addAction(self.up_action)
        self.edit_menu.addAction(self.down_action)
        self.edit_menu.addAction(self.top_action)
        self.edit_menu.addAction(self.bottom_action)
        self.edit_menu.addAction(self.undo_action)
        self.edit_menu.addAction(self.redo_action)

    def a6_toolbar(self):
        self.tool_bar = QToolBar(self)
        self.tool_bar.setObjectName("Toolbar")
        self.tool_bar.setIconSize(QSize(24, 24))
        self.tool_bar.setMovable(False)
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.addToolBar(self.tool_bar)
        self.tool_bar.addAction(self.open_folder_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.zoom_in_action)
        self.tool_bar.addAction(self.zoom_out_action)
        self.tool_bar.addAction(self.fit2screen_action)
        self.tool_bar.addAction(self.fit2width_action)
        self.tool_bar.addAction(self.fit2height_action)
        self.tool_bar.addAction(self.reset_zoom_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.first_img_action)
        self.tool_bar.addAction(self.prev_img_action)
        self.tool_bar.addAction(self.next_img_action)
        self.tool_bar.addAction(self.last_img_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.deleteAction)
        self.tool_bar.addAction(self.group1Action)
        self.tool_bar.addAction(self.group2Action)
        self.tool_bar.addAction(self.up_action)
        self.tool_bar.addAction(self.down_action)
        self.tool_bar.addAction(self.top_action)
        self.tool_bar.addAction(self.bottom_action)
        self.tool_bar.addAction(self.undo_action)
        self.tool_bar.addAction(self.redo_action)
        self.tool_bar.addAction(self.save_action)
        self.tool_bar.addSeparator()
        self.tool_bar.addWidget(self.le_scale_percent)
        self.tool_bar.addWidget(QLabel('%'))

    def a9_setting(self):
        self.open_img_by_path(self.img_file)
        self.setCentralWidget(self.cgv)
        self.show()

    def loop_time(self, leng):
        loop = QEventLoop()
        QTimer.singleShot(leng, loop.quit)
        loop.exec_()

    def open_img_by_path(self, img_file):
        if img_file is not None:
            img_file = Path(img_file)
            if img_file.exists() and img_file != self.cgs.img_file:
                self.img_file = img_file
                self.formatted_stem = get_formatted_stem(self.img_file)
                self.img_file_size = getsize(self.img_file)
                self.img_ind = self.img_list.index(self.img_file)
                self.setWindowTitle(self.img_file.name)
                # ================显示图片================
                self.img_raw = imdecode(fromfile(self.img_file, dtype=uint8), -1)
                self.ih, self.iw = self.img_raw.shape[0:2]
                self.cgs.load_qimg(self.img_raw, self.img_file)
                self.scale_by_percent()
                self.update_zoom_label()
                # ================将当前图片项设为选中状态================
                self.cil.blockSignals(True)  # 阻止信号
                self.cil.setCurrentRow(self.img_ind)
                self.cil.blockSignals(False)  # 恢复信号
                # ================更新状态栏信息================
                index_str = f'{self.img_ind + 1}/{len(self.img_list)}'
                meta_str = f'{self.tr("Width")}: {self.iw} {self.tr("Height")}: {self.ih} | {self.tr("File Size")}: {self.img_file_size} bytes'
                status_text = f'{index_str} | {self.tr("Filnename")}: {self.img_file.name} | {meta_str}'
                self.status_bar.showMessage(status_text)
                QApplication.processEvents()
                self.open_lp_bubbles()
        QApplication.processEvents()

    def open_lp_bubbles(self):
        self.undo_stack = []
        self.redo_stack = []
        self.bubble_ellipses.clear()
        rlp_pic_bubbles = self.rlp_para_dic.get(self.formatted_stem, [])
        # ================设置表格行数================
        self.plus_tv_im.setRowCount(len(rlp_pic_bubbles))
        for r in range(len(rlp_pic_bubbles)):
            # ================针对每一个气泡================
            rlp_pic_bubble = rlp_pic_bubbles[r]
            id = rlp_pic_bubble['id']
            coor_x = rlp_pic_bubble['coor_x']
            coor_y = rlp_pic_bubble['coor_y']
            group = rlp_pic_bubble['group']
            content = rlp_pic_bubble['content']
            x = int(self.iw * coor_x)
            y = int(self.ih * coor_y)
            pt_xy = (x, y)
            group_str = ''
            if group == 1:
                group_str = 'G1框内'
            elif group == 2:
                group_str = 'G2框外'

            # 创建一个可拖动的组
            bubble_ellipse = DraggableGroup(x, y, id, group, self)
            self.bubble_ellipses.append(bubble_ellipse)

            item0 = QStandardItem(str(id))
            item1 = QStandardItem(content)
            item2 = QStandardItem(group_str)
            item3 = QStandardItem(f'{x},{y}')
            self.plus_tv_im.setItem(r, 0, item0)
            self.plus_tv_im.setItem(r, 1, item1)
            self.plus_tv_im.setItem(r, 2, item2)
            self.plus_tv_im.setItem(r, 3, item3)

        for idx, bubble_ellipse in enumerate(self.bubble_ellipses):
            self.cgs.addItem(bubble_ellipse)

        # 检查是否有行已经被选中
        if not self.plus_tv.selectionModel().hasSelection() and len(rlp_pic_bubbles) > 0:
            # 选中第一行
            self.plus_tv.selectRow(0)

        self.update_plus_pte()

    @logger.catch
    def update_coordinates(self, item, x, y):
        # 更新表格中的坐标信息
        row_id = item.id - 1
        item3 = QStandardItem(f'{x},{y}')
        self.plus_tv_im.setItem(row_id, 3, item3)

    def update_plus_pte(self):
        current_index = self.plus_tv_sm.currentIndex()
        if current_index.isValid():
            row = current_index.row()
            content = self.plus_tv_im.item(row, 1).text()
            self.plus_pte.setPlainText(content)
        else:
            self.plus_pte.setPlainText('')

    def on_text_changed(self):
        text = self.plus_pte.toPlainText()
        current_index = self.plus_tv.currentIndex()
        if not current_index.isValid():
            return
        row = current_index.row()
        self.plus_tv_im.setItem(row, 1, QStandardItem(text))

    def on_delete(self):
        if self.plus_tv.selectionModel().hasSelection():
            selectedRow = self.plus_tv.selectionModel().selectedRows()[0]
            index = selectedRow.row()
            # logger.debug(f'{index=}')
            for i in range(index + 1, len(self.bubble_ellipses)):
                # logger.debug(f'{i=}')
                bubble_ellipse = self.bubble_ellipses[i]
                old_id = bubble_ellipse.id
                new_id = old_id - 1
                bubble_ellipse.change_id(new_id)
                # logger.debug(f'{old_id=}, {new_id=}')
                item = self.plus_tv_im.item(i, 0)  # ID column
                item.setText(str(new_id))
            # 删除场景中对应的气泡
            bubble_ellipse = self.bubble_ellipses.pop(index)
            self.cgs.removeItem(bubble_ellipse)
            self.plus_tv_im.removeRow(index)

            # 选择新行
            new_index = min(index, self.plus_tv_im.rowCount() - 1)
            if new_index >= 0:
                self.plus_tv.selectRow(new_index)

    def on_move(self, move_num):
        current_index = self.plus_tv.currentIndex()
        if not current_index.isValid():
            return

        row = current_index.row()
        if isinstance(move_num, str):
            if move_num == '1':
                # 移到开头
                target_row = 0
            else:  # move_num == '-1'
                # 移到结尾
                target_row = self.plus_tv_im.rowCount() - 1
            items = [self.plus_tv_im.takeItem(row, col) for col in range(self.plus_tv_im.columnCount())]
            self.plus_tv_im.removeRow(row)
            self.plus_tv_im.insertRow(target_row, items)

            # 移动气泡并更新ID
            bubble_to_move = self.bubble_ellipses.pop(row)
            self.bubble_ellipses.insert(target_row, bubble_to_move)
            # 更新所有行的ID和气泡ID
            for idx, bubble in enumerate(self.bubble_ellipses):
                bubble.change_id(idx + 1)
                item0 = QStandardItem(str(idx + 1))
                self.plus_tv_im.setItem(idx, 0, item0)
        else:
            target_row = row + move_num
            if 0 <= target_row < self.plus_tv_im.rowCount():
                items = [self.plus_tv_im.takeItem(row, col) for col in range(self.plus_tv_im.columnCount())]
                self.plus_tv_im.removeRow(row)
                self.plus_tv_im.insertRow(target_row, items)

                src_bubble_ellipse = self.bubble_ellipses[row]
                dst_bubble_ellipse = self.bubble_ellipses[target_row]

                item0 = QStandardItem(str(row + 1))
                target_item0 = QStandardItem(str(target_row + 1))
                self.plus_tv_im.setItem(row, 0, item0)
                self.plus_tv_im.setItem(target_row, 0, target_item0)

                src_bubble_ellipse.change_id(target_row + 1)
                dst_bubble_ellipse.change_id(row + 1)

                # 交换
                self.bubble_ellipses[row], self.bubble_ellipses[target_row] = self.bubble_ellipses[target_row], \
                    self.bubble_ellipses[row]

        # 更新选中
        self.plus_tv.selectRow(target_row)

    def on_create(self, x, y):
        new_id = len(self.bubble_ellipses) + 1
        new_bubble = DraggableGroup(x, y, new_id, 1, self)
        self.cgs.addItem(new_bubble)
        self.bubble_ellipses.append(new_bubble)

        row = self.plus_tv_im.rowCount()
        self.plus_tv_im.insertRow(row)

        item0 = QStandardItem(str(new_id))
        item1 = QStandardItem('')
        item2 = QStandardItem('G1框内')
        item3 = QStandardItem(f'{x},{y}')
        self.plus_tv_im.setItem(row, 0, item0)
        self.plus_tv_im.setItem(row, 1, item1)
        self.plus_tv_im.setItem(row, 2, item2)
        self.plus_tv_im.setItem(row, 3, item3)

        # 选择新行
        self.plus_tv.selectRow(self.plus_tv_im.rowCount() - 1)

    def on_group(self, group):
        current_index = self.plus_tv.currentIndex()
        if not current_index.isValid():
            return

        row = current_index.row()
        if group == 1:
            group_str = 'G1框内'
        elif group == 2:
            group_str = 'G2框外'
        else:
            group_str = ''
        item2 = QStandardItem(group_str)
        self.plus_tv_im.setItem(row, 2, item2)
        bubble_ellipse = self.bubble_ellipses[row]
        bubble_ellipse.change_group(group)

    def open_folder_by_path(self, folder_path):
        # 判断文件夹路径是否存在
        folder_path = Path(folder_path)
        if folder_path.exists():
            # 获取所有图片文件的路径
            img_list = get_valid_imgs(folder_path)
            if img_list and folder_path != self.img_folder:
                self.img_folder = folder_path
                self.auto_subdir = Auto / self.img_folder.name
                make_dir(self.auto_subdir)
                self.img_list = img_list
                self.all_masks = get_valid_imgs(self.img_folder, vmode='mask')
                self.filter_img_list = self.img_list
                self.img_ind = 0
                self.img_file = self.img_list[self.img_ind]
                # ================更新导航栏中的图片列表================
                self.cil.load_img_list()
                self.open_img_by_path(self.img_file)

    def open_folder_by_dialog(self):
        # 如果self.img_folder已经设置，使用其上一级目录作为起始目录，否则使用当前目录
        self.img_folder = Path(self.img_folder) if self.img_folder else None
        start_directory = self.img_folder.parent.as_posix() if self.img_folder else "."
        img_folder = QFileDialog.getExistingDirectory(self, self.tr('Open Folder'), start_directory)
        if img_folder:
            self.open_folder_by_path(img_folder)

    def nav_img(self, nav_step):
        cur_img_path = self.img_list[self.img_ind]
        # 检查当前图片路径是否在过滤后的图片列表中
        if cur_img_path not in self.filter_img_list:
            return
        cur_filter_ind = self.filter_img_list.index(cur_img_path)
        if nav_step == "first":
            new_filter_ind = 0
        elif nav_step == "last":
            new_filter_ind = len(self.filter_img_list) - 1
        else:
            new_filter_ind = cur_filter_ind + nav_step
        if 0 <= new_filter_ind < len(self.filter_img_list):
            new_img_file = self.filter_img_list[new_filter_ind]
            self.open_img_by_path(new_img_file)

    def filter_imgs(self, search_text: str):
        # 获取搜索框的三个条件：是否区分大小写、是否全词匹配、是否使用正则表达式
        case_sensitive = self.search_line.case_sensitive_button.isChecked()
        whole_word = self.search_line.whole_word_button.isChecked()
        use_regex = self.search_line.regex_button.isChecked()

        # 获取对应的正则表达式模式对象
        regex = get_search_regex(search_text, case_sensitive, whole_word, use_regex)
        if not regex:
            return

        # 根据正则表达式筛选图片列表
        self.filter_img_list = [img_file for img_file in self.img_list if regex.search(img_file.name)]

        # 更新缩略图列表：如果图片名匹配正则表达式，显示该项，否则隐藏
        for index in range(self.cil.count()):
            item = self.cil.item(index)
            item_text = item.text()
            item.setHidden(not bool(regex.search(item_text)))

    def update_zoom_label(self):
        self.le_scale_percent.setText(f'{self.cgv.zoom_level * 100:.2f}')

    def scale_by_percent(self):
        target_scale = float(self.le_scale_percent.text()) / 100
        current_scale = self.cgv.transform().m11()
        scale_factor = target_scale / current_scale
        self.cgv.scale(scale_factor, scale_factor)

    def undo(self):
        if not self.undo_stack:
            return

        self.undo_action.setEnabled(len(self.undo_stack) > 0)
        self.redo_action.setEnabled(True)

    def redo(self):
        if not self.redo_stack:
            return

        self.redo_action.setEnabled(len(self.redo_stack) > 0)
        self.undo_action.setEnabled(True)

    def get_table_data(self):
        data_list = []
        for row in range(self.plus_tv_im.rowCount()):
            row_data = []
            for col in range(self.plus_tv_im.columnCount()):
                item = self.plus_tv_im.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # 如果某个单元格没有数据，则添加空字符串
            data_list.append(row_data)
        return data_list

    def save2lp(self):
        self.formatted_stem = get_formatted_stem(self.img_file)
        table_data = self.get_table_data()
        if print_type == 'pprint':
            pprint(table_data)
        else:
            table = PrettyTable()
            # 设置表格的标题
            table.field_names = [self.tr('ID'), self.tr('Content'), self.tr('Group'), self.tr('Coordinates'), ]
            # 添加数据到表格
            for t in range(len(table_data)):
                row_data = table_data[t]
                table.add_row(row_data)
            # 打印表格
            print(table)

        rlp_pic_bubbles = []
        for t in range(len(table_data)):
            row_data = table_data[t]
            id, content, group_str, coor_str = row_data
            if group_str == 'G1框内':
                group = 1
            elif group_str == 'G2框外':
                group = 2
            else:
                group = 1
            x_str, par, y_str = coor_str.partition(',')
            coor_x = int(x_str) / self.iw
            coor_y = int(y_str) / self.ih
            rlp_pic_bubble = {}
            rlp_pic_bubble['id'] = id
            rlp_pic_bubble['coor_x'] = coor_x
            rlp_pic_bubble['coor_y'] = coor_y
            rlp_pic_bubble['group'] = group
            rlp_pic_bubble['content'] = content
            rlp_pic_bubbles.append(rlp_pic_bubble)
        self.rlp_para_dic[self.formatted_stem] = rlp_pic_bubbles
        save_rlp(self.rlp_txt, self.rlp_para_dic, self.img_list)


@logger.catch
def lp_qt(appgui):
    lp_window = LabelPlusWindow()
    sys.exit(appgui.exec())


def z():
    pass


if __name__ == "__main__":
    MomoHanhua = DOCUMENTS / '默墨汉化'
    Auto = MomoHanhua / 'Auto'
    Log = MomoHanhua / 'Log'
    DataOutput = MomoHanhua / 'DataOutput'
    ComicProcess = MomoHanhua / 'ComicProcess'  # 美漫
    MangaProcess = MomoHanhua / 'MangaProcess'  # 日漫
    ManhuaProcess = MomoHanhua / 'ManhuaProcess'  # 国漫
    ManhwaProcess = MomoHanhua / 'ManhwaProcess'  # 韩漫

    make_dir(MomoHanhua)
    make_dir(Auto)
    make_dir(Log)
    make_dir(DataOutput)
    make_dir(ComicProcess)
    make_dir(MangaProcess)
    make_dir(ManhuaProcess)
    make_dir(ManhwaProcess)

    date_str = strftime('%Y_%m_%d')
    log_path = Log / f'日志-{date_str}.log'
    logger.add(
        log_path.as_posix(),
        rotation='500MB',
        encoding='utf-8',
        enqueue=True,
        compression='zip',
        retention='10 days',
        # backtrace=True,
        # diagnose=True,
        # colorize=True,
        # format="<green>{time}</green> <level>{message}</level>",
    )

    # ================选择语言================
    # 不支持使用软件期间重选语言
    # 因为界面代码是手写的，没有 retranslateUi
    # lang_code = 'en_US'
    lang_code = 'zh_CN'
    # lang_code = 'zh_TW'
    # lang_code = 'ja_JP'
    qm_path = UserDataFolder / f'{APP_NAME}_{lang_code}.qm'


    def steps():
        pass


    img_ind = 0
    media_type = 'Manga'
    hide_extra = True
    print_type = 'pprint'
    folder_name = 'your_folder_name'
    thumb_size = 240
    window_size = '1200,800'
    if ',' in str(window_size):
        window_w, par, window_h = window_size.partition(',')
        window_w = int(window_w)
        window_h = int(window_h)
    else:
        window_w = window_h = window_size

    ProcessDir = MomoHanhua / f'{media_type}Process'
    img_folder = ProcessDir / folder_name

    img_list = get_valid_imgs(img_folder)
    img_stems = [x.stem for x in img_list]
    cpre = common_prefix(img_stems)
    csuf = common_suffix(img_stems)
    all_masks = get_valid_imgs(img_folder, vmode='mask')

    appgui = QApplication(sys.argv)
    translator = QTranslator()
    translator.load(str(qm_path))
    QApplication.instance().installTranslator(translator)
    appgui.installTranslator(translator)
    screen = QApplication.primaryScreen()
    if sys.platform == 'darwin':
        # 如果是 MacOS 系统
        scaling_factor = screen.devicePixelRatio()
    else:
        scaling_factor = 1
    scaling_factor_reci = 1 / scaling_factor
    lp_qt(appgui)
