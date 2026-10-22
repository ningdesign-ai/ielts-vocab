import json

words = json.load(open('words.json', encoding='utf-8'))
tpl = open('template.html', encoding='utf-8').read()
j = json.dumps(words, ensure_ascii=False, separators=(',', ':'))
assert '__WORDS_JSON__' in tpl, 'template 缺少占位符 __WORDS_JSON__'
open('index.html', 'w', encoding='utf-8').write(tpl.replace('__WORDS_JSON__', j))
print('已生成 index.html，词条数:', len(words))
