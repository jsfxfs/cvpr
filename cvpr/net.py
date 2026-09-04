"""HTTP 层：线程安全 Session、指数退避重试、礼貌延时。

注意：目标环境为 Python 3.9，禁止使用 ``str | None`` 这类 PEP 604 语法。
"""

import random
import threading
import time
from typing import Optional

import requests

BASE_URL = "https://openaccess.thecvf.com"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

_thread_local = threading.local()


def get_session() -> requests.Session:
    """每个工作线程独享一个 Session，复用 TCP 连接。"""
    session = getattr(_thread_local, "session", None)
    if session is None:
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})
        _thread_local.session = session
    return session


class Fetcher(object):
    """抓取器：统一处理延时、重试与超时。"""

    def __init__(self, delay: float = 0.5, retries: int = 4, timeout: int = 30):
        self.delay = delay
        self.retries = retries
        self.timeout = timeout

    def _polite_sleep(self) -> None:
        """带抖动的延时，避免多线程整齐地同时打服务器。"""
        if self.delay <= 0:
            return
        time.sleep(self.delay * (0.7 + 0.6 * random.random()))

    def get_text(self, url: str) -> Optional[str]:
        """获取页面文本，失败返回 None。"""
        for attempt in range(self.retries):
            try:
                resp = get_session().get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.text
            except requests.RequestException as exc:
                if attempt == self.retries - 1:
                    print("    [放弃] %s -> %s" % (url, exc))
                    return None
                time.sleep(2 ** attempt)
            finally:
                self._polite_sleep()
        return None

    def download(self, url: str, filepath) -> bool:
        """流式下载文件，返回是否成功。"""
        import os

        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return True
        try:
            resp = get_session().get(url, timeout=120, stream=True)
            resp.raise_for_status()
            tmp = str(filepath) + ".part"
            with open(tmp, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        fh.write(chunk)
            os.replace(tmp, filepath)
            return True
        except (requests.RequestException, OSError) as exc:
            print("    [下载失败] %s -> %s" % (filepath, exc))
            return False
        finally:
            self._polite_sleep()
