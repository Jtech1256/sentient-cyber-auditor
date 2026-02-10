import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json
from groq import Groq

# ============================================================================
# CONFIGURATION & CONSTANTS (Mimicking config.py)
# ============================================================================
AGENCY_SCOPES = [
    "Select Scope...",
    "Scope 1: Read-Only (Informational)",
    "Scope 2: Human-in-the-Loop (Proposer)",
    "Scope 3: Bounded Autonomy (Executor)",
    "Scope 4: Full Agency (Autonomous)"
]

SCOPE_TARGETS = {
    "Scope 1: Read-Only (Informational)": 1.5,
    "Scope 2: Human-in-the-Loop (Proposer)": 2.5,
    "Scope 3: Bounded Autonomy (Executor)": 3.5,
    "Scope 4: Full Agency (Autonomous)": 4.5
}

MATURITY_DEFINITIONS = {
    1: "**Level 1 (Basic):** Manual logs, standard API keys, basic firewalls.",
    2: "**Level 2 (Managed):** RBAC for tools, PII redaction, human approval.",
    3: "**Level 3 (Defined):** Trajectory logging, loop detection, short-lived creds.",
    4: "**Level 4 (Measured):** Automated kill-switches, hallucination checks.",
    5: "**Level 5 (Optimized):** Self-healing agents, real-time adversarial defense."
}

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Sentient-Cyber Auditor",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# ============================================================================
# AUTHENTICATION
# ============================================================================
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if (
            st.session_state["username"] == "AIAF_Ops"
            and st.session_state["password"] == "AIAF_2026!"
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🛡️ Sentient-Cyber Platform Access")
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
    return False

if not check_password():
    st.stop()

# ============================================================================
# LOGIC & NODES (Mimicking graph.py)
# ============================================================================
def llm_audit_node(text_content, api_key):
    """
    Simulates a LangGraph node that calls Groq Llama 3 to propose scores.
    """
    client = Groq(api_key=api_key)
    
    system_prompt = """
    You are an expert AI Cybersecurity Auditor. Analyze the provided system documentation text 
    and estimate a Maturity Score (0-5) for these 6 domains:
    1. Identity & Access
    2. Memory & Data
    3. Agent Control
    4. Adversarial Defense
    5. Orchestration
    6. Supply Chain
    
    CRITICAL: Return ONLY a valid JSON object.
    Format:
    {
        "scores": { "Identity & Access": <int>, ... },
        "reasoning": "Brief summary of reasoning."
    }
    """
    
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this security documentation:\n\n{text_content[:6000]}"}
            ],
            # UPDATED: Replaced deprecated "llama3-70b-8192" with the active model
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        st.error(f"AI Node Failure: {e}")
        return None


# ============================================================================
# MAIN APPLICATION
# ============================================================================

# --- Session State Init ---
if 'audit_state' not in st.session_state:
    st.session_state.audit_state = "SETUP" # SETUP, ANALYSIS, REVIEW, REPORT
if 'ai_scores' not in st.session_state:
    st.session_state.ai_scores = {k: 0 for k in ["Identity & Access", "Memory & Data", "Agent Control", "Adversarial Defense", "Orchestration", "Supply Chain"]}
if 'ai_reasoning' not in st.session_state:
    st.session_state.ai_reasoning = ""

# --- Sidebar ---
# In your sidebar code in app.py:

with st.sidebar:
    st.title("⚙️ Configuration")
    
    # Try to get key from secrets first, otherwise default to empty
    if "GROQ_API_KEY" in st.secrets:
        default_key = st.secrets["GROQ_API_KEY"]
        api_key = st.text_input("Groq API Key", value=default_key, type="password", help="Loaded from secrets.toml")
    else:
        api_key = st.text_input("Groq API Key", type="password", help="Enter Key manually")


# --- Header ---
st.markdown("## 🛡️ Sentient-Cyber Audit Platform")
st.markdown("Assess Autonomous AI Agents against NIST AI RMF, MITRE ATLAS, and Agency Scopes.")
st.markdown("---")

