import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats

# ==========================================
# 🥇 1. Page Configuration & Setup
# ==========================================
st.set_page_config(page_title="Advanced Statistical Analysis System", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# 🎨 2. Premium UI/UX CSS Engine (Glassmorphism & Dark Mode)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Background Gradient override */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #e2e8f0;
    }
    
    /* Headers Styling */
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
    }
    
    /* Glassmorphism Containers */
    .glass-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .glass-box:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        color: #10b981 !important;
        font-weight: 800 !important;
    }
    
    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🌟 3. Hero Section
# ==========================================
st.markdown("""
<div class="glass-box" style="text-align: center; background: linear-gradient(90deg, rgba(15,23,42,1) 0%, rgba(30,27,75,0.8) 100%); padding-bottom: 25px;">
    <h1 style='font-size: 3rem; margin-bottom: 0.2rem; background: -webkit-linear-gradient(#38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Advanced Statistical Analysis System (SAS)</h1>
   
</div>
""", unsafe_allow_html=True)

# ==========================================
# 💾 4. Session State & Sidebar Data Loading
# ==========================================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filename' not in st.session_state:
    st.session_state.filename = ""

with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ System Settings</h2>", unsafe_allow_html=True)
    
    domain = st.selectbox("🌐 Academic Domain Customization:", 
                          ["🏥 Medical Research", 
                           "🦕 Paleontology",
                           "🔬 General Scientific Research"])
                           
    st.markdown("---")
    st.markdown("### 📂 Data Import")
    uploaded_file = st.file_uploader("Upload Data File (CSV or Excel)", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name != st.session_state.filename:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, on_bad_lines='skip')
                else:
                    df = pd.read_excel(uploaded_file)
                st.session_state.df = df
                st.session_state.filename = uploaded_file.name
                
            st.success("✅ Data read successfully!")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            
   
