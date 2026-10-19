# 雅思背单词 App

用户自己用的雅思背单词网页 App，单页 HTML，添加到 iPhone 主屏幕使用。

## 文件结构

- `index.html` — 生成后的完整 App（**不要直接改这个文件**，会被 build 覆盖）
- `template.html` — App 的模板 / 源代码，改界面就改这里（里面有 `__WORDS_JSON__` 和 `__BBC_JSON__` 两个占位符）
- `words.json` — 5300 个雅思单词的数据（单词、美音、英音、音标、释义、例句）
- `bbc.json` — 最近 4 期 BBC 6 Minute English 的数据（标题、日期、音频、问题、词汇表、完整对话文字稿），由 fetch_bbc.py 生成
- `fetch_bbc.py` — 抓取 BBC 6 Minute English 的脚本（走梯子代理 127.0.0.1:7890），重跑即更新 bbc.json
- `build.py` — 构建脚本：把 words.json 和 bbc.json 填进 template.html，生成 index.html

## 构建

改完 `template.html`、`words.json` 或 `bbc.json` 后，运行：

```bash
python3 build.py
```

## 部署

App 部署在 GitHub Pages，网址：https://ningdesign-ai.github.io/ielts-vocab/ （仓库 ningdesign-ai/ielts-vocab，main 分支根目录）。

改完代码后：`git add -A && git commit -m "..." && git push origin main`，等 1~2 分钟 GitHub 自动部署，用户手机刷新网址即可看到。

## 更新每日英语（BBC）

用户说「更新文章」「更新 BBC」时，完整流程：
1. `python3 fetch_bbc.py`（需梯子代理 127.0.0.1:7890 开着）
2. `python3 build.py`
3. `git add -A && git commit -m "更新 BBC" && git push origin main`
4. 等 1~2 分钟，提醒用户手机刷新网址。

## 已实现的功能

- 学习页：单词流（每天 50 词一组滑动刷）、美音 / 英音发音、音标、释义、例句、收藏按钮
- 全部单词页：分组可展开 / 收起、收藏词标黄、只看收藏开关
- 每日英语页：最近 4 期 BBC 6 Minute English，音频播放（需梯子）、问题、词汇表、完整对话文字稿（可离线看）

## 用户情况

- 用户是中文非技术用户，沟通用中文大白话。
- 改完 `template.html` 记得运行 `python3 build.py` 重新生成 `index.html`，否则用户手机上看不到变化。
- 用户有梯子（电脑和手机都有），但 BBC 域名本身被墙，抓取/播放都依赖梯子。
