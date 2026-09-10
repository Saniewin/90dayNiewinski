import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# ==============================================================================
# PAGE CONFIGURATION & THEME SETUP
# ==============================================================================
st.set_page_config(
    page_title="CNS Healthcare Appraisal Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate-Executive Styling
st.markdown("""
<style>
    /* Main Canvas Background */
    .stApp {
        background-color: #0F172A !important; 
        color: #F8FAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    
    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        border: 1px solid #3B82F6;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        margin-bottom: 4px !important;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        color: #93C5FD !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    
    /* Audit Card Styling */
    .audit-card {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        transition: border-color 0.2s ease;
    }
    
    .audit-card:hover {
        border-color: #3B82F6 !important;
    }
    
    /* Badges */
    .badge-policy, .badge-target {
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        display: inline-block;
        margin-bottom: 8px;
        font-family: monospace;
    }
    .badge-policy {
        background-color: #1E3A8A;
        color: #DBEAFE;
        border: 1px solid #2563EB;
    }
    .badge-target {
        background-color: #065F46;
        color: #D1FAE5;
        margin-left: 6px;
        border: 1px solid #059669;
    }

    /* Alerts */
    .remedy-box {
        background-color: rgba(217, 119, 6, 0.15) !important;
        border-left: 4px solid #F59E0B !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin-top: 10px !important;
        font-size: 12px !important;
        color: #FDE68A !important;
    }
    .cascade-alert {
        background-color: rgba(220, 38, 38, 0.15) !important;
        border-left: 5px solid #EF4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        margin-bottom: 16px !important;
        font-size: 12px !important;
        color: #FCA5A5 !important;
    }
    
    /* Streamlit UI Overrides */
    div.stPopover > button {
        background-color: #0F172A !important;
        border: 1px solid #3B82F6 !important;
        color: #60A5FA !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
    }
    div.stPopover > button:hover {
        background-color: #1E3A8A !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CACHED DATA & REGULATORY FRAMEWORKS
# ==============================================================================
@st.cache_data
def load_claims_telemetry():
    denial_data = pd.DataFrame({
        "Denial Reason / Vulnerability": [
            "Same-Day Provider/Tech NCCI Error (96136/96138)",
            "Telehealth POS/Modifier Mismatch (POS 02/10, Mod 95)",
            "Exceeded Prior Authorization Limit (Meridian 8-Hr Cap)",
            "Missing CPT 96130 Interactive Feedback Note",
            "Unattached Diagnostic Justification / BTP Clearance"
        ],
        "Claim Count": [384, 298, 245, 182, 111],
        "Financial Exposure ($)": [76800, 53640, 49000, 36400, 22200]
    })
    tat_data = pd.DataFrame({
        "Clinic Site": ["Detroit", "Pontiac", "Southfield", "Novi", "Eastpointe"],
        "Referral-to-Auth (Days)": [3.2, 2.8, 2.5, 2.1, 3.0],
        "Auth-to-Testing (Days)": [8.5, 9.1, 7.2, 6.8, 8.9],
        "Testing-to-Signed Report (Days)": [14.2, 12.8, 11.5, 10.2, 13.5]
    })
    return denial_data, tat_data

@st.cache_resource
def load_regulatory_framework():
    return {
        "Phase 1": {
            "title": "Phase 1: Discovery, Baseline & Pipeline Mapping",
            "objective": "Verify 100% LARA LLP supervision logs, map referral-to-authorization pipelines, and audit CPT 96130 feedback integrity.",
            "tasks": {
                "p1_t1": {"label": "Verify LLP Supervision Logs & Form LARA/BPL", "policy": "MCL 333.18223", "target": "100% compliant logs", "desc": "Audit 100% of supervisory files for LLPs/TLLPs.", "rationale": "Direct violation of licensure law.", "remediation": "Halt unsupervised LLP billing. Enforce EHR co-signature locks."},
                "p1_t2": {"label": "Audit CPT 96130 Documentation Integrity", "policy": "CPT 96130 Guidelines", "target": "100% presence of feedback note", "desc": "Extract and audit 30 completed evaluation charts.", "rationale": "Missing interactive feedback constitutes billing non-compliance.", "remediation": "Deploy mandatory NextGen EHR templates."},
                "p1_t3": {"label": "Map Referral-to-Authorization Pipeline", "policy": "SAMHSA CCBHC Criteria", "target": "Map 100% of pipeline", "desc": "Shadow intake staff tracking testing referrals.", "rationale": "Violating CCBHC timely access benchmarks.", "remediation": "Resolve bottlenecks in PIHP portals."},
                "p1_t4": {"label": "Audit Access-to-Care Timeliness Benchmarks", "policy": "MDHHS CCBHC Mandate", "target": "Routine 14d, Comp Eval 60d", "desc": "Recalibrate clinic scheduling queues.", "rationale": "Threatens prospective payment system certification.", "remediation": "Deploy Stepped-Care triage screenings."}
            }
        },
        "Phase 2": {
            "title": "Phase 2: Operational Analytics, Financial Audit & Gaps",
            "objective": "Analyze denial codes, calculate Turnaround Times, and conduct Overhead vs. PPS ROI analysis.",
            "tasks": {
                "p2_t1": {"label": "Audit 12-Month CPT Remittance Denials", "policy": "RCM 835 Guidelines", "target": "Identify top 3 denial codes", "desc": "Extract claims dataset to isolate edit rejections.", "rationale": "Causes massive revenue leakage.", "remediation": "Correct billing errors at point of scheduling."},
                "p2_t2": {"label": "Execute NCCI Modifier XE/59 Audit", "policy": "CMS NCCI", "target": "100% accuracy", "desc": "Audit same-day psychologist and tech administration.", "rationale": "Triggers automated NCCI denials.", "remediation": "Hardcode NCCI validation rules in EHR."},
                "p2_t3": {"label": "Telehealth Modifier & POS Compliance", "policy": "MDHHS Telehealth Guidelines", "target": "100% compliance", "desc": "Verify virtual feedback claims append Modifier 95.", "rationale": "Improper POS codes cause immediate claim rejections.", "remediation": "Configure EHR telehealth modules to auto-append modifiers."},
                "p2_t4": {"label": "Evaluate PPS Encounter Splitting & Multi-Day Testing", "policy": "CMS & MDHHS FWA", "target": "100% documented justification", "desc": "Audit multi-day testing sessions.", "rationale": "Splitting testing to generate daily PPS claims violates CMS rules.", "remediation": "Enforce mandatory EHR justification prior to scheduling multi-day tests."},
                "p2_t5": {"label": "Calculate Clinician Report TAT", "policy": "CARF Timeliness Criteria", "target": "Median TAT < 14 days", "desc": "Extract EHR timestamps for turnaround.", "rationale": "Extended report TATs delay psychiatric prescriptions.", "remediation": "Deliver targeted coaching to outlying write-times."},
                "p2_t6": {"label": "Conduct Testing Kit Overhead vs. PPS-1 ROI Analysis", "policy": "CCBHC PPS Guidelines", "target": "Establish cost-per-assessment ratio", "desc": "Cross-reference vendor invoices against PPS revenues.", "rationale": "Unmonitored licensing expenses create unrecognized deficits.", "remediation": "Transition completely to digital scoring platforms."}
            }
        },
        "Phase 3": {
            "title": "Phase 3: Strategic Synthesis, CQI & Executive Roadmap",
            "objective": "Implement Protocols, launch dashboard, embed results, and deliver roadmap.",
            "tasks": {
                "p3_t1": {"label": "Implement Stepped-Care Protocol", "policy": "SAMHSA CCBHC Service #2", "target": "100% referrals triaged", "desc": "Deploy clinical algorithm filtering low-acuity cases.", "rationale": "Wastes psychologist FTE capacity.", "remediation": "Develop Stepped-Care Assessment clinical algorithm."},
                "p3_t2": {"label": "Configure Live EHR KPI Dashboard", "policy": "CCBHC CQI Plan", "target": "Live tracking of 5 KPIs", "desc": "Build an EHR-integrated Business Intelligence dashboard.", "rationale": "Lack of real-time visual tracking.", "remediation": "Coordinate with IT to configure a live BI dashboard."},
                "p3_t3": {"label": "Embed Results into Person-Centered Plans", "policy": "MDHHS & SAMHSA", "target": "100% integration", "desc": "Establish automated EHR workflows.", "rationale": "Testing operates as an isolated, high-cost exercise.", "remediation": "Implement automated notifications."},
                "p3_t4": {"label": "Deliver Executive Appraisal & 12-Month Roadmap", "policy": "CCBHC Program Requirement #6", "target": "Formal Board submission", "desc": "Synthesize all audit findings into the formal report.", "rationale": "Failure to plan for long-term investments results in operational stagnation.", "remediation": "Present the 12-month roadmap to executive leadership."}
            }
        }
    }

# ==============================================================================
# STATE MANAGEMENT
# ==============================================================================
reg_db = load_regulatory_framework()
denial_df, tat_df = load_claims_telemetry()

# Initialize session state for widgets binding to ensure snappy real-time reactivity
for phase_key, phase_val in reg_db.items():
    for task_key in phase_val["tasks"].keys():
        if f"status_{task_key}" not in st.session_state:
            st.session_state[f"status_{task_key}"] = "Pending"
        if f"note_{task_key}" not in st.session_state:
            st.session_state[f"note_{task_key}"] = ""

# ==============================================================================
# SIDEBAR: 90-DAY PROGRESS TRACKER WIDGET
# ==============================================================================
with st.sidebar:
    st.markdown("### ⏱️ 90-Day Execution Tracker")
    
    # Dashboard Slider Widget to act as timeframe
    current_day = st.slider("Timeline Progression (Days)", min_value=1, max_value=90, value=15, help="Simulate or track physical progress through the 90 day plan.")
    
    if current_day <= 30:
        st.info("**Current Stage:** Phase 1 (Discovery)\n\nDays 1-30")
    elif current_day <= 60:
        st.warning("**Current Stage:** Phase 2 (Analytics)\n\nDays 31-60")
    else:
        st.success("**Current Stage:** Phase 3 (Synthesis)\n\nDays 61-90")
        
    st.progress(current_day / 90.0)
    st.markdown("---")
    
    # Calculate global widget metrics directly from real-time session_state keys
    total_tasks, compliant, risks = 0, 0, 0
    
    for phase_key, phase_val in reg_db.items():
        for task_key in phase_val["tasks"].keys():
            total_tasks += 1
            status = st.session_state[f"status_{task_key}"]
            if status == "Compliant": compliant += 1
            elif status == "Outside of Compliance": risks += 1
                
    pending = total_tasks - compliant - risks
    
    st.markdown("### Compliance Overview")
    st.metric("Total Plan Objectives", total_tasks)
    st.metric("✅ Verified Compliant", compliant)
    st.metric("🚨 Active Risk Gaps", risks)
    st.metric("⏳ Pending Audits", pending)

# ==============================================================================
# MAIN APP HEADER & TABS
# ==============================================================================
st.markdown("""
<div class="header-banner">
    <div class="header-title">CNS Healthcare Psychological Services Appraisal Widget</div>
    <div class="header-subtitle">Executive Command Terminal • Dynamic 90-Day Execution & Compliance Engine</div>
</div>
""", unsafe_allow_html=True)

nav_tabs = st.tabs([
    "📍 Phase 1", "📊 Phase 2", "🚀 Phase 3", 
    "📈 Telemetry", "📄 Final Appraisal Builder"
])

status_opts = ["Pending", "Compliant", "Outside of Compliance"]

# DRY Function to seamlessly render execution phases 
def render_phase_tab(phase_key, cascade_checks=[]):
    phase_data = reg_db[phase_key]
    st.markdown(f"### **{phase_data['title']}**")
    st.info(f"**Objective**: {phase_data['objective']}")
    
    # Intelligent baseline dependency check that warns users of structural failures before continuing
    if cascade_checks:
        gaps = [tk for tk in cascade_checks if st.session_state[f"status_{tk}"] == "Outside of Compliance"]
        if gaps:
            gap_labels = [reg_db[p]["tasks"][tk]["label"] for p in reg_db for tk in reg_db[p]["tasks"] if tk in gaps]
            st.markdown(f'<div class="cascade-alert">🚨 <strong>CARRYOVER RISK DETECTED:</strong> Unresolved baseline issues threaten this phase: {", ".join(gap_labels)}</div>', unsafe_allow_html=True)

    for t_key, t_val in phase_data["tasks"].items():
        st.markdown('<div class="audit-card">', unsafe_allow_html=True)
        col_a, col_b = st.columns([3, 2])
        
        with col_a:
            st.markdown(f'<span class="badge-policy">{t_val["policy"]}</span> <span class="badge-target">KPI: {t_val["target"]}</span>', unsafe_allow_html=True)
            st.markdown(f"#### **{t_val['label']}**")
            st.write(t_val["desc"])
            
        with col_b:
            with st.popover(" TASK DIAGNOSTICS"):
                st.markdown(f"**Policy Source**: {t_val['policy']}")
                st.markdown(f"**Appraisal Rationale**: {t_val['rationale']}")

            # Widget keys bind DIRECTLY to st.session_state bypassing extra callback logic
            st.selectbox("Diagnostic Status", status_opts, key=f"status_{t_key}")
            st.text_input("Audit Notes / Findings", key=f"note_{t_key}", placeholder="Enter specific audit remarks here...")
            
        if st.session_state[f"status_{t_key}"] == "Outside of Compliance":
            st.markdown(f'<div class="remedy-box">⚠️ <strong>REMEDIATION DIRECTIVE:</strong> {t_val["remediation"]}</div>', unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

with nav_tabs[0]: render_phase_tab("Phase 1")
with nav_tabs[1]: render_phase_tab("Phase 2", cascade_checks=list(reg_db["Phase 1"]["tasks"].keys()))
with nav_tabs[2]: render_phase_tab("Phase 3", cascade_checks=list(reg_db["Phase 2"]["tasks"].keys()))

# ==============================================================================
# TAB 4: SUPERVISOR OVERSIGHT & TELEMETRY
# ==============================================================================
with nav_tabs[3]:
    st.markdown("### **Supervisor Oversight & Claims Telemetry**")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### **12-Month CPT Denial Drivers**")
        fig_donut = px.pie(denial_df, values="Claim Count", names="Denial Reason / Vulnerability", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
        fig_donut.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC", margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)
    with c2:
        st.markdown("##### **Report Turnaround Time (TAT)**")
        fig_bar = px.bar(tat_df, x="Clinic Site", y=["Referral-to-Auth (Days)", "Auth-to-Testing (Days)", "Testing-to-Signed Report (Days)"], barmode="stack", color_discrete_sequence=["#3B82F6", "#F59E0B", "#10B981"])
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC", margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

# ==============================================================================
# TAB 5: CONSTRUCT FINAL APPRAISAL (DYNAMIC REPORT COMPILER)
# ==============================================================================
def generate_appraisal_report(day):
    # Generates a pristine Markdown memo aggregating all inputs from the 3 Phases
    lines = [
        "# CNS Healthcare Psychological Services",
        "## 90-Day Executive Appraisal Report",
        f"**Generated on:** {datetime.now().strftime('%B %d, %Y')}",
        f"**Timeline Progression:** Day {day} of 90",
        "---",
        "### 1. Executive Summary",
        "This dynamic appraisal memorandum synthesizes operational baselines, compliance metrics, and strategic remediations across clinical sites, strictly aligned with LARA statutes and CCBHC program constraints.\n"
    ]
    
    comps, gaps, pends = [], [], []
    for ph_k, ph_v in reg_db.items():
        for tk, tv in ph_v["tasks"].items():
            status = st.session_state[f"status_{tk}"]
            notes = st.session_state[f"note_{tk}"]
            item = {"phase": ph_v["title"], "task": tv, "notes": notes}
            if status == "Compliant": comps.append(item)
            elif status == "Outside of Compliance": gaps.append(item)
            else: pends.append(item)
    
    total = len(comps) + len(gaps) + len(pends)
    comp_rate = (len(comps) / total) * 100 if total > 0 else 0
    lines.extend([
        f"- **Overall Compliance Rate:** {comp_rate:.1f}%",
        f"- **Verified Compliant Workflows:** {len(comps)}",
        f"- **Identified Operational Risks:** {len(gaps)}",
        f"- **Pending Evaluations:** {len(pends)}",
        "---",
        "### 2. Verified Compliant Operations"
    ])
    
    if not comps:
        lines.append("> *No fully compliant workflows logged yet.*")
    else:
        for c in comps:
            lines.append(f"#### ✅ {c['task']['label']}")
            lines.append(f"- **Policy:** {c['task']['policy']} | **Target:** {c['task']['target']}")
            lines.append(f"- **Auditor Notes:** {c['notes'] if c['notes'] else 'Verified without issue.'}\n")
            
    lines.extend([
        "---",
        "### 3. Active Risk & Mitigation Matrix"
    ])
    
    if not gaps:
        lines.append("> *No active non-compliant gaps flagged.*")
    else:
        for g in gaps:
            lines.append(f"#### ⚠️ [GAP] {g['task']['label']}")
            lines.append(f"- **Systemic Rationale:** {g['task']['rationale']}")
            lines.append(f"- **Auditor Notes:** {g['notes'] if g['notes'] else 'Pending auditor remarks.'}")
            lines.append(f"- **REMEDIATION DIRECTIVE:** {g['task']['remediation']}\n")
            
    lines.extend([
        "---",
        "### 4. Pending Reviews"
    ])
    
    if not pends:
         lines.append("> *All 90-Day Plan operational areas have been formally appraised.*")
    else:
        for p in pends:
            lines.append(f"- [ ] {p['task']['label']}")

    return "\n".join(lines)

with nav_tabs[4]:
    st.markdown("### **Final Executive Appraisal Constructor**")
    st.write("Review the compiled statuses, notes, and remediations. This report constructs itself in real-time as you progress through the 90-day plan.")
    
    report_md = generate_appraisal_report(current_day)
    
    col_view, col_action = st.columns([2, 1])
    
    with col_view:
        # Render Markdown compilation cleanly in a stylized CSS container
        st.markdown(
            f"""<div style="background-color: #1E293B; padding: 25px; border-radius: 12px; border: 1px solid #334155; max-height: 550px; overflow-y: auto; font-family: monospace; font-size: 14px;">
            {report_md.replace('---', '<hr style="border-color: #334155; margin: 20px 0;">').replace('\n', '<br>')}
            </div>""", 
            unsafe_allow_html=True
        )
        
    with col_action:
        st.info("The document compiles all findings, qualitative notes, and required CCBHC remediations into a single strategic export.")
        st.download_button(
            label="📥 Download Executive Appraisal (.md)",
            data=report_md,
            file_name=f"CNS_Appraisal_Report_Day_{current_day}.md",
            mime="text/markdown",
            use_container_width=True,
            type="primary"
        )
