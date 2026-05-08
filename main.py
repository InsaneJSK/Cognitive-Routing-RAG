"""
This is the main entry point for running the Cognitive Routing RAG system.
It orchestrates the execution of all three phases, collects results,
and generates markdown logs for each phase.
"""

from pathlib import Path
from datetime import datetime
from typing import Any

from app.phase1_router import phase1_demo
from app.phase2_langgraph import phase2_demo
from app.phase3_rag import phase3_demo
from app.testcases import phase3_tests

def get_timestamp():
    """Returns a timestamp string for log file naming."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def write_markdown_log(filepath, title, content):
    """Writes the given content to a markdown file with a title and timestamp."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n\n")
        f.write(content)

def render_phase1_markdown(phase1_results: dict[str, dict[str, Any]]) -> str:
    """Renders the phase 1 results into a markdown string."""
    md = ""
    for test_name, result in phase1_results.items():
        md += f"## {test_name}\n\n"
        md += "### Input Post\n"
        md += f"{result.get('content', '')}\n\n"
        md += "### Routed Bots\n"
        matches = result.get("matches", [])
        if matches:
            for bot_id, bot_name, similarity in matches:
                md += (
                    f"- **{bot_id}** ({bot_name}) "
                    f"| Similarity: `{similarity:.4f}`\n"
                )
        else:
            md += "- No matching bots found.\n"
        md += "\n---\n\n"
    return md


def render_phase2_markdown(phase2_results: dict[str, dict[str, str]]) -> str:
    """Renders the phase 2 results into a markdown string."""
    md = ""
    for _, result in phase2_results.items():
        md += f"## Bot ID: {result.get('bot_id', 'Unknown')}\n\n"
        md += "### Topic\n"
        md += f"{result.get('topic', '')}\n\n"
        md += "### Generated Post\n"
        md += f"{result.get('post_content', '')}\n\n"
        md += "---\n\n"
    return md


def render_phase3_markdown(
    phase3_results: dict[str, str],
    test_data: list[dict[str, Any]],
) -> str:
    """
    Renders the phase 3 results into a markdown string with test case details and bot responses.
    """
    md = ""
    for idx, (test_name, bot_response) in enumerate(phase3_results.items()):
        test_case = test_data[idx] if idx < len(test_data) else {}
        md += f"## {test_name}\n\n"
        md += "### Bot Persona\n"
        md += f"{test_case.get('bot_persona', '')}\n\n"
        md += "### Parent Post\n"
        md += f"{test_case.get('parent_post', '')}\n\n"
        md += "### Comment History\n"
        for comment in test_case.get("comment_history", []):
            md += f"- {comment}\n"
        md += "\n"
        md += "### Human Reply\n"
        md += f"{test_case.get('human_reply', '')}\n\n"
        md += "### Bot Response\n"
        md += f"{bot_response}\n\n"
        md += "---\n\n"
    return md


def main():
    """Main function to run all phases and generate logs."""
    timestamp = get_timestamp()
    run_dir = Path(f"logs/{timestamp}")
    run_dir.mkdir(parents=True, exist_ok=True)

    phase1_md = render_phase1_markdown(phase1_demo())
    phase2_md = render_phase2_markdown(phase2_demo())
    phase3_md = render_phase3_markdown(phase3_demo(), phase3_tests)

    write_markdown_log(
        run_dir / "phase1.md",
        "Phase 1 - Vector Persona Routing",
        phase1_md,
    )
    write_markdown_log(
        run_dir / "phase2.md",
        "Phase 2 - LangGraph Autonomous Content Engine",
        phase2_md,
    )
    write_markdown_log(
        run_dir / "phase3.md",
        "Phase 3 - Deep Thread RAG & Prompt Injection Defense",
        phase3_md,
    )

    print(f"\nLogs generated successfully in: {run_dir}\n")


if __name__ == "__main__":
    main()
