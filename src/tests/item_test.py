import time
import sys
import requests
import qrcode
from io import BytesIO
from qrcode.main import QRCode
import base64
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

# 常量定义
COOKIES = {
    'buvid3': '5DC9ECD6-F557-52A3-FF9E-1FDDA9E4C8D667977infoc',
    'b_nut': '1718168767',
    '_uuid': '388A2A52-DF5A-AD710-2109B-6CD2E15104710170096infoc',
    'buvid_fp': '80961b0a9fb75177e9b8b06359f9b857',
    'buvid4': 'F798A55C-17B6-0B9B-1443-B6938628F32269589-024061205-oIYOu8Gmrbm2NI8YXvd4bVKliyO57%2FKZqfGPCjRm1GceKwDw891ZsDL8xVr2A%2F%2FM',
    'enable_web_push': 'DISABLE',
    'header_theme_version': 'CLOSE',
    'CURRENT_FNVAL': '4048',
    'rpdid': '0zbfVFXP2t|yYajp5nV|2cV|3w1ShlGg',
    'LIVE_BUVID': 'AUTO4417264877862908',
    'PVID': '1',
    'hit-dyn-v2': '1',
    'enable_feed_channel': 'ENABLE',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDgwNzMwODMsImlhdCI6MTc0NzgxMzgyMywicGx0IjotMX0.gultaEOhc9_bssq1RKKJ4oJCYCVA4ul0PgJV2CT3Bck',
    'bili_ticket_expires': '1748073023',
    'sid': 'fwj52gnj',
    'b_lsid': 'E44A4683_196F25F7DC7',
    'home_feed_column': '4',
    'browser_resolution': '901-1051',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'origin': 'https://www.bilibili.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/',
    'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
}


def generate_qrcode(url):
    """生成二维码图像"""
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def qrcode_to_pixmap(qr_image):
    """将二维码图像转换为QPixmap"""
    buffer = BytesIO()
    qr_image.save(buffer)
    img_bytes = buffer.getvalue()
    pixmap = QPixmap()
    pixmap.loadFromData(img_bytes)
    return pixmap


def get_qrcode_info():
    """获取B站二维码登录信息"""
    response = requests.get(
        'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header&go_url=https:%2F%2Fwww.bilibili.com%2F&web_location=333.1007',
        cookies=COOKIES,
        headers=HEADERS,
    )
    return response.json()


def poll_login_status(qrcode_key):
    """轮询登录状态"""
    params = {
        'qrcode_key': qrcode_key,
        'source': 'main-fe-header',
        'web_location': '333.1007',
    }

    try:
        response = requests.get(
            'https://passport.bilibili.com/x/passport-login/web/qrcode/poll',
            params=params,
            cookies=COOKIES,
            headers=HEADERS,
        )
        print(response.text)
        return response.json()
    except Exception as e:
        print(f"Error polling login status: {e}")
        return None


def create_window(pixmap):
    """创建并显示二维码窗口"""
    window = QWidget(parent=None)
    window.setWindowTitle("B站扫码登录")
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    label = QLabel()
    label.setPixmap(pixmap)
    layout = QVBoxLayout()
    layout.addWidget(QLabel("请使用B站APP扫码登录:"))
    layout.addWidget(label)
    window.setLayout(layout)
    return window


def check_login_status(window, timer, qrcode_key):
    """检查登录状态"""
    response = poll_login_status(qrcode_key)
    if response and response.get("data", {}).get("code") == 0:  # 登录成功
        timer.stop()
        QMessageBox.information(window, "登录成功", "您已成功登录!")
        window.close()


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 获取二维码信息
    response_data = get_qrcode_info()
    qrcode_url = response_data["data"]["url"]
    qrcode_key = response_data["data"]["qrcode_key"]
    qr_image=generate_qrcode(qrcode_url)
    pixmap=qrcode_to_pixmap(qr_image)
    # 创建并显示窗口
    window = create_window(pixmap)
    window.show()
    # 设置定时器检查登录状态
    timer = QTimer(parent=None)
    timer.timeout.connect(lambda: check_login_status(window, timer, qrcode_key))
    timer.start(3000)  # 每3秒检查一次

    # sys.exit(app.exec_())
    exit_code = app.exec_()

    # 这里的事件循环结束后执行的代码
    print("应用程序已退出，退出码:", exit_code)
    time.sleep(3)
    print("这里可以执行清理工作或其他后续操作")

    # 如果需要可以再次调用sys.exit
    sys.exit(exit_code)


if __name__ == "__main__":
    main()