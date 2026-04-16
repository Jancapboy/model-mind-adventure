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
    # 核心模型组（第1组：解释个体行为）
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
    # 扩展模型组（第2组：解释群体动态）
    MentalModel(
        id="schelling",
        name="Schelling's Segregation Model",
        name_zh="谢林隔离模型",
        description="关注微歧视如何导致宏观隔离、自组织分离。",
        lens_prompt=(
            "请从谢林隔离模型的角度描述这个场景：强调微小的偏好如何导致宏观的分离，"
            "即使个体只是轻微偏好同质性，群体如何自发形成隔离。"
        ),
        color="bright_cyan",
    ),
    MentalModel(
        id="granovetter",
        name="Granovetter's Threshold Model",
        name_zh="格兰诺维特阈值模型",
        description="关注集体行动的阈值、革命与沉默的平衡。",
        lens_prompt=(
            "请从格兰诺维特阈值模型的角度描述这个场景：强调集体行动如何需要"
            "足够多的人突破个人阈值，革命何时爆发，以及沉默的大多数。"
        ),
        color="bright_magenta",
    ),
    MentalModel(
        id="diffusion",
        name="Diffusion of Innovation Model",
        name_zh="创新扩散模型",
        description="关注创新如何在群体中传播、S曲线采纳过程。",
        lens_prompt=(
            "请从创新扩散模型的角度描述这个场景：强调新事物如何在群体中传播，"
            "早期采用者与大众的区别，采纳的S曲线，以及临界质量。"
        ),
        color="bright_green",
    ),
    MentalModel(
        id="sir",
        name="SIR Model",
        name_zh="SIR传染病模型",
        description="关注疾病传播、易感-感染-康复动态、R0值。",
        lens_prompt=(
            "请从SIR传染病模型的角度描述这个场景：强调传播动力学，"
            "基本再生数R0，易感者、感染者、康复者的比例变化，以及群体免疫。"
        ),
        color="bright_red",
    ),
    MentalModel(
        id="replicator",
        name="Replicator Dynamics",
        name_zh="复制者动态模型",
        description="关注策略演化、适者生存、演化稳定策略。",
        lens_prompt=(
            "请从复制者动态的角度描述这个场景：强调不同策略如何在竞争中演化，"
            "成功策略的复制，演化稳定策略，以及策略频率的变化。"
        ),
        color="bright_blue",
    ),
    # 扩展模型组（第3组：解释系统性结果）
    MentalModel(
        id="normal_distribution",
        name="Normal Distribution Model",
        name_zh="正态分布模型",
        description="关注均值回归、极端事件的罕见性、中心极限定理。",
        lens_prompt=(
            "请从正态分布的角度描述这个场景：强调大多数事件集中在均值附近，"
            "极端事件的罕见性，以及统计规律如何约束可能性。"
        ),
        color="white",
    ),
    MentalModel(
        id="long_tail",
        name="Long Tail Model",
        name_zh="长尾模型",
        description="关注利基市场的力量、多样性胜过热门、累积的小众。",
        lens_prompt=(
            "请从长尾模型的角度描述这个场景：强调小众选择的累积力量，"
            "利基市场如何与主流竞争，以及多样性的价值。"
        ),
        color="purple",
    ),
    MentalModel(
        id="diversity_prediction",
        name="Diversity Prediction Theorem",
        name_zh="多样性预测定理",
        description="关注群体智慧、预测误差的分解、多样性的价值。",
        lens_prompt=(
            "请从多样性预测定理的角度描述这个场景：强调群体预测误差如何分解为"
            "个体能力和多样性，以及认知多样性如何提升集体智慧。"
        ),
        color="orange",
    ),
    MentalModel(
        id="wisdom_crowds",
        name="Wisdom of Crowds",
        name_zh="群体智慧模型",
        description="关注独立判断的聚合、误差抵消、集体决策。",
        lens_prompt=(
            "请从群体智慧的角度描述这个场景：强调独立判断的聚合如何产生准确预测，"
            "个体误差如何相互抵消，以及去中心化的价值。"
        ),
        color="bright_white",
    ),
    MentalModel(
        id="signaling",
        name="Signaling Model",
        name_zh="信号模型",
        description="关注信息不对称、可信信号、筛选机制。",
        lens_prompt=(
            "请从信号模型的角度描述这个场景：强调信息不对称如何影响行为，"
            "可信信号的发送与解读，以及信号成本如何维持真实性。"
        ),
        color="bright_red",
    ),
    MentalModel(
        id="mechanism_design",
        name="Mechanism Design",
        name_zh="机制设计模型",
        description="关注激励相容、机制如何塑造行为、规则设计。",
        lens_prompt=(
            "请从机制设计的角度描述这个场景：强调规则如何塑造参与者的激励，"
            "机制如何引导自利行为达成社会目标，以及激励相容的重要性。"
        ),
        color="bright_black",
    ),
    MentalModel(
        id="collective_action",
        name="Collective Action Model",
        name_zh="集体行动模型",
        description="关注搭便车问题、公共物品、群体协调困境。",
        lens_prompt=(
            "请从集体行动模型的角度描述这个场景：强调公共物品的供给困境，"
            "搭便车问题如何阻碍合作，以及克服集体行动困境的策略。"
        ),
        color="green",
    ),
    MentalModel(
        id="path_dependence",
        name="Path Dependence Model",
        name_zh="路径依赖模型",
        description="关注历史锁定、初始条件的重要性、转换成本。",
        lens_prompt=(
            "请从路径依赖的角度描述这个场景：强调早期选择如何锁定未来，"
            "历史偶然性的持续影响，以及转换成本如何维持现状。"
        ),
        color="blue",
    ),
]

MODEL_MAP = {m.id: m for m in MENTAL_MODELS}
