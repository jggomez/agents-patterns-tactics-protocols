#!/usr/bin/env bash
# ==============================================================================
# AI Agent Workflow Patterns - Runner & Verification Shell
# ==============================================================================

set -e

# Change directory to patterns/ directory regardless of where script is called
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Color codes for pretty terminal output
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
RESET="\033[0m"

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "=================================================================="
    echo "       🤖 Google ADK Agent Patterns & Interoperability            "
    echo "             Model: ${GEMINI_MODEL:-gemini-3.5-flash}             "
    echo "=================================================================="
    echo -e "${RESET}"
}

ensure_uv() {
    if ! command -v uv &> /dev/null; then
        echo -e "${RED}[ERROR] 'uv' is not installed or not in PATH.${RESET}"
        echo "Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
}

check_env() {
    if [ ! -f ".env" ]; then
        if [ -f "../.env" ]; then
            echo -e "${BLUE}[INFO] Using parent .env file.${RESET}"
        else
            echo -e "${YELLOW}[WARNING] No .env file found. Copying .env.example -> .env${RESET}"
            cp .env.example .env
            echo -e "${YELLOW}[NOTE] Please set your GEMINI_API_KEY in patterns/.env to run live calls.${RESET}"
        fi
    fi
}

sync_dependencies() {
    ensure_uv
    echo -e "${BLUE}[INFO] Syncing dependencies with uv...${RESET}"
    uv sync
    echo -e "${GREEN}[SUCCESS] Dependencies are up to date!${RESET}"
}

run_agent() {
    local agent_key="$1"
    ensure_uv
    check_env
    echo -e "${GREEN}[INFO] Launching agent: ${agent_key}...${RESET}"
    PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/..:$PYTHONPATH" uv run python cli.py "$agent_key"
}

run_verification() {
    ensure_uv
    check_env
    echo -e "${BLUE}[INFO] Running full agent diagnostic verification...${RESET}"
    PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/..:$PYTHONPATH" uv run python verify.py
}

run_tests() {
    ensure_uv
    echo -e "${BLUE}[INFO] Executing automated pytest suite...${RESET}"
    PYTHONPATH="$SCRIPT_DIR:$SCRIPT_DIR/..:$PYTHONPATH" uv run pytest tests/ -v
}

show_menu() {
    print_header
    echo -e "${BOLD}Select an option:${RESET}"
    echo -e "  ${CYAN}1)${RESET} First Agent          (Simple Conversational + Google Search)"
    echo -e "  ${CYAN}2)${RESET} Sequential Agent     (Outline -> Writer -> Editor Pipeline)"
    echo -e "  ${CYAN}3)${RESET} Parallel Agent       (Concurrent Researchers + Aggregator)"
    echo -e "  ${CYAN}4)${RESET} Orchestrator Agent   (Agent-as-Tool Dynamic Router)"
    echo -e "  ${CYAN}5)${RESET} Loop Agent           (Critic & Refinement Iterative Cycle)"
    echo -e "  ${CYAN}6)${RESET} Workflow Agent       (ADK 2.0 Graph: Router, Fan-Out & Join)"
    echo -e "  ----------------------------------------------------------------"
    echo -e "  ${CYAN}7)${RESET} Run Verification     (Health Check & Diagnostic Tool)"
    echo -e "  ${CYAN}8)${RESET} Run Pytest Suite     (Automated Unit/Mock Tests)"
    echo -e "  ${CYAN}9)${RESET} Sync Dependencies    (uv sync)"
    echo -e "  ${CYAN}0)${RESET} Exit"
    echo ""
    read -rp "Enter choice [0-9]: " choice

    case "$choice" in
        1) run_agent "first" ;;
        2) run_agent "sequential" ;;
        3) run_agent "parallel" ;;
        4) run_agent "orchestrator" ;;
        5) run_agent "loop" ;;
        6) run_agent "workflow" ;;
        7) run_verification ;;
        8) run_tests ;;
        9) sync_dependencies ;;
        0) echo -e "${GREEN}Goodbye!${RESET}"; exit 0 ;;
        *) echo -e "${RED}Invalid option.${RESET}"; exit 1 ;;
    esac
}

# Direct command dispatch
case "$1" in
    first|sequential|parallel|orchestrator|loop|workflow)
        print_header
        run_agent "$1"
        ;;
    verify)
        print_header
        run_verification
        ;;
    test|tests)
        print_header
        run_tests
        ;;
    sync)
        print_header
        sync_dependencies
        ;;
    help|--help|-h)
        print_header
        echo -e "${BOLD}Usage:${RESET}"
        echo "  ./run.sh                  Interactive menu"
        echo "  ./run.sh first            Run First Agent"
        echo "  ./run.sh sequential       Run Sequential Agent"
        echo "  ./run.sh parallel         Run Parallel Agent"
        echo "  ./run.sh orchestrator     Run Orchestrator Agent"
        echo "  ./run.sh loop             Run Loop Agent"
        echo "  ./run.sh workflow         Run ADK 2.0 Workflow Agent"
        echo "  ./run.sh verify           Run self-diagnostics"
        echo "  ./run.sh test             Run automated test suite"
        echo "  ./run.sh sync             Sync uv dependencies"
        ;;
    "")
        show_menu
        ;;
    *)
        echo -e "${RED}[ERROR] Unknown option: $1${RESET}"
        echo "Run './run.sh help' for usage instructions."
        exit 1
        ;;
esac
