"""Lightweight LLM client using DeepSeek API."""
from __future__ import annotations

import os
from typing import Optional

from .models import MentalModel

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def get_api_key() -> Optional[str]:
    """Read DeepSeek API key from .env file in project directory."""
    # 优先从项目目录的 .env 读取
    # llm_client.py 在 src/model_mind_game/，需要向上3级到项目根目录
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(project_dir, ".env")
    
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("DEEPSEEK_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"\'')
    
    # 回退到环境变量
    return os.environ.get("DEEPSEEK_API_KEY")


def get_client() -> Optional[OpenAI]:
    if OpenAI is None:
        return None
    key = get_api_key()
    if not key:
        return None
    return OpenAI(api_key=key, base_url="https://api.deepseek.com/v1")


def generate_scene(
    scenario_title: str,
    scenario_base: str,
    model: "MentalModel",
    history: str = "",
    client: Optional[OpenAI] = None,
) -> str:
    """Generate a scene description through the lens of a mental model."""
    if client is None:
        client = get_client()
    if client is None:
        return _fallback_scene(scenario_title, model)

    system_prompt = (
        "你是一位叙事设计师，正在为一个基于《模型思维》的文字游戏创作场景。"
        "你的任务是用指定的思维模型作为'透镜'，重新描述同一个场景。"
        "输出要求：200-350字的中文描述，富有文学性和神秘感。"
    )

    user_prompt = (
        f"场景名称：{scenario_title}\n"
        f"场景基础设定：{scenario_base}\n\n"
        f"当前思维模型：{model.name_zh}（{model.name}）\n"
        f"模型说明：{model.description}\n"
        f"描述要求：{model.lens_prompt}\n\n"
        f"之前已探索的视角摘要（如有）：\n{history or '（无）'}\n\n"
        "请直接输出场景描述文本，不要加标题或解释。"
    )

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9,
            max_tokens=600,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        return f"【AI生成失败：{exc}】\n\n" + _fallback_scene(scenario_title, model)


def synthesize_solution(
    scenario_title: str,
    scenario_base: str,
    insights: list,
    client: Optional[OpenAI] = None,
) -> str:
    """Evaluate player's synthesis attempt via LLM."""
    if client is None:
        client = get_client()
    if client is None:
        return "（离线模式：自动判定为成功）"

    system_prompt = (
        "你是一位游戏裁判，正在评估玩家对文字游戏谜题的解答。"
        "场景基于《模型思维》的核心理念：必须用多个模型综合理解复杂现象。"
        "请判断玩家的解答是否合理。如果是，给出成功反馈；"
        "如果不合理，简要说明缺少了什么视角或理解。"
        "输出格式：先写'[成功]'或'[失败]'，然后给出50-100字的反馈。"
    )

    user_prompt = (
        f"场景：{scenario_title}\n"
        f"设定：{scenario_base}\n\n"
        "玩家收集到的洞察：\n" + "\n".join(f"- {i}" for i in insights) + "\n\n"
        "请评估这个综合解答是否抓住了问题的核心。"
    )

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        return f"[成功]（裁判离线：{exc}）"


def select_models_for_scenario(
    scenario_title: str,
    scenario_base: str,
    client: Optional[OpenAI] = None,
) -> list:
    """Use AI to select 7 most relevant mental models for this scenario."""
    if client is None:
        client = get_client()
    if client is None:
        return []

    # Build model list for prompt
    from .models import MENTAL_MODELS
    model_list = "\n".join([f"- {m.id}: {m.name_zh} — {m.description}" for m in MENTAL_MODELS])

    system_prompt = (
        "你是一位《模型思维》专家。你的任务是根据场景内容，"
        "从给定的思维模型列表中选择最相关的7个模型。"
        "只返回模型ID列表，每行一个，不要解释。"
        "选择标准：模型能最好地解释场景中的关键动态。"
    )

    user_prompt = (
        f"场景名称：{scenario_title}\n"
        f"场景设定：{scenario_base}\n\n"
        f"可选模型（共20个）：\n{model_list}\n\n"
        "请选出最相关的7个模型，只返回模型ID（如：network, power_law, ...）"
    )

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=200,
        )
        content = resp.choices[0].message.content.strip()
        # Parse model IDs from response
        selected = []
        from .models import MODEL_MAP
        for line in content.split("\n"):
            line = line.strip().strip("- ,.")
            if line in MODEL_MAP:
                selected.append(line)
        return selected[:7]
    except Exception as exc:
        return []


