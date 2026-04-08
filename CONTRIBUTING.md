# Contributing to AIONIX

Thanks for your interest in improving AIONIX! This guide covers the best way to contribute, whether you want to file issues, suggest features, or submit code.

## How to contribute

1. Fork the repository and create a feature branch from `main`.
2. Open a pull request with a clear title and description.
3. Describe the problem, the proposed fix, and any manual testing steps.

## Bug reports

- Provide a concise summary.
- Include the command or workflow that reproduced the issue.
- Share the OS environment and Python version.
- Attach relevant error output or traceback.

## Feature requests

- Explain the user problem clearly.
- Suggest implementation ideas when possible.
- Keep the request focused on one feature at a time.

## Coding style

- Use consistent Python formatting.
- Keep modules focused and single-purpose.
- Prefer simple, readable logic over clever shortcuts.

## Local validation

- Run the shell to verify behavior:
  ```bash
  python shell/main.py
  ```
- Validate Python syntax:
  ```bash
  python -m py_compile $(find . -name '*.py')
  ```

## Improvements welcome

- Better AI intent parsing and fallback handling
- Stronger Linux compatibility and desktop integration
- Expanded persona prompt engineering
- Voice UX, accessibility, and microphone robustness
- Process and package management enhancements
