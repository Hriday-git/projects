import streamlit as st
import requests
import json
import plotly.graph_objects as go
import pandas as pd
import pdfplumber
import docx
import io
import csv

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PolicyIQ · Marsh IMEA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

WEBHOOK_URL = "https://ridhay.app.n8n.cloud/webhook-test/insurance-extract"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Figtree:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Figtree', sans-serif;
    background-color: #07090f;
    color: #dde2ee;
}
.stApp { background: #07090f; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.8rem 2.5rem 4rem 2.5rem; max-width: 1400px; }

[data-testid="stSidebar"] {
    background: #0b0f1a !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem; }

.hero {
    background: linear-gradient(135deg, #0c1424 0%, #0a1830 60%, #07101e 100%);
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:'';position:absolute;top:-80px;right:-80px;
    width:280px;height:280px;
    background:radial-gradient(circle,rgba(56,189,248,0.1) 0%,transparent 70%);
    border-radius:50%;
}
.hero-badge {
    display:inline-block;
    background:rgba(56,189,248,0.1);
    border:1px solid rgba(56,189,248,0.25);
    color:#38bdf8;
    font-size:0.65rem;font-weight:700;
    letter-spacing:0.18em;text-transform:uppercase;
    padding:0.28rem 0.8rem;border-radius:20px;margin-bottom:0.9rem;
}
.hero h1 {
    font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;
    color:#fff;margin:0 0 0.4rem 0;line-height:1.1;letter-spacing:-0.02em;
}
.hero h1 span { color:#38bdf8; }
.hero p { color:#64748b;font-size:0.9rem;margin:0;font-weight:400;max-width:500px; }

.slabel {
    font-size:0.65rem;font-weight:700;letter-spacing:0.18em;
    text-transform:uppercase;color:#38bdf8;margin-bottom:0.5rem;
}

.card {
    background:#0c1424;border:1px solid rgba(255,255,255,0.06);
    border-radius:16px;padding:1.6rem;margin-bottom:1.2rem;
}
.card h3 {
    font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;
    color:#fff;margin:0 0 1rem 0;
}

.mcard {
    background:#0c1424;border:1px solid rgba(255,255,255,0.06);
    border-radius:14px;padding:1.3rem 1.5rem;position:relative;overflow:hidden;
    margin-bottom:1rem;
}
.mcard::before {
    content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,#38bdf8,#00d2b4);
}
.mcard-label {
    font-size:0.65rem;font-weight:700;letter-spacing:0.12em;
    text-transform:uppercase;color:#334155;margin-bottom:0.45rem;
}
.mcard-val {
    font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;
    color:#fff;line-height:1;margin-bottom:0.25rem;
}
.mcard-val.good  { color:#00d2b4; }
.mcard-val.warn  { color:#fbbf24; }
.mcard-val.bad   { color:#f43f5e; }
.mcard-sub { font-size:0.7rem;color:#334155; }

.rbanner {
    border-radius:14px;padding:1.1rem 1.5rem;
    margin-bottom:1.2rem;display:flex;align-items:center;gap:1rem;border:1px solid;
}
.rbanner.LOW    { background:rgba(0,210,180,0.06);border-color:rgba(0,210,180,0.2); }
.rbanner.MEDIUM { background:rgba(251,191,36,0.06);border-color:rgba(251,191,36,0.2); }
.rbanner.HIGH   { background:rgba(244,63,94,0.06);border-color:rgba(244,63,94,0.2); }
.rdot { width:9px;height:9px;border-radius:50%;flex-shrink:0; }
.rdot.LOW    { background:#00d2b4;box-shadow:0 0 8px #00d2b4; }
.rdot.MEDIUM { background:#fbbf24;box-shadow:0 0 8px #fbbf24; }
.rdot.HIGH   { background:#f43f5e;box-shadow:0 0 8px #f43f5e; }
.rtitle { font-family:'Syne',sans-serif;font-weight:700;font-size:0.92rem;color:#fff; }
.rsub   { font-size:0.75rem;color:#64748b;margin-top:0.1rem; }

.frow {
    display:flex;justify-content:space-between;align-items:center;
    padding:0.6rem 0;border-bottom:1px solid rgba(255,255,255,0.04);
}
.frow:last-child { border-bottom:none; }
.fkey { font-size:0.75rem;font-weight:500;color:#334155;flex:1; }
.fval { font-size:0.82rem;font-weight:500;color:#cbd5e1;text-align:right;flex:2; }
.fval.missing { color:#f43f5e;font-style:italic;font-size:0.75rem; }

.chip {
    display:inline-block;
    background:rgba(244,63,94,0.08);border:1px solid rgba(244,63,94,0.2);
    color:#f43f5e;font-size:0.7rem;font-weight:500;
    padding:0.22rem 0.65rem;border-radius:20px;margin:0.15rem;
}
.chip.warn { background:rgba(251,191,36,0.08);border-color:rgba(251,191,36,0.2);color:#fbbf24; }
.chip.info { background:rgba(56,189,248,0.08);border-color:rgba(56,189,248,0.2);color:#38bdf8; }

.clause {
    background:rgba(56,189,248,0.04);border-left:3px solid #38bdf8;
    border-radius:0 8px 8px 0;padding:0.55rem 0.9rem;margin-bottom:0.4rem;
    font-size:0.8rem;color:#94a3b8;line-height:1.5;
}

.stTextArea textarea {
    background:#060810 !important;border:1px solid rgba(56,189,248,0.18) !important;
    border-radius:12px !important;color:#b0bcd0 !important;
    font-family:'Figtree',sans-serif !important;font-size:0.85rem !important;
    line-height:1.7 !important;padding:1rem !important;
}
.stTextArea textarea:focus {
    border-color:rgba(56,189,248,0.45) !important;
    box-shadow:0 0 0 3px rgba(56,189,248,0.07) !important;
}

.stButton > button {
    background:linear-gradient(135deg,#0369a1,#38bdf8) !important;
    color:white !important;border:none !important;border-radius:10px !important;
    padding:0.65rem 2rem !important;font-family:'Syne',sans-serif !important;
    font-weight:700 !important;font-size:0.82rem !important;
    letter-spacing:0.06em !important;text-transform:uppercase !important;
    width:100% !important;transition:all 0.2s !important;
}
.stButton > button:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 8px 24px rgba(56,189,248,0.2) !important;
}

.divider { height:1px;background:rgba(255,255,255,0.05);margin:1.5rem 0; }

.ptable { width:100%;border-collapse:collapse; }
.ptable th {
    font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
    color:#334155;padding:0.6rem 1rem;border-bottom:1px solid rgba(255,255,255,0.06);text-align:left;
}
.ptable td {
    font-size:0.82rem;color:#94a3b8;padding:0.75rem 1rem;
    border-bottom:1px solid rgba(255,255,255,0.03);
}
.badge { display:inline-block;font-size:0.65rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:20px; }
.badge.LOW    { background:rgba(0,210,180,0.1);color:#00d2b4; }
.badge.MEDIUM { background:rgba(251,191,36,0.1);color:#fbbf24; }
.badge.HIGH   { background:rgba(244,63,94,0.1);color:#f43f5e; }

.about-card {
    background:#0c1424;border:1px solid rgba(255,255,255,0.06);
    border-radius:14px;padding:1.5rem;height:100%;
}
.about-icon { font-size:1.8rem;margin-bottom:0.8rem; }
.about-title { font-family:'Syne',sans-serif;font-weight:700;font-size:0.95rem;color:#fff;margin-bottom:0.5rem; }
.about-desc { font-size:0.82rem;color:#64748b;line-height:1.6; }

.step {
    display:flex;gap:1rem;align-items:flex-start;padding:1rem;border-radius:12px;
    background:rgba(56,189,248,0.03);border:1px solid rgba(56,189,248,0.08);margin-bottom:0.8rem;
}
.step-num {
    background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.2);
    color:#38bdf8;font-family:'Syne',sans-serif;font-weight:800;font-size:0.85rem;
    width:32px;height:32px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;flex-shrink:0;
}
.step-title { font-weight:600;font-size:0.88rem;color:#e2e8f0;margin-bottom:0.25rem; }
.step-desc  { font-size:0.78rem;color:#64748b;line-height:1.5; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "page" not in st.session_state:
    st.session_state.page = "Policy Analyser"

# ── Sample policies ───────────────────────────────────────────────────────────
SAMPLES = {
    "🏭 Manufacturing — High Risk": """COMMERCIAL INSURANCE POLICY
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
4. Third-party liability subject to excess of INR 50,000""",

    "🏢 Corporate Office — Low Risk": """COMMERCIAL PROPERTY INSURANCE
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

    "🚢 Marine Cargo — Expiring Soon": """MARINE CARGO INSURANCE CERTIFICATE
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

# ── Helpers ───────────────────────────────────────────────────────────────────
def call_webhook(policy_text):
    try:
        r = requests.post(WEBHOOK_URL, json={"policy_text": policy_text}, timeout=60)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.Timeout:
        return None, "Request timed out. Make sure your n8n workflow is active."
    except Exception as e:
        return None, str(e)

def fmt_currency(val):
    if val is None: return "N/A"
    if val >= 1_000_000: return f"₹{val/1_000_000:.2f}M"
    if val >= 1_000:     return f"₹{val/1_000:.1f}K"
    return f"₹{val:,.0f}"

def ratio_cls(name, v):
    if v is None: return "mcard-val"
    if name == "loss_ratio":
        return "mcard-val bad" if v>=100 else "mcard-val warn" if v>=75 else "mcard-val good"
    if name == "coverage_utilization":
        return "mcard-val bad" if v>=80 else "mcard-val warn" if v>=50 else "mcard-val good"
    if name == "claim_frequency":
        return "mcard-val bad" if v>=3 else "mcard-val warn" if v>=1.5 else "mcard-val good"
    return "mcard-val"

def extract_text_from_file(uploaded_file):
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        elif name.endswith(".docx"):
            d = docx.Document(uploaded_file)
            return "\n".join(p.text for p in d.paragraphs)
        elif name.endswith(".csv"):
            content = uploaded_file.read().decode("utf-8")
            reader = csv.reader(io.StringIO(content))
            return "\n".join(", ".join(row) for row in reader)
        elif name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")
    except Exception as e:
        return None
    return None

def make_gauge(score, level):
    color = {"LOW":"#00d2b4","MEDIUM":"#fbbf24","HIGH":"#f43f5e"}.get(level,"#38bdf8")
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        domain={"x":[0,1],"y":[0,1]},
        gauge={
            "axis":{"range":[0,100],"tickcolor":"#334155","tickfont":{"color":"#334155","size":10}},
            "bar":{"color":color,"thickness":0.25},
            "bgcolor":"#0c1424","bordercolor":"rgba(0,0,0,0)",
            "steps":[
                {"range":[0,30],"color":"rgba(0,210,180,0.08)"},
                {"range":[30,60],"color":"rgba(251,191,36,0.08)"},
                {"range":[60,100],"color":"rgba(244,63,94,0.08)"}
            ],
            "threshold":{"line":{"color":color,"width":3},"thickness":0.8,"value":score}
        },
        number={"font":{"color":"#fff","size":32,"family":"Syne"},"suffix":"/100"}
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=200,margin=dict(t=20,b=10,l=20,r=20),font={"color":"#334155"})
    return fig

def make_pie(claims, premium):
    fig = go.Figure(go.Pie(
        labels=["Claims Paid","Retained Premium"],
        values=[claims, max(premium-claims,0)],
        hole=0.55,
        marker=dict(colors=["#f43f5e","#38bdf8"],line=dict(color="#07090f",width=2)),
        textfont=dict(color="#fff",size=11),
        hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>"
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,height=220,margin=dict(t=10,b=10,l=10,r=10),
        legend=dict(font=dict(color="#64748b",size=10),bgcolor="rgba(0,0,0,0)"))
    return fig

def make_donut(utilization):
    val = utilization if utilization else 0
    color = "#f43f5e" if val>=80 else "#fbbf24" if val>=50 else "#00d2b4"
    fig = go.Figure(go.Pie(
        labels=["Utilized","Available"],
        values=[val, max(100-val,0)],
        hole=0.65,
        marker=dict(colors=[color,"rgba(255,255,255,0.05)"],line=dict(color="#07090f",width=2)),
        textinfo="none",
        hovertemplate="%{label}: %{value:.1f}%<extra></extra>"
    ))
    fig.add_annotation(text=f"{val:.1f}%",x=0.5,y=0.5,showarrow=False,
        font=dict(size=20,color="#fff",family="Syne"),xanchor="center")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,height=200,margin=dict(t=10,b=10,l=10,r=10))
    return fig

def make_bar(ratios):
    names = ["Loss Ratio","Coverage Util.","Claim Freq. ×10"]
    vals  = [ratios.get("loss_ratio") or 0,
             ratios.get("coverage_utilization") or 0,
             (ratios.get("claim_frequency") or 0)*10]
    colors = []
    for n,v in zip(["loss_ratio","coverage_utilization","claim_frequency"],
                   [ratios.get("loss_ratio"),ratios.get("coverage_utilization"),ratios.get("claim_frequency")]):
        if v is None: colors.append("#334155")
        elif n=="loss_ratio":           colors.append("#f43f5e" if v>=100 else "#fbbf24" if v>=75 else "#00d2b4")
        elif n=="coverage_utilization": colors.append("#f43f5e" if v>=80  else "#fbbf24" if v>=50 else "#00d2b4")
        else:                           colors.append("#f43f5e" if v>=3   else "#fbbf24" if v>=1.5 else "#00d2b4")
    fig = go.Figure(go.Bar(
        x=names, y=vals, marker_color=colors,
        text=[f"{v:.1f}" for v in vals], textposition="outside",
        textfont=dict(color="#94a3b8",size=11),
        hovertemplate="%{x}: %{y:.2f}<extra></extra>"
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=230,margin=dict(t=30,b=10,l=10,r=10),bargap=0.4,
        xaxis=dict(tickfont=dict(color="#64748b",size=11),gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(255,255,255,0.04)",zeroline=False))
    return fig

def make_portfolio_chart(portfolio):
    names  = [p["name"][:16] for p in portfolio]
    scores = [p["risk_score"] for p in portfolio]
    colors = ["#f43f5e" if p["risk_level"]=="HIGH" else "#fbbf24" if p["risk_level"]=="MEDIUM" else "#00d2b4" for p in portfolio]
    fig = go.Figure(go.Bar(x=names,y=scores,marker_color=colors,
        text=scores,textposition="outside",textfont=dict(color="#94a3b8",size=11),
        hovertemplate="%{x}<br>Risk Score: %{y}<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=270,margin=dict(t=20,b=20,l=10,r=10),bargap=0.35,
        xaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(255,255,255,0.04)",
                   zeroline=False,range=[0,115]))
    return fig

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:#fff;">
            Policy<span style="color:#38bdf8;">IQ</span>
        </div>
        <div style="font-size:0.68rem;color:#334155;margin-top:0.2rem;letter-spacing:0.1em;text-transform:uppercase;">
            Marsh IMEA · OPEX Analytics
        </div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.05);margin-bottom:1.2rem;"></div>
    """, unsafe_allow_html=True)

    pages = {"Policy Analyser":"🔍","Portfolio Dashboard":"📊","Benchmarking":"⚖️","How It Works":"💡"}
    for pg, icon in pages.items():
        if st.button(f"{icon}  {pg}", key=f"nav_{pg}", use_container_width=True):
            st.session_state.page = pg
            st.rerun()

    st.markdown("""
    <div style="height:1px;background:rgba(255,255,255,0.05);margin:1.5rem 0 1rem 0;"></div>
    <div style="font-size:0.68rem;color:#1e293b;line-height:1.7;">
        Powered by n8n · GPT-4.1-mini<br>
        Built for Marsh IMEA OPEX<br>
        <span style="color:#38bdf8;">Data Science Internship 2025</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Policy Analyser
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Policy Analyser":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">AI Document Intelligence</div>
        <h1>Policy<span>IQ</span> Analyser</h1>
        <p>Paste or upload an insurance policy. The AI pipeline extracts entities, computes risk ratios, and flags anomalies instantly.</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1.25], gap="large")

    with left:
        st.markdown('<div class="slabel">Input Method</div>', unsafe_allow_html=True)
        input_mode = st.radio("input_mode", ["📝 Text","📄 PDF","📊 CSV","📃 Word Doc"],
                              horizontal=True, label_visibility="collapsed")
        policy_text = ""

        if input_mode == "📝 Text":
            sample = st.selectbox("Load sample",["— or load a sample policy —"]+list(SAMPLES.keys()),
                                  label_visibility="collapsed")
            default = SAMPLES.get(sample,"") if sample != "— or load a sample policy —" else ""
            policy_text = st.text_area("Policy text", value=default, height=320,
                placeholder="Paste raw insurance policy text here...",
                label_visibility="collapsed")
        else:
            ext = {"📄 PDF":["pdf"],"📊 CSV":["csv"],"📃 Word Doc":["docx"]}[input_mode]
            uploaded = st.file_uploader(f"Upload file", type=ext, label_visibility="collapsed")
            if uploaded:
                with st.spinner("Reading file..."):
                    policy_text = extract_text_from_file(uploaded)
                if policy_text:
                    st.success(f"✅ {len(policy_text)} characters extracted")
                    with st.expander("Preview extracted text"):
                        st.text(policy_text[:800]+("..." if len(policy_text)>800 else ""))
                else:
                    st.error("Could not extract text from this file.")

        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
        analyse = st.button("⚡  Run AI Analysis", use_container_width=True)

        st.markdown("""
        <div style="background:#060810;border:1px solid rgba(255,255,255,0.04);
                    border-radius:12px;padding:1rem 1.2rem;margin-top:1rem;">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.12em;
                        text-transform:uppercase;color:#1e293b;margin-bottom:0.6rem;">Pipeline extracts</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.25rem;">
                <div style="font-size:0.73rem;color:#334155;">✦ Policy & insured info</div>
                <div style="font-size:0.73rem;color:#334155;">✦ Coverage & premium</div>
                <div style="font-size:0.73rem;color:#334155;">✦ Claims history</div>
                <div style="font-size:0.73rem;color:#334155;">✦ Loss ratio</div>
                <div style="font-size:0.73rem;color:#334155;">✦ Risk score & flags</div>
                <div style="font-size:0.73rem;color:#334155;">✦ Risk clauses</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="slabel">Analysis Output</div>', unsafe_allow_html=True)

        if analyse:
            if not policy_text or not policy_text.strip():
                st.warning("Please provide policy text or upload a file.")
            else:
                with st.spinner("Running extraction pipeline..."):
                    result, error = call_webhook(policy_text)

                if error:
                    st.error(f"**Pipeline error:** {error}")
                elif result and result.get("status") == "success":
                    ef     = result.get("extracted_fields", {})
                    ratios = result.get("ratios", {})
                    risk   = result.get("risk_assessment", {})
                    rl     = risk.get("risk_level","LOW")
                    rs     = risk.get("risk_score",0)
                    flags  = risk.get("risk_flags",[])

                    # Save to portfolio
                    st.session_state.portfolio.append({
                        "name": ef.get("insured_name") or "Unknown",
                        "policy_type": ef.get("policy_type") or "N/A",
                        "risk_level": rl, "risk_score": rs,
                        "loss_ratio": ratios.get("loss_ratio"),
                        "coverage_utilization": ratios.get("coverage_utilization"),
                        "claim_frequency": ratios.get("claim_frequency"),
                        "premium": ef.get("premium_amount"),
                        "claims": ef.get("claims_paid"),
                        "expiry": ef.get("expiry_date") or "N/A"
                    })

                    # Risk banner
                    icons = {"LOW":"🟢","MEDIUM":"🟡","HIGH":"🔴"}
                    descs = {"LOW":"Policy looks healthy. No major anomalies detected.",
                             "MEDIUM":"Some concerns identified. Review flagged items.",
                             "HIGH":"Immediate attention required. Multiple risk indicators active."}
                    st.markdown(f"""
                    <div class="rbanner {rl}">
                        <div class="rdot {rl}"></div>
                        <div>
                            <div class="rtitle">{icons[rl]} {rl} RISK &nbsp;·&nbsp; Score: {rs}/100</div>
                            <div class="rsub">{descs[rl]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Ratio metrics
                    lr = ratios.get("loss_ratio")
                    cu = ratios.get("coverage_utilization")
                    cf = ratios.get("claim_frequency")
                    c1,c2,c3 = st.columns(3)
                    with c1:
                        st.markdown(f"""<div class="mcard">
                            <div class="mcard-label">Loss Ratio</div>
                            <div class="{ratio_cls('loss_ratio',lr)}">{f"{lr:.1f}%" if lr else "N/A"}</div>
                            <div class="mcard-sub">Claims ÷ Premium</div></div>""", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""<div class="mcard">
                            <div class="mcard-label">Coverage Util.</div>
                            <div class="{ratio_cls('coverage_utilization',cu)}">{f"{cu:.1f}%" if cu else "N/A"}</div>
                            <div class="mcard-sub">Claims ÷ Coverage</div></div>""", unsafe_allow_html=True)
                    with c3:
                        st.markdown(f"""<div class="mcard">
                            <div class="mcard-label">Claim Frequency</div>
                            <div class="{ratio_cls('claim_frequency',cf)}">{f"{cf:.2f}" if cf else "N/A"}</div>
                            <div class="mcard-sub">Claims ÷ Policies</div></div>""", unsafe_allow_html=True)

                    # Charts
                    ch1,ch2,ch3 = st.columns(3)
                    with ch1:
                        st.markdown('<div class="slabel" style="margin-top:0.8rem;">Risk Score</div>', unsafe_allow_html=True)
                        st.plotly_chart(make_gauge(rs,rl), use_container_width=True, config={"displayModeBar":False})
                    with ch2:
                        st.markdown('<div class="slabel" style="margin-top:0.8rem;">Claims vs Premium</div>', unsafe_allow_html=True)
                        st.plotly_chart(make_pie(ef.get("claims_paid") or 0, ef.get("premium_amount") or 1),
                                        use_container_width=True, config={"displayModeBar":False})
                    with ch3:
                        st.markdown('<div class="slabel" style="margin-top:0.8rem;">Coverage Utilization</div>', unsafe_allow_html=True)
                        st.plotly_chart(make_donut(cu), use_container_width=True, config={"displayModeBar":False})

                    st.markdown('<div class="slabel" style="margin-top:0.2rem;">Key Ratios Breakdown</div>', unsafe_allow_html=True)
                    st.plotly_chart(make_bar(ratios), use_container_width=True, config={"displayModeBar":False})

                    # Extracted fields
                    display = {
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
                    rows = ""
                    for k,v in display.items():
                        if not v or str(v).lower() in ["none","null",""]:
                            rows += f'<div class="frow"><div class="fkey">{k}</div><div class="fval missing">Not found</div></div>'
                        else:
                            rows += f'<div class="frow"><div class="fkey">{k}</div><div class="fval">{v}</div></div>'
                    st.markdown(f'<div class="card"><h3>📋 Extracted Fields</h3>{rows}</div>', unsafe_allow_html=True)

                    fc1,fc2 = st.columns(2)
                    with fc1:
                        if flags:
                            chips = "".join([f'<span class="chip">{f}</span>' for f in flags])
                            st.markdown(f'<div class="card"><h3>⚠️ Risk Flags</h3>{chips}</div>', unsafe_allow_html=True)
                        missing = ef.get("missing_fields",[])
                        if missing:
                            chips = "".join([f'<span class="chip warn">{m}</span>' for m in missing])
                            st.markdown(f'<div class="card"><h3>🔍 Missing Fields</h3>{chips}</div>', unsafe_allow_html=True)
                    with fc2:
                        clauses = ef.get("risk_clauses",[])
                        if clauses:
                            cl_html = "".join([f'<div class="clause">{c}</div>' for c in clauses])
                            st.markdown(f'<div class="card"><h3>📌 Risk Clauses</h3>{cl_html}</div>', unsafe_allow_html=True)
                else:
                    st.error("Unexpected response. Check n8n workflow is active.")
        else:
            st.markdown("""
            <div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.12);
                        border-radius:16px;padding:4rem 2rem;text-align:center;">
                <div style="font-size:2.5rem;margin-bottom:1rem;">🛡️</div>
                <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#1e293b;margin-bottom:0.4rem;">
                    No document analysed yet
                </div>
                <div style="font-size:0.8rem;color:#1e293b;max-width:260px;margin:0 auto;">
                    Paste a policy, upload a file, or load a sample — then click Run AI Analysis
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Portfolio Dashboard
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Portfolio Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Multi-Policy View</div>
        <h1>Portfolio <span>Dashboard</span></h1>
        <p>All analysed policies in one view. Track risk distribution across your portfolio and identify high-priority accounts.</p>
    </div>
    """, unsafe_allow_html=True)

    portfolio = st.session_state.portfolio

    if not portfolio:
        st.markdown("""
        <div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.12);
                    border-radius:16px;padding:4rem 2rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:1rem;">📊</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#1e293b;margin-bottom:0.4rem;">
                No policies in portfolio yet
            </div>
            <div style="font-size:0.8rem;color:#1e293b;">
                Analyse policies on the Policy Analyser page — they appear here automatically
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        total = len(portfolio)
        high  = sum(1 for p in portfolio if p["risk_level"]=="HIGH")
        med   = sum(1 for p in portfolio if p["risk_level"]=="MEDIUM")
        low   = sum(1 for p in portfolio if p["risk_level"]=="LOW")
        lr_vals = [p["loss_ratio"] for p in portfolio if p["loss_ratio"]]
        avg_lr  = sum(lr_vals)/len(lr_vals) if lr_vals else 0

        m1,m2,m3,m4 = st.columns(4)
        with m1:
            st.markdown(f"""<div class="mcard"><div class="mcard-label">Total Policies</div>
                <div class="mcard-val">{total}</div>
                <div class="mcard-sub">Analysed this session</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="mcard"><div class="mcard-label">High Risk</div>
                <div class="mcard-val bad">{high}</div>
                <div class="mcard-sub">Require attention</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="mcard"><div class="mcard-label">Medium Risk</div>
                <div class="mcard-val warn">{med}</div>
                <div class="mcard-sub">Monitor closely</div></div>""", unsafe_allow_html=True)
        with m4:
            cls = "bad" if avg_lr>=100 else "warn" if avg_lr>=75 else "good"
            st.markdown(f"""<div class="mcard"><div class="mcard-label">Avg Loss Ratio</div>
                <div class="mcard-val {cls}">{avg_lr:.1f}%</div>
                <div class="mcard-sub">Portfolio average</div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
        ch1,ch2 = st.columns(2)
        with ch1:
            st.markdown('<div class="slabel">Risk Distribution</div>', unsafe_allow_html=True)
            fig_dist = go.Figure(go.Pie(
                labels=["High","Medium","Low"],values=[high,med,low],hole=0.55,
                marker=dict(colors=["#f43f5e","#fbbf24","#00d2b4"],line=dict(color="#07090f",width=2)),
                textfont=dict(color="#fff",size=12),
                hovertemplate="%{label}: %{value}<extra></extra>"
            ))
            fig_dist.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=240,margin=dict(t=10,b=10,l=10,r=10),
                legend=dict(font=dict(color="#64748b",size=11),bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar":False})
        with ch2:
            st.markdown('<div class="slabel">Risk Scores by Policy</div>', unsafe_allow_html=True)
            st.plotly_chart(make_portfolio_chart(portfolio), use_container_width=True, config={"displayModeBar":False})

        # Table
        st.markdown('<div class="slabel" style="margin-top:0.5rem;">All Policies</div>', unsafe_allow_html=True)
        rows_html = ""
        for p in sorted(portfolio, key=lambda x: x["risk_score"], reverse=True):
            lr_s = f"{p['loss_ratio']:.1f}%" if p['loss_ratio'] else "N/A"
            cu_s = f"{p['coverage_utilization']:.1f}%" if p['coverage_utilization'] else "N/A"
            cf_s = f"{p['claim_frequency']:.2f}" if p['claim_frequency'] else "N/A"
            rows_html += f"""<tr>
                <td>{p['name']}</td><td>{p['policy_type']}</td>
                <td><span class="badge {p['risk_level']}">{p['risk_level']}</span></td>
                <td>{p['risk_score']}/100</td><td>{lr_s}</td><td>{cu_s}</td><td>{cf_s}</td><td>{p['expiry']}</td>
            </tr>"""
        st.markdown(f"""
        <div class="card" style="overflow-x:auto;">
            <table class="ptable"><thead><tr>
                <th>Insured</th><th>Type</th><th>Risk</th><th>Score</th>
                <th>Loss Ratio</th><th>Coverage Util.</th><th>Claim Freq.</th><th>Expiry</th>
            </tr></thead><tbody>{rows_html}</tbody></table>
        </div>""", unsafe_allow_html=True)

        if st.button("🗑️  Clear Portfolio", use_container_width=False):
            st.session_state.portfolio = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Benchmarking
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Benchmarking":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Side-by-Side Comparison</div>
        <h1>Policy <span>Benchmarking</span></h1>
        <p>Compare two insurance policies head-to-head. Identify which carries more risk and understand why.</p>
    </div>
    """, unsafe_allow_html=True)

    col1,col2 = st.columns(2, gap="large")
    for i, col in enumerate([col1,col2], 1):
        with col:
            st.markdown(f'<div class="slabel">Policy {i}</div>', unsafe_allow_html=True)
            mode = st.radio(f"bmode_{i}",["📝 Text","📄 File"],horizontal=True,label_visibility="collapsed")
            text = ""
            if mode == "📝 Text":
                sample = st.selectbox(f"bsample_{i}",["— load a sample —"]+list(SAMPLES.keys()),label_visibility="collapsed")
                default = SAMPLES.get(sample,"") if sample != "— load a sample —" else ""
                text = st.text_area(f"btext_{i}",value=default,height=240,label_visibility="collapsed",
                    placeholder="Paste policy text here...")
            else:
                up = st.file_uploader(f"bfile_{i}",type=["pdf","docx","csv","txt"],label_visibility="collapsed")
                if up:
                    text = extract_text_from_file(up)
                    if text: st.success(f"✅ {len(text)} chars extracted")

            if st.button(f"⚡ Analyse Policy {i}", key=f"bench_{i}", use_container_width=True):
                if text and text.strip():
                    with st.spinner("Analysing..."):
                        res, err = call_webhook(text)
                    if err: st.error(err)
                    elif res and res.get("status")=="success":
                        st.session_state[f"bench_result_{i}"] = res
                        st.success("✅ Done")
                    else: st.error("Pipeline error.")
                else: st.warning("Please provide policy text.")

    results = {}
    for i in [1,2]:
        if f"bench_result_{i}" in st.session_state:
            results[i] = st.session_state[f"bench_result_{i}"]

    if len(results) == 2:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown('<div class="slabel">Head-to-Head Comparison</div>', unsafe_allow_html=True)

        r1,r2 = results[1],results[2]
        ef1,ef2 = r1["extracted_fields"],r2["extracted_fields"]
        ra1,ra2 = r1["ratios"],r2["ratios"]
        ri1,ri2 = r1["risk_assessment"],r2["risk_assessment"]

        metrics = [
            ("Loss Ratio",ra1.get("loss_ratio"),ra2.get("loss_ratio"),"%"),
            ("Coverage Util.",ra1.get("coverage_utilization"),ra2.get("coverage_utilization"),"%"),
            ("Claim Frequency",ra1.get("claim_frequency"),ra2.get("claim_frequency"),""),
            ("Risk Score",ri1.get("risk_score"),ri2.get("risk_score"),"/100"),
        ]
        mc1,mc2,mc3,mc4 = st.columns(4)
        for col,(label,v1,v2,unit) in zip([mc1,mc2,mc3,mc4],metrics):
            with col:
                if v1 is not None and v2 is not None:
                    w = "P1" if v1<v2 else "P2" if v2<v1 else "Tie"
                    c1c = "mcard-val good" if w=="P1" else "mcard-val bad" if w=="P2" else "mcard-val"
                    c2c = "mcard-val good" if w=="P2" else "mcard-val bad" if w=="P1" else "mcard-val"
                    st.markdown(f"""<div class="mcard">
                        <div class="mcard-label">{label}</div>
                        <div class="{c1c}" style="font-size:1.2rem;">P1: {v1:.1f}{unit}</div>
                        <div class="{c2c}" style="font-size:1.2rem;margin-top:0.2rem;">P2: {v2:.1f}{unit}</div>
                        <div class="mcard-sub" style="margin-top:0.4rem;">{'🏆 '+w+' wins' if w!='Tie' else '🤝 Tie'}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown('<div class="slabel" style="margin-top:1rem;">Visual Comparison</div>', unsafe_allow_html=True)
        clabels = ["Loss Ratio","Coverage Util.","Claim Freq ×10","Risk Score ÷10"]
        v1s = [ra1.get("loss_ratio") or 0, ra1.get("coverage_utilization") or 0,
               (ra1.get("claim_frequency") or 0)*10, (ri1.get("risk_score") or 0)/10]
        v2s = [ra2.get("loss_ratio") or 0, ra2.get("coverage_utilization") or 0,
               (ra2.get("claim_frequency") or 0)*10, (ri2.get("risk_score") or 0)/10]
        fig_cmp = go.Figure()
        fig_cmp.add_trace(go.Bar(name=ef1.get("insured_name","Policy 1")[:18],x=clabels,y=v1s,
            marker_color="#38bdf8",hovertemplate="%{x}: %{y:.2f}<extra></extra>"))
        fig_cmp.add_trace(go.Bar(name=ef2.get("insured_name","Policy 2")[:18],x=clabels,y=v2s,
            marker_color="#f43f5e",hovertemplate="%{x}: %{y:.2f}<extra></extra>"))
        fig_cmp.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            barmode="group",height=290,margin=dict(t=20,b=20,l=10,r=10),
            legend=dict(font=dict(color="#64748b",size=11),bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickfont=dict(color="#64748b",size=11),gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(255,255,255,0.04)",zeroline=False),
            bargap=0.2,bargroupgap=0.05)
        st.plotly_chart(fig_cmp, use_container_width=True, config={"displayModeBar":False})

        s1,s2 = ri1.get("risk_score",0), ri2.get("risk_score",0)
        if s1 < s2:   verdict,vcls = f"🏆 {ef1.get('insured_name','Policy 1')} is lower risk (Score: {s1} vs {s2})","good"
        elif s2 < s1: verdict,vcls = f"🏆 {ef2.get('insured_name','Policy 2')} is lower risk (Score: {s2} vs {s1})","good"
        else:          verdict,vcls = "🤝 Both policies carry equal risk",""
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1.5rem;">
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#64748b;margin-bottom:0.5rem;">VERDICT</div>
            <div class="mcard-val {vcls}" style="font-size:1.2rem;">{verdict}</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — How It Works
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "How It Works":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Architecture & Relevance</div>
        <h1>How <span>It Works</span></h1>
        <p>An end-to-end AI pipeline mirroring what Marsh IMEA's OPEX team builds at scale — from raw documents to structured risk intelligence.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="slabel">The Pipeline — Step by Step</div>', unsafe_allow_html=True)
    steps = [
        ("1","Document Ingestion","Raw insurance policy documents are ingested via text paste, PDF upload, CSV, or Word format. Text is extracted and normalised before processing."),
        ("2","n8n Workflow Trigger","Streamlit POSTs the extracted text to an n8n webhook. n8n acts as the orchestration layer — managing the pipeline flow between all components."),
        ("3","LLM Entity Extraction","GPT-4.1-mini processes the raw policy text. A carefully engineered prompt extracts 13 structured fields as clean JSON — policy number, coverage, premium, claims, dates, and risk clauses."),
        ("4","Ratio Computation Engine","A custom JavaScript node computes three key insurance ratios: Loss Ratio (claims/premium), Coverage Utilization (claims/coverage), and Claim Frequency (claims/policies)."),
        ("5","Risk Scoring Algorithm","A rule-based scoring engine assigns a 0–100 risk score based on: expiry proximity, loss ratio thresholds, missing field count, and risk clause density."),
        ("6","Dashboard Rendering","The pipeline returns a single JSON response. Streamlit renders extracted fields, computed ratios, interactive Plotly charts, risk flags, and clause breakdowns.")
    ]
    for num,title,desc in steps:
        st.markdown(f"""
        <div class="step">
            <div class="step-num">{num}</div>
            <div><div class="step-title">{title}</div><div class="step-desc">{desc}</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.8rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="slabel">Why This Is Relevant to Marsh IMEA OPEX</div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    cards = [
        ("📄","Document Intelligence","Insurance broking is document-heavy. Marsh processes thousands of policies manually. This pipeline automates entity extraction — exactly what OPEX builds."),
        ("🔗","NLP Pipeline","End-to-end pipeline: ingestion → extraction → structuring → analytics. Mirrors the architecture described in the JD."),
        ("🤖","LLMs & Entity Extraction","GPT-4.1-mini for structured extraction from unstructured text directly applies LLM + entity extraction skills listed as standout qualifications."),
        ("📊","Descriptive Analytics","Loss Ratio, Coverage Utilization, Claim Frequency — the exact metrics Marsh's analytics team tracks, made instantly visible.")
    ]
    for col,(icon,title,desc) in zip([c1,c2,c3,c4],cards):
        with col:
            st.markdown(f"""
            <div class="about-card">
                <div class="about-icon">{icon}</div>
                <div class="about-title">{title}</div>
                <div class="about-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.8rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="slabel">Tech Stack</div>', unsafe_allow_html=True)
    stack = [
        ("n8n","Workflow orchestration — webhook trigger, LLM call, compute node, response"),
        ("GPT-4.1-mini","LLM for entity extraction from unstructured insurance documents"),
        ("Python / Streamlit","Frontend UI and file handling (PDF, CSV, DOCX, TXT)"),
        ("Plotly","Interactive charts — risk gauge, donut, pie, bar, grouped comparison"),
        ("pdfplumber / python-docx","Document parsing for PDF and Word file inputs"),
    ]
    for tech,desc in stack:
        st.markdown(f"""
        <div class="frow">
            <div class="fkey" style="font-weight:600;color:#38bdf8;font-size:0.82rem;">{tech}</div>
            <div class="fval" style="color:#64748b;">{desc}</div>
        </div>""", unsafe_allow_html=True)
