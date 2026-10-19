import json

words = json.load(open('words.json', encoding='utf-8'))
bbc = json.load(open('bbc.json', encoding='utf-8'))
tpl = open('template.html', encoding='utf-8').read()
j = json.dumps(words, ensure_ascii=False, separators=(',', ':'))
b = json.dumps(bbc, ensure_ascii=False, separators=(',', ':'))
assert '__WORDS_JSON__' in tpl, 'template 缺少占位符 __WORDS_JSON__'
assert '__BBC_JSON__' in tpl, 'template 缺少占位符 __BBC_JSON__'
out = tpl.replace('__WORDS_JSON__', j).replace('__BBC_JSON__', b)
open('index.html', 'w', encoding='utf-8').write(out)
print('已生成 index.html，词条数:', len(words), '，BBC 期数:', len(bbc.get('episodes', [])))
