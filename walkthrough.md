# 📚 自考英语速记打卡 (zk-english-flashcards) 项目全景总结与接棒指南

> **当前构建版本**: `v1.5.6`  
> **线上发布地址**: [https://santalin87.github.io/zk-english-flashcards/](https://santalin87.github.io/zk-english-flashcards/)  
> **本地工作区目录**: `d:\User\Documents\自考英语`  
> **核心仓库**: `santalin87/zk-english-flashcards`

---

## 🌟 一、 为什么创建此总结文档？

本文档记录了自考英语闪卡 Web App 从 `v1.0.0` 到 `v1.5.6` 的完整技术架构、算法实现与所有重大功能迭代。在新开窗口进行后续开发或接棒时，AI 可直接读取本文档，**100% 无缝接棒**后续所有优化细节。

---

## 🛠️ 二、 项目架构与核心技术实现

1. **单文件零依赖 Web 应用**:
   - 主入口文件: [index.html](file:///d:/User/Documents/自考英语/index.html) 和 [自考英语核心词汇_全功能互动闪卡.html](file:///d:/User/Documents/自考英语/自考英语核心词汇_全功能互动闪卡.html)
   - 核心构建脚本: [build_full_flashcard_app.py](file:///d:/User/Documents/自考英语/build_full_flashcard_app.py)
   - 数据集: 包含 1311 自考核心词汇（[prep_1_500_data.py](file:///d:/User/Documents/自考英语/prep_1_500_data.py) 前 117 精编词 + [target_words_data.json](file:///d:/User/Documents/自考英语/target_words_data.json) 后 1194 全量词）。

2. **核心算法与模块**:
   - **艾宾浩斯复习算法**：基于 `1, 2, 4, 8, 15` 天复习间隔，全量打卡进度与生词库保存在浏览器 `localStorage`（刷新/断网不丢失）。
   - **真实学习行为打卡**：只有当天产生了刷卡记录（标记“记住”/“没记住”），打卡天数才会递增，漏刷超过 1 天自动重置。
   - **今日任务每日锁定 + 🔀 随机打卡**：每天任务词单自动锁定存入 `localStorage`，防切换打乱；支持手动点击“🔀 随机打卡”重新抽词。
   - **Spoonfed Anki 共享牌组融合**：解包 `Spoonfed_Chinese.apkg`（7335 条句对），匹配替换 871 个自考词汇为 Anki 原装地道短句。
   - **词根词缀三大分类框**：44 个自考常考词根词缀分类为 **🌳 核心词根 (Roots)**、**🔤 高频前缀 (Prefixes)**、**🔠 常用后缀 (Suffixes)** 3 大容器框。

---

## 📋 三、 历史版本演进记录 (v1.0.0 ~ v1.5.6)

| 版本 | 核心功能改进 | 解决的实际问题 / 优化成果 |
| :--- | :--- | :--- |
| **v1.5.6** | **Anki Spoonfed 共享牌组 7335 例句全量融合** | 解包 `Spoonfed_Chinese.apkg`，871 个词直接替换为 Anki 社区原装地道例句。 |
| **v1.5.5** | **彻底清除所有 generic 机械模板句** | 清洗 388 个生硬废话模板句（如 `This is a useful face`），替换为 100% 自然地道英语表达。 |
| **v1.5.4** | **AI 量身定制 4-8 词极简助记例句重构** | 限制例句 4-8 词，周边 100% 基础常用词，无 `...` 碎片句。 |
| **v1.5.3** | **今日任务每日锁定 + 🔀 随机打卡** | 每天任务词单自动锁定防打乱，支持手动点击“🔀 随机打卡”重新抽词。 |
| **v1.5.2** | **闪卡直达模式 + 词根词缀三大分类框** | 打开应用直达闪卡；词根词缀重构为词根、前缀、后缀 3 大分类大框。 |
| **v1.5.1** | **真实打卡计数器重构** | 只有今天产生真实刷卡行为才触发打卡 +1，断档 2 天以上自动归零。 |
| **v1.5.0** | **44 词根词缀库扩充 + 真实 Latin/Greek 拆解** | 补充 44 个自考核心词根；清洗机械式词根剥离（如 `re- + frigerator`）。 |
| **v1.4.0** | **前缀优先搜索 + 词根卡片专区** | 搜索框优化为 Prefix-First 首字母优先；精简顶部导航标签。 |
| **v1.3.0** | **纯英文清单预览模式** | 增加列表模式与搜索框，点击清单中任意单词切入闪卡。 |
| **v1.0 - v1.2**| **单播发音引擎 + 艾宾浩斯复习 + PWA** | 解决手机端发音音色不一致；提供 0.8/1.0/1.2 语速调节；支持全屏沉浸 PWA。 |

---

## 💡 使用与部署指南

1. **本地调试**: 直接在浏览器中打开 [index.html](file:///d:/User/Documents/自考英语/index.html)。
2. **重新编译**: 运行 `python build_full_flashcard_app.py` 即可。
3. **GitHub Pages 部署**: 推送代码至 `main` 分支，GitHub Pages 会自动构建并发布到 [https://santalin87.github.io/zk-english-flashcards/](https://santalin87.github.io/zk-english-flashcards/)。
