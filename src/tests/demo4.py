import requests


class YourClass:
    def __init__(self):
        self.session = requests.Session()  # 初始化 session

    def check_cookies(self):
        print("Debug: Session type =", type(self.session))
        print("Debug: Cookies count =", len(self.session.cookies))

        # 先发送一个请求（可选）
        self.session.get("https://www.bilibili.com/video/BV1FYEEzEEEr/?spm_id_from=333.1007.tianma.1-1-1.click")

        print("Debug: After request, cookies =", self.session.cookies.get_dict())

        # 打印所有 Cookie 详情
        for cookie in self.session.cookies:
            print(
                f"{cookie.name}: {cookie.value} "
                f"(Domain: {cookie.domain}, Path: {cookie.path}, Expires: {cookie.expires})"
            )


# 测试
obj = YourClass()
obj.check_cookies()