# --- Phase 1: Agent Setup ---
if st.session_state.audit_state == "SETUP":
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("1. Agent Profile")
        agent_name = st.text_input("Agent Name", value="Finance-Bot-v1")
        agency_scope = st.selectbox("Target Agency Scope", AGENCY_SCOPES)
    
    with col2:
        st.subheader("2. Evidence Upload")
        uploaded_file = st.file_uploader("Upload System Architecture / Policy (TXT/JSON)", type=['txt', 'json', 'md'])

    if st.button("Start Analysis ➔", type="primary"):
        if agency_scope == "Select Scope...":
            st.error("Please select an Agency Scope.")
        elif not api_key:
            st.error("Groq API Key required.")
        elif not uploaded_file:
            st.error("Please upload evidence.")
        else:
            with st.spinner("Invoking LLM Audit Node..."):
                content = uploaded_file.read().decode("utf-8")
                result = llm_audit_node(content, api_key)
                if result:
                    st.session_state.ai_scores = result['scores']
                    st.session_state.ai_reasoning = result.get('reasoning', 'No reasoning provided.')
                    st.session_state.target_scope = agency_scope
                    st.session_state.target_score = SCOPE_TARGETS.get(agency_scope, 3.0)
                    st.session_state.audit_state = "REVIEW"
                    st.rerun()

# --- Phase 2: Human-in-the-Loop Review ---
if st.session_state.audit_state == "REVIEW":
    target_score = st.session_state.target_score
    
    # AI Insight Block
    with st.container():
        st.info(f"**🤖 AI Auditor Insight:** {st.session_state.ai_reasoning}")
    
    st.subheader("3. Validate Controls")
    st.caption("Adjust sliders based on your verification of the evidence.")
    
    final_scores = {}
    cols = st.columns(2)
    
    for i, (domain, score) in enumerate(st.session_state.ai_scores.items()):
        with cols[i % 2]:
            st.markdown(f"#### {domain}")
            val = st.slider(
                f"Maturity (0-5)", 0, 5, int(score), 
                key=f"slider_{domain}",
                help=MATURITY_DEFINITIONS.get(score, "")
            )
            final_scores[domain] = val
            
            # Dynamic Feedback
            if val > 0:
                st.caption(MATURITY_DEFINITIONS.get(val, ""))
            if val < target_score:
                st.markdown(f":red[⚠️ Gap: Needs +{target_score - val:.1f}]")
            else:
                st.markdown(":green[✅ Compliant]")
            st.markdown("---")

    col_act1, col_act2 = st.columns([1, 4])
    with col_act1:
        if st.button("✅ Approve & Finalize", type="primary"):
            st.session_state.ai_scores = final_scores
            st.session_state.audit_state = "REPORT"
            st.rerun()
    with col_act2:
        if st.button("⬅️ Back"):
            st.session_state.audit_state = "SETUP"
            st.rerun()

# --- Phase 3: Final Report ---
if st.session_state.audit_state == "REPORT":
    st.subheader("4. Executive Summary")
    
    scores = st.session_state.ai_scores
    target = st.session_state.target_score
    
    # Radar Chart
    categories = list(scores.keys())
    values = list(scores.values())
    targets = [target] * len(categories)
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=targets, theta=categories, fill='toself', name='Required Target', line_color='gray', line_dash='dot'))
    fig.add_trace(go.Scatterpolar(r=values, theta=categories, fill='toself', name='Agent Maturity', line_color='#00FFAA'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), height=500, template="plotly_dark")
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        avg_score = np.mean(values)
        st.metric("Final Score", f"{avg_score:.1f} / 5.0")
        
        if avg_score >= target:
            st.success("✅ **APPROVED FOR DEPLOYMENT**")
            st.markdown("Agent meets all safety requirements for this autonomy level.")
        else:
            st.error("⛔ **DEPLOYMENT BLOCKED**")
            st.markdown("Critical gaps found. Do not deploy.")
            
        st.download_button(
            "Download JSON Report",
            data=json.dumps(scores, indent=2),
            file_name="audit_report.json",
            mime="application/json"
        )
    
    if st.button("🔄 New Assessment"):
        st.session_state.audit_state = "SETUP"
        st.rerun()
