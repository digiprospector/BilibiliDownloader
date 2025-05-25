import os
from urllib.parse import urljoin
from src.implementations.data_loader import DataLoader
from src.implementations.network_fetcher import NetworkFetcher
from src.implementations.network_parser import NetworkParser
from src.implementations.submit_data import SubmitData
from src.utils.utils import (
    cookie_str_to_dict, get_sec_ch_ua, get_platform,
    get_random_ua, get_sec_ch_ua_mobile, extract_bv_id,
    check_file_integrity, find_highest_quality_file_index,
    merge_audio_video, get_file_format, delete_file
)


class BilibiliDownloader:
    def __init__(self):
        self.audio_info = {}
        self.video_info = {}
        self.loader = DataLoader()
        self.fetcher = NetworkFetcher()
        self.parser = NetworkParser()
        self.submit = SubmitData()
        self.config = None

    def _initialize_config(self):
        """初始化并验证配置"""
        self.config = self.loader.load_config()
        # 处理 cookies
        if not isinstance(self.config.get("cookies", {}), dict):
            self.config["cookies"] = cookie_str_to_dict(self.config.get("cookies", ""))
        # 设置请求头
        headers = self.config.setdefault("headers", {})
        if not headers.get("user-agent"):
            ua = get_random_ua()
            headers.update({
                "user-agent": ua,
                "sec-ch-ua": get_sec_ch_ua(ua),
                "sec-ch-ua-platform": get_platform(ua),
                "sec-ch-ua-mobile": get_sec_ch_ua_mobile(ua)
            })
        # 验证路径
        if not self.config.get("file_download_path"):
            raise ValueError("文件下载路径未配置")

    @staticmethod
    def _get_media_info(media_type, bv_json):
        """从 BV JSON 中获取媒体（音频/视频）信息"""
        if media_type == "audio":
            # 尝试获取 FLAC 音频
            flac_data = bv_json.get("data", {}).get("dash", {}).get("flac", {}).get("audio", {})
            if flac_data.get("baseUrl"):
                mime_type = flac_data.get("mime_type", "")
                return {
                    "link": flac_data["baseUrl"],
                    "audio_format": mime_type.split('/')[-1],
                    "is_flac": True
                }

            # 如果没有 FLAC，回退到普通音频
            audio_list = bv_json.get("data", {}).get("dash", {}).get("audio", [])
            if not audio_list:
                return None

            max_audio = audio_list[find_highest_quality_file_index(audio_list)]
            mime_type = max_audio.get('mime_type', "")
            return {
                "link": max_audio.get('baseUrl', ""),
                "audio_format": mime_type.split('/')[-1],
                "is_flac": False
            }

        elif media_type == "video":
            video_list = bv_json.get("data", {}).get("dash", {}).get("video", [])
            if not video_list:
                return None

            max_video = video_list[find_highest_quality_file_index(video_list)]
            mime_type = max_video.get('mime_type', "")
            return {
                "link": max_video.get('baseUrl', ""),
                "video_format": mime_type.split('/')[-1]
            }

        return None

    def _download_media(self, media_type, media_info, bv_id, file_download_path):
        """下载媒体文件（音频或视频）"""
        # 准备下载信息
        download_info = {
            "link": media_info["link"],
            "request_type": "file_size",
            "data_type": media_type
        }

        # 获取文件大小
        size_info = self.fetcher.fetch(download_info)
        if not size_info.get("size"):
            return None

        # 准备文件路径
        file_ext = media_info.get(f"{media_type}_format", "mp4")
        temp_filename = f"temp_{bv_id}_{size_info.get('type', '')}.{file_ext}"
        file_path = os.path.join(file_download_path, temp_filename)

        # 检查文件是否已存在
        existing_size = check_file_integrity(file_path)
        if existing_size == size_info["size"]:
            return {"complete": True, "filepath": file_path}

        # 下载文件内容
        download_info.update({
            "request_type": "file_content",
            "existing_size": existing_size,
            "total_size": size_info["size"]
        })

        content = self.fetcher.fetch(download_info)
        if not content.get("response"):
            return None

        # 保存文件
        save_result = self.submit.submit({
            "response": content["response"],
            "file_type": f"{media_type}_content",
            "filepath": file_path,
            "submit_type": "local"
        })

        save_result["filepath"] = file_path
        return save_result

    def download_audio(self, bv_json, bv_id, file_download_path):
        """下载 Bilibili 视频中的音频"""
        audio_info = self._get_media_info("audio", bv_json)
        if not audio_info:
            return

        self.audio_info = self._download_media("audio", audio_info, bv_id, file_download_path) or {}

    def download_video(self, bv_json, bv_id, file_download_path):
        """下载 Bilibili 视频"""
        video_info = self._get_media_info("video", bv_json)
        if not video_info:
            return

        self.video_info = self._download_media("video", video_info, bv_id, file_download_path) or {}

    def _process_download(self, link_info):
        """处理单个下载链接"""
        link = link_info.get("link", "")
        download_info = link_info.get("download_info", "")
        bv_id = extract_bv_id(link)

        if not bv_id:
            print(f"链接中无效的 BV ID: {link}")
            return

        # 获取视频信息
        bv_dict = self.fetcher.fetch({
            "link": urljoin(self.config["site"], link),
            "cookies": self.config["cookies"],
            "request_type": "bv_info",
            "headers": self.config["headers"],
            "site": self.config["site"]
        })

        if not bv_dict.get("text"):
            print(f"获取 BV ID 的信息失败: {bv_id}")
            return

        bv_content = self.parser.parse(bv_dict)
        bv_json = bv_content.get("data", {})
        bv_title = bv_content.get("title", f"bilibili_{bv_id}")

        # 下载请求的媒体
        file_download_path = self.config["file_download_path"]

        if download_info in ("视频", ""):
            self.download_video(bv_json, bv_id, file_download_path)

        if download_info in ("音频", ""):
            self.download_audio(bv_json, bv_id, file_download_path)

        # 处理下载的文件
        self._process_downloaded_files(bv_title, file_download_path)

    def _process_downloaded_files(self, bv_title, file_download_path):
        """合并或重命名下载的文件"""
        audio_complete = self.audio_info.get("complete", False)
        video_complete = self.video_info.get("complete", False)

        if audio_complete and video_complete:
            # 合并音频和视频
            output_path = os.path.join(file_download_path, f"{bv_title}{get_file_format(self.video_info['filepath'])}")
            if merge_audio_video(
                    video_path=self.video_info["filepath"],
                    audio_path=self.audio_info["filepath"],
                    output_path=output_path
            ):
                delete_file(self.video_info["filepath"])
                delete_file(self.audio_info["filepath"])

        elif audio_complete:
            # 重命名音频文件
            old_path = self.audio_info["filepath"]
            new_path = os.path.join(file_download_path, f"{bv_title}{get_file_format(old_path)}")
            os.rename(old_path, new_path)

    def main(self):
        """下载器的主入口点"""
        try:
            self._initialize_config()
            download_links = self.loader.load_download_info(self.config['download_link_path'])

            for link_info in download_links:
                self._process_download(link_info)

        except Exception as e:
            print(f"Bilibili 下载器出错: {str(e)}")
            raise


if __name__ == '__main__':
    downloader = BilibiliDownloader()
    downloader.main()