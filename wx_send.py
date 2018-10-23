#!F:\anco\python
# --coding:utf-8--
'''
调用微信api接口，给指定好友发送天气预报
name：包子
date：2018.10.22
'''

from setting import *
import weather_get
import win32api
import win32gui
import win32clipboard as w
import win32con
import os
import time
from ctypes import *
import win32ui
import aircv as ac


def main():
    # 打开微信程序，当微信程序处于打开状态时会将微信窗口调为焦点窗口
    os.startfile(wechat)
    # 创建截屏图片
    filename = "blackground.jpg"
    # 搜索栏标准图片
    search = 'search.jpg'
    # 获取天气
    weather = weather_get.weather()
    print(weather)
    # 拼接要发送的消息
    msg = weather[0][0]
    for i in range(number):
        i += 1
        msg += weather[i][0] + "，天气" + weather[i][1] + '，最高温度 ' + str(weather[i][2]) \
                                      + "，最低温度 " + weather[i][3]
    msg += love
    while True:
        # 设置隔1秒运行一次
        time.sleep(1)
        # 对整个屏幕截图，并保存截图为filename
        window_capture(filename)
        # 将屏幕截图和搜索栏标准图像的文件名给matchImg函数进行图像匹配
        result_all = matchImg(filename, search)
        print(result_all)
        # 返回结果：
        # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)),
        # 'result': (422.0, 400.0)}
        # confidence：匹配相似率
        # rectangle：匹配图片在原始图像上四边形的坐标
        # result：匹配图片在原始图片上的中心坐标点，也就是我们要找的点击点

        # 如果微信未登录，返回none表示未匹配，继续执行
        if result_all == None:
            continue
        # 如果相似度匹配，视为微信处于登录状态
        else:
            #点击微信界面
            clickLeftCur()
            time.sleep(0.5)
            # 虚幻给列表中指定的好友发送消息
            for friend in friend_name:
                # ctrl+f键搜索好友备注名
                ctrlF()
                # 输入你要发送好友的备注名
                setText(friend)
                ctrlV()
                time.sleep(1)
                # 回车确认
                enter_r()
                time.sleep(0.5)
                # 给该好友发送消息
                setText(msg)
                ctrlV()
                altS()
            break

# 把文字放到剪切板：
def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()

# 把图片放到剪切板：
# def setImage(data):  # 写入剪切板
#     w.OpenClipboard()
#     try:
#         # Unicode tests
#         w.EmptyClipboard()
#         w.SetClipboardData(win32con.CF_DIB, data)
#     except:
#         traceback.print_exc()
#     finally:
#         w.CloseClipboard()

# 模拟ctrl+v
def ctrlV():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)

# 模拟ctrl+f
def ctrlF():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(70, 0, 0, 0)  # f键位码是70
    win32api.keybd_event(70, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


# 模拟alt+s
def altS():
    win32api.keybd_event(18, 0, 0, 0)  # Alt
    win32api.keybd_event(83, 0, 0, 0)  # s
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)


# 其次是定义鼠标的一些动作  单击
def clickLeftCur():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# 模拟回车按键
def enter_r():
    win32api.keybd_event(13, 0, 0, 0)
    win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键

# 移动鼠标
def moveCurPos(x, y):
    windll.user32.SetCursorPos(x, y)


# 获得鼠标位置信息，这个再实际代码没用上，调试用得上
def getCurPos():
    return win32gui.GetCursorPos()

# 截图
def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


# imgsrc=原始图像，imgobj=待查找的图片
def matchImg(imgsrc, imgobj, confidencevalue=0.5):
    imsrc = ac.imread(imgsrc)   # 原始图像
    imobj = ac.imread(imgobj) # 带查找的部分
    # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416),
    #  (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    match_result = ac.find_template(imsrc, imobj,confidencevalue)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽
    return match_result

# 说明：通过aircv的find_template()
# 方法，来返回匹配图片的坐标结果
# find_template(原始图像imsrc，待查找的图片imobj，最低相似度confidence)

if __name__ == "__main__":
    main()







