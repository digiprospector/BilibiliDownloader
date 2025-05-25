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


class QRCodeWindow(QWidget):
    def __init__(self, qrcode_url, qrcode_key):
        super().__init__(parent=None)
        self.qrcode_key = qrcode_key
        self.setWindowTitle("B站扫码登录")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Generate QR code
        qr = QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qrcode_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to QPixmap
        buffer = BytesIO()
        img.save(buffer)
        img_bytes = buffer.getvalue()
        pixmap = QPixmap()
        pixmap.loadFromData(img_bytes)

        # Setup UI
        label = QLabel()
        label.setPixmap(pixmap)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("请使用B站APP扫码登录:"))
        layout.addWidget(label)
        self.setLayout(layout)

        # Start polling
        self.timer = QTimer(parent=None)
        self.timer.timeout.connect(self.check_login_status)
        self.timer.start(3000)  # Check every 3 seconds

    def check_login_status(self):
        response = self.poll_login_status()
        if response and response.get("data", {}).get("code") == 0:  # 登录成功
            self.timer.stop()
            cookies = response.get("data", {}).get("cookie_info", {}).get("cookies", [])
            # cookie_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
            QMessageBox.information(self, "登录成功", "您已成功登录!")
            self.close()

    def poll_login_status(self):
        cookies = {
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

        headers = {
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

        params = {
            'qrcode_key': self.qrcode_key,
            'source': 'main-fe-header',
            'web_location': '333.1007',
        }

        try:
            response = requests.get(
                'https://passport.bilibili.com/x/passport-login/web/qrcode/poll',
                params=params,
                cookies=cookies,
                headers=headers,
            )
            print(response.text)
            return response.json()

        except Exception as e:
            print(f"Error polling login status: {e}")
            return None


def request_api():
    cookies = {
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
        'b_lsid': '4FA104527_196F1C04AD4',
        'home_feed_column': '4',
        'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDgwNzMwODMsImlhdCI6MTc0NzgxMzgyMywicGx0IjotMX0.gultaEOhc9_bssq1RKKJ4oJCYCVA4ul0PgJV2CT3Bck',
        'bili_ticket_expires': '1748073023',
        'browser_resolution': '901-1051',
    }

    headers = {
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

    response = requests.get(
        'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header&go_url=https:%2F%2Fwww.bilibili.com%2F&web_location=333.1007',
        cookies=cookies,
        headers=headers,
    )
    return response.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    response_data = request_api()
    qrcode_url = response_data["data"]["url"]
    qrcode_key = response_data["data"]["qrcode_key"]
    window = QRCodeWindow(qrcode_url, qrcode_key)
    window.show()
    sys.exit(app.exec_())