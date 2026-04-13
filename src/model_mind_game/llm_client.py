"""Lightweight LLM client using DeepSeek API."""
from __future__ import annotations

import os
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def get_api_key() -> Optional[str]:
    """Read DeepSeek API key from known locations."""
    paths = [
        os.path.expanduser("~/.openviking/ov.conf"),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("api_key"):
                        return line.split("=", 1)[1].strip()
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


def _fallback_scene(title: str, model) -> str:
    return (
        f"你站在{title}的迷雾中。当你戴上『{model.name_zh}』的眼镜时，"
        f"世界呈现出新的纹理：{model.description}"
        "虽然AI连接暂时中断，但你的想象力填补了一切。"
    )
