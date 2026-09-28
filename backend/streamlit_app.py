import os
import json
import time
import threading
import queue
import difflib

import streamlit as st
import websocket

st.set_page_config(
    page_title="Autonomous Refactoring Agent",
    page_icon="🤖",
    layout="wide",
)

WS_URL = os.getenv("WS_URL", "ws://localhost:8000/ws")

COLORS = {
    "info": "#93c5fd",
    "warn": "#fcd34d",
    "error": "#f87171",
    "success": "#34d399",
}


def init_state():
    defaults = {
        "logs": [],
        "diff": None,
        "repo_url": "",
        "ws_started": False,
        "ws_thread": None,
        "ws_ref": None,
        "event_q": queue.Queue(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def start_ws():
    if st.session_state.ws_thread and st.session_state.ws_thread.is_alive():
        return st.session_state.ws_ref

    def on_open(ws):
        st.session_state.event_q.put(
            {"type": "log", "payload": {"level": "info", "message": "Connected to agent WebSocket"}}
        )

    def on_message(ws, message):
        try:
            st.session_state.event_q.put(json.loads(message))
        except Exception:
            pass

    def on_error(ws, error):
        st.session_state.event_q.put(
            {"type": "log", "payload": {"level": "error", "message": f"WebSocket error: {error}"}}
        )

    def on_close(ws, *args):
        st.session_state.event_q.put(
            {"type": "log", "payload": {"level": "warn", "message": "WebSocket disconnected, auto-reconnecting..."}}
        )

    ws_app = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    thread = threading.Thread(target=ws_app.run_forever, daemon=True)
    st.session_state.ws_thread = thread
    st.session_state.ws_ref = ws_app
    thread.start()
    return ws_app


def send_message(msg):
    ws = st.session_state.ws_ref
    if ws:
        try:
            ws.send(json.dumps(msg))
            return True
        except Exception as exc:
            st.session_state.event_q.put(
                {"type": "log", "payload": {"level": "error", "message": f"Send failed: {exc}"}}
            )
    return False


def process_events():
    while True:
        try:
            event = st.session_state.event_q.get_nowait()
        except queue.Empty:
            break
        event_type = event.get("type")
        payload = event.get("payload", {})
        if event_type == "log":
            st.session_state.logs.append(
                {
                    "timestamp": time.strftime("%H:%M:%S"),
                    "level": payload.get("level", "info"),
                    "message": payload.get("message", ""),
                }
            )
        elif event_type == "diff":
            st.session_state.diff = {
                "original": payload.get("original", ""),
                "modified": payload.get("modified", ""),
            }


st.title("Autonomous Refactoring Agent")
st.caption(
    "Autonomous, self-healing system that ingests repositories, proposes AST-aware changes, "
    "tests them in a sandbox, and streams the process for final PR approval."
)

with st.sidebar:
    st.header("Task Configuration")
    repo_url = st.text_input(
        "Target Repository",
        value=st.session_state.repo_url,
        placeholder="https://github.com/user/repo",
    )
    st.session_state.repo_url = repo_url

    start_btn = st.button(
        "Start Refactoring Agent",
        type="primary",
        use_container_width=True,
        disabled=not repo_url or st.session_state.ws_started,
    )
    approve_btn = st.button(
        "Approve & Create PR",
        use_container_width=True,
        disabled=st.session_state.diff is None,
    )

    if start_btn:
        st.session_state.ws_started = True
        start_ws()
        send_message({"type": "start", "payload": {"repoUrl": repo_url}})
    if approve_btn:
        send_message({"type": "approve"})

if st.session_state.ws_started:
    start_ws()

process_events()

col_logs, col_diff = st.columns([1, 1])

with col_logs:
    st.subheader("Agent Execution Logs")
    if not st.session_state.logs:
        st.info("Waiting for agent to start...")
    else:
        for log in st.session_state.logs:
            color = COLORS.get(log["level"], "#9ca3af")
            st.markdown(
                f"<span style='color:{color}'>[{log['timestamp']}] {log['message']}</span>",
                unsafe_allow_html=True,
            )

with col_diff:
    st.subheader("File Diff")
    diff_data = st.session_state.diff
    if diff_data:
        unified = "\n".join(
            difflib.unified_diff(
                diff_data["original"].splitlines(),
                diff_data["modified"].splitlines(),
                fromfile="original",
                tofile="modified",
                lineterm="",
            )
        )
        if unified.strip():
            st.code(unified, language="diff")
        else:
            st.info("No changes detected.")
        with st.expander("Original code"):
            st.code(diff_data["original"], language="python")
        with st.expander("Modified code"):
            st.code(diff_data["modified"], language="python")
    else:
        st.info("No diff yet. Start the agent to see changes.")

if st.session_state.ws_started:
    time.sleep(2)
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()