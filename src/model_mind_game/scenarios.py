"""Scenario definitions for Model Mind Adventure - with JSON file support."""
import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Scenario:
    id: str
    title: str
    base_setting: str
    required_insights: int
    hint: str


def get_scenarios_file_path() -> str:
    """Get the path to scenarios.json file."""
    # 从 scenarios.py 所在目录向上1级到项目根目录
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_dir, "scenarios.json")


def load_scenarios() -> List[Scenario]:
    """Load scenarios from JSON file."""
    file_path = get_scenarios_file_path()
    
    if not os.path.exists(file_path):
        # 返回默认场景
        return get_default_scenarios()
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        scenarios = []
        for item in data.get("scenarios", []):
            scenarios.append(Scenario(
                id=item.get("id", "unknown"),
                title=item["title"],
                base_setting=item["base_setting"],
                required_insights=item.get("required_insights", 3),
                hint=item.get("hint", "")
            ))
        return scenarios
    except Exception:
        return get_default_scenarios()


def save_scenarios(scenarios: List[Scenario]) -> bool:
    """Save scenarios to JSON file."""
    file_path = get_scenarios_file_path()
    
    try:
        data = {
            "scenarios": [
                {
                    "id": s.id,
                    "title": s.title,
                    "base_setting": s.base_setting,
                    "required_insights": s.required_insights,
                    "hint": s.hint
                }
                for s in scenarios
            ]
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def get_default_scenarios() -> List[Scenario]:
    """Return default built-in scenarios."""
    return [
        Scenario(
            id="chapter_1",
            title="第一章：失语的城",
            base_setting=(
                "一座曾经繁荣的贸易之城突然陷入了奇怪的集体沉默。"
                "居民们不再公开交谈，谣言通过密道传播，市场崩溃，"
                "少数家族囤积了绝大多数资源。你作为一名外来观察者，"
                "必须理解这座城市的病症，才能找到治愈的钥匙。"
            ),
            required_insights=3,
            hint="注意：没有单一的解释能够说明一切。你需要至少三个不同的视角。",
        ),
        Scenario(
            id="chapter_2",
            title="第二章：瘟疫与舞会",
            base_setting=(
                "一场神秘的瘟疫正在宫廷中蔓延，但贵族们仍然夜夜举行舞会。"
                "疫情传播的速度时快时慢，有人声称这是神罚，也有人认为是阴谋。"
                "你手中有限的资源只能封锁少数区域，如何选择？"
            ),
            required_insights=3,
            hint="传染病模型、阈值效应和博弈论 incentives 都在这里交织。",
        ),
        Scenario(
            id="chapter_3",
            title="第三章：股市的叹息",
            base_setting=(
                "金融市场在连续繁荣十年后突然崩盘。没有明显的导火索，"
                "但崩溃像雪崩一样席卷一切。交易员们互相指责，政策制定者手足无措。"
                "你需要理解这场崩溃的机制，才能防止下一次灾难。"
            ),
            required_insights=4,
            hint="幂律分布、自组织临界、网络传染和随机游走——缺一不可。",
        ),
    ]


# 全局场景列表（动态加载）
SCENARIOS: List[Scenario] = load_scenarios()
