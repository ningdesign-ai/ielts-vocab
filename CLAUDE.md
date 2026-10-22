# 雅思背单词 App

用户自己用的雅思背单词网页 App，单页 HTML，通过网址访问（也支持添加到 iPhone 主屏幕）。

## 文件结构

- `index.html` — 生成后的完整 App（**不要直接改这个文件**，会被 build 覆盖）
- `template.html` — App 的模板 / 源代码，改界面就改这里（里面有 `__WORDS_JSON__` 占位符）
- `words.json` — 5300 个雅思单词的数据（单词、美音、英音、音标、释义、例句）
- `build.py` — 构建脚本：把 words.json 填进 template.html，生成 index.html

## 构建

改完 `template.html` 或 `words.json` 后，运行：

```bash
python3 build.py
```

## 部署

App 部署在 GitHub Pages，网址：https://ningdesign-ai.github.io/ielts-vocab/ （仓库 ningdesign-ai/ielts-vocab，main 分支根目录）。

改完代码后：`git add -A && git commit -m "..." && git push origin main`，等 1~2 分钟 GitHub 自动部署，用户手机刷新网址即可看到。

## 已实现的功能

- 学习页：单词流（每天 50 词一组滑动刷）、美音 / 英音发音、音标、释义、例句、收藏按钮
- 全部单词页：分组可展开 / 收起、收藏词标黄、只看收藏开关

## 用户情况

- 用户是中文非技术用户，沟通用中文大白话。
- 改完 `template.html` 记得运行 `python3 build.py` 重新生成 `index.html`，否则用户手机上看不到变化。
- 用户有梯子（电脑和手机都有）。
- 2026-10 曾尝试加「每日英语」（BBC 6 Minute English）页，因音频与文字稿对不上、体验不好，用户决定移除。相关文件 fetch_bbc.py、bbc.json 已删除，如需恢复可从 git 历史（commit 89797eb）找回。
