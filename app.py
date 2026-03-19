import streamlit as st
import requests
import json
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PolicyIQ · Marsh IMEA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

WEBHOOK_URL = "https://ridhay.app.n8n.cloud/webhook-test/insurance-extract"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #080c14;
    color: #e8eaf0;
}

.stApp {
    background: #080c14;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1300px; }

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, #0d1626 0%, #0a1a2e 50%, #091220 100%);
    border: 1px solid rgba(0,168,255,0.15);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(0,168,255,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 300px; height: 150px;
    background: radial-gradient(ellipse, rgba(0,210,180,0.06) 0%, transparent 70%);
}
.hero-badge {
    display: inline-block;
    background: rgba(0,168,255,0.12);
    border: 1px solid rgba(0,168,255,0.3);
    color: #00a8ff;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.hero h1 span { color: #00a8ff; }
.hero p {
    color: #7a8aaa;
    font-size: 0.95rem;
    margin: 0;
    font-weight: 300;
    max-width: 520px;
}

/* ── Section label ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #00a8ff;
    margin-bottom: 0.6rem;
}

/* ── Input card ── */
.input-card {
    background: #0d1626;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}

/* ── Textarea override ── */
.stTextArea textarea {
    background: #060a12 !important;
    border: 1px solid rgba(0,168,255,0.2) !important;
    border-radius: 12px !important;
    color: #c8d0e0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: rgba(0,168,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,168,255,0.08) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #0070cc, #00a8ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,168,255,0.25) !important;
}

/* ── Metric cards ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #0d1626;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00a8ff, #00d2b4);
}
.metric-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #4a6080;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-value.warning { color: #ffb84d; }
.metric-value.danger  { color: #ff4d6a; }
.metric-value.good    { color: #00d2b4; }
.metric-sub {
    font-size: 0.72rem;
    color: #4a6080;
}

/* ── Risk banner ── */
.risk-banner {
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    border: 1px solid;
}
.risk-banner.LOW    { background: rgba(0,210,180,0.07);  border-color: rgba(0,210,180,0.25);  }
.risk-banner.MEDIUM { background: rgba(255,184,77,0.07); border-color: rgba(255,184,77,0.25); }
.risk-banner.HIGH   { background: rgba(255,77,106,0.07); border-color: rgba(255,77,106,0.25); }
.risk-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.risk-dot.LOW    { background: #00d2b4; box-shadow: 0 0 8px #00d2b4; }
.risk-dot.MEDIUM { background: #ffb84d; box-shadow: 0 0 8px #ffb84d; }
.risk-dot.HIGH   { background: #ff4d6a; box-shadow: 0 0 8px #ff4d6a; }
.risk-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #fff;
}
.risk-sub { font-size: 0.78rem; color: #7a8aaa; margin-top: 0.15rem; }

/* ── Fields table ── */
.fields-card {
    background: #0d1626;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}
.fields-card h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    margin: 0 0 1.2rem 0;
}
.field-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.field-row:last-child { border-bottom: none; }
.field-key {
    font-size: 0.78rem;
    font-weight: 500;
    color: #4a6080;
    text-transform: capitalize;
    letter-spacing: 0.03em;
    flex: 1;
}
.field-val {
    font-size: 0.85rem;
    font-weight: 500;
    color: #c8d0e0;
    text-align: right;
    flex: 2;
}
.field-val.null-val {
    color: #ff4d6a;
    font-style: italic;
    font-size: 0.78rem;
}

/* ── Flags ── */
.flag-chip {
    display: inline-block;
    background: rgba(255,77,106,0.1);
    border: 1px solid rgba(255,77,106,0.25);
    color: #ff4d6a;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    margin: 0.2rem 0.2rem 0.2rem 0;
}
.flag-chip.warning {
    background: rgba(255,184,77,0.1);
    border-color: rgba(255,184,77,0.25);
    color: #ffb84d;
}

/* ── Risk clauses ── */
.clause-item {
    background: rgba(0,168,255,0.05);
    border-left: 3px solid #00a8ff;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    color: #a0b0cc;
    line-height: 1.5;
}

/* ── Score ring ── */
.score-wrap {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
}

/* ── Sample pills ── */
.sample-label {
    font-size: 0.72rem;
    color: #4a6080;
    margin-bottom: 0.5rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)


# ── Sample policies ────────────────────────────────────────────────────────────
SAMPLES = {
    "🏭 Manufacturing (High Risk)": """COMMERCIAL INSURANCE POLICY

Policy Number: MMC-MFG-2024-00892
Insured: Bharat Steel Industries Pvt. Ltd.
Location: Navi Mumbai, Maharashtra, India
Policy Type: Industrial All-Risk

Coverage Amount: INR 45,000,000
Annual Premium: INR 1,200,000
Policy Start Date: 15-03-2024
Policy Expiry Date: 28-03-2025

Claims History:
- Total Claims Filed: 6
- Total Claims Paid: INR 1,050,000
- Number of Active Policies: 3

Risk Clauses:
1. Machinery breakdown exclusion applies beyond normal wear
2. Flood damage limited to ground floor only
3. Business interruption coverage capped at 90 days
4. Third-party liability subject to excess of INR 50,000

Notes: Policy under review due to elevated claim frequency.""",

    "🏢 Corporate Office (Low Risk)": """COMMERCIAL PROPERTY INSURANCE

Policy Number: MMC-CORP-2025-04421
Insured: TechNova Solutions Pvt. Ltd.
Location: BKC, Mumbai, Maharashtra
Policy Type: Commercial Property & Liability

Coverage Amount: INR 20,000,000
Annual Premium: INR 380,000
Start Date: 01-01-2025
Expiry Date: 31-12-2025

Claims History:
- Claims Filed: 1
- Claims Paid: INR 45,000
- Number of Policies: 2

Risk Clauses:
1. Electronic equipment covered up to replacement value
2. Acts of terrorism covered under separate endorsement""",

    "🚢 Marine Cargo (Expiring Soon)": """MARINE CARGO INSURANCE CERTIFICATE

Policy Reference: MMC-MCG-2025-00134
Insured Party: Global Exports Ltd.
Location: JNPT, Nhava Sheva, Mumbai
Coverage Type: Marine Cargo Open Cover

Sum Insured: USD 500,000
Premium Paid: USD 12,500
Inception Date: 20-03-2025
Expiry Date: 05-04-2025

Claim Records:
- Number of Claims: 3
- Settled Amount: USD 28,000
- Policies in Force: 1

Special Conditions:
1. Institute Cargo Clauses (A) apply
2. War and strikes risk covered under separate endorsement
3. Temperature-sensitive cargo requires refrigerated container certification"""
}


# ── Helper functions ───────────────────────────────────────────────────────────
def call_webhook(policy_text: str):
    try:
        resp = requests.post(
            WEBHOOK_URL,
            json={"policy_text": policy_text},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.Timeout:
        return None, "Request timed out. Make sure your n8n workflow is active."
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to n8n. Make sure your workflow is active and the webhook URL is correct."
    except Exception as e:
        return None, f"Error: {str(e)}"


def fmt_currency(val, prefix="₹"):
    if val is None:
        return None
    if val >= 1_000_000:
        return f"{prefix}{val/1_000_000:.2f}M"
    if val >= 1_000:
        return f"{prefix}{val/1_000:.1f}K"
    return f"{prefix}{val:,.0f}"


def ratio_color(name, value):
    if value is None:
        return "metric-value"
    if name == "loss_ratio":
        if value >= 100: return "metric-value danger"
        if value >= 75:  return "metric-value warning"
        return "metric-value good"
    if name == "coverage_utilization":
        if value >= 80: return "metric-value danger"
        if value >= 50: return "metric-value warning"
        return "metric-value good"
    if name == "claim_frequency":
        if value >= 3:   return "metric-value danger"
        if value >= 1.5: return "metric-value warning"
        return "metric-value good"
    return "metric-value"


# ── UI ─────────────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-badge">Marsh IMEA · OPEX Analytics</div>
    <h1>Policy<span>IQ</span></h1>
    <p>AI-powered insurance document intelligence. Extract entities, compute risk ratios, and flag anomalies in seconds.</p>
</div>
""", unsafe_allow_html=True)

# Layout
left, right = st.columns([1, 1.2], gap="large")

with left:
    st.markdown('<div class="section-label">Input Document</div>', unsafe_allow_html=True)

    # Sample selector
    st.markdown('<div class="sample-label">Load a sample policy →</div>', unsafe_allow_html=True)
    sample_choice = st.selectbox(
        "sample",
        ["— select a sample —"] + list(SAMPLES.keys()),
        label_visibility="collapsed"
    )

    default_text = SAMPLES.get(sample_choice, "") if sample_choice != "— select a sample —" else ""

    policy_text = st.text_area(
        "Paste your insurance policy text",
        value=default_text,
        height=380,
        placeholder="Paste raw insurance policy text here...\n\nInclude: policy number, insured name, coverage amount, premium, expiry date, claims history, risk clauses.",
        label_visibility="collapsed"
    )

    analyze_btn = st.button("⚡  Analyse Policy", use_container_width=True)

    # Info box
    st.markdown("""
    <div style="background:#060a12;border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:1rem 1.2rem;margin-top:1rem;">
        <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#4a6080;margin-bottom:0.6rem;">What gets extracted</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.3rem;">
            <div style="font-size:0.75rem;color:#5a7090;">✦ Policy & insured details</div>
            <div style="font-size:0.75rem;color:#5a7090;">✦ Coverage & premium</div>
            <div style="font-size:0.75rem;color:#5a7090;">✦ Claims history</div>
            <div style="font-size:0.75rem;color:#5a7090;">✦ Expiry & dates</div>
            <div style="font-size:0.75rem;color:#5a7090;">✦ Loss & risk ratios</div>
            <div style="font-size:0.75rem;color:#5a7090;">✦ Risk clause flags</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


with right:
    st.markdown('<div class="section-label">Analysis Output</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not policy_text.strip():
            st.warning("Please paste a policy document or load a sample.")
        else:
            with st.spinner("Running extraction pipeline..."):
                result, error = call_webhook(policy_text)

            if error:
                st.error(f"**Pipeline Error:** {error}")
            elif result and result.get("status") == "success":
                ef = result.get("extracted_fields", {})
                ratios = result.get("ratios", {})
                risk = result.get("risk_assessment", {})

                risk_level = risk.get("risk_level", "LOW")
                risk_score = risk.get("risk_score", 0)
                risk_flags = risk.get("risk_flags", [])

                # ── Risk banner ──
                risk_icons = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
                risk_desc = {
                    "LOW": "Policy looks healthy. No major anomalies detected.",
                    "MEDIUM": "Some concerns identified. Review flagged items.",
                    "HIGH": "Immediate attention required. Multiple risk indicators active."
                }
                st.markdown(f"""
                <div class="risk-banner {risk_level}">
                    <div class="risk-dot {risk_level}"></div>
                    <div>
                        <div class="risk-title">{risk_icons[risk_level]} {risk_level} RISK &nbsp;·&nbsp; Score: {risk_score}/100</div>
                        <div class="risk-sub">{risk_desc[risk_level]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Ratio metrics ──
                lr = ratios.get("loss_ratio")
                cu = ratios.get("coverage_utilization")
                cf = ratios.get("claim_frequency")

                st.markdown(f"""
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Loss Ratio</div>
                        <div class="{ratio_color('loss_ratio', lr)}">{f"{lr:.1f}%" if lr is not None else "N/A"}</div>
                        <div class="metric-sub">Claims ÷ Premium</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Coverage Utilization</div>
                        <div class="{ratio_color('coverage_utilization', cu)}">{f"{cu:.1f}%" if cu is not None else "N/A"}</div>
                        <div class="metric-sub">Claims ÷ Coverage</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Claim Frequency</div>
                        <div class="{ratio_color('claim_frequency', cf)}">{f"{cf:.2f}" if cf is not None else "N/A"}</div>
                        <div class="metric-sub">Claims ÷ Policies</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Extracted fields ──
                display_fields = {
                    "Policy Number": ef.get("policy_number"),
                    "Insured Name": ef.get("insured_name"),
                    "Location": ef.get("insured_location"),
                    "Policy Type": ef.get("policy_type"),
                    "Coverage Amount": fmt_currency(ef.get("coverage_amount")),
                    "Premium Amount": fmt_currency(ef.get("premium_amount")),
                    "Claims Paid": fmt_currency(ef.get("claims_paid")),
                    "No. of Claims": ef.get("number_of_claims"),
                    "Start Date": ef.get("start_date"),
                    "Expiry Date": ef.get("expiry_date"),
                }

                rows_html = ""
                for k, v in display_fields.items():
                    if v is None or str(v).lower() in ["none", "null", ""]:
                        val_html = f'<div class="field-val null-val">Not found</div>'
                    else:
                        val_html = f'<div class="field-val">{v}</div>'
                    rows_html += f'<div class="field-row"><div class="field-key">{k}</div>{val_html}</div>'

                st.markdown(f"""
                <div class="fields-card">
                    <h3>📋 Extracted Fields</h3>
                    {rows_html}
                </div>
                """, unsafe_allow_html=True)

                # ── Risk flags ──
                if risk_flags:
                    flags_html = "".join([f'<span class="flag-chip">{f}</span>' for f in risk_flags])
                    st.markdown(f"""
                    <div class="fields-card">
                        <h3>⚠️ Risk Flags</h3>
                        {flags_html}
                    </div>
                    """, unsafe_allow_html=True)

                # ── Risk clauses ──
                clauses = ef.get("risk_clauses", [])
                if clauses:
                    clauses_html = "".join([f'<div class="clause-item">{c}</div>' for c in clauses])
                    st.markdown(f"""
                    <div class="fields-card">
                        <h3>📌 Risk Clauses Identified</h3>
                        {clauses_html}
                    </div>
                    """, unsafe_allow_html=True)

                # ── Missing fields ──
                missing = ef.get("missing_fields", [])
                if missing:
                    missing_html = "".join([f'<span class="flag-chip warning">{m}</span>' for m in missing])
                    st.markdown(f"""
                    <div class="fields-card">
                        <h3>🔍 Missing / Unclear Fields</h3>
                        {missing_html}
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.error("Unexpected response from pipeline. Check your n8n workflow is active.")

    else:
        # Empty state
        st.markdown("""
        <div style="background:#0d1626;border:1px dashed rgba(0,168,255,0.15);border-radius:16px;
                    padding:4rem 2rem;text-align:center;margin-top:0.5rem;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">🛡️</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#2a3a55;margin-bottom:0.5rem;">
                No document analysed yet
            </div>
            <div style="font-size:0.82rem;color:#2a3a55;max-width:280px;margin:0 auto;">
                Paste a policy document or load a sample, then click Analyse Policy
            </div>
        </div>
        """, unsafe_allow_html=True)
