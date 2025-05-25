import requests


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
        # cookies=cookies,
        headers=headers,
    )
    return response.json()
print(request_api())