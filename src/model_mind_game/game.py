"""Main game loop for Model Mind Adventure."""
import sys
from typing import Dict, List, Set

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.text import Text

from .llm_client import generate_scene, get_client, synthesize_solution
from .models import MENTAL_MODELS, MODEL_MAP
from .scenarios import SCENARIOS

# Pre-defined insights for reliable gameplay
SCENARIO_INSIGHTS: Dict[str, Dict[str, str]] = {
    "第一章：失语的城": {
        "network": "谣言网络显示，信息不再通过公开广场流动，而是通过少数密道家族控制的暗网传递。切断中心节点即可恢复公共话语。",
        "power_law": "资源分配呈现极端幂律，3%的家族控制了80%的财富。这种不平等破坏了信任，使公开合作变得不可能。",
        "game_theory": "每个居民都陷入囚徒困境——公开说话会被报复，沉默更安全。除非改变激励结构，否则均衡就是集体沉默。",
        "markov": "城市已从『开放交流』稳态转移到了『猜疑稳态』。历史路径不重要，当前状态决定未来。",
        "threshold": "沉默具有阈值效应。当足够多的人选择沉默，剩余者的阈值被触发，级联导致全城失语。",
        "random_walk": "最初的导火索可能是随机的（一个谣言、一次误会），但在无纠错机制下，偏差被无限放大。",
        "rugged_landscape": "城市被困在『猜疑』的局部最优。任何个体单方面改变都会受损，所以系统无法自发跳出这个陷阱。",
    },
    "第二章：瘟疫与舞会": {
        "network": "舞会是高度连接的超级传播节点。少数社交名媛连接了不同的贵族圈子。",
        "power_law": "感染人数呈现幂律，少数舞会导致了绝大多数传播案例。",
        "game_theory": "每个贵族都知道舞会有风险，但缺席会被排斥。这是一个典型的协调失败/囚徒困境。",
        "markov": "疫情状态转移只取决于当前感染率，与最初病源无关。当前处于爆发临界点。",
        "threshold": "每个贵族参加舞会的阈值不同。但当感染率超过某个临界点，级联式退席才会开始。",
        "random_walk": "病毒传播具有随机性，精准预测下一场爆发的时间几乎不可能。",
        "rugged_landscape": "公共卫生政策被困在『封锁』和『开放』两个局部最优之间，中间状态难以维持。",
    },
    "第三章：股市的叹息": {
        "network": "金融机构高度互联。一家中小型机构的违约会通过债务网络引发连锁反应。",
        "power_law": "市场回报呈现幂律分布。十年的低波动让人们忽视了尾部风险，但幂律意味着大崩溃始终可能。",
        "game_theory": "每个机构都知道杠杆率过高，但如果别人都在加杠杆，单方面降低杠杆会失去市场份额。这是逐底竞争。",
        "markov": "市场已从『乐观稳态』转移到了『恐慌稳态』。一旦转移发生，很难快速恢复。",
        "threshold": "崩溃具有阈值。当违约消息越过投资者的心理阈值，恐慌级联开始。",
        "random_walk": "资产价格遵循随机游走。十年上涨只是历史路径的一部分，不保证未来方向。",
        "rugged_landscape": "金融体系被困在『高杠杆高增长』的局部最优。探索更稳健的结构需要短期代价。",
    },
}

console = Console()


def print_title():
    console.print(Panel.fit(
        "[bold bright_cyan]模型思维冒险[/bold bright_cyan]\n"
        "[dim]Model Mind Adventure[/dim]\n"
        "——没有单一模型能解释一切",
        border_style="bright_cyan",
    ))


def print_models():
    console.print("\n[bold]可用的思维模型：[/bold]")
    for m in MENTAL_MODELS:
        console.print(f"  [{m.color}]{m.id:<18}[/{m.color}] {m.name_zh} — {m.description}")
    console.print()