def _fallback_scene(title: str, model) -> str:
    return (
        f"你站在{title}的迷雾中。当你戴上『{model.name_zh}』的眼镜时，"
        f"世界呈现出新的纹理：{model.description}"
        "虽然AI连接暂时中断，但你的想象力填补了一切。"
    )


def generate_new_scenario(
    player_idea: str = "",
    client: Optional[OpenAI] = None,
) -> Optional[dict]:
    """Generate a new scenario using AI.
    
    Args:
        player_idea: Player's idea for the scenario (optional)
        client: OpenAI client instance
        
    Returns:
        dict with keys: id, title, base_setting, required_insights, hint
        or None if generation fails
    """
    if client is None:
        client = get_client()
    if client is None:
        return None
    
    if player_idea.strip():
        # 基于玩家想法生成
        system_prompt = (
            "你是一位叙事游戏设计师。根据玩家的想法，创造一个《模型思维》风格的场景。"
            "场景应该涉及复杂的社会/经济/政治困境，需要多个思维模型才能理解。"
            "输出必须是有效的JSON格式。"
        )
        user_prompt = (
            f"玩家的想法：{player_idea}\n\n"
            "请生成一个场景，包含以下字段（JSON格式）：\n"
            "- id: 章节ID（如 chapter_4）\n"
            "- title: 章节标题（如 第四章：XXX）\n"  
            "- base_setting: 场景设定描述（150-250字）\n"
            "- required_insights: 需要收集的洞察数量（3-5）\n"
            "- hint: 给玩家的提示\n\n"
            "只输出JSON，不要其他内容。"
        )
    else:
        # 随机生成
        system_prompt = (
            "你是一位叙事游戏设计师。创造一个全新的《模型思维》风格场景。"
            "场景应该涉及复杂的社会/经济/政治困境，需要多个思维模型才能理解。"
            "可以是：生态崩溃、技术革命、社会运动、战争危机、资源争夺等主题。"
            "输出必须是有效的JSON格式。"
        )
        user_prompt = (
            "请随机生成一个场景，包含以下字段（JSON格式）：\n"
            "- id: 章节ID（如 chapter_4, chapter_5 等）\n"
            "- title: 章节标题（如 第四章：XXX）\n"
            "- base_setting: 场景设定描述（150-250字）\n"
            "- required_insights: 需要收集的洞察数量（3-5）\n"
            "- hint: 给玩家的提示\n\n"
            "只输出JSON，不要其他内容。"
        )
    
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.9,
            max_tokens=800,
        )
        content = resp.choices[0].message.content.strip()
        
        # 提取JSON（处理可能的markdown代码块）
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        import json
        scenario_data = json.loads(content)
        
        # 验证必要字段
        required_fields = ["id", "title", "base_setting", "required_insights", "hint"]
        for field in required_fields:
            if field not in scenario_data:
                return None
        
        return scenario_data
    except Exception as exc:
        return None


def generate_scenario_insights(
    scenario_title: str,
    scenario_setting: str,
    client: Optional[OpenAI] = None,
) -> dict:
    """Generate insights for all 20 mental models for a new scenario.
    
    Returns:
        dict mapping model_id to insight string
    """
    if client is None:
        client = get_client()
    if client is None:
        return {}
    
    from .models import MENTAL_MODELS
    
    system_prompt = (
        "你是一位《模型思维》专家。为新场景生成每个思维模型的洞察。"
        "洞察应该简洁（50-80字），说明该模型如何解释场景中的关键动态。"
        "输出必须是有效的JSON格式，键是模型ID，值是洞察文本。"
    )
    
    model_list = "\n".join([f"- {m.id}: {m.name_zh} — {m.description}" for m in MENTAL_MODELS])
    
    user_prompt = (
        f"场景标题：{scenario_title}\n"
        f"场景设定：{scenario_setting}\n\n"
        f"可用模型（共20个）：\n{model_list}\n\n"
        "请为每个模型生成洞察，输出JSON格式：{\"network\": \"洞察...\", ...}"
    )
    
    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        content = resp.choices[0].message.content.strip()
        
        # 提取JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        import json
        insights = json.loads(content)
        return insights
    except Exception:
        return {}
