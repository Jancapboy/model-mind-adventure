# 模型思维冒险 (Model Mind Adventure)

一款基于斯科特·佩奇《模型思维》核心理念的文字冒险游戏。

## 核心理念

> "要想成为一个有智慧的人，你必须拥有多个模型。"
> —— 查理·芒格

在这个游戏中，没有任何单一的思维模型能够完整解释一个复杂场景。你必须像真正的多模型思考者一样，切换不同的认知透镜，收集多样的洞察，然后综合它们来解开谜题。

## 游戏特色

### 🧠 20 种思维模型
分为三组，覆盖个体、群体和系统层面：

**个体行为模型（7个）**
- 网络模型、幂律分布、博弈论、马尔可夫模型、随机游走、阈值模型、崎岖景观

**群体动态模型（5个）**
- 谢林隔离、格兰诺维特阈值、创新扩散、SIR传染病、复制者动态

**系统性结果模型（8个）**
- 正态分布、长尾、多样性预测定理、群体智慧、信号模型、机制设计、集体行动、路径依赖

### 🤖 AI 驱动的场景生成
- 每个场景由 AI 根据模型特性生成独特的视角描述
- AI 智能选择最相关的 7 个模型供玩家探索
- 所有 20 个模型都有预定义的洞察，确保游戏深度

### 📚 模型图书馆
- 随时查看任意模型的详细介绍
- 学习《模型思维》中的核心概念
- 按组浏览，系统学习

### ✨ 无限扩展：AI 生成新章节
完成所有预设章节后，游戏不会结束！你可以选择：

- **随机生成** - 让 AI 自由创造全新场景
- **自定义主题** - 提供你的想法（如"AI觉醒的世界"），AI 转换成完整章节
- AI 自动为新场景生成 20 个模型的洞察

场景存储在 `scenarios.json`，可随时编辑添加。

## 安装与运行

### 1. 克隆项目
```bash
git clone https://github.com/Jancapboy/model-mind-adventure.git
cd model-mind-adventure
```

### 2. 配置 API Key
创建 `.env` 文件：
```bash
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
```

### 3. 安装依赖
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 4. 运行游戏
```bash
model-mind
```

## 游戏流程

1. **选择场景** - 从预设章节开始，或加载自定义场景
2. **选择模型** - AI 推荐 7 个最相关的思维模型
3. **收集洞察** - 通过不同模型视角观察场景，收集关键洞察
4. **综合解答** - 收集足够洞察后，尝试综合理解并给出解答
5. **AI 评估** - AI 评估你的综合思维能力
6. **继续或生成** - 完成所有章节后，可让 AI 生成无限新章节

## 添加自定义场景

编辑 `scenarios.json`：

```json
{
  "scenarios": [
    {
      "id": "chapter_4",
      "title": "第四章：你的标题",
      "base_setting": "场景描述...",
      "required_insights": 3,
      "hint": "给玩家的提示"
    }
  ]
}
```

## 技术栈

- Python 3.10+
- Rich（终端 UI）
- OpenAI SDK（调用 DeepSeek API）

## 项目架构

```
model-mind-adventure/
├── scenarios.json          # 场景配置文件（可编辑）
├── .env                    # API Key 配置
├── src/model_mind_game/
│   ├── __init__.py
│   ├── models.py           # 20个思维模型定义
│   ├── scenarios.py        # 场景加载/保存
│   ├── llm_client.py       # DeepSeek API 客户端 + 场景生成
│   └── game.py             # 主游戏循环 + AI 章节生成
└── README.md
```

## 许可证

MIT License

---

*愿你在现实世界中，也能成为一个多模型思考者。* 🌌