def run_scenario(scenario, llm_client) -> bool:
    insights: Set[str] = set()
    history_blocks: List[str] = []
    scenario_insights = SCENARIO_INSIGHTS.get(scenario.title, {})

    console.print(Panel(
        f"[bold]{scenario.title}[/bold]\n\n{scenario.base_setting}\n\n"
        f"[dim]{scenario.hint}[/dim]",
        border_style="blue",
    ))

    while True:
        console.print(Rule())
        console.print(
            f"当前收集洞察：{len(insights)} / 需要至少 {scenario.required_insights} 个"
        )
        choice = Prompt.ask(
            "\n[操作] (m)选择模型观察  (i)查看已收集洞察  (s)尝试综合解答  (n)跳过本章",
            choices=["m", "i", "s", "n"],
            default="m",
        )

        if choice == "n":
            return True

        if choice == "i":
            if not insights:
                console.print("[yellow]你还没有收集到任何洞察。[/yellow]")
            else:
                console.print("[bold]已收集的洞察：[/bold]")
                for idx, ins in enumerate(insights, 1):
                    console.print(f"  {idx}. {ins}")
            continue

        if choice == "s":
            if len(insights) < scenario.required_insights:
                console.print(
                    f"[red]洞察不足（{len(insights)}/{scenario.required_insights}）。"
                    f"你需要更多视角。[/red]"
                )
                continue

            console.print("[bold green]你尝试综合所有洞察，给出解答...[/bold green]")
            with console.status("[bold green]AI正在评估你的综合思维..."):
                result = synthesize_solution(
                    scenario.title, scenario.base_setting, list(insights), llm_client
                )
            if result.startswith("[成功]") or "成功" in result:
                console.print(Panel(
                    f"[bold green]{result}[/bold green]",
                    border_style="green",
                ))
                return True
            else:
                console.print(Panel(
                    f"[bold yellow]{result}[/bold yellow]",
                    border_style="yellow",
                ))
            continue

        if choice == "m":
            console.print("\n可用的模型：")
            for idx, m in enumerate(MENTAL_MODELS, 1):
                tag = "✓" if m.id in {k for k, v in scenario_insights.items() if v in insights} else " "
                console.print(f"  [{m.color}]{idx}. [{tag}] {m.name_zh} ({m.name})[/{m.color}]")
            model_choices = [str(i) for i in range(1, len(MENTAL_MODELS) + 1)]
            model_idx = int(Prompt.ask("选择模型编号", choices=model_choices)) - 1
            model = MENTAL_MODELS[model_idx]

            if model.id in {k for k, v in scenario_insights.items() if v in insights}:
                console.print("[dim]你已经用这个视角观察过了，但世界永远有新的细节。[/dim]")

            with console.status(f"[bold {model.color}]正在通过 {model.name_zh} 的透镜观察世界..."):
                history = "\n".join(history_blocks[-3:])
                scene_text = generate_scene(
                    scenario.title, scenario.base_setting, model, history, llm_client
                )

            console.print(Panel(
                f"[bold {model.color}]{model.name_zh} 视角[/bold {model.color}]\n\n{scene_text}",
                border_style=model.color,
            ))

            # Record insight
            insight = scenario_insights.get(model.id)
            if insight:
                if insight not in insights:
                    insights.add(insight)
                    console.print(f"\n[green]★ 获得洞察：{insight}[/green]")
                else:
                    console.print(f"\n[dim]（已记录此洞察）[/dim]")

            history_blocks.append(f"通过{model.name_zh}观察：{scene_text[:80]}...")


def main():
    print_title()
    console.print(
        "\n欢迎来到[bold]模型思维冒险[/bold]。"
        "在这个游戏中，你将学习查理·芒格和斯科特·佩奇倡导的多模型思维："
        "[italic]没有任何一个模型能够完整描述现实，但多个模型的交叉可以生成智慧。[/italic]\n"
    )
    print_models()

    llm_client = get_client()
    if llm_client:
        console.print("[green]✓ AI场景生成已就绪（DeepSeek API）[/green]\n")
    else:
        console.print("[yellow]⚠ AI场景生成未就绪，将使用本地描述继续游戏[/yellow]\n")

    for scenario in SCENARIOS:
        success = run_scenario(scenario, llm_client)
        if not success:
            console.print("[red]你未能解开谜题，冒险结束。[/red]")
            sys.exit(0)
        console.print(Rule(style="green"))

    console.print(Panel.fit(
        "[bold bright_cyan]恭喜你完成了所有章节！[/bold bright_cyan]\n\n"
        "你亲身体验了多模型思维的力量：\n"
        "  • 孔多塞陪审团定理——多数视角比单一视角更可靠\n"
        "  • 多样性预测定理——多样性的洞察相互抵消误差\n"
        "  • 没有模型是完美的，但模型集合可以逼近真理\n\n"
        "愿你在现实世界中，也能成为一个多模型思考者。",
        border_style="bright_cyan",
    ))


if __name__ == "__main__":
    main()
