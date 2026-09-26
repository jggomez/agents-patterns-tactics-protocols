"""Comprehensive verification and self-diagnostic script for ADK Agent Patterns."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add patterns and repository root to sys.path
BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
for directory in (str(BASE_DIR), str(PARENT_DIR)):
    if directory not in sys.path:
        sys.path.insert(0, directory)

GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_step(title: str) -> None:
    print(f"\n{BOLD}{BLUE}[CHECK]{RESET} {title}...")


def print_ok(msg: str) -> None:
    print(f"  {GREEN}✔ {msg}{RESET}")


def print_warn(msg: str) -> None:
    print(f"  {YELLOW}⚠ {msg}{RESET}")


def print_err(msg: str) -> None:
    print(f"  {RED}✘ {msg}{RESET}")


def check_environment() -> bool:
    print_step("Python Environment & Dependencies")
    print_ok(f"Python: {sys.version.split()[0]}")

    try:
        import google.adk
        print_ok(f"google-adk: {getattr(google.adk, '__version__', 'installed')}")
    except ImportError:
        print_err("google-adk is not installed. Run 'uv sync'.")
        return False

    try:
        import google.genai
        print_ok(f"google-genai: {getattr(google.genai, '__version__', 'installed')}")
    except ImportError:
        print_err("google-genai is not installed. Run 'uv sync'.")
        return False

    try:
        import dotenv
        print_ok("python-dotenv: installed")
    except ImportError:
        print_err("python-dotenv is not installed. Run 'uv sync'.")
        return False

    return True


def check_credentials() -> None:
    print_step("API Key & Model Configuration")
    from patterns.agents.common.config import DEFAULT_MODEL

    print_ok(f"Target Gemini Model: {DEFAULT_MODEL}")

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key and not api_key.startswith("your_"):
        masked = api_key[:4] + "..." + api_key[-4:] if len(api_key) > 8 else "***"
        print_ok(f"Gemini API Key detected: {masked}")
    else:
        print_warn(
            "GEMINI_API_KEY is not set or using placeholder in .env.\n"
            "    (Unit and structural tests will pass, but live LLM queries require a valid key)."
        )


def check_agent_imports() -> bool:
    print_step("Validating Agent Imports & Casing")
    agents_to_test = [
        ("patterns.agents.first_agent.agent", "First Agent (Simple + Search)"),
        ("patterns.agents.sequential_agent.agent", "Sequential Agent (Pipeline)"),
        ("patterns.agents.parallel_agent.agent", "Parallel Agent (Concurrent)"),
        ("patterns.agents.orchestrator_agent.agent", "Orchestrator Agent (Agent-as-Tool)"),
        ("patterns.agents.loop_agent.agent", "Loop Agent (Iterative Refinement)"),
        ("patterns.agents.workflow_agent.agent", "Workflow Agent (ADK 2.0 Graph)"),
    ]

    all_passed = True
    for mod_name, label in agents_to_test:
        try:
            mod = __import__(mod_name, fromlist=["root_agent"])
            agent = getattr(mod, "root_agent", None)
            if agent:
                print_ok(f"{label} imported successfully: '{agent.name}'")
            else:
                print_err(f"{label}: root_agent attribute not found.")
                all_passed = False
        except Exception as exc:
            print_err(f"Failed to import {label}: {exc}")
            all_passed = False

    return all_passed


def run_pytest_suite() -> bool:
    print_step("Running Automated Pytest Suite")
    import pytest

    tests_dir = str(BASE_DIR / "tests")
    exit_code = pytest.main(["-q", tests_dir])
    if exit_code == 0:
        print_ok("All automated unit/mock tests passed successfully!")
        return True
    else:
        print_err(f"Pytest exited with status code {exit_code}")
        return False


def main() -> None:
    print(f"\n{BOLD}{CYAN}======================================================{RESET}")
    print(f"{BOLD}{CYAN}       ADK Agent Patterns Diagnostic & Verification   {RESET}")
    print(f"{BOLD}{CYAN}======================================================{RESET}")

    env_ok = check_environment()
    if not env_ok:
        sys.exit(1)

    check_credentials()
    imports_ok = check_agent_imports()
    if not imports_ok:
        sys.exit(1)

    tests_ok = run_pytest_suite()
    if not tests_ok:
        sys.exit(1)

    print(f"\n{BOLD}{GREEN}======================================================{RESET}")
    print(f"{BOLD}{GREEN}  🎉 All checks passed! Agent patterns are fully ready!{RESET}")
    print(f"{BOLD}{GREEN}======================================================{RESET}\n")


if __name__ == "__main__":
    main()
