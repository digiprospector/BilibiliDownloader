import time

import requests
import qrcode
from io import BytesIO
from qrcode.main import QRCode
import base64
def generate_qrcode_base64(url):
    """
    生成二维码并返回Base64编码的图片数据
    :param url: 要编码的URL
    :return: Base64编码的图片数据
    """
    # 创建QRCode对象
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 添加数据
    qr.add_data(url)
    qr.make(fit=True)

    # 生成二维码图片
    img = qr.make_image(fill_color="black", back_color="white")

    # 将图片保存到内存缓冲区
    buffer = BytesIO()
    img.save(buffer)

    # 获取字节数据并编码为Base64
    img_bytes = buffer.getvalue()
    base64_data = base64.b64encode(img_bytes).decode('utf-8')

    # 返回可直接在HTML中使用的data URI
    return f"data:image/png;base64,{base64_data}"
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
        # 'cookie': 'buvid3=5DC9ECD6-F557-52A3-FF9E-1FDDA9E4C8D667977infoc; b_nut=1718168767; _uuid=388A2A52-DF5A-AD710-2109B-6CD2E15104710170096infoc; buvid_fp=80961b0a9fb75177e9b8b06359f9b857; buvid4=F798A55C-17B6-0B9B-1443-B6938628F32269589-024061205-oIYOu8Gmrbm2NI8YXvd4bVKliyO57%2FKZqfGPCjRm1GceKwDw891ZsDL8xVr2A%2F%2FM; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=0zbfVFXP2t|yYajp5nV|2cV|3w1ShlGg; LIVE_BUVID=AUTO4417264877862908; PVID=1; hit-dyn-v2=1; enable_feed_channel=ENABLE; b_lsid=4FA104527_196F1C04AD4; home_feed_column=4; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDgwNzMwODMsImlhdCI6MTc0NzgxMzgyMywicGx0IjotMX0.gultaEOhc9_bssq1RKKJ4oJCYCVA4ul0PgJV2CT3Bck; bili_ticket_expires=1748073023; browser_resolution=901-1051',
    }

    response = requests.get(
        'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header&go_url=https:%2F%2Fwww.bilibili.com%2F&web_location=333.1007',
        cookies=cookies,
        headers=headers,
    )
    return response.json()

def request_api_login(qrcode_key):
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
        # 'cookie': 'buvid3=5DC9ECD6-F557-52A3-FF9E-1FDDA9E4C8D667977infoc; b_nut=1718168767; _uuid=388A2A52-DF5A-AD710-2109B-6CD2E15104710170096infoc; buvid_fp=80961b0a9fb75177e9b8b06359f9b857; buvid4=F798A55C-17B6-0B9B-1443-B6938628F32269589-024061205-oIYOu8Gmrbm2NI8YXvd4bVKliyO57%2FKZqfGPCjRm1GceKwDw891ZsDL8xVr2A%2F%2FM; enable_web_push=DISABLE; header_theme_version=CLOSE; CURRENT_FNVAL=4048; rpdid=0zbfVFXP2t|yYajp5nV|2cV|3w1ShlGg; LIVE_BUVID=AUTO4417264877862908; PVID=1; hit-dyn-v2=1; enable_feed_channel=ENABLE; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDgwNzMwODMsImlhdCI6MTc0NzgxMzgyMywicGx0IjotMX0.gultaEOhc9_bssq1RKKJ4oJCYCVA4ul0PgJV2CT3Bck; bili_ticket_expires=1748073023; sid=fwj52gnj; b_lsid=E44A4683_196F25F7DC7; home_feed_column=4; browser_resolution=901-1051',
    }

    params = {
        'qrcode_key': qrcode_key,
        'source': 'main-fe-header',
        'web_location': '333.1007',
    }

    response = requests.get(
        'https://passport.bilibili.com/x/passport-login/web/qrcode/poll',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.json())
    # 获取 cookies
    cookies = response.cookies
    # 手动拼接成字符串
    cookies_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
    print(cookies_str)
if __name__=="__main__":
    response_data=request_api()
    qrcode_url = response_data["data"]["url"]
    qrcode_key = response_data["data"]["qrcode_key"]
    base64_qrcode = generate_qrcode_base64(qrcode_url)
    print("Base64编码的二维码:")
    print(base64_qrcode)
    url = "".join(base64_qrcode)
    base64_data = url.split(",", 1)[1]
    # 解码Base64数据
    image_data = base64.b64decode(base64_data)
    # 将解码后的数据保存为图片文件
    with open("output_image.png", "wb") as image_file:
        image_file.write(image_data)
    print("图片已保存为 output_image.png")
    time.sleep(10)
    request_api_login(qrcode_key)
