import streamlit as st
import requests
import plotly.graph_objects as go
import pdfplumber
import docx
import io
import csv

st.set_page_config(page_title="PolicyIQ · Marsh IMEA", page_icon="🛡️",
                   layout="wide", initial_sidebar_state="expanded")

WEBHOOK_URL = "https://ridhay.app.n8n.cloud/webhook-test/insurance-extract"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Figtree:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Figtree',sans-serif;background-color:#07090f;color:#dde2ee;}
.stApp{background:#07090f;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:1.8rem 2.5rem 4rem 2.5rem;max-width:1400px;}
[data-testid="stSidebar"]{background:#0b0f1a !important;border-right:1px solid rgba(255,255,255,0.05) !important;}
[data-testid="stSidebar"] .block-container{padding:1.5rem 1.2rem;}
.hero{background:linear-gradient(135deg,#0c1424 0%,#0a1830 60%,#07101e 100%);border:1px solid rgba(56,189,248,0.12);border-radius:20px;padding:2.2rem 2.8rem;margin-bottom:2rem;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:-80px;right:-80px;width:280px;height:280px;background:radial-gradient(circle,rgba(56,189,248,0.1) 0%,transparent 70%);border-radius:50%;}
.hero-badge{display:inline-block;background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.25);color:#38bdf8;font-size:0.65rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;padding:0.28rem 0.8rem;border-radius:20px;margin-bottom:0.9rem;}
.hero h1{font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:#fff;margin:0 0 0.4rem 0;line-height:1.1;letter-spacing:-0.02em;}
.hero h1 span{color:#38bdf8;}
.hero p{color:#64748b;font-size:0.9rem;margin:0;font-weight:400;max-width:500px;}
.slabel{font-size:0.65rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#38bdf8;margin-bottom:0.5rem;}
.card{background:#0c1424;border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.6rem;margin-bottom:1.2rem;}
.card h3{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#fff;margin:0 0 1rem 0;}
.mcard{background:#0c1424;border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:1.3rem 1.5rem;position:relative;overflow:hidden;margin-bottom:1rem;}
.mcard::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#38bdf8,#00d2b4);}
.mcard-label{font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#334155;margin-bottom:0.45rem;}
.mcard-val{font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:#fff;line-height:1;margin-bottom:0.25rem;}
.mcard-val.good{color:#00d2b4;}.mcard-val.warn{color:#fbbf24;}.mcard-val.bad{color:#f43f5e;}
.mcard-sub{font-size:0.7rem;color:#334155;}
.rbanner{border-radius:14px;padding:1.1rem 1.5rem;margin-bottom:1.2rem;display:flex;align-items:center;gap:1rem;border:1px solid;}
.rbanner.LOW{background:rgba(0,210,180,0.06);border-color:rgba(0,210,180,0.2);}
.rbanner.MEDIUM{background:rgba(251,191,36,0.06);border-color:rgba(251,191,36,0.2);}
.rbanner.HIGH{background:rgba(244,63,94,0.06);border-color:rgba(244,63,94,0.2);}
.rdot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}
.rdot.LOW{background:#00d2b4;box-shadow:0 0 8px #00d2b4;}
.rdot.MEDIUM{background:#fbbf24;box-shadow:0 0 8px #fbbf24;}
.rdot.HIGH{background:#f43f5e;box-shadow:0 0 8px #f43f5e;}
.rtitle{font-family:'Syne',sans-serif;font-weight:700;font-size:0.92rem;color:#fff;}
.rsub{font-size:0.75rem;color:#64748b;margin-top:0.1rem;}
.frow{display:flex;justify-content:space-between;align-items:center;padding:0.6rem 0;border-bottom:1px solid rgba(255,255,255,0.04);}
.frow:last-child{border-bottom:none;}
.fkey{font-size:0.75rem;font-weight:500;color:#334155;flex:1;}
.fval{font-size:0.82rem;font-weight:500;color:#cbd5e1;text-align:right;flex:2;}
.fval.missing{color:#f43f5e;font-style:italic;font-size:0.75rem;}
.chip{display:inline-block;background:rgba(244,63,94,0.08);border:1px solid rgba(244,63,94,0.2);color:#f43f5e;font-size:0.7rem;font-weight:500;padding:0.22rem 0.65rem;border-radius:20px;margin:0.15rem;}
.chip.warn{background:rgba(251,191,36,0.08);border-color:rgba(251,191,36,0.2);color:#fbbf24;}
.chip.info{background:rgba(56,189,248,0.08);border-color:rgba(56,189,248,0.2);color:#38bdf8;}
.clause{background:rgba(56,189,248,0.04);border-left:3px solid #38bdf8;border-radius:0 8px 8px 0;padding:0.55rem 0.9rem;margin-bottom:0.4rem;font-size:0.8rem;color:#94a3b8;line-height:1.5;}
.stTextArea textarea{background:#060810 !important;border:1px solid rgba(56,189,248,0.18) !important;border-radius:12px !important;color:#b0bcd0 !important;font-family:'Figtree',sans-serif !important;font-size:0.85rem !important;line-height:1.7 !important;padding:1rem !important;}
.stTextArea textarea:focus{border-color:rgba(56,189,248,0.45) !important;box-shadow:0 0 0 3px rgba(56,189,248,0.07) !important;}
.stButton>button{background:linear-gradient(135deg,#0369a1,#38bdf8) !important;color:white !important;border:none !important;border-radius:10px !important;padding:0.65rem 2rem !important;font-family:'Syne',sans-serif !important;font-weight:700 !important;font-size:0.82rem !important;letter-spacing:0.06em !important;text-transform:uppercase !important;width:100% !important;transition:all 0.2s !important;}
.stButton>button:hover{transform:translateY(-2px) !important;box-shadow:0 8px 24px rgba(56,189,248,0.2) !important;}
.divider{height:1px;background:rgba(255,255,255,0.05);margin:1.5rem 0;}
.ptable{width:100%;border-collapse:collapse;}
.ptable th{font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#334155;padding:0.6rem 1rem;border-bottom:1px solid rgba(255,255,255,0.06);text-align:left;}
.ptable td{font-size:0.82rem;color:#94a3b8;padding:0.75rem 1rem;border-bottom:1px solid rgba(255,255,255,0.03);}
.badge{display:inline-block;font-size:0.65rem;font-weight:700;padding:0.2rem 0.6rem;border-radius:20px;}
.badge.LOW{background:rgba(0,210,180,0.1);color:#00d2b4;}
.badge.MEDIUM{background:rgba(251,191,36,0.1);color:#fbbf24;}
.badge.HIGH{background:rgba(244,63,94,0.1);color:#f43f5e;}
/* Why Risk Score card */
.why-card{background:#0c1424;border:1px solid rgba(56,189,248,0.12);border-radius:16px;padding:1.4rem;margin-bottom:1.2rem;}
.why-card h3{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#fff;margin:0 0 0.8rem 0;}
.why-row{display:flex;align-items:flex-start;gap:0.7rem;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.04);}
.why-row:last-child{border-bottom:none;}
.why-num{background:rgba(244,63,94,0.12);color:#f43f5e;font-family:'Syne',sans-serif;font-weight:800;font-size:0.75rem;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px;}
.why-num.warn{background:rgba(251,191,36,0.12);color:#fbbf24;}
.why-num.info{background:rgba(56,189,248,0.12);color:#38bdf8;}
.why-text{font-size:0.8rem;color:#94a3b8;line-height:1.5;}
.why-text b{color:#cbd5e1;}
/* Action card */
.action-card{background:#0c1424;border:1px solid rgba(0,210,180,0.12);border-radius:16px;padding:1.4rem;margin-bottom:1.2rem;}
.action-card h3{font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:#fff;margin:0 0 0.8rem 0;}
.action-row{display:flex;align-items:flex-start;gap:0.7rem;padding:0.5rem 0;border-bottom:1px solid rgba(255,255,255,0.04);}
.action-row:last-child{border-bottom:none;}
.action-icon{font-size:1rem;flex-shrink:0;margin-top:1px;}
.action-text{font-size:0.8rem;color:#94a3b8;line-height:1.5;}
.action-text b{color:#00d2b4;}
/* Score breakdown mini */
.score-breakdown{background:#060810;border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:0.8rem 1rem;margin-top:0.8rem;}
.score-row{display:flex;justify-content:space-between;align-items:center;padding:0.3rem 0;}
.score-key{font-size:0.72rem;color:#4a6080;}
.score-pts{font-size:0.72rem;font-weight:700;color:#f43f5e;}
.score-pts.zero{color:#00d2b4;}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "portfolio" not in st.session_state:
    st.session_state.portfolio = []
if "page" not in st.session_state:
    st.session_state.page = "Policy Analyser"
if "analyser_result" not in st.session_state:
    st.session_state.analyser_result = None

# ── Samples ───────────────────────────────────────────────────────────────────
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

CATEGORIES = ["Commercial Property","Industrial / Manufacturing","Marine Cargo",
               "Health / Medical","Life","Motor","Liability","Cyber","Agriculture"]
REGIONS    = ["North India","South India","East India","West India","Central India"]

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
    except:
        return None
    return None

def build_why_score(risk, ratios, ef):
    """Returns list of (severity, explanation, points) tuples"""
    reasons = []
    rs = risk.get("risk_score", 0)
    lr = ratios.get("loss_ratio")
    cu = ratios.get("coverage_utilization")
    cf = ratios.get("claim_frequency")
    expiry = ef.get("expiry_date")
    missing = ef.get("missing_fields", [])
    clauses = ef.get("risk_clauses", [])

    # Loss ratio
    if lr is not None:
        if lr >= 100:
            reasons.append(("bad", f"Loss Ratio = <b>{lr:.1f}%</b> — insurer is paying out more than it earns (threshold: &lt;60%)", 40))
        elif lr >= 75:
            reasons.append(("warn", f"Loss Ratio = <b>{lr:.1f}%</b> — elevated, approaching unprofitable territory (threshold: &lt;60%)", 20))
        else:
            reasons.append(("info", f"Loss Ratio = <b>{lr:.1f}%</b> — healthy, well within safe threshold of 60%", 0))

    # Expiry
    if expiry:
        try:
            from datetime import datetime
            parts = expiry.split("-")
            exp_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
            days_left = (exp_date - datetime.now()).days
            if days_left < 0:
                reasons.append(("bad", f"Policy has <b>expired</b> {abs(days_left)} days ago — coverage is no longer active", 40))
            elif days_left <= 30:
                reasons.append(("warn", f"Policy expires in <b>{days_left} days</b> — urgent renewal required", 30))
            elif days_left <= 60:
                reasons.append(("warn", f"Policy expires in <b>{days_left} days</b> — renewal planning recommended", 10))
            else:
                reasons.append(("info", f"Policy valid for <b>{days_left} more days</b> — no expiry concern", 0))
        except:
            pass

    # Coverage utilization
    if cu is not None:
        if cu >= 80:
            reasons.append(("bad", f"Coverage Utilization = <b>{cu:.1f}%</b> — claims are consuming most of the coverage limit", 0))
        elif cu >= 50:
            reasons.append(("warn", f"Coverage Utilization = <b>{cu:.1f}%</b> — moderate usage, monitor closely", 0))
        else:
            reasons.append(("info", f"Coverage Utilization = <b>{cu:.1f}%</b> — low, adequate buffer remaining", 0))

    # Claim frequency
    if cf is not None:
        if cf >= 3:
            reasons.append(("bad", f"Claim Frequency = <b>{cf:.2f}</b> — unusually high number of claims per policy", 0))
        elif cf >= 1.5:
            reasons.append(("warn", f"Claim Frequency = <b>{cf:.2f}</b> — above average, indicates frequent incidents", 0))
        else:
            reasons.append(("info", f"Claim Frequency = <b>{cf:.2f}</b> — normal, no unusual claim pattern", 0))

    # Missing fields
    if len(missing) > 3:
        reasons.append(("warn", f"<b>{len(missing)} key fields</b> missing from document — incomplete policy data reduces confidence", 15))
    elif len(missing) > 0:
        reasons.append(("info", f"<b>{len(missing)} minor field(s)</b> not found in document", 0))

    # Risk clauses
    if len(clauses) > 2:
        reasons.append(("warn", f"<b>{len(clauses)} risk clauses</b> identified — multiple exclusions and limitations present", 10))

    return reasons

def build_actions(risk, ratios, ef):
    """Returns list of (icon, action) strings based on risk profile"""
    actions = []
    rl = risk.get("risk_level", "LOW")
    lr = ratios.get("loss_ratio")
    cf = ratios.get("claim_frequency")
    cu = ratios.get("coverage_utilization")
    expiry = ef.get("expiry_date")
    missing = ef.get("missing_fields", [])

    if lr is not None and lr >= 100:
        actions.append(("📈", "Increase premium at renewal", f"Current loss ratio of {lr:.1f}% is unsustainable. Recommend premium increase of 20–30% to restore profitability."))
    elif lr is not None and lr >= 75:
        actions.append(("📊", "Review premium adequacy", f"Loss ratio of {lr:.1f}% approaching critical threshold. Consider 10–15% premium uplift at next renewal."))

    if expiry:
        try:
            from datetime import datetime
            parts = expiry.split("-")
            exp_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
            days_left = (exp_date - datetime.now()).days
            if days_left < 0:
                actions.append(("🚨", "Immediate policy renewal required", "Policy has expired. Insured is currently without coverage. Initiate emergency renewal process immediately."))
            elif days_left <= 30:
                actions.append(("⏰", "Initiate renewal within 48 hours", f"Only {days_left} days until expiry. Contact insured and insurer to begin renewal documentation."))
            elif days_left <= 60:
                actions.append(("📅", "Schedule renewal meeting", f"Policy expires in {days_left} days. Schedule renewal discussion with client within the next 2 weeks."))
        except:
            pass

    if cf is not None and cf >= 2:
        actions.append(("🔍", "Conduct risk inspection", f"High claim frequency of {cf:.2f} suggests recurring incidents. Recommend on-site risk inspection and loss prevention audit."))

    if cf is not None and cf >= 1.5:
        actions.append(("📋", "Add risk improvement clauses", "Elevated claim frequency warrants additional safety clauses — fire safety compliance, security upgrades, or preventive maintenance warranty."))

    if cu is not None and cu >= 80:
        actions.append(("💰", "Recommend coverage limit increase", f"Coverage utilization at {cu:.1f}% — insured is close to exhausting their limit. Advise increasing sum insured by at least 25%."))

    if missing and len(missing) > 2:
        actions.append(("📝", "Request missing documentation", f"Obtain the following missing fields from insured: {', '.join(missing[:4])}. Incomplete documents increase settlement risk."))

    if rl == "LOW" and not actions:
        actions.append(("✅", "Standard renewal recommended", "Policy profile is healthy. Proceed with standard renewal at existing terms. Consider loyalty discount for clean claims record."))
        actions.append(("🤝", "Upsell opportunity", "Low-risk client is a good candidate for additional covers — cyber liability, D&O, or key-person insurance."))
        actions.append(("📊", "Share risk report with client", "Generate and share this risk analytics report with the client — demonstrates Marsh's value and strengthens the relationship."))

    return actions

# ── Chart helpers ─────────────────────────────────────────────────────────────
def make_gauge(score, level):
    color = {"LOW":"#00d2b4","MEDIUM":"#fbbf24","HIGH":"#f43f5e"}.get(level,"#38bdf8")
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score, domain={"x":[0,1],"y":[0,1]},
        gauge={"axis":{"range":[0,100],"tickcolor":"#334155","tickfont":{"color":"#334155","size":10}},
               "bar":{"color":color,"thickness":0.25},"bgcolor":"#0c1424","bordercolor":"rgba(0,0,0,0)",
               "steps":[{"range":[0,30],"color":"rgba(0,210,180,0.08)"},
                        {"range":[30,60],"color":"rgba(251,191,36,0.08)"},
                        {"range":[60,100],"color":"rgba(244,63,94,0.08)"}],
               "threshold":{"line":{"color":color,"width":3},"thickness":0.8,"value":score}},
        number={"font":{"color":"#fff","size":32,"family":"Syne"},"suffix":"/100"}))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=200,margin=dict(t=20,b=10,l=20,r=20),font={"color":"#334155"})
    return fig

def make_pie(claims, premium):
    fig = go.Figure(go.Pie(
        labels=["Claims Paid","Retained Premium"],values=[claims,max(premium-claims,0)],hole=0.55,
        marker=dict(colors=["#f43f5e","#38bdf8"],line=dict(color="#07090f",width=2)),
        textfont=dict(color="#fff",size=11),hovertemplate="%{label}: ₹%{value:,.0f}<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,height=220,margin=dict(t=10,b=10,l=10,r=10),
        legend=dict(font=dict(color="#64748b",size=10),bgcolor="rgba(0,0,0,0)"))
    return fig

def make_donut(utilization):
    val = utilization if utilization else 0
    color = "#f43f5e" if val>=80 else "#fbbf24" if val>=50 else "#00d2b4"
    fig = go.Figure(go.Pie(labels=["Utilized","Available"],values=[val,max(100-val,0)],hole=0.65,
        marker=dict(colors=[color,"rgba(255,255,255,0.05)"],line=dict(color="#07090f",width=2)),
        textinfo="none",hovertemplate="%{label}: %{value:.1f}%<extra></extra>"))
    fig.add_annotation(text=f"{val:.1f}%",x=0.5,y=0.5,showarrow=False,
        font=dict(size=20,color="#fff",family="Syne"),xanchor="center")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,height=200,margin=dict(t=10,b=10,l=10,r=10))
    return fig

def make_bar(ratios):
    names=["Loss Ratio","Coverage Util.","Claim Freq. ×10"]
    vals=[ratios.get("loss_ratio") or 0,ratios.get("coverage_utilization") or 0,(ratios.get("claim_frequency") or 0)*10]
    colors=[]
    for n,v in zip(["loss_ratio","coverage_utilization","claim_frequency"],
                   [ratios.get("loss_ratio"),ratios.get("coverage_utilization"),ratios.get("claim_frequency")]):
        if v is None: colors.append("#334155")
        elif n=="loss_ratio": colors.append("#f43f5e" if v>=100 else "#fbbf24" if v>=75 else "#00d2b4")
        elif n=="coverage_utilization": colors.append("#f43f5e" if v>=80 else "#fbbf24" if v>=50 else "#00d2b4")
        else: colors.append("#f43f5e" if v>=3 else "#fbbf24" if v>=1.5 else "#00d2b4")
    fig=go.Figure(go.Bar(x=names,y=vals,marker_color=colors,
        text=[f"{v:.1f}" for v in vals],textposition="outside",
        textfont=dict(color="#94a3b8",size=11),hovertemplate="%{x}: %{y:.2f}<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=230,margin=dict(t=30,b=10,l=10,r=10),bargap=0.4,
        xaxis=dict(tickfont=dict(color="#64748b",size=11),gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(255,255,255,0.04)",zeroline=False))
    return fig

def make_portfolio_risk_chart(portfolio):
    names=[p["name"][:16] for p in portfolio]
    scores=[p["risk_score"] for p in portfolio]
    colors=["#f43f5e" if p["risk_level"]=="HIGH" else "#fbbf24" if p["risk_level"]=="MEDIUM" else "#00d2b4" for p in portfolio]
    fig=go.Figure(go.Bar(x=names,y=scores,marker_color=colors,
        text=scores,textposition="outside",textfont=dict(color="#94a3b8",size=11),
        hovertemplate="%{x}<br>Risk Score: %{y}<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=260,margin=dict(t=20,b=20,l=10,r=10),bargap=0.35,
        xaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(255,255,255,0.04)",zeroline=False,range=[0,115]))
    return fig

def make_loss_ratio_by_category(portfolio):
    from collections import defaultdict
    cat_data = defaultdict(list)
    for p in portfolio:
        if p.get("loss_ratio") and p.get("category"):
            cat_data[p["category"]].append(p["loss_ratio"])
    if not cat_data:
        return None
    cats = list(cat_data.keys())
    avgs = [sum(v)/len(v) for v in cat_data.values()]
    colors=["#f43f5e" if v>=100 else "#fbbf24" if v>=75 else "#00d2b4" for v in avgs]
    fig=go.Figure(go.Bar(x=cats,y=avgs,marker_color=colors,
        text=[f"{v:.1f}%" for v in avgs],textposition="outside",
        textfont=dict(color="#94a3b8",size=10),hovertemplate="%{x}<br>Avg Loss Ratio: %{y:.1f}%<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        height=280,margin=dict(t=30,b=60,l=10,r=10),bargap=0.35,
        xaxis=dict(tickfont=dict(color="#64748b",size=9),gridcolor="rgba(0,0,0,0)",tickangle=-25),
        yaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(255,255,255,0.04)",zeroline=False))
    return fig

def make_claims_by_region(portfolio):
    from collections import defaultdict
    region_data = defaultdict(float)
    for p in portfolio:
        if p.get("claims") and p.get("region"):
            region_data[p["region"]] += p["claims"]
    if not region_data:
        return None
    labels=list(region_data.keys())
    values=[region_data[l] for l in labels]
    colors=["#38bdf8","#00d2b4","#fbbf24","#f43f5e","#a78bfa"]
    fig=go.Figure(go.Pie(labels=labels,values=values,hole=0.5,
        marker=dict(colors=colors[:len(labels)],line=dict(color="#07090f",width=2)),
        textfont=dict(color="#fff",size=11),hovertemplate="%{label}<br>Claims: ₹%{value:,.0f}<extra></extra>"))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,height=280,margin=dict(t=10,b=10,l=10,r=10),
        legend=dict(font=dict(color="#64748b",size=10),bgcolor="rgba(0,0,0,0)"))
    return fig

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:#fff;">
            Policy<span style="color:#38bdf8;">IQ</span></div>
        <div style="font-size:0.68rem;color:#334155;margin-top:0.2rem;letter-spacing:0.1em;text-transform:uppercase;">
            Marsh IMEA · OPEX Analytics</div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.05);margin-bottom:1.2rem;"></div>
    """, unsafe_allow_html=True)

    pages = {"Policy Analyser":"🔍","Portfolio Dashboard":"📊","Benchmarking":"⚖️"}
    for pg,icon in pages.items():
        if st.button(f"{icon}  {pg}", key=f"nav_{pg}", use_container_width=True):
            st.session_state.page = pg
            st.rerun()

    st.markdown("""
    <div style="height:1px;background:rgba(255,255,255,0.05);margin:1.5rem 0 1rem 0;"></div>
    <div style="font-size:0.68rem;color:#1e293b;line-height:1.7;">
        Powered by n8n · GPT-4.1-mini<br>
        Built for Marsh IMEA OPEX<br>
        <span style="color:#38bdf8;">Data Science Internship 2025</span>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Policy Analyser
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Policy Analyser":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">AI Document Intelligence</div>
        <h1>Policy<span>IQ</span> Analyser</h1>
        <p>Paste or upload an insurance policy. The AI pipeline extracts entities, computes risk ratios, and flags anomalies instantly.</p>
    </div>""", unsafe_allow_html=True)

    left, right = st.columns([1, 1.25], gap="large")

    with left:
        st.markdown('<div class="slabel">Input Method</div>', unsafe_allow_html=True)
        input_mode = st.radio("input_mode",["📝 Text","📄 PDF","📊 CSV","📃 Word Doc"],
                              horizontal=True,label_visibility="collapsed")
        policy_text = ""

        if input_mode == "📝 Text":
            sample = st.selectbox("Load sample",["— or load a sample policy —"]+list(SAMPLES.keys()),
                                  label_visibility="collapsed")
            default = SAMPLES.get(sample,"") if sample != "— or load a sample policy —" else ""
            policy_text = st.text_area("Policy text",value=default,height=260,
                placeholder="Paste raw insurance policy text here...",label_visibility="collapsed")
        else:
            ext = {"📄 PDF":["pdf"],"📊 CSV":["csv"],"📃 Word Doc":["docx"]}[input_mode]
            uploaded = st.file_uploader("Upload file",type=ext,label_visibility="collapsed")
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
        analyse = st.button("⚡  Extract & Analyse", use_container_width=True)

        # ── Why Risk Score + Actions shown in LEFT column after analysis ──
        result = st.session_state.get("analyser_result")
        if result and result.get("status") == "success":
            ef     = result.get("extracted_fields", {})
            ratios = result.get("ratios", {})
            risk   = result.get("risk_assessment", {})
            rl     = risk.get("risk_level","LOW")

            st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

            # ── Why this risk score ──
            reasons = build_why_score(risk, ratios, ef)
            rows_html = ""
            for idx,(sev,text,pts) in enumerate(reasons,1):
                num_cls = "why-num" if sev=="bad" else "why-num warn" if sev=="warn" else "why-num info"
                rows_html += f'<div class="why-row"><div class="{num_cls}">{idx}</div><div class="why-text">{text}</div></div>'

            # Score breakdown mini table
            score_items = [(r[1].split("—")[0].strip(), r[2]) for r in reasons if r[2]>0]
            score_rows = "".join([f'<div class="score-row"><div class="score-key">{k}</div><div class="score-pts">+{p} pts</div></div>'
                                   for k,p in score_items])
            if not score_items:
                score_rows = '<div class="score-row"><div class="score-key">No penalty factors</div><div class="score-pts zero">+0 pts</div></div>'

            st.markdown(f"""
            <div class="why-card">
                <h3>🧠 Why This Risk Score?</h3>
                {rows_html}
                <div class="score-breakdown">
                    <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#1e293b;margin-bottom:0.4rem;">Score Breakdown</div>
                    {score_rows}
                    <div class="score-row" style="border-top:1px solid rgba(255,255,255,0.06);margin-top:0.3rem;padding-top:0.4rem;">
                        <div class="score-key" style="font-weight:700;color:#94a3b8;">Total Risk Score</div>
                        <div class="score-pts" style="font-size:0.82rem;">{risk.get('risk_score',0)} / 100</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            # ── Action Recommendations ──
            actions = build_actions(risk, ratios, ef)
            action_rows = ""
            for icon,title,desc in actions:
                action_rows += f'<div class="action-row"><div class="action-icon">{icon}</div><div class="action-text"><b>{title}</b><br/>{desc}</div></div>'

            st.markdown(f"""
            <div class="action-card">
                <h3>💼 Action Recommendations</h3>
                {action_rows}
            </div>""", unsafe_allow_html=True)

        elif not result:
            st.markdown("""
            <div style="background:#060810;border:1px solid rgba(255,255,255,0.04);border-radius:12px;
                        padding:1.2rem;margin-top:1.2rem;">
                <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
                            color:#1e293b;margin-bottom:0.6rem;">Pipeline extracts</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.25rem;">
                    <div style="font-size:0.73rem;color:#334155;">✦ Policy & insured info</div>
                    <div style="font-size:0.73rem;color:#334155;">✦ Coverage & premium</div>
                    <div style="font-size:0.73rem;color:#334155;">✦ Claims history</div>
                    <div style="font-size:0.73rem;color:#334155;">✦ Loss ratio</div>
                    <div style="font-size:0.73rem;color:#334155;">✦ Risk score & flags</div>
                    <div style="font-size:0.73rem;color:#334155;">✦ Risk clauses</div>
                    <div style="font-size:0.73rem;color:#334155;">✦ Why this risk score</div>
                    <div style="font-size:0.73rem;color:#334155;">✦ Action recommendations</div>
                </div>
            </div>""", unsafe_allow_html=True)

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
                    st.session_state.analyser_result = result
                    ef     = result.get("extracted_fields", {})
                    ratios = result.get("ratios", {})
                    risk   = result.get("risk_assessment", {})
                    rl     = risk.get("risk_level","LOW")
                    rs     = risk.get("risk_score",0)
                    flags  = risk.get("risk_flags",[])

                    st.session_state.portfolio.append({
                        "name": ef.get("insured_name") or "Unknown",
                        "policy_type": ef.get("policy_type") or "N/A",
                        "risk_level": rl,"risk_score": rs,
                        "loss_ratio": ratios.get("loss_ratio"),
                        "coverage_utilization": ratios.get("coverage_utilization"),
                        "claim_frequency": ratios.get("claim_frequency"),
                        "premium": ef.get("premium_amount"),
                        "claims": ef.get("claims_paid"),
                        "expiry": ef.get("expiry_date") or "N/A",
                        "category": None,
                        "region": None
                    })

                    icons={"LOW":"🟢","MEDIUM":"🟡","HIGH":"🔴"}
                    descs={"LOW":"Policy looks healthy. No major anomalies detected.",
                           "MEDIUM":"Some concerns identified. Review flagged items.",
                           "HIGH":"Immediate attention required. Multiple risk indicators active."}
                    st.markdown(f"""
                    <div class="rbanner {rl}">
                        <div class="rdot {rl}"></div>
                        <div>
                            <div class="rtitle">{icons[rl]} {rl} RISK &nbsp;·&nbsp; Score: {rs}/100</div>
                            <div class="rsub">{descs[rl]}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                    lr=ratios.get("loss_ratio"); cu=ratios.get("coverage_utilization"); cf=ratios.get("claim_frequency")
                    c1,c2,c3=st.columns(3)
                    with c1: st.markdown(f"""<div class="mcard"><div class="mcard-label">Loss Ratio</div><div class="{ratio_cls('loss_ratio',lr)}">{f"{lr:.1f}%" if lr else "N/A"}</div><div class="mcard-sub">Claims ÷ Premium</div></div>""",unsafe_allow_html=True)
                    with c2: st.markdown(f"""<div class="mcard"><div class="mcard-label">Coverage Util.</div><div class="{ratio_cls('coverage_utilization',cu)}">{f"{cu:.1f}%" if cu else "N/A"}</div><div class="mcard-sub">Claims ÷ Coverage</div></div>""",unsafe_allow_html=True)
                    with c3: st.markdown(f"""<div class="mcard"><div class="mcard-label">Claim Frequency</div><div class="{ratio_cls('claim_frequency',cf)}">{f"{cf:.2f}" if cf else "N/A"}</div><div class="mcard-sub">Claims ÷ Policies</div></div>""",unsafe_allow_html=True)

                    ch1,ch2,ch3=st.columns(3)
                    with ch1:
                        st.markdown('<div class="slabel" style="margin-top:0.8rem;">Risk Score</div>',unsafe_allow_html=True)
                        st.plotly_chart(make_gauge(rs,rl),use_container_width=True,config={"displayModeBar":False})
                    with ch2:
                        st.markdown('<div class="slabel" style="margin-top:0.8rem;">Claims vs Premium</div>',unsafe_allow_html=True)
                        st.plotly_chart(make_pie(ef.get("claims_paid") or 0,ef.get("premium_amount") or 1),use_container_width=True,config={"displayModeBar":False})
                    with ch3:
                        st.markdown('<div class="slabel" style="margin-top:0.8rem;">Coverage Utilization</div>',unsafe_allow_html=True)
                        st.plotly_chart(make_donut(cu),use_container_width=True,config={"displayModeBar":False})

                    st.markdown('<div class="slabel" style="margin-top:0.2rem;">Key Ratios Breakdown</div>',unsafe_allow_html=True)
                    st.plotly_chart(make_bar(ratios),use_container_width=True,config={"displayModeBar":False})

                    display={
                        "Policy Number":ef.get("policy_number"),"Insured Name":ef.get("insured_name"),
                        "Location":ef.get("insured_location"),"Policy Type":ef.get("policy_type"),
                        "Coverage Amount":fmt_currency(ef.get("coverage_amount")),
                        "Premium Amount":fmt_currency(ef.get("premium_amount")),
                        "Claims Paid":fmt_currency(ef.get("claims_paid")),
                        "No. of Claims":ef.get("number_of_claims"),
                        "Start Date":ef.get("start_date"),"Expiry Date":ef.get("expiry_date"),
                    }
                    rows=""
                    for k,v in display.items():
                        if not v or str(v).lower() in ["none","null",""]:
                            rows+=f'<div class="frow"><div class="fkey">{k}</div><div class="fval missing">Not found</div></div>'
                        else:
                            rows+=f'<div class="frow"><div class="fkey">{k}</div><div class="fval">{v}</div></div>'
                    st.markdown(f'<div class="card"><h3>📋 Extracted Fields</h3>{rows}</div>',unsafe_allow_html=True)

                    fc1,fc2=st.columns(2)
                    with fc1:
                        if flags:
                            chips="".join([f'<span class="chip">{f}</span>' for f in flags])
                            st.markdown(f'<div class="card"><h3>⚠️ Risk Flags</h3>{chips}</div>',unsafe_allow_html=True)
                        missing=ef.get("missing_fields",[])
                        if missing:
                            chips="".join([f'<span class="chip warn">{m}</span>' for m in missing])
                            st.markdown(f'<div class="card"><h3>🔍 Missing Fields</h3>{chips}</div>',unsafe_allow_html=True)
                    with fc2:
                        clauses=ef.get("risk_clauses",[])
                        if clauses:
                            cl_html="".join([f'<div class="clause">{c}</div>' for c in clauses])
                            st.markdown(f'<div class="card"><h3>📌 Risk Clauses</h3>{cl_html}</div>',unsafe_allow_html=True)
                    st.rerun()
                else:
                    st.error("Unexpected response. Check n8n workflow is active.")
        else:
            if not st.session_state.get("analyser_result"):
                st.markdown("""
                <div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.12);
                            border-radius:16px;padding:4rem 2rem;text-align:center;">
                    <div style="font-size:2.5rem;margin-bottom:1rem;">🛡️</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#1e293b;margin-bottom:0.4rem;">
                        No document analysed yet</div>
                    <div style="font-size:0.8rem;color:#1e293b;max-width:260px;margin:0 auto;">
                        Paste a policy, upload a file, or load a sample — then click Extract & Analyse</div>
                </div>""",unsafe_allow_html=True)
            else:
                # Re-render cached result
                result = st.session_state.analyser_result
                ef     = result.get("extracted_fields", {})
                ratios = result.get("ratios", {})
                risk   = result.get("risk_assessment", {})
                rl     = risk.get("risk_level","LOW")
                rs     = risk.get("risk_score",0)
                flags  = risk.get("risk_flags",[])

                icons={"LOW":"🟢","MEDIUM":"🟡","HIGH":"🔴"}
                descs={"LOW":"Policy looks healthy.","MEDIUM":"Some concerns identified.","HIGH":"Immediate attention required."}
                st.markdown(f"""<div class="rbanner {rl}"><div class="rdot {rl}"></div>
                    <div><div class="rtitle">{icons[rl]} {rl} RISK &nbsp;·&nbsp; Score: {rs}/100</div>
                    <div class="rsub">{descs[rl]}</div></div></div>""",unsafe_allow_html=True)

                lr=ratios.get("loss_ratio"); cu=ratios.get("coverage_utilization"); cf=ratios.get("claim_frequency")
                c1,c2,c3=st.columns(3)
                with c1: st.markdown(f"""<div class="mcard"><div class="mcard-label">Loss Ratio</div><div class="{ratio_cls('loss_ratio',lr)}">{f"{lr:.1f}%" if lr else "N/A"}</div><div class="mcard-sub">Claims ÷ Premium</div></div>""",unsafe_allow_html=True)
                with c2: st.markdown(f"""<div class="mcard"><div class="mcard-label">Coverage Util.</div><div class="{ratio_cls('coverage_utilization',cu)}">{f"{cu:.1f}%" if cu else "N/A"}</div><div class="mcard-sub">Claims ÷ Coverage</div></div>""",unsafe_allow_html=True)
                with c3: st.markdown(f"""<div class="mcard"><div class="mcard-label">Claim Frequency</div><div class="{ratio_cls('claim_frequency',cf)}">{f"{cf:.2f}" if cf else "N/A"}</div><div class="mcard-sub">Claims ÷ Policies</div></div>""",unsafe_allow_html=True)

                ch1,ch2,ch3=st.columns(3)
                with ch1:
                    st.markdown('<div class="slabel" style="margin-top:0.8rem;">Risk Score</div>',unsafe_allow_html=True)
                    st.plotly_chart(make_gauge(rs,rl),use_container_width=True,config={"displayModeBar":False})
                with ch2:
                    st.markdown('<div class="slabel" style="margin-top:0.8rem;">Claims vs Premium</div>',unsafe_allow_html=True)
                    st.plotly_chart(make_pie(ef.get("claims_paid") or 0,ef.get("premium_amount") or 1),use_container_width=True,config={"displayModeBar":False})
                with ch3:
                    st.markdown('<div class="slabel" style="margin-top:0.8rem;">Coverage Utilization</div>',unsafe_allow_html=True)
                    st.plotly_chart(make_donut(cu),use_container_width=True,config={"displayModeBar":False})

                st.markdown('<div class="slabel" style="margin-top:0.2rem;">Key Ratios Breakdown</div>',unsafe_allow_html=True)
                st.plotly_chart(make_bar(ratios),use_container_width=True,config={"displayModeBar":False})

                display={
                    "Policy Number":ef.get("policy_number"),"Insured Name":ef.get("insured_name"),
                    "Location":ef.get("insured_location"),"Policy Type":ef.get("policy_type"),
                    "Coverage Amount":fmt_currency(ef.get("coverage_amount")),
                    "Premium Amount":fmt_currency(ef.get("premium_amount")),
                    "Claims Paid":fmt_currency(ef.get("claims_paid")),
                    "No. of Claims":ef.get("number_of_claims"),
                    "Start Date":ef.get("start_date"),"Expiry Date":ef.get("expiry_date"),
                }
                rows=""
                for k,v in display.items():
                    if not v or str(v).lower() in ["none","null",""]:
                        rows+=f'<div class="frow"><div class="fkey">{k}</div><div class="fval missing">Not found</div></div>'
                    else:
                        rows+=f'<div class="frow"><div class="fkey">{k}</div><div class="fval">{v}</div></div>'
                st.markdown(f'<div class="card"><h3>📋 Extracted Fields</h3>{rows}</div>',unsafe_allow_html=True)

                fc1,fc2=st.columns(2)
                with fc1:
                    if flags:
                        chips="".join([f'<span class="chip">{f}</span>' for f in flags])
                        st.markdown(f'<div class="card"><h3>⚠️ Risk Flags</h3>{chips}</div>',unsafe_allow_html=True)
                    missing=ef.get("missing_fields",[])
                    if missing:
                        chips="".join([f'<span class="chip warn">{m}</span>' for m in missing])
                        st.markdown(f'<div class="card"><h3>🔍 Missing Fields</h3>{chips}</div>',unsafe_allow_html=True)
                with fc2:
                    clauses=ef.get("risk_clauses",[])
                    if clauses:
                        cl_html="".join([f'<div class="clause">{c}</div>' for c in clauses])
                        st.markdown(f'<div class="card"><h3>📌 Risk Clauses</h3>{cl_html}</div>',unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Portfolio Dashboard
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Portfolio Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Multi-Policy View</div>
        <h1>Portfolio <span>Dashboard</span></h1>
        <p>All analysed policies in one view. Assign category and region to unlock loss ratio and claims distribution charts.</p>
    </div>""", unsafe_allow_html=True)

    portfolio = st.session_state.portfolio

    if not portfolio:
        st.markdown("""
        <div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.12);border-radius:16px;padding:4rem 2rem;text-align:center;">
            <div style="font-size:2rem;margin-bottom:1rem;">📊</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#1e293b;margin-bottom:0.4rem;">No policies in portfolio yet</div>
            <div style="font-size:0.8rem;color:#1e293b;">Analyse policies on the Policy Analyser page — they appear here automatically</div>
        </div>""", unsafe_allow_html=True)
    else:
        # ── Let user tag each policy with category + region ──
        st.markdown('<div class="slabel">Tag Policies (for charts)</div>', unsafe_allow_html=True)
        for idx, p in enumerate(portfolio):
            c1,c2,c3 = st.columns([2,2,1])
            with c1:
                cat = st.selectbox(f"Category — {p['name'][:20]}",["— select —"]+CATEGORIES,
                    index=CATEGORIES.index(p["category"])+1 if p.get("category") in CATEGORIES else 0,
                    key=f"cat_{idx}", label_visibility="collapsed")
                portfolio[idx]["category"] = cat if cat != "— select —" else None
            with c2:
                reg = st.selectbox(f"Region — {p['name'][:20]}",["— select —"]+REGIONS,
                    index=REGIONS.index(p["region"])+1 if p.get("region") in REGIONS else 0,
                    key=f"reg_{idx}", label_visibility="collapsed")
                portfolio[idx]["region"] = reg if reg != "— select —" else None
            with c3:
                st.markdown(f'<div style="padding-top:0.4rem;"><span class="badge {p[\'risk_level\']}">{p["risk_level"]}</span></div>',unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

        # Summary metrics
        total=len(portfolio)
        high=sum(1 for p in portfolio if p["risk_level"]=="HIGH")
        med=sum(1 for p in portfolio if p["risk_level"]=="MEDIUM")
        low=sum(1 for p in portfolio if p["risk_level"]=="LOW")
        lr_vals=[p["loss_ratio"] for p in portfolio if p["loss_ratio"]]
        avg_lr=sum(lr_vals)/len(lr_vals) if lr_vals else 0

        m1,m2,m3,m4=st.columns(4)
        with m1: st.markdown(f"""<div class="mcard"><div class="mcard-label">Total Policies</div><div class="mcard-val">{total}</div><div class="mcard-sub">Analysed this session</div></div>""",unsafe_allow_html=True)
        with m2: st.markdown(f"""<div class="mcard"><div class="mcard-label">High Risk</div><div class="mcard-val bad">{high}</div><div class="mcard-sub">Require attention</div></div>""",unsafe_allow_html=True)
        with m3: st.markdown(f"""<div class="mcard"><div class="mcard-label">Medium Risk</div><div class="mcard-val warn">{med}</div><div class="mcard-sub">Monitor closely</div></div>""",unsafe_allow_html=True)
        with m4:
            cls="bad" if avg_lr>=100 else "warn" if avg_lr>=75 else "good"
            st.markdown(f"""<div class="mcard"><div class="mcard-label">Avg Loss Ratio</div><div class="mcard-val {cls}">{avg_lr:.1f}%</div><div class="mcard-sub">Portfolio average</div></div>""",unsafe_allow_html=True)

        st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

        # Row 1: Risk distribution + Risk scores
        ch1,ch2=st.columns(2)
        with ch1:
            st.markdown('<div class="slabel">Risk Distribution</div>',unsafe_allow_html=True)
            fig_dist=go.Figure(go.Pie(labels=["High","Medium","Low"],values=[high,med,low],hole=0.55,
                marker=dict(colors=["#f43f5e","#fbbf24","#00d2b4"],line=dict(color="#07090f",width=2)),
                textfont=dict(color="#fff",size=12),hovertemplate="%{label}: %{value}<extra></extra>"))
            fig_dist.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                height=250,margin=dict(t=10,b=10,l=10,r=10),
                legend=dict(font=dict(color="#64748b",size=11),bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_dist,use_container_width=True,config={"displayModeBar":False})
        with ch2:
            st.markdown('<div class="slabel">Risk Scores by Policy</div>',unsafe_allow_html=True)
            st.plotly_chart(make_portfolio_risk_chart(portfolio),use_container_width=True,config={"displayModeBar":False})

        # Row 2: Loss ratio by category + Claims by region
        ch3,ch4=st.columns(2)
        with ch3:
            st.markdown('<div class="slabel">Avg Loss Ratio by Category</div>',unsafe_allow_html=True)
            fig_cat = make_loss_ratio_by_category(portfolio)
            if fig_cat:
                st.plotly_chart(fig_cat,use_container_width=True,config={"displayModeBar":False})
            else:
                st.markdown("""<div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.1);border-radius:12px;
                    padding:2rem;text-align:center;height:200px;display:flex;align-items:center;justify-content:center;">
                    <div style="font-size:0.8rem;color:#334155;">Tag policies with a category above to see this chart</div>
                </div>""",unsafe_allow_html=True)
        with ch4:
            st.markdown('<div class="slabel">Claims Paid by Region</div>',unsafe_allow_html=True)
            fig_reg = make_claims_by_region(portfolio)
            if fig_reg:
                st.plotly_chart(fig_reg,use_container_width=True,config={"displayModeBar":False})
            else:
                st.markdown("""<div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.1);border-radius:12px;
                    padding:2rem;text-align:center;height:200px;display:flex;align-items:center;justify-content:center;">
                    <div style="font-size:0.8rem;color:#334155;">Tag policies with a region above to see this chart</div>
                </div>""",unsafe_allow_html=True)

        # Table
        st.markdown('<div class="slabel" style="margin-top:0.5rem;">All Policies</div>',unsafe_allow_html=True)
        rows_html=""
        for p in sorted(portfolio,key=lambda x:x["risk_score"],reverse=True):
            lr_s=f"{p['loss_ratio']:.1f}%" if p['loss_ratio'] else "N/A"
            cu_s=f"{p['coverage_utilization']:.1f}%" if p['coverage_utilization'] else "N/A"
            cf_s=f"{p['claim_frequency']:.2f}" if p['claim_frequency'] else "N/A"
            cat_s=p.get("category") or "—"
            reg_s=p.get("region") or "—"
            rows_html+=f"""<tr><td>{p['name']}</td><td>{p['policy_type']}</td>
                <td><span class="badge {p['risk_level']}">{p['risk_level']}</span></td>
                <td>{p['risk_score']}/100</td><td>{lr_s}</td><td>{cu_s}</td>
                <td>{cf_s}</td><td>{cat_s}</td><td>{reg_s}</td><td>{p['expiry']}</td></tr>"""
        st.markdown(f"""
        <div class="card" style="overflow-x:auto;">
            <table class="ptable"><thead><tr>
                <th>Insured</th><th>Type</th><th>Risk</th><th>Score</th>
                <th>Loss Ratio</th><th>Coverage Util.</th><th>Claim Freq.</th>
                <th>Category</th><th>Region</th><th>Expiry</th>
            </tr></thead><tbody>{rows_html}</tbody></table>
        </div>""",unsafe_allow_html=True)

        if st.button("🗑️  Clear Portfolio",use_container_width=False):
            st.session_state.portfolio=[]
            st.session_state.analyser_result=None
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Benchmarking
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Benchmarking":

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">Side-by-Side Comparison</div>
        <h1>Policy <span>Benchmarking</span></h1>
        <p>Compare two insurance policies head-to-head. Analyse each independently then see the full comparison below.</p>
    </div>""", unsafe_allow_html=True)

    # ── Analyse Policy 1 ──
    st.markdown('<div class="slabel">Policy 1</div>', unsafe_allow_html=True)
    b1c1, b1c2 = st.columns([1,1], gap="large")

    with b1c1:
        mode1 = st.radio("bmode_1",["📝 Text","📄 File"],horizontal=True,label_visibility="collapsed",key="bmode1")
        text1 = ""
        if mode1 == "📝 Text":
            s1 = st.selectbox("bs1",["— load a sample —"]+list(SAMPLES.keys()),label_visibility="collapsed",key="bs1")
            d1 = SAMPLES.get(s1,"") if s1 != "— load a sample —" else ""
            text1 = st.text_area("bt1",value=d1,height=200,label_visibility="collapsed",
                placeholder="Paste Policy 1 text here...",key="bt1")
        else:
            up1 = st.file_uploader("bf1",type=["pdf","docx","csv","txt"],label_visibility="collapsed",key="bf1")
            if up1:
                text1 = extract_text_from_file(up1)
                if text1: st.success(f"✅ {len(text1)} chars")

        if st.button("⚡ Analyse Policy 1", key="bench_1", use_container_width=True):
            if text1 and text1.strip():
                with st.spinner("Analysing Policy 1..."):
                    res1, err1 = call_webhook(text1)
                if err1:
                    st.error(err1)
                elif res1 and res1.get("status") == "success":
                    st.session_state["bench_result_1"] = res1
                    st.success("✅ Policy 1 analysed")
                else:
                    st.error("Pipeline error — check n8n is active")
            else:
                st.warning("Please provide Policy 1 text")

    with b1c2:
        if "bench_result_1" in st.session_state:
            r = st.session_state["bench_result_1"]
            ef = r.get("extracted_fields",{})
            ra = r.get("ratios",{})
            ri = r.get("risk_assessment",{})
            rl = ri.get("risk_level","LOW")
            rs = ri.get("risk_score",0)
            icons={"LOW":"🟢","MEDIUM":"🟡","HIGH":"🔴"}
            st.markdown(f"""<div class="rbanner {rl}"><div class="rdot {rl}"></div>
                <div><div class="rtitle">{icons[rl]} {rl} RISK · Score: {rs}/100</div>
                <div class="rsub">{ef.get('insured_name','Policy 1')}</div></div></div>""",unsafe_allow_html=True)
            lr=ra.get("loss_ratio"); cu=ra.get("coverage_utilization"); cf=ra.get("claim_frequency")
            mc1,mc2,mc3=st.columns(3)
            with mc1: st.markdown(f"""<div class="mcard"><div class="mcard-label">Loss Ratio</div><div class="{ratio_cls('loss_ratio',lr)}">{f"{lr:.1f}%" if lr else "N/A"}</div></div>""",unsafe_allow_html=True)
            with mc2: st.markdown(f"""<div class="mcard"><div class="mcard-label">Coverage Util.</div><div class="{ratio_cls('coverage_utilization',cu)}">{f"{cu:.1f}%" if cu else "N/A"}</div></div>""",unsafe_allow_html=True)
            with mc3: st.markdown(f"""<div class="mcard"><div class="mcard-label">Claim Freq.</div><div class="{ratio_cls('claim_frequency',cf)}">{f"{cf:.2f}" if cf else "N/A"}</div></div>""",unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.1);border-radius:12px;
                padding:2.5rem;text-align:center;margin-top:0.5rem;">
                <div style="font-size:0.8rem;color:#334155;">Policy 1 results will appear here after analysis</div>
            </div>""",unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Analyse Policy 2 ──
    st.markdown('<div class="slabel">Policy 2</div>', unsafe_allow_html=True)
    b2c1, b2c2 = st.columns([1,1], gap="large")

    with b2c1:
        mode2 = st.radio("bmode_2",["📝 Text","📄 File"],horizontal=True,label_visibility="collapsed",key="bmode2")
        text2 = ""
        if mode2 == "📝 Text":
            s2 = st.selectbox("bs2",["— load a sample —"]+list(SAMPLES.keys()),label_visibility="collapsed",key="bs2")
            d2 = SAMPLES.get(s2,"") if s2 != "— load a sample —" else ""
            text2 = st.text_area("bt2",value=d2,height=200,label_visibility="collapsed",
                placeholder="Paste Policy 2 text here...",key="bt2")
        else:
            up2 = st.file_uploader("bf2",type=["pdf","docx","csv","txt"],label_visibility="collapsed",key="bf2")
            if up2:
                text2 = extract_text_from_file(up2)
                if text2: st.success(f"✅ {len(text2)} chars")

        if st.button("⚡ Analyse Policy 2", key="bench_2", use_container_width=True):
            if text2 and text2.strip():
                with st.spinner("Analysing Policy 2..."):
                    res2, err2 = call_webhook(text2)
                if err2:
                    st.error(err2)
                elif res2 and res2.get("status") == "success":
                    st.session_state["bench_result_2"] = res2
                    st.success("✅ Policy 2 analysed")
                else:
                    st.error("Pipeline error — check n8n is active")
            else:
                st.warning("Please provide Policy 2 text")

    with b2c2:
        if "bench_result_2" in st.session_state:
            r = st.session_state["bench_result_2"]
            ef = r.get("extracted_fields",{})
            ra = r.get("ratios",{})
            ri = r.get("risk_assessment",{})
            rl = ri.get("risk_level","LOW")
            rs = ri.get("risk_score",0)
            icons={"LOW":"🟢","MEDIUM":"🟡","HIGH":"🔴"}
            st.markdown(f"""<div class="rbanner {rl}"><div class="rdot {rl}"></div>
                <div><div class="rtitle">{icons[rl]} {rl} RISK · Score: {rs}/100</div>
                <div class="rsub">{ef.get('insured_name','Policy 2')}</div></div></div>""",unsafe_allow_html=True)
            lr=ra.get("loss_ratio"); cu=ra.get("coverage_utilization"); cf=ra.get("claim_frequency")
            mc1,mc2,mc3=st.columns(3)
            with mc1: st.markdown(f"""<div class="mcard"><div class="mcard-label">Loss Ratio</div><div class="{ratio_cls('loss_ratio',lr)}">{f"{lr:.1f}%" if lr else "N/A"}</div></div>""",unsafe_allow_html=True)
            with mc2: st.markdown(f"""<div class="mcard"><div class="mcard-label">Coverage Util.</div><div class="{ratio_cls('coverage_utilization',cu)}">{f"{cu:.1f}%" if cu else "N/A"}</div></div>""",unsafe_allow_html=True)
            with mc3: st.markdown(f"""<div class="mcard"><div class="mcard-label">Claim Freq.</div><div class="{ratio_cls('claim_frequency',cf)}">{f"{cf:.2f}" if cf else "N/A"}</div></div>""",unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#0c1424;border:1px dashed rgba(56,189,248,0.1);border-radius:12px;
                padding:2.5rem;text-align:center;margin-top:0.5rem;">
                <div style="font-size:0.8rem;color:#334155;">Policy 2 results will appear here after analysis</div>
            </div>""",unsafe_allow_html=True)

    # ── Head-to-head only when both are done ──
    if "bench_result_1" in st.session_state and "bench_result_2" in st.session_state:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown('<div class="slabel">Head-to-Head Comparison</div>', unsafe_allow_html=True)

        r1=st.session_state["bench_result_1"]; r2=st.session_state["bench_result_2"]
        ef1=r1["extracted_fields"]; ef2=r2["extracted_fields"]
        ra1=r1["ratios"]; ra2=r2["ratios"]
        ri1=r1["risk_assessment"]; ri2=r2["risk_assessment"]

        metrics=[
            ("Loss Ratio",ra1.get("loss_ratio"),ra2.get("loss_ratio"),"%"),
            ("Coverage Util.",ra1.get("coverage_utilization"),ra2.get("coverage_utilization"),"%"),
            ("Claim Frequency",ra1.get("claim_frequency"),ra2.get("claim_frequency"),""),
            ("Risk Score",ri1.get("risk_score"),ri2.get("risk_score"),"/100"),
        ]
        mc1,mc2,mc3,mc4=st.columns(4)
        for col,(label,v1,v2,unit) in zip([mc1,mc2,mc3,mc4],metrics):
            with col:
                if v1 is not None and v2 is not None:
                    w="P1" if v1<v2 else "P2" if v2<v1 else "Tie"
                    c1c="mcard-val good" if w=="P1" else "mcard-val bad" if w=="P2" else "mcard-val"
                    c2c="mcard-val good" if w=="P2" else "mcard-val bad" if w=="P1" else "mcard-val"
                    st.markdown(f"""<div class="mcard"><div class="mcard-label">{label}</div>
                        <div class="{c1c}" style="font-size:1.2rem;">P1: {v1:.1f}{unit}</div>
                        <div class="{c2c}" style="font-size:1.2rem;margin-top:0.2rem;">P2: {v2:.1f}{unit}</div>
                        <div class="mcard-sub" style="margin-top:0.4rem;">{'🏆 '+w+' wins' if w!='Tie' else '🤝 Tie'}</div>
                    </div>""",unsafe_allow_html=True)

        st.markdown('<div class="slabel" style="margin-top:1rem;">Visual Comparison</div>',unsafe_allow_html=True)
        clabels=["Loss Ratio","Coverage Util.","Claim Freq ×10","Risk Score ÷10"]
        v1s=[ra1.get("loss_ratio") or 0,ra1.get("coverage_utilization") or 0,
             (ra1.get("claim_frequency") or 0)*10,(ri1.get("risk_score") or 0)/10]
        v2s=[ra2.get("loss_ratio") or 0,ra2.get("coverage_utilization") or 0,
             (ra2.get("claim_frequency") or 0)*10,(ri2.get("risk_score") or 0)/10]
        fig_cmp=go.Figure()
        n1=ef1.get("insured_name","Policy 1")[:18]; n2=ef2.get("insured_name","Policy 2")[:18]
        fig_cmp.add_trace(go.Bar(name=n1,x=clabels,y=v1s,marker_color="#38bdf8",
            hovertemplate="%{x}: %{y:.2f}<extra></extra>"))
        fig_cmp.add_trace(go.Bar(name=n2,x=clabels,y=v2s,marker_color="#f43f5e",
            hovertemplate="%{x}: %{y:.2f}<extra></extra>"))
        fig_cmp.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            barmode="group",height=290,margin=dict(t=20,b=20,l=10,r=10),
            legend=dict(font=dict(color="#64748b",size=11),bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickfont=dict(color="#64748b",size=11),gridcolor="rgba(0,0,0,0)"),
            yaxis=dict(tickfont=dict(color="#64748b",size=10),gridcolor="rgba(255,255,255,0.04)",zeroline=False),
            bargap=0.2,bargroupgap=0.05)
        st.plotly_chart(fig_cmp,use_container_width=True,config={"displayModeBar":False})

        s1=ri1.get("risk_score",0); s2=ri2.get("risk_score",0)
        if s1<s2:   verdict,vcls=f"🏆 {ef1.get('insured_name','Policy 1')} is lower risk (Score: {s1} vs {s2})","good"
        elif s2<s1: verdict,vcls=f"🏆 {ef2.get('insured_name','Policy 2')} is lower risk (Score: {s2} vs {s1})","good"
        else:        verdict,vcls="🤝 Both policies carry equal risk",""
        st.markdown(f"""<div class="card" style="text-align:center;padding:1.5rem;">
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#64748b;margin-bottom:0.5rem;">VERDICT</div>
            <div class="mcard-val {vcls}" style="font-size:1.2rem;">{verdict}</div>
        </div>""",unsafe_allow_html=True)

        if st.button("🔄 Reset Benchmarking", use_container_width=False):
            for k in ["bench_result_1","bench_result_2"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
