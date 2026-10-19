#!/usr/bin/env python3
# 抓取 BBC 6 Minute English 最近几期，生成 bbc.json
# 用法：python3 fetch_bbc.py
# 依赖梯子代理（默认 127.0.0.1:7890，可在下方 PROXY 修改）

import json, re, html, ssl, time, urllib.request
from email.utils import parsedate_to_datetime

PROXY = '127.0.0.1:7890'   # 梯子代理地址，改这里
N = 4                        # 抓最近几期
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

def parse_intro(desc):
    idx = desc.find('6 Minute English now has')
    if idx >= 0:
        desc = desc[:idx]
    return clean(desc)

def strip_links(raw):
    raw = re.sub(r'<a\b[^>]*>', '', raw)
    return raw.replace('</a>', '')

def extract_question(raw):
    m = re.search(r"This week's question\s*</h3>(.*?)(?=<h3)", raw, re.S)
    if not m:
        return '', []
    seg = clean(m.group(1))
    parts = re.split(r'\s*[abc]\)\s*', seg)
    question = re.sub(r'\s*Listen to the programme.*$', '', parts[0]).strip()
    options = []
    for p in parts[1:]:
        p = re.sub(r'\s*Listen to the programme.*$', '', p).strip()
        if p:
            options.append(p)
    return question, options

def parse_episode(raw):
    raw = strip_links(raw)
    question, options = extract_question(raw)
    vocab, transcript = [], []

    v = re.search(r"<h3[^>]*>\s*Vocabulary\s*</h3>\s*<p>(.*?)</p>", raw, re.S)
    if v:
        for m in re.finditer(r'<strong>([^<]+)</strong>\s*<br\s*/?>\s*(.*?)(?=<strong>|$)', v.group(1), re.S):
            w, d = clean(m.group(1)), clean(m.group(2))
            if w and d:
                vocab.append([w, d])

    t = re.search(r"TRANSCRIPT</strong>", raw)
    if t:
        seg = raw[t.end():]
        for m in re.finditer(r'<strong>([^<]+)</strong>\s*<br\s*/?>\s*(.*?)(?=<strong>|<p[^>]*>\s*<img\s)', seg, re.S):
            sp, tx = clean(m.group(1)), clean(m.group(2))
            if sp and tx:
                transcript.append([sp, tx])

    return question, options, vocab, transcript

def main():
    import xml.etree.ElementTree as ET
    rss = fetch(RSS_URL)
    items = ET.fromstring(rss).findall('.//item')

    episodes = []
    for it in items[:N]:
        title = it.findtext('title')
        dt = parsedate_to_datetime(it.findtext('pubDate'))
        audio = it.find('enclosure').get('url').replace('http://', 'https://', 1)
        desc = it.findtext('description') or ''

        year = dt.year
        yymmdd = dt.strftime('%y%m%d')
        ep_url = 'https://www.bbc.co.uk/learningenglish/english/features/6-minute-english_%d/ep-%s' % (year, yymmdd)

        question, options, vocab, transcript = parse_episode(fetch(ep_url))

        episodes.append({
            'title': title,
            'date': dt.strftime('%Y-%m-%d'),
            'audio': audio,
            'web': ep_url,
            'intro': parse_intro(desc),
            'question': question,
            'options': options,
            'vocab': vocab,
            'transcript': transcript,
        })
        print('已抓取:', title, '·', dt.strftime('%Y-%m-%d'))

    data = {'updated': episodes[0]['date'] if episodes else '', 'episodes': episodes}
    with open('bbc.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print('已生成 bbc.json，共', len(episodes), '期')

if __name__ == '__main__':
    main()
