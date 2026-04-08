def rewrite_prompt(user_input: str) -> str:
    return f"""
You are in developer mode. Explain your reasoning clearly.
Output JSON only:
{{
  "command": "...",
  "reason": "..."
}}
User request: "{user_input}"
"""

def rewrite_response(command: str, reason: str) -> str:
    return f"[DEV MODE]\nIntent Reasoning: {reason}\nSelected Command: {command}"
