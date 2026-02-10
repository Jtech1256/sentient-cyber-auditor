
# Sentient-Cyber AI Auditor 🛡️
## About
The **Sentient-Cyber AI Auditor** is an enterprise-grade Streamlit platform for assessing AI agent security maturity against NIST AI RMF, MITRE ATLAS, and AWS Agency Scopes. 

AI agents are autonomous, but are they *secure*? This tool provides **AI-powered first-pass analysis** with **human-in-the-loop review**, generating executive-ready radar charts and compliance reports.

## Features
### 1. Evidence Upload & AI Analysis
- Upload system architecture, policies, or audit logs (TXT/JSON).
- **Groq Llama 3.3** automatically scores 6 security domains (Identity, Control, Adversarial Defense, etc.).

### 2. Human-in-the-Loop Review
- AI pre-fills sliders with recommended scores + reasoning.
- Override scores based on expert judgment.
- Real-time gap analysis vs. your target Agency Scope.

### 3. Agency Scope Framework
- **Scope 1:** Read-Only (Informational)
- **Scope 2:** Human-in-the-Loop (Proposer)
- **Scope 3:** Bounded Autonomy (Executor)
- **Scope 4:** Full Agency (Autonomous)

### 4. Executive Visualizations
- Interactive radar charts comparing current vs. required maturity.
- Automatic **APPROVED/REJECTED** decisions with audit trails.

### 5. JSON Audit Reports
- Downloadable compliance reports for SOC2, ISO 42001.
- Session state persistence for audit continuity.

### 6. Enterprise Authentication
- Username/Password login (`AIAF_Ops` / `AIAF_2026!`).
- Secrets management via `.streamlit/secrets.toml`.

## Tech Stack
```
Frontend: Streamlit + Plotly (Radar Charts)
Backend: Python + Groq Llama 3.3 70B
Security: NIST AI RMF, MITRE ATLAS, OWASP LLM Top 10
Data: Pandas + JSON Session State
Deployment: GitHub Pages / Streamlit Cloud
```

## Installation

### Prerequisites
- Python 3.10+
- GitHub account
- [Groq API Key](https://console.groq.com) (free tier available)

### Steps
```bash
# Clone the repo
git clone https://github.com/Jtech1256/sentient-cyber-auditor.git
cd sentient-cyber-auditor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Setup secrets (add your Groq key)
# Edit .streamlit/secrets.toml
```

### Run Locally
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501)

## Usage Workflow
```
1. Login → Configure Agent Profile → Select Agency Scope
2. Upload Evidence → AI Analyzes → Review Sliders
3. Approve → Generate Radar Chart → Download Report
```

## File Structure
```
.
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── .gitignore              # Git exclusions
├── .streamlit/secrets.toml # API keys (gitignored)
└── README.md              # This file
```

## Screenshots
### Dashboard
![Dashboard](https://via.placeholder.com/800x400/1e3a8a/ffffff?text=AI+Auditor+Dashboard)
### Radar Chart Analysis
![Radar Chart](https://via.placeholder.com/800x400/0ea5e9/ffffff?text=Agency+Scope+Radar+Chart)
### Gap Analysis
![Gap Analysis](https://via.placeholder.com/800x400/10b981/ffffff?text=Security+Gaps+Identified)

## Deployment Options
### Streamlit Cloud (Free)
1. Fork this repo on GitHub.
2. Connect to [share.streamlit.io](https://share.streamlit.io).
3. Deploy → Live URL in 2 minutes.

### GitHub Pages (Static Demo)
Add `streamlit hello` output to `/docs`.

## Security Maturity Levels
| Score | Level | Controls |
|-------|-------|----------|
| 0-1 | **Basic** | Manual logs, static keys |
| 2 | **Managed** | RBAC, PII redaction |
| 3 | **Defined** | Trajectory logging, kill-switches |
| 4-5 | **Optimized** | Self-healing, real-time defense |

## Future Improvements
- Multi-agent orchestration assessment.
- Integration with AWS Bedrock Guardrails, Azure Content Safety.
- Automated remediation code generation.
- SOC2/ISO 42001 compliance templates.

## Contributing
Contributions welcome! Open issues for:
- New security domains
- Framework integrations (CSA, OWASP)
- Model provider support (Anthropic, OpenAI)

## License
MIT License - see [LICENSE](LICENSE) © 2026

## Contact
**Author:** Joel Gashaw

```
