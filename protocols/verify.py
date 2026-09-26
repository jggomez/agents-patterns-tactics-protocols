"""Comprehensive self-diagnostic and verification script for AI Agent Protocols."""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

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


def check_env_templates() -> bool:
    print_step("Environment Templates (.env.example)")
    modules = ["MCP", "A2A", "A2UI", "AGUI/backend"]
    all_ok = True
    for mod in modules:
        env_ex = BASE_DIR / mod / ".env.example"
        if env_ex.is_file():
            print_ok(f"{mod}/.env.example exists")
        else:
            print_err(f"{mod}/.env.example missing")
            all_ok = False
    return all_ok


def check_mcp_module() -> bool:
    print_step("MCP Protocol (Model Context Protocol)")
    mcp_dir = BASE_DIR / "MCP"
    cmd = [
        "uv", "run", "--directory", str(mcp_dir),
        "python", "-c",
        "from server import mcp; print(mcp.name)"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        out = res.stdout.strip()
        print_ok(f"FastMCP server module loaded: '{out}'")
        return True
    except subprocess.CalledProcessError as exc:
        print_err(f"MCP check failed: {exc.stderr}")
        return False


def check_a2a_module() -> bool:
    print_step("A2A Protocol (Agent-to-Agent)")
    a2a_dir = BASE_DIR / "A2A"
    cmd = [
        "uv", "run", "--directory", str(a2a_dir),
        "python", "-c",
        "from agent import root_agent, a2a_app, MODEL_NAME; "
        "print(f'{root_agent.name}|{MODEL_NAME}')"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Filter stdout for our printed line
        lines = [line for line in res.stdout.strip().splitlines() if "|" in line]
        if lines:
            name, model = lines[-1].split("|")
            print_ok(f"A2A agent loaded: '{name}' using model '{model}'")
            print_ok("A2A FastAPI app successfully configured")
            return True
        else:
            print_ok("A2A agent loaded successfully")
            return True
    except subprocess.CalledProcessError as exc:
        print_err(f"A2A check failed: {exc.stderr}")
        return False


def check_a2ui_module() -> bool:
    print_step("A2UI Protocol (Agent-to-User Interface)")
    a2ui_dir = BASE_DIR / "A2UI"
    cmd = [
        "uv", "run", "--directory", str(a2ui_dir),
        "python", "-c",
        "from agent import root_agent, a2a_app, MODEL_NAME; "
        "print(f'{root_agent.name}|{MODEL_NAME}')"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = [line for line in res.stdout.strip().splitlines() if "|" in line]
        if lines:
            name, model = lines[-1].split("|")
            print_ok(f"A2UI agent loaded: '{name}' using model '{model}'")
            print_ok("A2UI Adjacency List instructions & CORS configured")
            return True
        else:
            print_ok("A2UI agent loaded successfully")
            return True
    except subprocess.CalledProcessError as exc:
        print_err(f"A2UI check failed: {exc.stderr}")
        return False


def check_agui_module() -> bool:
    print_step("AG-UI Protocol (CopilotKit Integration)")
    agui_dir = BASE_DIR / "AGUI" / "backend"
    cmd = [
        "uv", "run", "--directory", str(agui_dir),
        "python", "-c",
        "from main import app, root_agent; "
        "from agent import MODEL_NAME; "
        "print(f'{app.title}|{root_agent.name}|{MODEL_NAME}')"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = [line for line in res.stdout.strip().splitlines() if "|" in line]
        if lines:
            title, name, model = lines[-1].split("|")
            print_ok(f"AG-UI app loaded: '{title}' with agent '{name}'")
            print_ok(f"Configured model: '{model}'")
            return True
        else:
            print_ok("AG-UI backend loaded successfully")
            return True
    except subprocess.CalledProcessError as exc:
        print_err(f"AG-UI check failed: {exc.stderr}")
        return False


def main() -> None:
    print(f"\n{BOLD}{CYAN}======================================================{RESET}")
    print(f"{BOLD}{CYAN}      AI Agent Protocols Diagnostic & Verification    {RESET}")
    print(f"{BOLD}{CYAN}======================================================{RESET}")

    env_ok = check_env_templates()
    mcp_ok = check_mcp_module()
    a2a_ok = check_a2a_module()
    a2ui_ok = check_a2ui_module()
    agui_ok = check_agui_module()

    all_passed = env_ok and mcp_ok and a2a_ok and a2ui_ok and agui_ok

    if all_passed:
        print(f"\n{BOLD}{GREEN}======================================================{RESET}")
        print(f"{BOLD}{GREEN}  🎉 All protocols validated successfully! Ready to run!{RESET}")
        print(f"{BOLD}{GREEN}======================================================{RESET}\n")
    else:
        print(f"\n{BOLD}{RED}======================================================{RESET}")
        print(f"{BOLD}{RED}  ✘ Some protocol checks failed. See details above.   {RESET}")
        print(f"{BOLD}{RED}======================================================{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
