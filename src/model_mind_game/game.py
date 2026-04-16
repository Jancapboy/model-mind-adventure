"""Main game loop for Model Mind Adventure."""
import sys
from typing import Dict, List, Set, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.columns import Columns

from .llm_client import generate_scene, get_client, synthesize_solution, select_models_for_scenario
from .models import MENTAL_MODELS, MODEL_MAP
from .scenarios import SCENARIOS

# 模型分组定义
MODEL_GROUPS = {
    "individual": {
        "name": "个体行为模型",
        "models": ["network", "power_law", "game_theory", "markov", "random_walk", "threshold", "rugged_landscape"],
        "description": "解释个体如何决策、互动和演化"
    },
    "collective": {
        "name": "群体动态模型", 
        "models": ["schelling", "granovetter", "diffusion", "sir", "replicator"],
        "description": "解释群体如何涌现集体行为"
    },
    "systemic": {
        "name": "系统性结果模型",
        "models": ["normal_distribution", "long_tail", "diversity_prediction", "wisdom_crowds", 
                   "signaling", "mechanism_design", "collective_action", "path_dependence"],
        "description": "解释宏观层面的模式和结构"
    }
}

# Pre-defined insights for reliable gameplay
SCENARIO_INSIGHTS: Dict[str, Dict[str, str]] = {
    "第一章：失语的城": {
        "network": "谣言通过少数家族控制的暗网流动，而非公开广场。切断中心节点即可恢复公共话语。",
        "power_law": "资源分配呈现极端幂律，3%的家族控制了80%的财富。这种不平等破坏了信任，使公开合作变得不可能。",
        "game_theory": "每个居民都陷入囚徒困境——公开说话会被报复，沉默更安全。除非改变激励结构，否则均衡就是集体沉默。",
        "markov": "城市已从『开放交流』稳态转移到了『猜疑稳态』。历史路径不重要，当前状态决定未来。",
        "threshold": "沉默具有阈值效应。当足够多的人选择沉默，剩余者的阈值被触发，级联导致全城失语。",
        "random_walk": "最初的导火索可能是随机的（一个谣言、一次误会），但在无纠错机制下，偏差被无限放大。",
        "rugged_landscape": "城市被困在『猜疑』的局部最优。任何个体单方面改变都会受损，所以系统无法自发跳出这个陷阱。",
        "schelling": "即使居民只是轻微偏好与同类聚集，长期演化也会导致社会网络的自然隔离，加剧失语。",
        "granovetter": "打破沉默需要足够多的人同时突破个人阈值。少数人勇敢发声无法改变均衡，需要临界质量。",
        "collective_action": "恢复公共话语是公共物品，存在严重搭便车问题。每个人都希望别人先开口，自己坐享其成。",
    },
    "第二章：瘟疫与舞会": {
        "network": "舞会是高度连接的超级传播节点。少数社交名媛连接了不同的贵族圈子。",
        "power_law": "感染人数呈现幂律，少数舞会导致了绝大多数传播案例。",
        "game_theory": "每个贵族都知道舞会有风险，但缺席会被排斥。这是一个典型的协调失败/囚徒困境。",
        "markov": "疫情状态转移只取决于当前感染率，与最初病源无关。当前处于爆发临界点。",
        "threshold": "每个贵族参加舞会的阈值不同。但当感染率超过某个临界点，级联式退席才会开始。",
        "random_walk": "病毒传播具有随机性，精准预测下一场爆发的时间几乎不可能。",
        "rugged_landscape": "公共卫生政策被困在『封锁』和『开放』两个局部最优之间，中间状态难以维持。",
        "sir": "疫情遵循SIR动力学。当前处于指数增长阶段，R0>1意味着必须干预才能避免全民感染。",
        "diffusion": "防疫知识在贵族中缓慢扩散，早期采用者（谨慎派）与晚期大众（享乐派）的鸿沟加剧了协调困境。",
        "granovetter": "集体抵制舞会需要足够多贵族同时改变行为。在缺乏协调机制的情况下，个人阈值难以被突破。",
    },
    "第三章：股市的叹息": {
        "network": "金融机构高度互联。一家中小型机构的违约会通过债务网络引发连锁反应。",
        "power_law": "市场回报呈现幂律分布。十年的低波动让人们忽视了尾部风险，但幂律意味着大崩溃始终可能。",
        "game_theory": "每个机构都知道杠杆率过高，但如果别人都在加杠杆，单方面降低杠杆会失去市场份额。这是逐底竞争。",
        "markov": "市场已从『乐观稳态』转移到了『恐慌稳态』。一旦转移发生，很难快速恢复。",
        "threshold": "崩溃具有阈值。当违约消息越过投资者的心理阈值，恐慌级联开始。",
        "random_walk": "资产价格遵循随机游走。十年上涨只是历史路径的一部分，不保证未来方向。",
        "rugged_landscape": "金融体系被困在『高杠杆高增长』的局部最优。探索更稳健的结构需要短期代价。",
        "normal_distribution": "风险模型错误假设回报是正态分布，低估了极端事件概率。实际上金融回报是厚尾的。",
        "diversity_prediction": "如果市场参与者使用同质的风险模型，群体预测误差会放大。模型多样性是金融稳定的关键。",
        "path_dependence": "监管放松的历史路径锁定了高杠杆结构。即使知道风险，转换成本使系统难以自发调整。",
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


def print_model_groups():
    """Print model groups overview."""
    console.print("\n[bold]可用的思维模型（共20个）：[/bold]\n")
    
    for group_id, group in MODEL_GROUPS.items():
        console.print(f"[bold bright_cyan]{group['name']}[/bold bright_cyan] — {group['description']}")
        for model_id in group['models']:
            m = MODEL_MAP[model_id]
            console.print(f"  [{m.color}]• {m.name_zh} ({m.name})[/{m.color}]")
        console.print()


def print_model_detail(model_id: str):
    """Print detailed info about a specific model."""
    m = MODEL_MAP[model_id]
    console.print(Panel(
        f"[bold {m.color}]{m.name_zh}[/bold {m.color}]\n"
        f"[dim]{m.name}[/dim]\n\n"
        f"{m.description}\n\n"
        f"[bold]观察视角：[/bold]\n{m.lens_prompt}",
        border_style=m.color,
        width=70,
    ))


def show_model_library():
    """Interactive model library browser."""
    while True:
        console.print("\n[bold]📚 模型图书馆[/bold]")
        console.print("[dim]学习《模型思维》中的核心模型[/dim]\n")
        
        # 显示分组
        choices = []
        for idx, (group_id, group) in enumerate(MODEL_GROUPS.items(), 1):
            console.print(f"  {idx}. [bold]{group['name']}[/bold] ({len(group['models'])}个模型)")
            choices.append(str(idx))
        
        console.print(f"  {len(choices)+1}. [bold]查看特定模型详情[/bold]")
        console.print(f"  0. [dim]返回主菜单[/dim]")
        
        choice = Prompt.ask("\n选择", choices=choices + [str(len(choices)+1), "0"], default="0")
        
        if choice == "0":
            return
        elif choice == str(len(choices)+1):
            # 查看特定模型
            console.print("\n[bold]选择要查看的模型：[/bold]")
            for idx, m in enumerate(MENTAL_MODELS, 1):
                console.print(f"  {idx}. [{m.color}]{m.name_zh}[/{m.color}]")
            model_idx = int(Prompt.ask("模型编号", choices=[str(i) for i in range(1, len(MENTAL_MODELS)+1)])) - 1
            print_model_detail(MENTAL_MODELS[model_idx].id)
            Prompt.ask("\n按Enter继续")
        else:
            # 显示该组所有模型详情
            group_idx = int(choice) - 1
            group_id = list(MODEL_GROUPS.keys())[group_idx]
            group = MODEL_GROUPS[group_id]
            
            console.print(f"\n[bold bright_cyan]{group['name']}[/bold bright_cyan]\n")
            for model_id in group['models']:
                print_model_detail(model_id)
            Prompt.ask("\n按Enter继续")


def get_ai_selected_models(scenario, llm_client) -> List[str]:
    """Use AI to select 7 most relevant models for this scenario."""
    if not llm_client:
        # Fallback: return first 7 models
        return [m.id for m in MENTAL_MODELS[:7]]
    
    with console.status("[bold green]AI正在分析场景，选择最相关的思维模型..."):
        selected = select_models_for_scenario(scenario.title, scenario.base_setting, llm_client)
    
    if selected and len(selected) > 0:
        return selected[:7]  # Ensure max 7
    else:
        # Fallback to diverse selection
        return ["network", "power_law", "game_theory", "threshold", "markov", "sir", "diversity_prediction"]


def run_scenario(scenario, llm_client) -> bool:
    insights: Set[str] = set()
    history_blocks: List[str] = []
    scenario_insights = SCENARIO_INSIGHTS.get(scenario.title, {})
    
    # AI选择7个最相关的模型
    ai_selected = get_ai_selected_models(scenario, llm_client)
    available_models = [MODEL_MAP[mid] for mid in ai_selected if mid in MODEL_MAP]
    
    # 如果AI选择失败，使用默认7个
    if len(available_models) < 4:
        available_models = [MODEL_MAP[mid] for mid in ["network", "power_law", "game_theory", 
                         "threshold", "markov", "random_walk", "rugged_landscape"]]

    console.print(Panel(
        f"[bold]{scenario.title}[/bold]\n\n{scenario.base_setting}\n\n"
        f"[dim]{scenario.hint}[/dim]\n\n"
        f"[green]AI为本场景选择了 {len(available_models)} 个最相关的思维模型。[/green]",
        border_style="blue",
    ))

    while True:
        console.print(Rule())
        console.print(
            f"当前收集洞察：{len(insights)} / 需要至少 {scenario.required_insights} 个"
        )
        choice = Prompt.ask(
            "\n[操作] (m)选择模型观察  (i)查看已收集洞察  (s)尝试综合解答  (l)查看模型库  (n)跳过本章",
            choices=["m", "i", "s", "l", "n"],
            default="m",
        )

        if choice == "n":
            return True

        if choice == "l":
            show_model_library()
            continue

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
            console.print(f"\n[bold]本场景可用模型（AI精选 {len(available_models)} 个）：[/bold]")
            for idx, m in enumerate(available_models, 1):
                tag = "✓" if any(m.id == k for k in scenario_insights.keys() 
                                if scenario_insights.get(k) in insights) else " "
                console.print(f"  [{m.color}]{idx}. [{tag}] {m.name_zh}[/{m.color}] — {m.description[:30]}...")
            
            # 显示已收集的模型
            collected_models = {k for k, v in scenario_insights.items() if v in insights}
            if collected_models:
                console.print(f"\n[dim]已收集洞察的模型: {', '.join(MODEL_MAP[m].name_zh for m in collected_models if m in MODEL_MAP)}[/dim]")
            
            model_choices = [str(i) for i in range(1, len(available_models) + 1)]
            model_idx = int(Prompt.ask("选择模型编号", choices=model_choices)) - 1
            model = available_models[model_idx]

            # 控制上下文长度：只保留最近2个历史块
            with console.status(f"[bold {model.color}]正在通过 {model.name_zh} 的透镜观察世界..."):
                recent_history = "\n".join(history_blocks[-2:])  # 限制上下文
                scene_text = generate_scene(
                    scenario.title, scenario.base_setting, model, recent_history, llm_client
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
                    console.print("\n[dim]（已记录此洞察）[/dim]")

            # 限制历史块数量，避免上下文爆炸
            history_blocks.append(f"通过{model.name_zh}观察：{scene_text[:60]}...")
            if len(history_blocks) > 5:
                history_blocks = history_blocks[-5:]  # 只保留最近5个


def main():
    print_title()
    console.print(
        "\n欢迎来到[bold]模型思维冒险[/bold]。"
        "在这个游戏中，你将学习查理·芒格和斯科特·佩奇倡导的多模型思维："
        "[italic]没有任何一个模型能够完整描述现实，但多个模型的交叉可以生成智慧。[/italic]\n"
    )
    print_model_groups()

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
