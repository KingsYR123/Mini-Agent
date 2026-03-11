---
name: generative-ui
description: "生成式 UI 专家。基于 Google 论文《Generative UI》，实现模型动态生成完整交互式 UI。核心架构：Tool Access + System Instructions + Post-processing + 直接渲染。"
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["node"]}}}
---

# 生成式 UI 专家技能 (Generative UI Expert)

基于 Google 论文《Generative UI: LLMs are Effective UI Generators》实现。

## 论文核心发现

| 指标 | 数据 |
|------|------|
| 用户偏好 Generative UI vs Markdown | **82.8%** |
| 与人类专家相当的案例 | **44%** |
| 零错误率（最新模型） | **Gemini 3: 0%** |

---

## 核心架构 (Three Additions)

```
用户提示词
    ↓
┌─────────────────────────────────────────┐
│  1. Tool Access                         │
│     - 图像生成 (DALL-E, Midjourney)      │
│     - 网页搜索 (实时信息获取)             │
│     - 代码执行验证                       │
│     → 结果可给模型 或 直接发给用户        │
├─────────────────────────────────────────┤
│  2. System Instructions                 │
│     - Goal (目标)                        │
│     - Planning (规划思考)                │
│     - Examples (示例)                    │
│     - Technical Specs (技术规格)         │
├─────────────────────────────────────────┤
│  3. Post-processing                     │
│     - 语法修正                           │
│     - 安全过滤                           │
│     - 错误检测                           │
└─────────────────────────────────────────┘
    ↓
Code Artifact (完整网页)
    ↓
直接渲染到用户浏览器
```

### 1. Tool Access（工具访问）
- **图像生成**: 创建配图、图标、背景图
- **网页搜索**: 获取实时信息提升质量
- **结果路由**: 
  - 发给模型 → 提升生成质量
  - 直发浏览器 → 提高效率

### 2. System Instructions（系统指令）
详细指令包含四部分：

**Goal**:
```
创建一个[应用类型]，实现[核心功能]，满足用户需求。
```

**Planning**:
```
1. 分析用户需求和目标
2. 设计 UI 结构和交互流程
3. 规划数据流和状态管理
4. 考虑边界情况和错误处理
```

**Examples**:
```
参考模式：
- 番茄钟：倒计时 + 控制按钮 + 统计面板
- 2048：网格布局 + 滑动手势 + 分数系统
- 天气：卡片展示 + 动态图标 + 预报列表
```

**Technical Specs**:
```
输出格式: 单 HTML 文件（推荐）或 React 组件
样式: CSS-in-JS 或内联样式，使用 CSS 变量
交互: 事件驱动，响应式设计
性能: 首屏加载 < 1s
```

### 3. Post-processing（后处理）
- **JS 语法检查**: 确保无语法错误
- **XSS 安全过滤**: 移除危险代码
- **HTML/CSS 修正**: 修复常见格式问题
- **资源验证**: 检查外部链接有效性

---

## 核心能力

### 1. Code Artifacts - 直接生成完整 UI
- **完整网页**: HTML + CSS + JS 一次性生成
- **直接渲染**: 在浏览器中直接运行，非仅返回代码
- **可交互**: 用户可直接使用，无需二次开发

### 2. 工具增强生成
- 必要时调用图像生成丰富界面
- 搜索实时信息融入应用
- 验证代码功能确保可用

### 3. 多风格支持
- **Classic**: 经典专业风格
- **Wizard Green**: 绿色魔法风格
- 模型会自动适配元素风格

---

## 触发条件

**创建类**: "创建一个..."、"生成..."、"做..."
**交互类**: "交互式..."、"可视化..."、"模拟器"
**游戏类**: "游戏"、"2048"、"贪吃蛇"
**工具类**: "计时器"、"计算器"、"追踪器"

---

## 输出规范

### 完整 Code Artifact 模板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>应用标题</title>
    <style>
        :root {
            --primary: #e94560;
            --bg: #1a1a2e;
            --text: #fff;
        }
        /* 现代简约风格 */
    </style>
</head>
<body>
    <div id="app">
        <!-- UI 结构 -->
    </div>
    <script>
        // 交互逻辑
    </script>
</body>
</html>
```

### System Instructions 生成模板

```markdown
## Goal
创建一个{应用类型}，实现{核心功能}。

## Planning
1. 分析需求：{用户目标和场景}
2. UI 设计：{布局、颜色、交互}
3. 数据流：{状态管理、持久化}
4. 边界处理：{错误、空状态、加载}

## Examples
参考：
- {示例1}
- {示例2}

## Technical Specs
- 格式: 单 HTML 文件
- 样式: 现代简约，CSS 变量
- 交互: 响应式，事件驱动
- 性能: 轻量，无外部依赖
```

---

## 工作流程

```
用户请求
    ↓
[Goal + Planning + Examples + Tech Specs]
    ↓
模型生成 Code Artifact
    ↓
Post-processing (语法 + 安全 + 格式)
    ↓
直接渲染给用户
    ↓
用户即时交互使用
```

---

## 论文关键结论

> "Generative UI 是最新强大模型的**新兴能力** (Emergent Capability)"
> — Gemini 3 达到 0% 错误率

**核心价值**: 模型不仅生成内容，还生成**整个用户界面**，实现真正的"AI 即时创建应用"！
