# 模型思维冒险 (Model Mind Adventure)

一款基于斯科特·佩奇《模型思维》核心理念的文字冒险游戏。

## 核心理念

> "要想成为一个有智慧的人，你必须拥有多个模型。"
> —— 查理·芒格

在这个游戏中，没有任何单一的思维模型能够完整解释一个复杂场景。你必须像真正的多模型思考者一样，切换不同的认知透镜，收集多样的洞察，然后综合它们来解开谜题。

## 游戏机制

- **AI 辅助场景生成**：同一个场景，通过不同的思维模型观察，会得到截然不同的描述。
- **7 种思维模型**：网络模型、幂律分布、博弈论、马尔可夫模型、随机游走、阈值模型、崎岖景观。
- **综合解答**：收集足够的洞察后，AI 会评估你的综合思维能力。

## 安装与运行

```bash
cd ~/workspace/model-mind-adventure
python -m venv .venv
source .venv/bin/activate
pip install -e .
model-mind
```

## 技术栈

- Python 3.10+
- Rich（终端 UI）
- OpenAI SDK（调用 DeepSeek API）

## 项目架构

```
src/model_mind_game/
├── __init__.py
├── models.py       # 思维模型定义
├── scenarios.py    # 场景设定
├── llm_client.py   # DeepSeek API 客户端
└── game.py         # 主游戏循环
```
