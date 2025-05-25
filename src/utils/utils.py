import base64
import json
import os
import re
from io import BytesIO
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
import qrcode
from PyQt5.QtGui import QPixmap
from qrcode.main import QRCode
from user_agents import parse
from fake_useragent import UserAgent
from urllib.parse import unquote
import subprocess
from pathlib import Path
import random
import string
import time
import uuid
import hashlib
import base64
import hmac
def get_random_ua():
    return UserAgent().random

def get_sec_ch_ua_mobile(ua):
    user_agent = parse(ua)
    if user_agent:
        return "?1"
    else:
        return "?0"

def get_sec_ch_ua(user_agent):
    chrome_version_match = re.search(r"Chrome/(\d+)", user_agent)
    if chrome_version_match:
        version = chrome_version_match.group(1)
        return f'"Chromium";v="{version}", "Google Chrome";v="{version}", "Not.A/Brand";v="99"'
    return None

def get_platform(user_agent):
    if "iPhone" in user_agent or "iPad" in user_agent:
        return "iOS"
    elif "Mac OS X" in user_agent and "Mobile" not in user_agent:
        return "macOS"
    elif "Android" in user_agent:
        return "Android"
    elif "Windows" in user_agent:
        return "Windows"
    else:
        return "Unknown"

def cookie_str_to_dict(cookie_str):
    """
    将 Cookie 字符串转换为字典格式，适用于 requests 库
    Args:
        cookie_str (str): 原始的 Cookie 字符串，如 "name1=value1; name2=value2"
    Returns:
        dict: 可用于 requests 的 Cookie 字典
    """
    cookie_dict = {}
    for item in cookie_str.split(';'):
        item = item.strip()
        if not item:
            continue
        if '=' in item:
            key, value = item.split('=', 1)
        else:
            key, value = item, ''
        cookie_dict[key] = value
    return cookie_dict

def find_highest_quality_file_index(video_list):
    if not video_list:
        return -1
    highest_index = 0
    for index, video in enumerate(video_list):
        current_width = video.get('width', 0)
        current_height = video.get('height', 0)
        current_frame_rate = video.get('frameRate', video.get('frame_rate', 0))
        current_bandwidth = video.get('bandwidth', 0)
        highest_video = video_list[highest_index]
        highest_width = highest_video.get('width', 0)
        highest_height = highest_video.get('height', 0)
        highest_frame_rate = highest_video.get('frameRate', highest_video.get('frame_rate', 0))
        highest_bandwidth = highest_video.get('bandwidth', 0)
        if (current_width > highest_width or
                (current_width == highest_width and current_height > highest_height) or
                (
                        current_width == highest_width and current_height == highest_height and current_frame_rate > highest_frame_rate) or
                (
                        current_width == highest_width and current_height == highest_height and current_frame_rate == highest_frame_rate and current_bandwidth > highest_bandwidth)):
            highest_index = index
    return highest_index

def check_file_integrity(filepath):
    if os.path.exists(filepath):
        existing_size = os.path.getsize(filepath)
    else:
        existing_size = 0
    return existing_size

def extract_bv_id(link):
    try:
        decoded_url = unquote(link)
        pattern = r"(?:/video/|b23\.tv/)(BV[0-9A-Za-z]{10})"
        match = re.search(pattern, decoded_url)
        return match.group(1) if match else None
    except (AttributeError, TypeError):
        return None

def get_file_format(filepath):
    file_path = Path(filepath)
    file_extension = file_path.suffix
    return file_extension

