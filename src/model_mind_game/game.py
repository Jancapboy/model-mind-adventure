"""Main game loop for Model Mind Adventure."""
import sys
from typing import Dict, List, Set, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table
from rich.columns import Columns

from .llm_client import generate_scene, get_client, synthesize_solution, select_models_for_scenario, generate_new_scenario, generate_scenario_insights, predict_future_with_models, predict_future_with_intervention
from .models import MENTAL_MODELS, MODEL_MAP
from .scenarios import load_scenarios, save_scenarios, Scenario

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
        # 核心模型组（第1组）
        "network": "谣言通过少数家族控制的暗网流动，而非公开广场。切断中心节点即可恢复公共话语。",
        "power_law": "资源分配呈现极端幂律，3%的家族控制了80%的财富。这种不平等破坏了信任，使公开合作变得不可能。",
        "game_theory": "每个居民都陷入囚徒困境——公开说话会被报复，沉默更安全。除非改变激励结构，否则均衡就是集体沉默。",
        "markov": "城市已从『开放交流』稳态转移到了『猜疑稳态』。历史路径不重要，当前状态决定未来。",
        "threshold": "沉默具有阈值效应。当足够多的人选择沉默，剩余者的阈值被触发，级联导致全城失语。",
        "random_walk": "最初的导火索可能是随机的（一个谣言、一次误会），但在无纠错机制下，偏差被无限放大。",
        "rugged_landscape": "城市被困在『猜疑』的局部最优。任何个体单方面改变都会受损，所以系统无法自发跳出这个陷阱。",
        # 群体动态模型组（第2组）
        "schelling": "即使居民只是轻微偏好与同类聚集，长期演化也会导致社会网络的自然隔离，加剧失语。",
        "granovetter": "打破沉默需要足够多的人同时突破个人阈值。少数人勇敢发声无法改变均衡，需要临界质量。",
        "diffusion": "真相和谣言都在以不同速度扩散。早期采用者已知晓真相，但大众仍被误导，形成信息鸿沟。",
        "sir": "沉默像病毒一样传播。『感染者』（沉默者）持续影响『易感者』（犹豫者），形成流行病动力学。",
        "replicator": "沉默策略在群体中复制扩散，因为开口说话的人受到惩罚。成功的策略是『等待别人先开口』。",
        # 系统性结果模型组（第3组）
        "normal_distribution": "大多数居民的恐惧程度集中在均值附近，但少数极端恐惧者通过影响力扭曲了整体行为。",
        "long_tail": "少数边缘群体（地下反抗者）虽然人数少，但可能通过长尾效应积累足够力量打破沉默。",
        "diversity_prediction": "如果所有居民用相同的恐惧模型做决策，群体预测误差会放大。需要认知多样性才能打破均衡。",
        "wisdom_crowds": "集体智慧失效了，因为居民的判断不再独立——每个人都在观察别人的沉默并模仿。",
        "signaling": "昂贵的信号（如公开抗议）才能打破沉默。廉价的信号（如私下抱怨）无法传递可信承诺。",
        "mechanism_design": "需要重新设计激励机制：奖励公开说话者，惩罚报复行为，才能改变均衡结果。",
        "collective_action": "恢复公共话语是公共物品，存在严重搭便车问题。每个人都希望别人先开口，自己坐享其成。",
        "path_dependence": "城市的历史路径锁定了沉默状态。即使最初的原因消失，转换成本使系统难以自发恢复。",
    },
    "第二章：瘟疫与舞会": {
        # 核心模型组（第1组）
        "network": "舞会是高度连接的超级传播节点。少数社交名媛连接了不同的贵族圈子。",
        "power_law": "感染人数呈现幂律，少数舞会导致了绝大多数传播案例。",
        "game_theory": "每个贵族都知道舞会有风险，但缺席会被排斥。这是一个典型的协调失败/囚徒困境。",
        "markov": "疫情状态转移只取决于当前感染率，与最初病源无关。当前处于爆发临界点。",
        "threshold": "每个贵族参加舞会的阈值不同。但当感染率超过某个临界点，级联式退席才会开始。",
        "random_walk": "病毒传播具有随机性，精准预测下一场爆发的时间几乎不可能。",
        "rugged_landscape": "公共卫生政策被困在『封锁』和『开放』两个局部最优之间，中间状态难以维持。",
        # 群体动态模型组（第2组）
        "schelling": "贵族自然分离成『谨慎派』和『享乐派』两个集群，即使个体只是轻微偏好同类。",
        "granovetter": "集体抵制舞会需要足够多贵族同时改变行为。在缺乏协调机制的情况下，个人阈值难以被突破。",
        "diffusion": "防疫知识在贵族中缓慢扩散，早期采用者（谨慎派）与晚期大众（享乐派）的鸿沟加剧了协调困境。",
        "sir": "疫情遵循SIR动力学。当前处于指数增长阶段，R0>1意味着必须干预才能避免全民感染。",
        "replicator": "『参加舞会』策略在复制，因为缺席者失去社交地位。需要改变收益结构才能让『隔离』策略占优。",
        # 系统性结果模型组（第3组）
        "normal_distribution": "大多数贵族的感染风险感知集中在均值，但少数极端冒险者推动了超级传播事件。",
        "long_tail": "少数大型舞会（长尾中的头部）贡献了绝大多数传播案例，控制这些节点比全面封锁更有效。",
        "diversity_prediction": "如果所有贵族用相同的风险评估模型，群体预测会系统性地低估疫情。需要多样性视角。",
        "wisdom_crowds": "集体智慧失效了，因为贵族的判断互相影响——每个人都在观察别人是否参加舞会。",
        "signaling": "参加舞会成为了一种地位信号。只有昂贵的信号（如主动隔离并公开声明）才能打破这种均衡。",
        "mechanism_design": "需要设计机制让『隔离』成为占优策略：补偿缺席者的社交损失，奖励早期隔离者。",
        "collective_action": "集体抵制舞会是公共物品。每个贵族都希望别人先停止举办，自己继续享受。",
        "path_dependence": "举办舞会的传统路径锁定了高风险行为。即使疫情严重，改变社交规范需要克服巨大惯性。",
    },
    "第三章：股市的叹息": {
        # 核心模型组（第1组）
        "network": "金融机构高度互联。一家中小型机构的违约会通过债务网络引发连锁反应。",
        "power_law": "市场回报呈现幂律分布。十年的低波动让人们忽视了尾部风险，但幂律意味着大崩溃始终可能。",
        "game_theory": "每个机构都知道杠杆率过高，但如果别人都在加杠杆，单方面降低杠杆会失去市场份额。这是逐底竞争。",
        "markov": "市场已从『乐观稳态』转移到了『恐慌稳态』。一旦转移发生，很难快速恢复。",
        "threshold": "崩溃具有阈值。当违约消息越过投资者的心理阈值，恐慌级联开始。",
        "random_walk": "资产价格遵循随机游走。十年上涨只是历史路径的一部分，不保证未来方向。",
        "rugged_landscape": "金融体系被困在『高杠杆高增长』的局部最优。探索更稳健的结构需要短期代价。",
        # 群体动态模型组（第2组）
        "schelling": "投资者自然分离成『多头』和『空头』阵营，即使个体只是轻微偏好同类观点。",
        "granovetter": "集体抛售需要足够多投资者同时突破个人阈值。在缺乏协调的情况下，恐慌难以自发停止。",
        "diffusion": "风险认知在市场中扩散，早期采用者（谨慎派）早已离场，晚期大众（跟风者）加剧了崩盘。",
        "sir": "恐慌像病毒一样传播。『恐慌者』影响『理性者』，形成情绪传染动力学。",
        "replicator": "『高杠杆』策略在牛市中复制扩散，因为保守者跑输市场。需要危机才能改变策略分布。",
        # 系统性结果模型组（第3组）
        "normal_distribution": "风险模型错误假设回报是正态分布，低估了极端事件概率。实际上金融回报是厚尾的。",
        "long_tail": "少数极端事件（黑天鹅）贡献了绝大多数损失。传统的风险管理忽视了长尾风险。",
        "diversity_prediction": "如果市场参与者使用同质的风险模型，群体预测误差会放大。模型多样性是金融稳定的关键。",
        "wisdom_crowds": "集体智慧在泡沫期失效了，因为投资者的判断不再独立——每个人都在追涨，形成羊群效应。",
        "signaling": "高杠杆成为了一种能力信号。只有昂贵的信号（如主动降杠杆并承受短期业绩下滑）才能传递稳健承诺。",
        "mechanism_design": "需要重新设计激励机制：奖励长期稳健而非短期收益，才能避免逐底竞争。",
        "collective_action": "集体去杠杆是公共物品。每个机构都希望别人先降杠杆，自己继续享受泡沫收益。",
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


def run_scenario(scenario, llm_client, dynamic_insights: Optional[Dict[str, Dict[str, str]]] = None) -> bool:
    insights: Set[str] = set()
    history_blocks: List[str] = []
    
    # 合并预定义洞察和动态生成的洞察
    scenario_insights = SCENARIO_INSIGHTS.get(scenario.title, {})
    if dynamic_insights and scenario.title in dynamic_insights:
        scenario_insights.update(dynamic_insights[scenario.title])
    
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
                
                # 成功后询问是否查看未来预测
                if llm_client and insights:
                    predict_choice = Prompt.ask(
                        "\n[预测] 是否基于多模型洞察查看未来走向？",
                        choices=["y", "n"],
                        default="y",
                    )
                    if predict_choice == "y":
                        # 选择预测类型
                        predict_type = Prompt.ask(
                            "[预测类型] (s)简单预测  (i)干预预测（指定时间点干预）",
                            choices=["s", "i"],
                            default="s",
                        )
                        
                        # 让玩家输入预测时间
                        console.print("\n[dim]你想预测多久后的未来？（例如：3天、2周、6个月、1年）[/dim]")
                        time_horizon = Prompt.ask("预测时间", default="6个月")
                        
                        if predict_type == "i":
                            # 干预预测：输入干预时间和措施
                            console.print(f"\n[dim]你想在什么时候干预？（必须在{time_horizon}之前，例如：2个月）[/dim]")
                            intervention_time = Prompt.ask("干预时间点", default="2个月")
                            console.print("\n[dim]干预措施是什么？（例如：切断谣言网络、改变激励机制）[/dim]")
                            intervention_action = Prompt.ask("干预措施")
                            
                            with console.status(f"[bold cyan]AI正在分层预测（多模型→干预→未来）..."):
                                prediction = predict_future_with_intervention(
                                    scenario.title,
                                    scenario.base_setting,
                                    list(insights),
                                    result,
                                    time_horizon,
                                    intervention_time,
                                    intervention_action,
                                    llm_client,
                                )
                            
                            if prediction:
                                confidence = prediction.get('confidence', 50)
                                confidence_color = "green" if confidence >= 70 else "yellow" if confidence >= 40 else "red"
                                
                                console.print(Panel(
                                    f"[bold bright_cyan]🔮 分层干预预测[/bold bright_cyan]\n"
                                    f"[dim]总预测时间：{prediction.get('total_time', time_horizon)} | "
                                    f"干预时间点：{prediction.get('intervention_time', intervention_time)}[/dim]\n"
                                    f"[bold {confidence_color}]置信度：{confidence}%[/bold {confidence_color}]\n\n"
                                    f"[bold white]━━━ 不干预路径 ━━━[/bold white]\n"
                                    f"[green]乐观：[/green]{prediction['no_intervention'].get('optimistic', 'N/A')[:80]}...\n"
                                    f"[red]悲观：[/red]{prediction['no_intervention'].get('pessimistic', 'N/A')[:80]}...\n\n"
                                    f"[bold yellow]━━━ 干预路径（分层预测）━━━[/bold yellow]\n"
                                    f"[dim]第一阶段（多模型预测到干预点）：[/dim]\n"
                                    f"{prediction['intervention'].get('phase1_state', 'N/A')[:100]}...\n\n"
                                    f"[dim]干预措施：{intervention_action}[/dim]\n"
                                    f"[dim]第二阶段（干预后到终点）：[/dim]\n"
                                    f"{prediction['intervention'].get('phase2_final_state', 'N/A')[:100]}...\n\n"
                                    f"[yellow]干预影响：[/yellow]{prediction['intervention'].get('intervention_impact', 'N/A')[:80]}...",
                                    border_style="bright_cyan",
                                    width=85,
                                ))
                            else:
                                console.print("[dim]预测生成失败。[/dim]")
                        else:
                            # 简单预测（原有逻辑）
                            with console.status(f"[bold cyan]AI正在分析{time_horizon}后的未来..."):
                                prediction = predict_future_with_models(
                                    scenario.title,
                                    scenario.base_setting,
                                    list(insights),
                                    result,
                                    time_horizon,
                                    llm_client,
                                )
                            
                            if prediction:
                                confidence = prediction.get('confidence', 50)
                                confidence_color = "green" if confidence >= 70 else "yellow" if confidence >= 40 else "red"
                                
                                console.print(Panel(
                                    f"[bold bright_cyan]🔮 基于多模型的未来预测[/bold bright_cyan]\n"
                                    f"[dim]预测时间范围：{time_horizon}[/dim]\n"
                                    f"[bold {confidence_color}]置信度：{confidence}%[/bold {confidence_color}] "
                                    f"（基于{len(insights)}个模型洞察）\n\n"
                                    f"[bold green]乐观路径：[/bold green]\n{prediction.get('optimistic', 'N/A')}\n\n"
                                    f"[bold red]悲观路径：[/bold red]\n{prediction.get('pessimistic', 'N/A')}\n\n"
                                    f"[bold yellow]⚡ 临界点：[/bold yellow]\n{prediction.get('critical_point', 'N/A')}\n\n"
                                    f"[dim]推理依据：{prediction.get('reasoning', 'N/A')[:150]}...[/dim]",
                                    border_style="bright_cyan",
                                    width=80,
                                ))
                            else:
                                console.print("[dim]预测生成失败。[/dim]")
                
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
                # 使用预定义的洞察
                if insight not in insights:
                    insights.add(insight)
                    console.print(f"\n[green]★ 获得洞察：{insight}[/green]")
                else:
                    console.print("\n[dim]（已记录此洞察）[/dim]")
            else:
                # 没有预定义洞察，从AI生成的内容中提取关键句作为洞察
                # 取场景文本的第一句或前80字作为洞察
                generated_insight = scene_text.split('。')[0][:80] + "..."
                if generated_insight not in insights:
                    insights.add(generated_insight)
                    console.print(f"\n[green]★ 获得洞察（AI生成）：{generated_insight}[/green]")
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

    # 动态加载场景
    scenarios = load_scenarios()
    
    # 动态场景洞察存储（用于AI生成的新场景）
    dynamic_insights: Dict[str, Dict[str, str]] = {}
    
    chapter_num = 0
    while chapter_num < len(scenarios):
        scenario = scenarios[chapter_num]
        success = run_scenario(scenario, llm_client, dynamic_insights)
        if not success:
            console.print("[red]你未能解开谜题，冒险结束。[/red]")
            sys.exit(0)
        console.print(Rule(style="green"))
        chapter_num += 1
    
    # 所有预设场景完成后，询问是否生成新场景
    while True:
        console.print(Panel.fit(
            "[bold bright_cyan]🎉 恭喜！你已完成所有预设章节！[/bold bright_cyan]\n\n"
            f"已完成 {len(scenarios)} 个章节的挑战。",
            border_style="bright_cyan",
        ))
        
        if not llm_client:
            console.print("[yellow]⚠ AI未连接，无法生成新场景。[/yellow]")
            break
        
        choice = Prompt.ask(
            "\n[新章节] (g)生成新章节  (r)随机生成  (c)自定义想法  (q)结束游戏",
            choices=["g", "r", "c", "q"],
            default="q",
        )
        
        if choice == "q":
            break
        
        # 准备生成新场景
        player_idea = ""
        if choice == "c":
            console.print("\n[dim]请输入你的想法（例如：'一个AI觉醒的世界'、'气候危机下的资源战争'等）：[/dim]")
            player_idea = Prompt.ask("你的想法")
        
        # 生成新场景
        with console.status("[bold green]AI正在构思新章节..."):
            new_scenario_data = generate_new_scenario(
                player_idea=player_idea if choice == "c" else "",
                client=llm_client,
            )
        
        if not new_scenario_data:
            console.print("[red]❌ 场景生成失败，请重试。[/red]")
            continue
        
        # 创建新场景对象
        new_scenario = Scenario(
            id=new_scenario_data["id"],
            title=new_scenario_data["title"],
            base_setting=new_scenario_data["base_setting"],
            required_insights=new_scenario_data["required_insights"],
            hint=new_scenario_data["hint"],
        )
        
        console.print(Panel(
            f"[bold bright_green]新章节生成成功！[/bold bright_green]\n\n"
            f"[bold]{new_scenario.title}[/bold]\n"
            f"{new_scenario.base_setting[:100]}...\n\n"
            f"[dim]需要洞察：{new_scenario.required_insights} 个[/dim]",
            border_style="bright_green",
        ))
        
        confirm = Prompt.ask(
            "是否开始这个新章节？",
            choices=["y", "n"],
            default="y",
        )
        
        if confirm == "n":
            continue
        
        # 生成该场景的洞察
        with console.status("[bold green]AI正在为场景生成模型洞察..."):
            new_insights = generate_scenario_insights(
                new_scenario.title,
                new_scenario.base_setting,
                llm_client,
            )
        
        if new_insights:
            dynamic_insights[new_scenario.title] = new_insights
            console.print(f"[green]✓ 已为 {len(new_insights)} 个模型生成洞察[/green]\n")
        
        # 添加到场景列表并运行
        scenarios.append(new_scenario)
        
        # 运行新场景
        success = run_scenario(new_scenario, llm_client, dynamic_insights)
        if not success:
            console.print("[red]你未能解开谜题，冒险结束。[/red]")
            sys.exit(0)
        console.print(Rule(style="green"))

    console.print(Panel.fit(
        "[bold bright_cyan]游戏结束[/bold bright_cyan]\n\n"
        "你亲身体验了多模型思维的力量：\n"
        "  • 孔多塞陪审团定理——多数视角比单一视角更可靠\n"
        "  • 多样性预测定理——多样性的洞察相互抵消误差\n"
        "  • 没有模型是完美的，但模型集合可以逼近真理\n\n"
        "愿你在现实世界中，也能成为一个多模型思考者。",
        border_style="bright_cyan",
    ))


if __name__ == "__main__":
    main()
