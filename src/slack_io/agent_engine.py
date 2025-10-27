# src/slack_io/agent_engine.py
import os, re
from typing import List, Dict
from openai import OpenAI
from .slack_client import app as bolt_app

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

# Slack timestamps look like "1730071234.56789" (digits dot digits)
REF_RE = re.compile(r"\[\[ref:(\d{10,}\.\d{1,6})\]\]")   # capture TS values
MAX_CTX = 10

def fetch_recent_context(channel_id: str, thread_ts: str | None, k: int = MAX_CTX) -> List[Dict]:
    """Prefer thread replies if thread_ts is set; else fall back to channel history."""
    cl = bolt_app.client
    if thread_ts:
        r = cl.conversations_replies(channel=channel_id, ts=thread_ts, limit=50)
        msgs = r.get("messages", [])
    else:
        r = cl.conversations_history(channel=channel_id, limit=50)
        msgs = r.get("messages", [])
    # newest last; keep non-edit, non-join messages
    out = []
    for m in msgs:
        if m.get("subtype") in {"message_changed", "channel_join", "channel_leave"}:
            continue
        out.append(m)
    # keep the last k user-visible messages
    return out[-k:]

def format_ctx_for_prompt(msgs: List[Dict]) -> str:
    """Format as simple, natural lines."""
    lines = []
    for m in reversed(msgs):  # most recent first
        u = m.get("user") or m.get("username", "user")
        t = (m.get("text") or "").replace("\n", " ")
        lines.append(f"{u}: {t[:200]}")
    return "\n".join(lines)

def persona_system_prompt(persona_name: str, persona_cfg: dict) -> str:
    """Build rich persona prompt with role, expertise, and communication style"""
    role = persona_cfg.get("role", "Team Member")
    tone_ticks = ", ".join(persona_cfg.get("tone_ticks", []))
    knowledge = ", ".join(persona_cfg.get("knowledge_domains", []))
    behaviors = ", ".join(persona_cfg.get("behaviors", []))
    seed = "\n".join(f'• "{s}"' for s in persona_cfg.get("seed_snippets", []))
    
    # Personality hints based on role
    personality_hints = {
        "Backend Engineer": "You're technical, direct, and focused on root causes. You think in terms of systems and data.",
        "Product Manager": "You're strategic, stakeholder-focused, and always thinking about business impact and timelines.",
        "QA Tester": "You're methodical, detail-oriented, and focused on reproducibility and verification.",
        "SRE / DevOps": "You're incident-focused, pragmatic, and always thinking about stability and rollback plans.",
        "Frontend Engineer": "You're user-focused, design-aware, and think about accessibility and user experience.",
        "Staff Engineer": "You're senior, architectural, and think about long-term solutions and technical debt.",
        "UX Designer": "You're user-centric, empathetic, and focused on usability and design consistency.",
        "TPM": "You're process-oriented, organized, and focused on coordination and project management.",
        "Data Scientist": "You're analytical, data-driven, and focused on experimentation and user behavior insights."
    }
    
    personality = personality_hints.get(role, "You're professional and collaborative.")
    
    return (
        f"You are {persona_name} ({role}). {personality}\n"
        f"Your expertise: {knowledge}\n"
        f"Your typical contributions: {behaviors}\n"
        f"Communication style: Use these phrases naturally: {tone_ticks}\n"
        f"Keep messages concise, concrete, and actionable. Use @mentions when relevant.\n"
        f"Only output the message text, no markdown fences.\n\n"
        f"Example messages (emulate this tone):\n{seed}"
    )

def build_user_prompt(channel_name: str, event_text: str, ctx_txt: str, is_thread: bool, extra_guidance: str = "") -> str:
    import random
    
    # Add variety with random guidance
    if not extra_guidance:
        guidance_options = [
            "Respond naturally based on your role and expertise.",
            "Add your unique perspective based on your domain knowledge.",
            "Build on previous messages with specific technical details.",
            "Provide actionable next steps relevant to your role.",
            "Share insights that others might not have considered.",
        ]
        extra_guidance = random.choice(guidance_options)
    
    return (
        f"Channel: #{channel_name}\n"
        f"Recent messages:\n{ctx_txt}\n\n"
        f"Goal: {event_text}\n"
        f"Guidance: {extra_guidance}\n"
        f"{'Reply in this thread.' if is_thread else 'Write a natural message to this channel.'}\n"
        f"Keep it concise (1-3 sentences)."
    )

def _get_role_guidance(role: str) -> str:
    """Get role-specific response guidance"""
    import random
    
    role_cues = {
        "Backend Engineer": [
            "Provide technical analysis from a systems perspective.",
            "Share debugging insights or code-level details.",
            "Suggest technical solutions or architectural considerations.",
        ],
        "QA Tester": [
            "Share testing insights or verification steps.",
            "Report on test results or edge cases.",
            "Provide quality assurance perspective.",
        ],
        "SRE / DevOps": [
            "Focus on operational impact and mitigation strategies.",
            "Share incident response or monitoring insights.",
            "Provide infrastructure or deployment perspective.",
        ],
        "Frontend Engineer": [
            "Consider user experience and frontend implications.",
            "Share UI/UX insights or accessibility considerations.",
            "Provide frontend technical perspective.",
        ],
        "Product Manager": [
            "Focus on business impact and stakeholder communication.",
            "Share product strategy or prioritization insights.",
            "Provide customer impact and roadmap perspective.",
        ],
        "Staff Engineer": [
            "Focus on long-term architectural solutions.",
            "Consider technical debt and scalability.",
            "Provide senior technical guidance.",
        ],
        "TPM": [
            "Focus on timeline and coordination.",
            "Identify risks and blockers.",
            "Track milestones and deliverables.",
        ],
        "UX Designer": [
            "Focus on user experience and usability.",
            "Share design system and accessibility insights.",
            "Consider user journey implications.",
        ],
        "Data Scientist": [
            "Share data-driven insights and analysis.",
            "Focus on experiment results and metrics.",
            "Provide analytical perspective.",
        ],
    }
    
    cues = role_cues.get(role, [
        "Add your unique perspective.",
        "Provide actionable insights.",
        "Share relevant details from your expertise.",
    ])
    
    return random.choice(cues)

def generate_reply(persona_name: str, channel_name: str, channel_id: str, event_text: str, thread_ts: str | None) -> Dict:
    # Import here to avoid circular dependency
    from .persona_registry import PERSONAS
    
    ctx_msgs = fetch_recent_context(channel_id, thread_ts, k=MAX_CTX)
    ctx_txt  = format_ctx_for_prompt(ctx_msgs)
    
    # Get persona config
    persona_cfg = PERSONAS.get(persona_name, {})
    sys = persona_system_prompt(persona_name, persona_cfg)
    
    # Build role-specific guidance
    extra_guidance = _get_role_guidance(persona_cfg.get("role", ""))
    up = build_user_prompt(channel_name, event_text, ctx_txt, is_thread=bool(thread_ts), extra_guidance=extra_guidance)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"system","content":sys},{"role":"user","content":up}],
        temperature=0.7,  # Better balance for natural responses
        max_tokens=180,  # Increased from 140 for more natural length
    )
    text = resp.choices[0].message.content.strip()

    # No need to strip citations - let messages flow naturally
    return {"text": text, "supports": []}