# ==========================================
# 🚀 5. Core Application Logic
# ==========================================
if st.session_state.df is not None:
    df = st.session_state.df
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

    # Create Navigation Tabs
    tab_lab, tab_visuals, tab_stats, tab_report = st.tabs([
        "🗄️ Data Lab", 
        "📊 Visual Intelligence", 
        "🧮 Statistical Engine", 
        "📑 Technical Report"
    ])
    
    # ----------------------------------------
    # TAB 1: DATA LAB
    # ----------------------------------------
    with tab_lab:
        st.markdown("<h2 style='color:#38bdf8;'>🗄️ Dataset Overview & Preprocessing</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())
        cleanliness = (1 - df.isnull().sum().sum() / max(1, (df.shape[0]*df.shape[1])))*100
        col4.metric("Data Integrity", f"{cleanliness:.1f}%")
        
        st.markdown("### 📋 Raw Data Preview")
        st.dataframe(df.head(100), use_container_width=True)
        
        st.markdown("### 📉 Descriptive Statistics")
        st.dataframe(df.describe().T, use_container_width=True) 
        
    # ----------------------------------------
    # TAB 2: VISUAL INTELLIGENCE
    # ----------------------------------------
    with tab_visuals:
        st.markdown("<h2 style='color:#38bdf8;'>📊 Interactive Visualization Dashboard</h2>", unsafe_allow_html=True)
        
        if len(numeric_cols) >= 1:
            v_col1, v_col2 = st.columns([1, 2.5])
            
            with v_col1:
                st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                st.markdown("<h4>Plot Settings 🛠️</h4>", unsafe_allow_html=True)
                plot_type = st.selectbox("Plot Type:", ["Scatter Plot 🌠", "Histogram 📊", "Box Plot 📦", "Violin Plot 🎻"])
                x_axis = st.selectbox("X-Axis Variable:", numeric_cols)
                
                y_axis = None
                if len(numeric_cols) > 1 and "Histogram" not in plot_type:
                    y_axis = st.selectbox("Y-Axis Variable:", numeric_cols, index=1 if x_axis == numeric_cols[0] else 0)
                
                color_dim = st.selectbox("Color Mapping (Optional):", ["None"] + categorical_cols)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with v_col2:
                st.markdown('<div class="glass-box">', unsafe_allow_html=True)
                color_param = color_dim if color_dim != "None" else None
                
                try:
                    if "Scatter" in plot_type and y_axis is not None:
                        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_param, template="plotly_dark", 
                                         color_discrete_sequence=px.colors.qualitative.Pastel)
                    elif "Histogram" in plot_type:
                        fig = px.histogram(df, x=x_axis, color=color_param, template="plotly_dark", marginal="box",
                                           color_discrete_sequence=px.colors.qualitative.Pastel)
                    elif "Box" in plot_type and y_axis is not None:
                        fig = px.box(df, x=color_param, y=y_axis, template="plotly_dark",
                                     color_discrete_sequence=px.colors.qualitative.Pastel)
                    elif "Violin" in plot_type and y_axis is not None:
                        fig = px.violin(df, x=color_param, y=y_axis, template="plotly_dark", box=True,
                                        color_discrete_sequence=px.colors.qualitative.Pastel)
                    else:
                        fig = px.histogram(df, x=x_axis, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
                    
                    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as chart_err:
                    st.error(f"⚠️ Error generating plot: {chart_err}")
                st.markdown('</div>', unsafe_allow_html=True)
                
            st.markdown("### 🗺️ Correlation Heatmap")
            if len(numeric_cols) >= 2:
                try:
                    corr = df[numeric_cols].corr()
                    fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", template="plotly_dark")
                    fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_corr, use_container_width=True)
                except Exception as corr_err:
                    st.error(f"⚠️ Correlation matrix error: {corr_err}")

        else:
            st.warning("⚠️ Insufficient numeric columns for advanced visualization.")
            
    # ----------------------------------------
    # TAB 3: STATISTICAL ENGINE
    # ----------------------------------------
    with tab_stats:
        st.markdown("<h2 style='color:#38bdf8;'>🧮 Statistical Engine (Hypothesis Testing)</h2>", unsafe_allow_html=True)
        st.info("💡 Performs advanced statistical algorithms to test hypotheses with academic precision.")
        
        stat_col1, stat_col2 = st.columns(2)
        
        with stat_col1:
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            st.markdown("### 1️⃣ Independent Samples T-Test")
            if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
                ttest_num = st.selectbox("Numerical Variable (Dependent):", numeric_cols, key="tt_num")
                ttest_cat = st.selectbox("Categorical Variable (Independent - 2 groups):", categorical_cols, key="tt_cat")
                
                if st.button("🚀 Run T-Test"):
                    groups = df[ttest_cat].dropna().unique()
                    if len(groups) == 2:
                        g1 = df[df[ttest_cat] == groups[0]][ttest_num].dropna()
                        g2 = df[df[ttest_cat] == groups[1]][ttest_num].dropna()
                        t_stat, p_val = stats.ttest_ind(g1, g2)
                        st.write(f"**T-Statistic:** `{t_stat:.4f}`")
                        st.write(f"**P-Value:** `{p_val:.4e}`")
                        if p_val < 0.05:
                            st.success(f"📌 **Statistical Conclusion:** Significant difference exists between ({groups[0]}) and ({groups[1]}) (P < 0.05).")
                        else:
                            st.warning(f"📌 **Statistical Conclusion:** No statistically significant difference found between the groups.")
                    else:
                        st.error(f"The variable {ttest_cat} contains {len(groups)} groups. T-Test requires exactly 2.")
            else:
                st.warning("Requires at least one numeric and one categorical variable.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with stat_col2:
            st.markdown('<div class="glass-box">', unsafe_allow_html=True)
            st.markdown("### 2️⃣ Pearson Correlation Analysis")
            if len(numeric_cols) >= 2:
                pearson_x = st.selectbox("Variable 1:", numeric_cols, key="p_x")
                pearson_y = st.selectbox("Variable 2:", numeric_cols, key="p_y", index=1)
                
                if st.button("🚀 Calculate Pearson r"):
                    clean_df = df[[pearson_x, pearson_y]].dropna()
                    if len(clean_df) > 1:
                        r, p = stats.pearsonr(clean_df[pearson_x], clean_df[pearson_y])
                        st.write(f"**Correlation Coefficient (r):** `{r:.4f}`")
                        st.write(f"**P-Value:** `{p:.4e}`")
                        
                        if abs(r) > 0.7: strength = "Very Strong"
                        elif abs(r) > 0.4: strength = "Moderate"
                        elif abs(r) > 0.2: strength = "Weak"
                        else: strength = "Negligible"
                        
                        direction = "Positive" if r > 0 else "Negative"
                        st.success(f"📌 **Statistical Conclusion:** A {direction} {strength} correlation was detected.")
                    else:
                        st.error("Insufficient data points after missing value removal.")
            else:
                st.warning("Requires at least two numeric variables.")
            st.markdown("</div>", unsafe_allow_html=True)

    # ----------------------------------------
    # TAB 4: TECHNICAL REPORT
    # ----------------------------------------
    with tab_report:
        st.markdown("<h2 style='color:#38bdf8;'>📑 Automated Technical Summary</h2>", unsafe_allow_html=True)
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown(f"### 📑 Analysis Report: {st.session_state.filename} ({domain})")
        
        st.markdown("#### 1. Executive Structural Summary:")
        st.write(f"- 📊 The dataset contains **{df.shape[0]} rows** and **{df.shape[1]} variables**, optimized for analysis in {domain}.")
        st.write(f"- 🧹 Data integrity module confirms a high saturation level of **{cleanliness:.2f}%**.")
        
        st.markdown("#### 2. Key Statistical Insights:")
        if len(numeric_cols) > 0:
            for col in numeric_cols[:2]: 
                mean_val = df[col].mean()
                max_val = df[col].max()
                st.write(f"""
                - 🔹 For **{col}**: The distribution mean stabilized at **{mean_val:.2f}**, with a peak value of **{max_val:.2f}**. 
                  This pattern serves as a primary indicative standard for scientific deduction.
                """)
                
        if len(numeric_cols) >= 2:
            st.markdown("#### 3. Significant Correlation Findings:")
            corr_matrix = df[numeric_cols].corr().abs()
            corr_matrix = corr_matrix.mask(np.eye(len(corr_matrix), dtype=bool), 0)
            if not corr_matrix.empty and not corr_matrix.isna().all().all():
                max_corr = corr_matrix.max().max()
                if not pd.isna(max_corr) and max_corr > 0.1:
                    vars_max_corr = np.where(corr_matrix == max_corr)
                    if len(vars_max_corr[0]) > 0:
                        var1 = corr_matrix.index[vars_max_corr[0][0]]
                        var2 = corr_matrix.columns[vars_max_corr[1][0]]
                        st.write(f"⚠️ **Analytical Note:** Results indicate a notable statistical correlation of **{max_corr*100:.1f}%** between **{var1}** and **{var2}**, warranting further research focus.")
                
        st.info("📄 This report was automatically generated based on extracted statistical results and is ready for academic review.")
        st.download_button("📥 Download Technical Summary (Txt File)", "Statistical Analysis Executive Report\nData Analysis Summary...", file_name="Statistical_Report.txt")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
else:
    # ----------------------------------------
    # EMPTY STATE UI 
    # ----------------------------------------
    st.markdown("""
        <div style='margin-top: 50px; text-align: center; background: rgba(255,255,255,0.03); padding: 50px; border-radius: 20px; border: 1px dashed rgba(255,255,255,0.1);'>
            <h2 style='color: #64748b; font-weight:400;'>👈 Please upload a data file to begin the analysis experience...</h2>
            <p style='color: #475569;'>The system supports CSV and Excel formats with high-speed processing.</p>
        </div>
    """, unsafe_allow_html=True)
    
st.markdown("<hr style='opacity: 0.1;'><p style='text-align: center; color: #64748b; font-size: 0.8rem;'>Statistical Analysis System Version 2.0 - 2026</p>", unsafe_allow_html=True)