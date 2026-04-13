"""Mental models from the book 'Model Thinking'."""
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class MentalModel:
    id: str
    name: str
    name_zh: str
    description: str
    lens_prompt: str
    color: str


MENTAL_MODELS: List[MentalModel] = [
    MentalModel(
        id="network",
        name="Network Model",
        name_zh="网络模型",
        description="关注节点之间的连接、中心性和信息流动。",
        lens_prompt=(
            "请从网络模型的角度描述这个场景：强调人物/实体之间的连接关系，"
            "谁是中心节点，信息如何流动，结构洞在哪里，以及网络的脆弱性。"
        ),
        color="cyan",
    ),
    MentalModel(
        id="power_law",
        name="Power Law Model",
        name_zh="幂律分布模型",
        description="关注不平等、马太效应、少数大赢家和多数输家。",
        lens_prompt=(
            "请从幂律分布的角度描述这个场景：强调资源/影响力的极度不平等，"
            "是否存在马太效应（更多导致更多），极端值的影响，以及长尾分布。"
        ),
        color="red",
    ),
    MentalModel(
        id="game_theory",
        name="Game Theory Model",
        name_zh="博弈论模型",
        description="关注策略互动、纳什均衡、囚徒困境和激励结构。",
        lens_prompt=(
            "请从博弈论的角度描述这个场景：强调各参与者的策略选择、激励结构、"
            "可能的均衡点、囚徒困境或协调问题，以及占优策略。"
        ),
        color="yellow",
    ),
    MentalModel(
        id="markov",
        name="Markov Model",
        name_zh="马尔可夫模型",
        description="关注状态转移、路径依赖和长期稳态。",
        lens_prompt=(
            "请从马尔可夫模型的角度描述这个场景：强调当前状态如何决定未来，"
            "状态转移的可能性，路径依赖性，以及长期可能收敛到的稳态。"
        ),
        color="green",
    ),
    MentalModel(
        id="random_walk",
        name="Random Walk Model",
        name_zh="随机游走模型",
        description="关注不可预测性、累积变化和回归均值。",
        lens_prompt=(
            "请从随机游走的角度描述这个场景：强调事件的不可预测性、"
            "历史路径的累积效应、波动性和回归均值的倾向。"
        ),
        color="blue",
    ),
    MentalModel(
        id="threshold",
        name="Threshold Model",
        name_zh="阈值模型",
        description="关注临界点、级联效应和集体行为。",
        lens_prompt=(
            "请从阈值模型的角度描述这个场景：强调个体行动的临界点，"
            "级联效应如何触发，小变化如何导致大结果，以及群体行为的爆发。"
        ),
        color="magenta",
    ),
    MentalModel(
        id="rugged_landscape",
        name="Rugged Landscape Model",
        name_zh="崎岖景观模型",
        description="关注局部最优、探索与开发的权衡、适应的困难。",
        lens_prompt=(
            "请从崎岖景观模型的角度描述这个场景：强调局部最优陷阱，"
            "改变路径的困难，探索与开发的权衡，以及适应和进化的挑战。"
        ),
        color="bright_yellow",
    ),
]

MODEL_MAP = {m.id: m for m in MENTAL_MODELS}
