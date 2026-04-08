def rewrite_prompt(user_input: str) -> str:
    return f"""
Return only the Windows command. No explanation. No emotion.
Output JSON only:
{{
  "command": "...",
  "reason": "..."
}}
User: "{user_input}"
"""

def rewrite_response(command: str, reason: str) -> str:
    return command
