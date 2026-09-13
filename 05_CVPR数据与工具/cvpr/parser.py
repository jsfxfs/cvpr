"""解析 CVF openaccess 页面（列表页 / 详情页）。

实测到的真实结构（CVPR2025 / CVPR2026 完全一致）：

    <dt class="ptitle"><br><a href="/content/CVPR2026/html/XXX.html">Title</a></dt>
    <dd>
      <form class="authsearch">
        <input type="hidden" name="query_author" value="Jie Xiao"><a href="#">Jie Xiao</a>,
      </form>                       ... 每位作者一个 form
    </dd>
    <dd>
      [<a href="..._paper.pdf">pdf</a>]
      [<a href="...supp">supp</a>]            <!-- 可选，约 89% 有 -->
      <div class="link2">[<a class="fakelink">bibtex</a>]
        <div class="bibref pre-white-space">@InProceedings{...}</div>  <!-- 内联，不是 .bib 链接 -->
      </div>
    </dd>
"""

import re
from pathlib import PurePosixPath
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .net import BASE_URL

_BIB_FIELDS = ("author", "title", "booktitle", "year", "month", "pages")


def paper_id(detail_url: str) -> str:
    """用详情页文件名作为稳定主键（去掉 .html 后缀）。"""
    return PurePosixPath(urlparse(detail_url).path).stem


def _block_nodes(dt) -> list:
    """收集 dt 之后、下一个 dt 之前的全部兄弟节点。"""
    nodes = []
    for sibling in dt.next_siblings:
        if getattr(sibling, "name", None) == "dt":
            break
        nodes.append(sibling)
    return nodes


def _scan_block(nodes) -> tuple:
    """在块内广度优先查找：作者、pdf、supp、bibtex。

    用 BFS 而非固定取两个 <dd>，这样即使 CVF 调整嵌套结构也不会解析失败。
    """
    authors, pdf_url, supp_url, bibtex = [], "", "", ""
    queue = list(nodes)

    while queue:
        node = queue.pop(0)
        name = getattr(node, "name", None)
        if not name:
            continue

        if name == "input":
            if node.get("name") == "query_author":
                value = (node.get("value") or "").strip()
                if value and value not in authors:
                    authors.append(value)
            continue

        if name == "a":
            href = node.get("href", "")
            text = node.get_text(strip=True).lower()
            if href.startswith("#"):       # bibtex 是 fakelink，href 为 "#"
                continue
            if text == "pdf" and not pdf_url:
                pdf_url = urljoin(BASE_URL, href)
            elif text == "supp" and not supp_url:
                supp_url = urljoin(BASE_URL, href)
            continue

        if name == "div" and "bibref" in (node.get("class") or []) and not bibtex:
            bibtex = node.get_text("\n", strip=True)
            continue

        children = getattr(node, "children", None)
        if children is not None:
            queue.extend(list(children))

    return authors, pdf_url, supp_url, bibtex


def parse_bibtex(bibtex: str) -> dict:
    """从内联 bibtex 文本里抽取关键字段。"""
    fields = {}
    for field in _BIB_FIELDS:
        match = re.search(field + r"\s*=\s*\{([^{}]*)\}", bibtex, re.I | re.S)
        if match:
            fields[field] = " ".join(match.group(1).split())
    return fields


def parse_list_page(html: str, year: int) -> list:
    """解析列表页，返回论文元数据列表。"""
    soup = BeautifulSoup(html, "lxml")
    papers = []

    for dt in soup.select("dt.ptitle"):
        link = dt.find("a", href=True)
        if not link:
            continue

        detail_url = urljoin(BASE_URL, link["href"])
        authors, pdf_url, supp_url, bibtex = _scan_block(_block_nodes(dt))
        bib = parse_bibtex(bibtex)

        papers.append({
            "paper_id": paper_id(detail_url),
            "year": year,
            "title": " ".join(link.get_text(" ", strip=True).split()),
            "authors": "; ".join(authors),
            "n_authors": len(authors),
            "pages": bib.get("pages", ""),
            "booktitle": bib.get("booktitle", ""),
            "pdf_url": pdf_url,
            "supp_url": supp_url,
            "detail_url": detail_url,
            "bibtex": " ".join(bibtex.split()),
        })

    return papers


def parse_abstract(html: str) -> str:
    """从详情页抽取摘要文本。"""
    soup = BeautifulSoup(html, "lxml")
    div = soup.find("div", id="abstract")
    if div is None:
        return ""
    return " ".join(div.get_text(" ", strip=True).split())
