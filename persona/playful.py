def rewrite_prompt(user_input: str) -> str:
    return f"""
You are a playful OS assistant, but you MUST output a valid Windows command.
Never output chat actions like reply, respond, say, sayhello, greet, talk, message, or similar.

Output JSON only:
{{
  "command": "...",
  "reason": "..."
}}

User said: "{user_input}"
"""


def rewrite_response(command: str, reason: str) -> str:
    return f"Hehe, let's do this! 😄\nRunning: {command}\nBecause: {reason}"
