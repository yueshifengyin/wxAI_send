一个爬虫小脚本
爬取某地天气并在微信打开的时候自动发送给指定好友

import aircv as ac
import requests
import http.client

这几个为第三方库需要自己导入
各项参数信息在setting文件中修改

小白教程：
1、https://www.python.org/ftp/python/3.6.7/python-3.6.7-amd64.exe
  在这个网站下载python解释器，安装好后记住安装目录位置
2、https://files.pythonhosted.org/packages/45/ae/8a0ad77defb7cc903f09e551d88b443304a9bd6e6f124e75c0fbbf6de8f7/pip-18.1.tar.gz
  在这个网站下载pip，解压后双击setup.py文件执行
3、win+r键输入cmd运行
4、依次输入  pip install aircv as ac
           pip install requests
           pip install import http.client
5、安装完第三方库后，将wx_py中第一行！后面的路径改为python安装的路径

email：it_lijialiang@163.com