def get_media_info(filepath: str):
    """
    使用 ffprobe 检测媒体文件的真实格式（容器、视频编码、音频编码）
    参数:
        filepath: 媒体文件路径
    返回:
        包含媒体信息的字典，格式为:
        {
            "container": "mp4",      # 容器格式
            "video_codec": "h264",  # 视频编码（可能不存在）
            "audio_codec": "aac"     # 音频编码（可能不存在）
        }
        如果出错则返回None
    异常:
        不会抛出异常，所有错误都会被捕获并打印
    """
    if not Path(filepath).exists():
        print(f"[错误] 文件不存在: {filepath}")
        return None
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries",
        "format=format_name:stream=codec_type,codec_name",
        "-of", "json",
        filepath
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        media_info = {
            "container": "",
            "video_codec": None,
            "audio_codec": None
        }
        if "format" in data and "format_name" in data["format"]:
            media_info["container"] = data["format"]["format_name"].split(",")[0]
        for stream in data.get("streams", []):
            codec_type = stream.get("codec_type")
            codec_name = stream.get("codec_name")
            if not codec_type or not codec_name:
                continue
            if codec_type == "video" and not media_info["video_codec"]:
                media_info["video_codec"] = codec_name
            elif codec_type == "audio" and not media_info["audio_codec"]:
                media_info["audio_codec"] = codec_name
        return media_info
    except subprocess.CalledProcessError as e:
        print(f"[错误] FFprobe执行失败: {e.stderr.strip()}")
    except json.JSONDecodeError as e:
        print(f"[错误] JSON解析失败: {e}")
    except Exception as e:
        print(f"[错误] 未知错误: {e}")
    return None

def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            return False
    except Exception as e:
        return False

def merge_audio_video(video_path, audio_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'copy',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 错误: {e}")
        return False
    except FileNotFoundError:
        print("错误: 未找到 FFmpeg 或输入文件")
        return False

def generate_random_cookie():
    # 基础随机值生成
    def random_str(length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def random_uuid():
        return str(uuid.uuid4()).upper().replace('-', '')[:32] + 'infoc'

    def random_device_id():
        parts = [
            ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            ''.join(random.choices(string.ascii_letters + string.digits, k=6)),
            ''.join(random.choices(string.ascii_letters + string.digits, k=4)),
            ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        ]
        return '|'.join(parts)

    def random_buvid():
        return f"{random_str(8)}-{random_str(4)}-{random_str(4)}-{random_str(4)}-{random_str(12)}{random_str(5)}infoc"

    def random_lsid():
        return f"{random_str(8)}_{random_str(12)}"

    # 生成时间戳相关值
    current_time = int(time.time())
    b_nut = str(current_time)
    bili_ticket_expires = str(current_time + 86400 * 3)  # 3天后过期

    # 模拟 JWT token (简化的伪实现)
    def fake_jwt_token():
        header = base64.urlsafe_b64encode('{"alg":"HS256","kid":"s03","typ":"JWT"}'.encode()).decode().rstrip('=')
        payload = base64.urlsafe_b64encode(
            f'{{"exp":{bili_ticket_expires},"iat":{current_time},"plt":-1}}'.encode()).decode().rstrip('=')
        signature = base64.urlsafe_b64encode(
            hmac.new(b'secret', f"{header}.{payload}".encode(), hashlib.sha256).digest()).decode().rstrip('=')
        return f"{header}.{payload}.{signature}"

    # 生成指纹 (模拟)
    fp = hashlib.md5(random_str(32).encode()).hexdigest()

    # 构建完整 Cookie
    cookies = {
        'buvid3': random_buvid(),
        'b_nut': b_nut,
        '_uuid': random_uuid(),
        'buvid4': f"{random_str(8)}-{random_str(4)}-{random_str(4)}-{random_str(4)}-{random_str(12)}%2F{random_str(8)}",
        'enable_web_push': 'DISABLE',
        'header_theme_version': 'CLOSE',
        'CURRENT_FNVAL': '4048',
        'rpdid': random_device_id(),
        'LIVE_BUVID': f"AUTO{random.randint(1000000000000000, 9999999999999999)}",
        'PVID': str(random.randint(1, 10)),
        'hit-dyn-v2': '1',
        'enable_feed_channel': 'ENABLE',
        'sid': random_str(8),
        'bili_ticket': fake_jwt_token(),
        'bili_ticket_expires': bili_ticket_expires,
        'fingerprint': fp,
        'buvid_fp_plain': 'undefined',
        'b_lsid': random_lsid(),
        'home_feed_column': str(random.choice([4, 5])),
        'browser_resolution': f"{random.randint(800, 1920)}-{random.randint(800, 1080)}",
        'buvid_fp': fp,
    }

    return cookies

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




