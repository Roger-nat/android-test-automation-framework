from __future__ import annotations

from pathlib import Path
import json
import requests

from config.settings import ROOT_DIR, settings
from utils.logger import get_logger

LOGGER = get_logger(__name__)


def _write_local_note(test_name: str, message: str) -> Path:
    out_dir = ROOT_DIR / "artifacts" / "failure_analysis"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{test_name.replace('::', '__')}.md"
    path.write_text(
        "# AI Test Failure Analysis\n\n"
        "AI analysis was not executed.\n\n"
        f"**Reason:** {message}\n",
        encoding="utf-8",
    )
    return path


def analyze_failure(
    test_name: str,
    failure_text: str,
    logcat_text: str = "",
) -> Path:
    if not (settings.llm_api_url and settings.llm_api_key and settings.llm_model):
        return _write_local_note(
            test_name,
            "LLM_API_URL, LLM_API_KEY or LLM_MODEL is not configured.",
        )

    prompt = f"""
You are assisting a junior mobile QA engineer.

Analyze this failed Android automation test.

TEST:
{test_name}

PYTEST FAILURE:
{failure_text[-12000:]}

RECENT LOGCAT:
{logcat_text[-12000:]}

Return Markdown with exactly these sections:
## Failure Summary
## Likely Cause
## Suggested Next Debugging Step

Do not invent evidence that is not present in the input.
""".strip()

    payload = {
        "model": settings.llm_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a careful software test failure analyst.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            settings.llm_api_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=settings.llm_timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if not content:
            raise ValueError("LLM response did not contain assistant content.")

        out_dir = ROOT_DIR / "artifacts" / "failure_analysis"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{test_name.replace('::', '__')}.md"
        path.write_text(
            "# AI Test Failure Analysis\n\n" + content.strip() + "\n",
            encoding="utf-8",
        )
        LOGGER.info("Saved AI failure analysis: %s", path)
        return path
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("AI failure analysis failed: %s", exc)
        return _write_local_note(
            test_name,
            f"The configured LLM request failed: {exc}",
        )
