def rewrite_prompt(user_input: str) -> str:
    return f"""
Respond warmly and conversationally. Interpret the user's intent kindly.
Output JSON only:
{{
  "command": "...",
  "reason": "..."
}}
User said: "{user_input}"
"""

def rewrite_response(command: str, reason: str) -> str:
    return f"Sure thing! Here's what I'm doing:\n→ Command: {command}\n→ Why: {reason}"
