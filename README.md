# 墨客排版 inker-layout

专为微信公众号打造的内容排版 Skill。十种风格主题，九种 SVG 交互组件，三阶段问答式引导。


## 核心能力

- 三阶段问答式引导 —— 十个问题分三批，从标题、风格、配图到 SVG 交互和收尾方式，答完确认再生成
- 十种风格主题 —— 时尚、潮流、艺术、国风、极简、科技、生活、奢华、编辑、品牌，每种含完整配色和字体方案
- 九种 SVG 交互组件 —— 轮播图、点击揭示卡片、图片热区、展开卡片、时间线、滚动触发、前后对比、进度条、手风琴
- HTML 校验器 —— 11 项自动检测，确保代码在微信中正常渲染
- 交付即导入 —— 源码粘贴进微信后台「源代码」模式即可

## 使用方法

把 SKILL.md 丢给 WorkBuddy，告诉它：

> 帮我安装这个 Skill

装好后说「帮我排版公众号文章」，跟随 Agent 的引导回答即可。

## 文件结构

```
inker-layout/
├── SKILL.md                              # 主指令文件
├── scripts/
│   └── validate_mp.py                    # HTML 兼容性校验
├── references/
│   ├── wechat-layout-guide.md            # 排版规则与约束
│   ├── wechat-svg-guide.md               # SVG 交互模式
│   └── wechat-design-tokens.md           # 十种风格设计令牌
└── assets/templates/
    ├── article-*.html                    # 风格专属模板（12个）
    ├── article-*-svg.html                # 风格+SVG 组合模板（6个）
    └── svg/
        ├── svg-carousel.html             # 轮播图
        ├── svg-click-reveal.html         # 点击揭示卡片
        ├── svg-click-hotspot.html        # 图片热区
        ├── svg-expand-cards.html         # 自动展开卡片
        ├── svg-timeline.html             # 时间线动画
        ├── svg-scroll-trigger.html       # 滚动触发
        ├── svg-comparison.html           # 前后对比
        ├── svg-progress.html             # 进度条
        └── svg-accordion.html            # 手风琴面板
```

## 作者

刘淮安LIUHUAIAN
