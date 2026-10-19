#!/usr/bin/env python3
# 抓取 BBC 6 Minute English 最新一期，生成 bbc.json
# 用法：python3 fetch_bbc.py
# 依赖梯子代理（默认 127.0.0.1:7890，可在下方 PROXY 修改）

import json, re, html, ssl, time, urllib.request
from email.utils import parsedate_to_datetime

PROXY = '127.0.0.1:7890'   # 梯子代理地址，改这里
RSS_URL = 'https://podcasts.files.bbci.co.uk/p02pc9tn.rss'

def fetch(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    proxy = urllib.request.ProxyHandler({'http': 'http://' + PROXY, 'https': 'http://' + PROXY})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPSHandler(context=ctx))
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)'})
    last = None
    for _ in range(3):
        try:
            return opener.open(req, timeout=40).read().decode('utf-8', 'ignore')
        except Exception as e:
            last = e
            time.sleep(2)
    raise last

def clean(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = s.replace('&nbsp;', ' ')
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()

def strip_links(raw):
    raw = re.sub(r'<a\b[^>]*>', '', raw)
    return raw.replace('</a>', '')

def parse_transcript(raw):
    raw = strip_links(raw)
    transcript = []
    t = re.search(r"TRANSCRIPT</strong>", raw)
    if t:
        seg = raw[t.end():]
        # 截断到对话结束后的「Next episode」图片为止，去掉页面底部垃圾
        end = re.search(r'alt="Next episode"', seg)
        if end:
            img_start = seg.rfind('<img', 0, end.start())
            seg = seg[:img_start] if img_start >= 0 else seg[:end.start()]
        # 按「说话人名字 + 换行」切分，句子内部的加粗词不会被误切
        parts = re.split(r'<strong>([^<]+)</strong>\s*<br\s*/?>', seg)
        for i in range(1, len(parts) - 1, 2):
            sp = clean(parts[i])
            tx = clean(parts[i + 1])
            if sp and tx:
                transcript.append([sp, tx])
    return transcript

def main():
    import xml.etree.ElementTree as ET
    items = ET.fromstring(fetch(RSS_URL)).findall('.//item')
    it = items[0]  # 最新一期
    title = it.findtext('title')
    dt = parsedate_to_datetime(it.findtext('pubDate'))
    ep_url = 'https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_%d/ep-%s' % (dt.year, dt.strftime('%y%m%d'))
    raw = fetch(ep_url)

    # 用网页里配套的音频（和文字稿同一版，能对上）
    m = re.search(r'https?://[^"\'\s]+_download\.mp3', raw)
    audio = m.group(0).replace('http://', 'https://', 1) if m else ''

    data = {
        'updated': dt.strftime('%Y-%m-%d'),
        'episodes': [{
            'title': title,
            'date': dt.strftime('%Y-%m-%d'),
            'audio': audio,
            'web': ep_url,
            'summary': '',
            'transcript': parse_transcript(raw),
        }],
    }
    json.dump(data, open('bbc.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('已抓取最新一期:', title, '·', dt.strftime('%Y-%m-%d'), '· 对话', len(data['episodes'][0]['transcript']), '轮')

if __name__ == '__main__':
    main()
