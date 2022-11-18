import sys
import os.path
import requests
import time
import pystray
import ctypes
from PIL import Image
from pystray import MenuItem as item
from pathlib import Path


class WallPaper(object):

    def __init__(self):
        """
        程序初始化
        """
        self.relative_path = None
        menu = (
            item(text='更换壁纸', action=self._change_wallpaper),
            item(text='退出', action=self._on_exit)
        )
        # 托盘图标resource/wallpaper.ico
        icon_path = self._resource_path(str(Path('resource/wallpaper.ico')))
        image = Image.open(icon_path)
        # 设置托盘
        self.icon = pystray.Icon("name", image, "每日壁纸", menu)
        self._run()

    def _run(self):
        """
        执行
        Returns:

        """
        self.icon.run()

    @staticmethod
    def _change_wallpaper():
        """
        更换壁纸
        Args:
            self:

        Returns:

        """
        # 获取屏幕分辨率
        user32 = ctypes.windll.user32
        # 屏幕高、宽
        height, width = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        url = f"https://source.unsplash.com/{height}x{width}/?wallpaper"
        response = requests.get(url)
        if response.status_code == 200:
            images = response.content
            wallpaper = f'{time.strftime("%Y%m%d")}.jpg'
            with open(wallpaper, 'wb') as file:
                file.write(images)
            # 通知
            self._notify("每日壁纸", "壁纸下载成功")
            # 设置成壁纸
            user32.SystemParametersInfoW(20, 0, wallpaper, 0)
            # 通知
            self._notify("每日壁纸", "设置壁纸成功")
        else:
            # 通知
            self._notify("每日壁纸", "壁纸下载失败")

    def _notify(self, title: str, message: str):
        """
        程序通知
        Args:
            title: 通知标题
            message: 通知内容

        Returns:

        """
        return self.icon.notify(title, message)

    def _resource_path(self, relative_path):
        """
        返回资源文件路径
        Args:
            relative_path:

        Returns:

        """
        self.relative_path = relative_path
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath('.')
        return Path(f'{base_path}/{relative_path}')

    def _on_exit(self):
        """
        退出程序
        Returns:

        """
        self.icon.stop()


if __name__ == "__main__":
    daily_wallpaper = WallPaper()
