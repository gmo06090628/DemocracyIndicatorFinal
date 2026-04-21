import streamlit as st
import pandas as pd
import plotly.express as px 
import os

# my_project_v10.py
# Global Democracy Monitor V10
# Indicators: Free & Fair Elections, Civil Liberties, Polarization, Political Corruption
# Features: Acceleration detection, country comparison, event timeline, heatmap, leaderboard

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

st.set_page_config(
    page_title="Democracy Monitor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# GLOBAL STYLES
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: #0d1117;
    color: #c9d1d9;
}

/* Main header */
.main-header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border-bottom: 1px solid #f0a500;
    padding: 2rem 0 1.5rem 0;
    margin-bottom: 2rem;
}
.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #f0f6fc;
    letter-spacing: -0.02em;
    margin: 0;
}
.main-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #f0a500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* Section headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f0f6fc;
    border-left: 3px solid #f0a500;
    padding-left: 0.75rem;
    margin: 1.5rem 0 0.75rem 0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.5rem;
}
.metric-label {
    font-size: 0.65rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.2rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #f0f6fc;
}
.metric-delta-neg { color: #f85149; font-size: 0.8rem; }
.metric-delta-pos { color: #3fb950; font-size: 0.8rem; }
.metric-delta-neu { color: #8b949e; font-size: 0.8rem; }

/* Alert tiers */
.alert-critical {
    background: rgba(248, 81, 73, 0.1);
    border-left: 3px solid #f85149;
    padding: 0.6rem 0.9rem;
    border-radius: 0 4px 4px 0;
    margin: 0.3rem 0;
    font-size: 0.8rem;
}
.alert-watch {
    background: rgba(240, 165, 0, 0.1);
    border-left: 3px solid #f0a500;
    padding: 0.6rem 0.9rem;
    border-radius: 0 4px 4px 0;
    margin: 0.3rem 0;
    font-size: 0.8rem;
}
.alert-monitor {
    background: rgba(210, 153, 34, 0.08);
    border-left: 3px solid #d29922;
    padding: 0.6rem 0.9rem;
    border-radius: 0 4px 4px 0;
    margin: 0.3rem 0;
    font-size: 0.8rem;
}
.alert-stable {
    background: rgba(63, 185, 80, 0.08);
    border-left: 3px solid #3fb950;
    padding: 0.6rem 0.9rem;
    border-radius: 0 4px 4px 0;
    margin: 0.3rem 0;
    font-size: 0.8rem;
}

/* Narrative box */
.narrative-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-top: 2px solid #f0a500;
    padding: 1rem 1.25rem;
    border-radius: 0 0 6px 6px;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #c9d1d9;
    margin-top: 0;
}

/* Watchlist row */
.watchlist-country {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    color: #f0f6fc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d1117;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label {
    color: #8b949e;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* Plotly chart backgrounds */
.js-plotly-plot .plotly .bg { fill: #161b22 !important; }

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8b949e;
    padding: 0.6rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    color: #f0a500 !important;
    border-bottom: 2px solid #f0a500 !important;
}

/* Dataframe */
.dataframe { font-size: 0.75rem !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# PLOTLY THEME
# ---------------------------
PLOTLY_THEME = dict(
    paper_bgcolor='#161b22',
    plot_bgcolor='#161b22',
    font=dict(family='JetBrains Mono, monospace', color='#c9d1d9', size=11),
    colorway=['#f0a500', '#58a6ff', '#3fb950', '#f85149', '#d2a8ff', '#79c0ff'],
)
# Reusable axis style dicts — merge these inline instead of putting in PLOTLY_THEME
_AX = dict(gridcolor='#21262d', linecolor='#30363d', tickcolor='#30363d')
_XAX = dict(**_AX)
_YAX = dict(**_AX)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
<div class="main-header">
    <div class="main-title">🌍 Democracy Monitor</div>
    <div class="main-subtitle">Democratic Backsliding Dashboard · V-Dem Dataset</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_vdem():
    # Replace with your direct download URL
    url = "https://www.dropbox.com/scl/fi/6v3q7vq9y8wumsnvff2dh/V-Dem-CY-Full-Others-v16.csv?rlkey=vdvkuy2tdwd5nmfx7ocnei8s3&st=rt2p553n&dl=1"
    cols_to_load = ['country_name', 'year', 'v2xel_frefair', 'v2x_civlib', 'v2x_corr', 'v2cacamps', 'v2smpolsoc']
    return pd.read_csv(url, usecols=cols_to_load)

with st.spinner("Loading V-Dem dataset..."):
    vdem = load_vdem()

if vdem is None:
    st.error("❌ V-Dem dataset not found. Ensure `V-Dem-CY-Full+Others-v16.csv` is in the working directory.")
    st.stop()

# ---------------------------
# COLUMN MAPPING + INDICATOR CONSTRUCTION
# ---------------------------
# Core renames
rename_map = {
    'country_name': 'Country',
    'year': 'Year',
    'v2xel_frefair': 'Free and Fair Elections',
    'v2x_civlib': 'Civil Liberties',
    'v2x_corr': '_corruption_raw',      # Political Corruption composite (higher = more corrupt)
    'v2cacamps': '_pol_camps',           # Political polarization (camps)
    'v2smpolsoc': '_soc_polar',           # Society polarization (ethnic/affective)
}
existing = {k: v for k, v in rename_map.items() if k in vdem.columns}
vdem = vdem.rename(columns=existing)

# --- POLARIZATION: combine v2cacamps + v2smpetap ---
# Both are coded higher = more polarized; we average them, then invert so higher = healthier
vdem['_pol_camps'] = pd.to_numeric(vdem.get('_pol_camps', pd.NA), errors='coerce')
vdem['_soc_polar'] = pd.to_numeric(vdem.get('_soc_polar', pd.NA), errors='coerce')

if '_pol_camps' in vdem.columns and '_soc_polar' in vdem.columns:
    # Normalize each to 0-1 before combining
    for c in ['_pol_camps', '_soc_polar']:
        mn, mx = vdem[c].min(), vdem[c].max()
        if mx > mn:
            vdem[c] = (vdem[c] - mn) / (mx - mn)
    vdem['Polarization'] = vdem[['_pol_camps', '_soc_polar']].mean(axis=1)
elif '_pol_camps' in vdem.columns:
    vdem['Polarization'] = pd.to_numeric(vdem['_pol_camps'], errors='coerce')
    mn, mx = vdem['Polarization'].min(), vdem['Polarization'].max()
    if mx > mn:
        vdem['Polarization'] = (vdem['Polarization'] - mn) / (mx - mn)
else:
    vdem['Polarization'] = np.nan

# Invert: high polarization = low health
vdem['Polarization'] = (1 - vdem['Polarization']).clip(0, 1)

# --- CORRUPTION: invert so higher = less corrupt (healthier) ---
if '_corruption_raw' in vdem.columns:
    vdem['_corruption_raw'] = pd.to_numeric(vdem['_corruption_raw'], errors='coerce').clip(0, 1)
    vdem['Political Corruption'] = (1 - vdem['_corruption_raw']).clip(0, 1)
else:
    vdem['Political Corruption'] = np.nan

# --- Clamp Free & Fair Elections and Civil Liberties ---
for col in ['Free and Fair Elections', 'Civil Liberties']:
    if col in vdem.columns:
        vdem[col] = pd.to_numeric(vdem[col], errors='coerce').clip(0, 1)

# ---------------------------
# INDICATORS (only those present)
# ---------------------------
ALL_INDICATORS = ['Free and Fair Elections', 'Civil Liberties', 'Polarization', 'Political Corruption']
INDICATORS = [i for i in ALL_INDICATORS if i in vdem.columns and vdem[i].notna().sum() > 0]

INDICATOR_DESCRIPTIONS = {
    'Free and Fair Elections': 'Whether elections are free from fraud, irregularities, and intimidation (v2xel_frefair)',
    'Civil Liberties': 'Freedom of expression, association, movement, and personal integrity (v2x_civlib)',
    'Polarization': 'Combined political + societal polarization, inverted — higher = less polarized (v2cacamps + v2smpetap)',
    'Political Corruption': 'Executive, legislative & judicial corruption composite, inverted — higher = less corrupt (v2x_corr)',
}

# ---------------------------
# TIME SERIES CALCULATIONS
# ---------------------------
vdem_sorted = vdem.sort_values(['Country', 'Year'])

for col in INDICATORS:
    vdem_sorted[f'{col}_1yr'] = vdem_sorted.groupby('Country')[col].diff(1)
    vdem_sorted[f'{col}_3yr'] = vdem_sorted.groupby('Country')[col].diff(3)
    vdem_sorted[f'{col}_5yr'] = vdem_sorted.groupby('Country')[col].diff(5)
    vdem_sorted[f'{col}_10yr'] = vdem_sorted.groupby('Country')[col].diff(10)

vdem_sorted['Democratic Health'] = vdem_sorted[INDICATORS].mean(axis=1)

for w in [1, 3, 5, 10]:
    vdem_sorted[f'Health_{w}yr'] = vdem_sorted.groupby('Country')['Democratic Health'].diff(w)

# Acceleration: is backsliding speeding up? (1yr change minus 3yr average annual change)
vdem_sorted['Health_accel'] = (
    vdem_sorted['Health_1yr'] - (vdem_sorted['Health_3yr'] / 3)
).round(4)

# ---------------------------
# LATEST SNAPSHOT
# ---------------------------
latest_year = vdem_sorted['Year'].max()
latest = vdem_sorted[vdem_sorted['Year'] == latest_year].copy()

def backsliding_score(row):
    level_risk   = 1 - row.get('Democratic Health', 0.5)
    vel_1yr      = max(0, -(row.get('Health_1yr', 0) or 0)) * 5
    vel_5yr      = max(0, -(row.get('Health_5yr', 0) or 0)) * 3
    accel_risk   = max(0, -(row.get('Health_accel', 0) or 0)) * 4
    score = (0.25 * level_risk) + (0.35 * vel_1yr) + (0.25 * vel_5yr) + (0.15 * accel_risk)
    return round(min(score, 1.0), 4)

latest['Backsliding Risk'] = latest.apply(backsliding_score, axis=1)

def alert_tier(row):
    s  = row.get('Backsliding Risk', 0)
    c1 = row.get('Health_1yr', 0) or 0
    c5 = row.get('Health_5yr', 0) or 0
    ac = row.get('Health_accel', 0) or 0
    if c1 <= -0.06 or s >= 0.65 or ac <= -0.04:
        return "🔴 CRITICAL"
    elif c5 <= -0.05 or s >= 0.42:
        return "🟠 WATCH"
    elif c1 < -0.02 or c5 < -0.02:
        return "🟡 MONITOR"
    else:
        return "🟢 STABLE"

latest['Alert Tier'] = latest.apply(alert_tier, axis=1)

def generate_narrative(row):
    country = row['Country']
    risk    = row.get('Backsliding Risk', 0)
    chg1    = row.get('Health_1yr', 0) or 0
    chg5    = row.get('Health_5yr', 0) or 0
    accel   = row.get('Health_accel', 0) or 0

    available = [(col, row[col]) for col in INDICATORS if col in row and pd.notna(row.get(col))]
    weakest   = sorted(available, key=lambda x: x[1])[:2]

    driver_map = {
        'Free and Fair Elections': 'deteriorating electoral quality',
        'Civil Liberties': 'civil liberties restrictions',
        'Polarization': 'deepening societal polarization',
        'Political Corruption': 'rising political corruption',
    }
    drivers = [driver_map.get(n, n) for n, _ in weakest]

    if chg1 <= -0.06:
        trend = "undergoing rapid democratic backsliding"
    elif accel <= -0.03:
        trend = "showing accelerating democratic deterioration"
    elif chg5 <= -0.05:
        trend = "exhibiting sustained democratic erosion over five years"
    elif chg1 < -0.02:
        trend = "showing early-stage democratic deterioration"
    elif risk >= 0.5:
        trend = "structurally fragile despite recent stability"
    else:
        trend = "broadly stable with no acute backsliding signals"

    driver_text = " and ".join(drivers) if drivers else "multiple institutional pressures"
    accel_note  = " Backsliding is accelerating." if accel <= -0.03 else ""
    return (
        f"{country} is {trend}.{accel_note} "
        f"Primary drivers include {driver_text}. "
        f"(Risk: {risk:.3f} | 1yr: {chg1:+.3f} | 5yr: {chg5:+.3f} | Accel: {accel:+.3f})"
    )

latest['Narrative'] = latest.apply(generate_narrative, axis=1)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.markdown("### 🌍 DEMOCRACY MONITOR")
st.sidebar.markdown("---")

countries   = sorted(latest['Country'].dropna().unique())
selected_country = st.sidebar.selectbox("Country Focus", countries, index=countries.index("United States") if "United States" in countries else 0)

st.sidebar.markdown("---")
st.sidebar.markdown("**ALERT TIERS**")
for tier, desc in [
    ("🔴 CRITICAL", "Rapid or severe backsliding"),
    ("🟠 WATCH", "Meaningful erosion detected"),
    ("🟡 MONITOR", "Mild deterioration"),
    ("🟢 STABLE", "No acute warning signals"),
]:
    st.sidebar.markdown(f"`{tier}` {desc}")

st.sidebar.markdown("---")
st.sidebar.markdown("**INDICATORS**")
for ind in INDICATORS:
    st.sidebar.markdown(f"· {ind}")

# ---------------------------
# TABS
# ---------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Country Profile",
    "⚠️ Watchlist",
    "🗺️ Global Map",
    "🔀 Comparison",
    "📈 Leaderboard",
    "🔥 Heatmap"
])

# ================================================================
# TAB 1: COUNTRY PROFILE
# ================================================================
with tab1:
    country_ts     = vdem_sorted[vdem_sorted['Country'] == selected_country]
    country_latest = latest[latest['Country'] == selected_country]

    if country_latest.empty:
        st.warning("No data for selected country.")
    else:
        row = country_latest.iloc[0]

        # --- Top metrics row ---
        st.markdown(f'<div class="section-header">{selected_country} — Current Status</div>', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        def delta_color(v):
            if v is None or pd.isna(v): return "neu"
            return "neg" if v < -0.01 else ("pos" if v > 0.01 else "neu")

        for col, label, val, delta in [
            (c1, "BACKSLIDING RISK", row.get('Backsliding Risk'), None),
            (c2, "ALERT TIER", row.get('Alert Tier'), None),
            (c3, "DEMOCRATIC HEALTH", row.get('Democratic Health'), row.get('Health_1yr')),
            (c4, "1-YEAR CHANGE", row.get('Health_1yr'), None),
            (c5, "ACCELERATION", row.get('Health_accel'), None),
        ]:
            dval = f"{delta:+.3f}" if delta is not None and not pd.isna(delta) else ""
            dc   = delta_color(delta)
            vdisp = f"{val:.3f}" if isinstance(val, float) else str(val)
            col.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{vdisp}</div>
                <div class="metric-delta-{dc}">{dval}</div>
            </div>""", unsafe_allow_html=True)

        # --- Narrative ---
        st.markdown('<div class="section-header">Intelligence Summary</div>', unsafe_allow_html=True)
        tier = row.get('Alert Tier', '')
        tier_class = 'critical' if 'CRITICAL' in tier else ('watch' if 'WATCH' in tier else ('monitor' if 'MONITOR' in tier else 'stable'))
        st.markdown(f'<div class="alert-{tier_class}">{row.get("Narrative","")}</div>', unsafe_allow_html=True)

        # --- Indicator scores ---
        st.markdown('<div class="section-header">Indicator Breakdown</div>', unsafe_allow_html=True)
        icols = st.columns(len(INDICATORS))
        for i, ind in enumerate(INDICATORS):
            val   = row.get(ind, np.nan)
            chg   = row.get(f'{ind}_1yr', np.nan)
            color = "#f85149" if (pd.notna(val) and val < 0.35) else ("#f0a500" if (pd.notna(val) and val < 0.55) else "#3fb950")
            vdisp = f"{val:.3f}" if pd.notna(val) else "N/A"
            cdisp = f"{chg:+.3f}" if pd.notna(chg) else ""
            dc    = delta_color(chg)
            icols[i].markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{ind}</div>
                <div class="metric-value" style="color:{color};font-size:1.5rem">{vdisp}</div>
                <div class="metric-delta-{dc}">{cdisp} (1yr)</div>
                <div style="font-size:0.6rem;color:#8b949e;margin-top:0.3rem">{INDICATOR_DESCRIPTIONS.get(ind,'')[:60]}...</div>
            </div>""", unsafe_allow_html=True)

        # --- Trend chart ---
        st.markdown('<div class="section-header">Trends Over Time</div>', unsafe_allow_html=True)
        show_inds = st.multiselect(
            "Indicators to display",
            INDICATORS + ['Democratic Health'],
            default=INDICATORS,
            key="profile_inds"
        )
        if show_inds:
            fig = go.Figure()
            colors = ['#f0a500','#58a6ff','#3fb950','#f85149','#d2a8ff']
            for i, ind in enumerate(show_inds):
                ts = country_ts[['Year', ind]].dropna()
                fig.add_trace(go.Scatter(
                    x=ts['Year'], y=ts[ind], name=ind,
                    line=dict(color=colors[i % len(colors)], width=2),
                    hovertemplate=f'<b>{ind}</b>: %{{y:.3f}}<extra></extra>'
                ))
            fig.update_layout(
                **PLOTLY_THEME,
                height=380,
                hovermode='x unified',
                legend=dict(orientation='h', y=-0.2),
                yaxis=dict(**_YAX, range=[0,1], title='Score (0–1)'),
                xaxis=dict(**_XAX, title='Year'),
                margin=dict(l=40, r=20, t=20, b=60)
            )
            st.plotly_chart(fig, use_container_width=True)

        # --- Radar chart ---
        st.markdown('<div class="section-header">Current Indicator Radar</div>', unsafe_allow_html=True)
        avail_ind = [i for i in INDICATORS if pd.notna(row.get(i))]
        if avail_ind:
            r_vals = [row[i] for i in avail_ind]
            fig_r = go.Figure(go.Scatterpolar(
                r=r_vals + [r_vals[0]],
                theta=avail_ind + [avail_ind[0]],
                fill='toself',
                fillcolor='rgba(240,165,0,0.15)',
                line=dict(color='#f0a500', width=2),
                name=selected_country
            ))
            fig_r.update_layout(
                **PLOTLY_THEME,
                height=350,
                polar=dict(
                    bgcolor='#161b22',
                    radialaxis=dict(visible=True, range=[0,1], gridcolor='#30363d', tickcolor='#30363d', tickfont=dict(size=9)),
                    angularaxis=dict(gridcolor='#30363d', tickfont=dict(size=10, color='#c9d1d9'))
                ),
                showlegend=False,
                margin=dict(l=60, r=60, t=30, b=30)
            )
            st.plotly_chart(fig_r, use_container_width=True)

        # --- Acceleration chart ---
        st.markdown('<div class="section-header">Backsliding Acceleration (1yr vs 3yr avg)</div>', unsafe_allow_html=True)
        st.caption("Negative values = deteriorating. Bars below zero AND getting more negative = accelerating backsliding.")
        accel_ts = country_ts[['Year','Health_1yr','Health_accel']].dropna().tail(30)
        fig_a = go.Figure()
        fig_a.add_trace(go.Bar(
            x=accel_ts['Year'], y=accel_ts['Health_1yr'],
            name='1-Year Change',
            marker_color=['#f85149' if v < 0 else '#3fb950' for v in accel_ts['Health_1yr']],
        ))
        fig_a.add_trace(go.Scatter(
            x=accel_ts['Year'], y=accel_ts['Health_accel'],
            name='Acceleration',
            line=dict(color='#f0a500', width=2, dash='dot'),
        ))
        fig_a.add_hline(y=0, line_color='#30363d', line_width=1)
        fig_a.update_layout(**PLOTLY_THEME, height=280, margin=dict(l=40,r=20,t=20,b=40),
                            legend=dict(orientation='h',y=-0.25))
        st.plotly_chart(fig_a, use_container_width=True)

        # --- Historical backsliding event detector ---
        st.markdown('<div class="section-header">Historical Backsliding Events</div>', unsafe_allow_html=True)
        st.caption("Years where 1-year democratic health dropped ≥ 0.04 (significant decline threshold).")
        events = country_ts[country_ts['Health_1yr'] <= -0.04][['Year','Democratic Health','Health_1yr','Health_accel'] + INDICATORS].copy()
        if not events.empty:
            events = events.sort_values('Health_1yr')
            events.columns = [c.replace('Health_','Δ Health ') for c in events.columns]
            st.dataframe(events.round(3), use_container_width=True)
        else:
            st.markdown('<div class="alert-stable">No significant backsliding events detected for this country.</div>', unsafe_allow_html=True)

# ================================================================
# TAB 2: WATCHLIST
# ================================================================
with tab2:
    st.markdown('<div class="section-header">Backsliding Early Warning Watchlist</div>', unsafe_allow_html=True)
    st.caption("All countries showing CRITICAL, WATCH, or MONITOR signals. Sorted by backsliding risk.")

    tier_filter = st.multiselect(
        "Filter by Alert Tier",
        ["🔴 CRITICAL", "🟠 WATCH", "🟡 MONITOR"],
        default=["🔴 CRITICAL", "🟠 WATCH", "🟡 MONITOR"],
        key="watchlist_filter"
    )

    watchlist = latest[latest['Alert Tier'].isin(tier_filter)].copy()
    watchlist = watchlist.sort_values('Backsliding Risk', ascending=False)

    disp_cols = ['Country','Alert Tier','Backsliding Risk','Health_1yr','Health_5yr','Health_accel'] + INDICATORS
    disp_cols = [c for c in disp_cols if c in watchlist.columns]

    st.dataframe(
        watchlist[disp_cols].rename(columns={
            'Health_1yr': 'Δ1yr', 'Health_5yr': 'Δ5yr', 'Health_accel': 'Accel'
        }).round(3),
        use_container_width=True,
        height=400,
        column_config={"Alert Tier": st.column_config.TextColumn("Alert Tier", width="medium")}
    )

    # Drill-down
    st.markdown('<div class="section-header">Watchlist Drill-Down</div>', unsafe_allow_html=True)
    if not watchlist.empty:
        watch_country = st.selectbox("Select Country", watchlist['Country'].unique(), key="watch_drill")
        if watch_country:
            wr = latest[latest['Country'] == watch_country].iloc[0]
            tier = wr.get('Alert Tier','')
            tc = 'critical' if 'CRITICAL' in tier else ('watch' if 'WATCH' in tier else 'monitor')
            st.markdown(f'<div class="alert-{tc}">{wr["Narrative"]}</div>', unsafe_allow_html=True)

            # Sparklines for each indicator
            wts = vdem_sorted[vdem_sorted['Country'] == watch_country]
            fig_sp = make_subplots(rows=1, cols=len(INDICATORS), subplot_titles=INDICATORS)
            colors = ['#f0a500','#58a6ff','#3fb950','#f85149']
            for i, ind in enumerate(INDICATORS):
                ts = wts[['Year', ind]].dropna().tail(30)
                fig_sp.add_trace(
                    go.Scatter(x=ts['Year'], y=ts[ind], line=dict(color=colors[i], width=2), showlegend=False),
                    row=1, col=i+1
                )
            fig_sp.update_layout(**PLOTLY_THEME, height=200, margin=dict(l=20,r=20,t=40,b=20))
            st.plotly_chart(fig_sp, use_container_width=True)

# ================================================================
# TAB 3: GLOBAL MAP
# ================================================================
with tab3:
    st.markdown('<div class="section-header">Global Backsliding Risk Map</div>', unsafe_allow_html=True)

    map_metric = st.selectbox(
        "Map Metric",
        ['Backsliding Risk', 'Democratic Health', 'Health_1yr', 'Health_5yr'] + INDICATORS,
        key="map_metric"
    )

    hover_cols = ['Alert Tier','Backsliding Risk','Health_1yr','Health_5yr'] + INDICATORS
    hover_cols = [c for c in hover_cols if c in latest.columns]

    scale = "RdYlGn" if map_metric in INDICATORS + ['Democratic Health'] else "RdYlGn_r"
    fig_map = px.choropleth(
        latest,
        locations="Country",
        locationmode="country names",
        color=map_metric,
        color_continuous_scale=scale,
        hover_data=hover_cols,
        title=f"Global View: {map_metric}"
    )
    fig_map.update_layout(
        paper_bgcolor='#161b22',
        plot_bgcolor='#161b22',
        font=dict(family='JetBrains Mono', color='#c9d1d9', size=11),
        geo=dict(bgcolor='#0d1117', showframe=False, showcoastlines=True,
                 coastlinecolor='#30363d', landcolor='#1c2128', showocean=True,
                 oceancolor='#0d1117', lakecolor='#0d1117'),
        coloraxis_colorbar=dict(title=map_metric[:20], tickfont=dict(size=9)),
        margin=dict(l=0, r=0, t=40, b=0),
        height=500
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ================================================================
# TAB 4: COUNTRY COMPARISON
# ================================================================
with tab4:
    st.markdown('<div class="section-header">Country Comparison</div>', unsafe_allow_html=True)
    st.caption("Compare up to 5 countries across all indicators and trend windows.")

    compare_countries = st.multiselect(
        "Select Countries to Compare",
        countries,
        default=[selected_country] + (["France","Brazil","Hungary"] if all(c in countries for c in ["France","Brazil","Hungary"]) else []),
        max_selections=5,
        key="compare_sel"
    )

    if compare_countries:
        comp_data = latest[latest['Country'].isin(compare_countries)]

        # Radar overlay
        st.markdown('<div class="section-header">Radar Overlay</div>', unsafe_allow_html=True)
        fig_cmp = go.Figure()
        colors = ['#f0a500','#58a6ff','#3fb950','#f85149','#d2a8ff']
        for i, c in enumerate(compare_countries):
            crow = comp_data[comp_data['Country'] == c]
            if crow.empty: continue
            crow = crow.iloc[0]
            avail = [ind for ind in INDICATORS if pd.notna(crow.get(ind))]
            if not avail: continue
            rvals = [crow[ind] for ind in avail]
            fig_cmp.add_trace(go.Scatterpolar(
                r=rvals + [rvals[0]],
                theta=avail + [avail[0]],
                name=c,
                line=dict(color=colors[i], width=2),
                fill='toself',
                fillcolor=f"rgba({int(colors[i][1:3],16)},{int(colors[i][3:5],16)},{int(colors[i][5:7],16)},0.08)"
            ))
        fig_cmp.update_layout(
            **PLOTLY_THEME,
            height=420,
            polar=dict(
                bgcolor='#161b22',
                radialaxis=dict(visible=True, range=[0,1], gridcolor='#30363d', tickfont=dict(size=9)),
                angularaxis=dict(gridcolor='#30363d', tickfont=dict(size=10, color='#c9d1d9'))
            ),
            legend=dict(orientation='h', y=-0.1),
            margin=dict(l=60, r=60, t=30, b=60)
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        # Trend lines — Democratic Health
        st.markdown('<div class="section-header">Democratic Health Over Time</div>', unsafe_allow_html=True)
        fig_cmp2 = go.Figure()
        for i, c in enumerate(compare_countries):
            ts = vdem_sorted[vdem_sorted['Country'] == c][['Year','Democratic Health']].dropna()
            fig_cmp2.add_trace(go.Scatter(
                x=ts['Year'], y=ts['Democratic Health'],
                name=c,
                line=dict(color=colors[i], width=2),
                hovertemplate=f'<b>{c}</b>: %{{y:.3f}}<extra></extra>'
            ))
        fig_cmp2.update_layout(
            **PLOTLY_THEME, height=350,
            hovermode='x unified',
            yaxis=dict(**_YAX, range=[0,1], title='Democratic Health'),
            xaxis=dict(**_XAX, title='Year'),
            legend=dict(orientation='h', y=-0.2),
            margin=dict(l=40, r=20, t=20, b=60)
        )
        st.plotly_chart(fig_cmp2, use_container_width=True)

        # Comparison table
        st.markdown('<div class="section-header">Side-by-Side Metrics</div>', unsafe_allow_html=True)
        cmp_cols = ['Country','Alert Tier','Backsliding Risk','Democratic Health','Health_1yr','Health_5yr','Health_accel'] + INDICATORS
        cmp_cols = [c for c in cmp_cols if c in comp_data.columns]
        st.dataframe(comp_data[cmp_cols].round(3).set_index('Country'), use_container_width=True)

# ================================================================
# TAB 5: LEADERBOARD
# ================================================================
with tab5:
    st.markdown('<div class="section-header">Most Deteriorated (5-Year)</div>', unsafe_allow_html=True)
    st.caption("Countries with the largest drops in Democratic Health over the past 5 years.")

    deteriorated = latest.sort_values('Health_5yr').head(20)[
        ['Country','Alert Tier','Health_5yr','Health_1yr','Backsliding Risk','Democratic Health'] + INDICATORS
    ].round(3)
    st.dataframe(deteriorated, use_container_width=True,
                 column_config={"Alert Tier": st.column_config.TextColumn("Alert Tier", width="medium")})

    fig_det = px.bar(
        deteriorated.head(15),
        x='Country', y='Health_5yr',
        color='Backsliding Risk',
        color_continuous_scale='Reds',
        title='Top 15 Most Deteriorated (5-Year Δ Democratic Health)',
        labels={'Health_5yr': '5-Year Change'}
    )
    fig_det.update_layout(**PLOTLY_THEME, height=350, margin=dict(l=40,r=20,t=40,b=100),
                          xaxis_tickangle=-45)
    st.plotly_chart(fig_det, use_container_width=True)

    st.markdown('<div class="section-header">Most Improved (5-Year)</div>', unsafe_allow_html=True)
    improved = latest.sort_values('Health_5yr', ascending=False).head(15)[
        ['Country','Health_5yr','Health_1yr','Democratic Health'] + INDICATORS
    ].round(3)
    fig_imp = px.bar(
        improved,
        x='Country', y='Health_5yr',
        color='Health_5yr',
        color_continuous_scale='Greens',
        title='Top 15 Most Improved (5-Year Δ Democratic Health)',
        labels={'Health_5yr': '5-Year Change'}
    )
    fig_imp.update_layout(**PLOTLY_THEME, height=350, margin=dict(l=40,r=20,t=40,b=100),
                          xaxis_tickangle=-45)
    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown('<div class="section-header">Fastest Accelerating Decline (Right Now)</div>', unsafe_allow_html=True)
    st.caption("Acceleration = 1-year change minus 3-year average annual change. Most negative = backsliding is speeding up fastest.")
    accel_top = latest.sort_values('Health_accel').head(15)[
        ['Country','Health_accel','Health_1yr','Backsliding Risk','Alert Tier']
    ].round(4)
    st.dataframe(accel_top, use_container_width=True)

# ================================================================
# TAB 6: CORRELATION HEATMAP
# ================================================================
with tab6:
    st.markdown('<div class="section-header">Indicator Correlation Heatmap</div>', unsafe_allow_html=True)
    st.caption("Correlation between indicators across all countries in the latest year. Values near 1 = move together; near -1 = move oppositely.")

    corr_cols = INDICATORS + ['Democratic Health', 'Backsliding Risk', 'Health_1yr', 'Health_5yr']
    corr_cols = [c for c in corr_cols if c in latest.columns]
    corr_matrix = latest[corr_cols].corr().round(2)

    fig_heat = go.Figure(go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns.tolist(),
        y=corr_matrix.index.tolist(),
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate="%{text}",
        textfont=dict(size=10),
        hoverongaps=False,
        colorbar=dict(title='r', tickfont=dict(size=9))
    ))
    fig_heat.update_layout(
        **PLOTLY_THEME,
        height=500,
        margin=dict(l=120, r=40, t=40, b=120),
        xaxis=dict(**_XAX, tickangle=-40, tickfont=dict(size=10)),
        yaxis=dict(**_YAX, tickfont=dict(size=10))
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<div class="section-header">Long-Run Indicator Trends — Global Average</div>', unsafe_allow_html=True)
    st.caption("Mean score across all countries, each year. Shows global democratic trajectory.")

    global_avg = vdem_sorted.groupby('Year')[INDICATORS + ['Democratic Health']].mean().reset_index()
    fig_glob = go.Figure()
    for i, ind in enumerate(INDICATORS + ['Democratic Health']):
        colors_g = ['#f0a500','#58a6ff','#3fb950','#f85149','#d2a8ff']
        fig_glob.add_trace(go.Scatter(
            x=global_avg['Year'], y=global_avg[ind],
            name=ind, line=dict(color=colors_g[i % len(colors_g)], width=2),
        ))
    fig_glob.update_layout(
        **PLOTLY_THEME, height=380,
        hovermode='x unified',
        yaxis=dict(**_YAX, range=[0,1], title='Global Mean Score'),
        legend=dict(orientation='h', y=-0.25),
        margin=dict(l=40, r=20, t=20, b=80)
    )
    st.plotly_chart(fig_glob, use_container_width=True)

# ---------------------------
# DOWNLOAD
# ---------------------------
st.markdown("---")
export_cols = ['Country','Year','Alert Tier','Backsliding Risk','Democratic Health',
               'Health_1yr','Health_5yr','Health_accel'] + INDICATORS + ['Narrative']
export_cols = [c for c in export_cols if c in latest.columns]
st.download_button(
    "📥 Download Full Dataset (CSV)",
    latest[export_cols].to_csv(index=False).encode('utf-8'),
    "democracy_monitor_v10.csv",
    use_container_width=False
)
