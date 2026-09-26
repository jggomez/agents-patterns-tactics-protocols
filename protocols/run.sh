#!/usr/bin/env bash
# ==============================================================================
# Agent Interoperability Protocols - Interactive Runner & Diagnostics
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Color formatting
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
    echo "       🌐 AI Agent Interoperability Protocols (ADK + Gemini)       "
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

sync_submodule() {
    local dir="$1"
    echo -e "${BLUE}[INFO] Syncing uv dependencies in protocols/${dir}...${RESET}"
    (cd "$SCRIPT_DIR/$dir" && uv sync)
}

sync_all() {
    ensure_uv
    sync_submodule "MCP"
    sync_submodule "A2A"
    sync_submodule "A2UI"
    sync_submodule "AGUI/backend"
    echo -e "${GREEN}[SUCCESS] All Python protocol dependencies synced!${RESET}"
}

run_mcp() {
    ensure_uv
    echo -e "${GREEN}[INFO] Starting MCP Server on http://0.0.0.0:8080/mcp ...${RESET}"
    (cd "$SCRIPT_DIR/MCP" && uv run python server.py)
}

run_mcp_test() {
    ensure_uv
    echo -e "${BLUE}[INFO] Running MCP Test Client against http://localhost:8080/mcp ...${RESET}"
    (cd "$SCRIPT_DIR/MCP" && uv run python test_server.py)
}

run_a2a() {
    ensure_uv
    echo -e "${GREEN}[INFO] Starting A2A Agent Server on port 10000 ...${RESET}"
    (cd "$SCRIPT_DIR/A2A" && uv run python agent.py)
}

run_a2a_test() {
    ensure_uv
    echo -e "${BLUE}[INFO] Running A2A Test Client against http://localhost:10000 ...${RESET}"
    (cd "$SCRIPT_DIR/A2A" && uv run python test_client.py)
}

run_a2ui_backend() {
    ensure_uv
    echo -e "${GREEN}[INFO] Starting A2UI Agent Server on port 10001 ...${RESET}"
    (cd "$SCRIPT_DIR/A2UI" && uv run python agent.py)
}

run_a2ui_frontend() {
    echo -e "${GREEN}[INFO] Starting A2UI Lit Web Client on port 5173 ...${RESET}"
    (cd "$SCRIPT_DIR/A2UI/client-lit" && npm run dev)
}

run_agui_backend() {
    ensure_uv
    echo -e "${GREEN}[INFO] Starting AG-UI FastAPI Server on port 8000 ...${RESET}"
    (cd "$SCRIPT_DIR/AGUI/backend" && uv run python main.py)
}

run_agui_frontend() {
    echo -e "${GREEN}[INFO] Starting AG-UI Next.js 16 Frontend on port 3000 ...${RESET}"
    (cd "$SCRIPT_DIR/AGUI/frontend" && npm run dev)
}

run_verify() {
    ensure_uv
    echo -e "${BLUE}[INFO] Running comprehensive protocols verification...${RESET}"
    (cd "$SCRIPT_DIR" && uv run --directory "$SCRIPT_DIR/A2A" python "$SCRIPT_DIR/verify.py")
}

show_menu() {
    print_header
    echo -e "${BOLD}Select a service to start or test:${RESET}"
    echo -e "  ${CYAN}1)${RESET} MCP Server            (FastMCP Tool Provider on :8080)"
    echo -e "  ${CYAN}2)${RESET} MCP Test Client       (Test :8080 exchange rate tool)"
    echo -e "  ----------------------------------------------------------------"
    echo -e "  ${CYAN}3)${RESET} A2A Server            (Agent-to-Agent Service on :10000)"
    echo -e "  ${CYAN}4)${RESET} A2A Test Client       (Test :10000 A2A tasks)"
    echo -e "  ----------------------------------------------------------------"
    echo -e "  ${CYAN}5)${RESET} A2UI Backend          (Adjacency List Agent on :10001)"
    echo -e "  ${CYAN}6)${RESET} A2UI Frontend         (Lit Web Client on :5173)"
    echo -e "  ----------------------------------------------------------------"
    echo -e "  ${CYAN}7)${RESET} AG-UI Backend         (CopilotKit FastAPI Agent on :8000)"
    echo -e "  ${CYAN}8)${RESET} AG-UI Frontend        (Next.js 16 App on :3000)"
    echo -e "  ----------------------------------------------------------------"
    echo -e "  ${CYAN}9)${RESET} Run Verification      (Diagnostic Health Check)"
    echo -e "  ${CYAN}s)${RESET} Sync Dependencies     (uv sync across all modules)"
    echo -e "  ${CYAN}0)${RESET} Exit"
    echo ""
    read -rp "Enter choice [0-9, s]: " choice

    case "$choice" in
        1) run_mcp ;;
        2) run_mcp_test ;;
        3) run_a2a ;;
        4) run_a2a_test ;;
        5) run_a2ui_backend ;;
        6) run_a2ui_frontend ;;
        7) run_agui_backend ;;
        8) run_agui_frontend ;;
        9) run_verify ;;
        s|S) sync_all ;;
        0) echo -e "${GREEN}Goodbye!${RESET}"; exit 0 ;;
        *) echo -e "${RED}Invalid option.${RESET}"; exit 1 ;;
    esac
}

case "$1" in
    mcp) print_header; run_mcp ;;
    mcp-test) print_header; run_mcp_test ;;
    a2a) print_header; run_a2a ;;
    a2a-test) print_header; run_a2a_test ;;
    a2ui|a2ui-backend) print_header; run_a2ui_backend ;;
    a2ui-frontend) print_header; run_a2ui_frontend ;;
    agui|agui-backend) print_header; run_agui_backend ;;
    agui-frontend) print_header; run_agui_frontend ;;
    verify) print_header; run_verify ;;
    sync) print_header; sync_all ;;
    help|--help|-h)
        print_header
        echo -e "${BOLD}Usage:${RESET}"
        echo "  ./run.sh                  Interactive menu"
        echo "  ./run.sh mcp              Start MCP server (:8080)"
        echo "  ./run.sh mcp-test         Test MCP server"
        echo "  ./run.sh a2a              Start A2A agent (:10000)"
        echo "  ./run.sh a2a-test         Test A2A client"
        echo "  ./run.sh a2ui-backend     Start A2UI agent (:10001)"
        echo "  ./run.sh a2ui-frontend    Start A2UI Lit client (:5173)"
        echo "  ./run.sh agui-backend     Start AG-UI FastAPI backend (:8000)"
        echo "  ./run.sh agui-frontend    Start AG-UI Next.js frontend (:3000)"
        echo "  ./run.sh verify           Run protocol diagnostics"
        echo "  ./run.sh sync             Sync all uv environments"
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
