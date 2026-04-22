import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats


PRIMARY_BLUE = "#0B5DAA"
DEEP_BLUE = "#114E8A"
MINT = "#34C6B3"
SOFT_MINT = "#DDF7F4"
SOFT_BLUE = "#E8F1FB"
SOFT_RED = "#FCE8E8"
BG_LIGHT = "#F7F9FC"
CARD_BG = "#FFFFFF"
TEXT_MAIN = "#223042"
TEXT_MUTED = "#7B8794"
BORDER = "#E4EAF1"
CUSTOM_SEQ = [PRIMARY_BLUE, MINT, DEEP_BLUE, "#6FB9D6", "#96D9CF"]


st.set_page_config(
    page_title="Statistical Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    .stApp {{
        background:
            radial-gradient(circle at top left, rgba(11, 93, 170, 0.08), transparent 22%),
            radial-gradient(circle at top right, rgba(52, 198, 179, 0.08), transparent 24%),
            linear-gradient(180deg, {BG_LIGHT} 0%, #FFFFFF 100%);
        color: {TEXT_MAIN};
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] h5,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span {{
        color: {TEXT_MAIN} !important;
    }}

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(180deg, rgba(11, 93, 170, 0.98) 0%, rgba(10, 76, 138, 0.98) 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {{
        color: #ffffff !important;
    }}

    /* Sidebar uploader contrast fix */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {{
        background: rgba(255, 255, 255, 0.96);
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 18px;
        padding: 12px;
    }}

    [data-testid="stSidebar"] [data-testid="stFileUploader"] * {{
        color: {TEXT_MAIN} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stFileUploader"] svg {{
        color: {PRIMARY_BLUE} !important;
        fill: {PRIMARY_BLUE} !important;
    }}

    [data-testid="stSidebar"] [data-testid="stFileUploader"] button {{
        background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, {DEEP_BLUE} 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
    }}

    .hero-banner {{
        background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, {DEEP_BLUE} 100%);
        border: 1px solid rgba(11, 93, 170, 0.12);
        padding: 34px 30px;
        border-radius: 22px;
        margin-bottom: 28px;
        box-shadow: 0 18px 44px rgba(11, 93, 170, 0.22);
    }}

    .hero-banner h1,
    .hero-banner p {{
        color: white !important;
        margin: 0;
    }}

    .hero-banner p {{
        margin-top: 10px;
        opacity: 0.9;
        font-size: 1.05rem;
    }}

    .stat-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.06);
        margin-bottom: 16px;
    }}

    .metric-container {{
        display: flex;
        align-items: center;
        gap: 14px;
    }}

    .metric-icon-box {{
        min-width: 56px;
        min-height: 56px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        letter-spacing: 0.02em;
    }}

    .metric-label {{
        color: {TEXT_MUTED};
        font-size: 0.92rem;
        margin-bottom: 2px;
    }}

    .metric-value {{
        color: {TEXT_MAIN};
        font-size: 1.5rem;
        font-weight: 800;
        line-height: 1.1;
    }}

    button[data-baseweb="tab"] {{
        color: {TEXT_MUTED} !important;
        font-weight: 600 !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {PRIMARY_BLUE} !important;
        border-bottom-color: {PRIMARY_BLUE} !important;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    textarea,
    input {{
        background-color: #FFFFFF !important;
        color: {TEXT_MAIN} !important;
        border-color: {BORDER} !important;
    }}

    div[data-baseweb="select"] * {{
        color: {TEXT_MAIN} !important;
    }}

    .stButton > button,
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {PRIMARY_BLUE} 0%, {DEEP_BLUE} 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 24px rgba(11, 93, 170, 0.22);
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover {{
        filter: brightness(1.07);
        transform: translateY(-1px);
    }}

    [data-testid="stFileUploader"] {{
        background: rgba(11, 93, 170, 0.04);
        border: 1px dashed rgba(11, 93, 170, 0.22);
        border-radius: 16px;
        padding: 8px;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 16px;
        overflow: hidden;
    }}

    div[data-testid="stAlert"] {{
        border-radius: 14px;
    }}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    """
<div class="hero-banner">
    <h1 style="font-size: 2.5rem; font-weight: 800;">Analysis Dashboard</h1>
    <p>Advanced statistical analysis, visualization, and reporting in one place.</p>
</div>
""",
    unsafe_allow_html=True,
)


def render_card(label, value, icon, bg, text_color):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="metric-container">
                <div class="metric-icon-box" style="background: {bg}; color: {text_color};">{icon}</div>
                <div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if "df" not in st.session_state:
    st.session_state.df = None
if "filename" not in st.session_state:
    st.session_state.filename = ""


with st.sidebar:
    st.markdown("### System Configuration")
    domain = st.selectbox(
        "Select a scientific domain",
        ["🏥 Medical Research", 
                           "🦕 Paleontology",
                           "🔬 General Scientific Research"],
    )

    st.markdown("---")
    st.markdown("### Data Acquisition")
    uploaded_file = st.file_uploader("Upload a dataset (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name != st.session_state.filename:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file, on_bad_lines="skip")
                else:
                    df = pd.read_excel(uploaded_file)

                st.session_state.df = df
                st.session_state.filename = uploaded_file.name

            st.success("File loaded successfully.")
        except Exception as e:
            st.error(f"Could not load the file: {e}")


if st.session_state.df is not None:
    df = st.session_state.df
    numeric_cols = df.select_dtypes(include=["float64", "int64", "float32", "int32"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    tabs = st.tabs(["Overview", "Visualizer", "Statistics", "Technical Report"])

    with tabs[0]:
        st.markdown("### Dataset Overview")

        integrity = (1 - df.isnull().sum().sum() / max(1, df.size)) * 100

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_card("Rows", df.shape[0], "Rows", SOFT_BLUE, PRIMARY_BLUE)
        with c2:
            render_card("Columns", df.shape[1], "Cols", "#E9F0FB", DEEP_BLUE)
        with c3:
            render_card("Missing Cells", int(df.isnull().sum().sum()), "Warn", SOFT_RED, "#D84F4F")
        with c4:
            render_card("Data Integrity", f"{integrity:.1f}%", "OK", SOFT_MINT, MINT)

        st.markdown("#### Raw Data Preview")
        st.dataframe(df.head(100), use_container_width=True)

        st.markdown("#### Descriptive Statistics")
        if numeric_cols:
            st.dataframe(df[numeric_cols].describe().T, use_container_width=True)
        else:
            st.info("No numeric columns were found, so descriptive statistics are limited.")

    with tabs[1]:
        st.markdown("### Interactive Data Visualization")

        if numeric_cols:
            left, right = st.columns([1, 3])

            with left:
                st.markdown("#### Plot Settings")
                p_type = st.selectbox("Visualization type", ["Scatter Plot", "Histogram", "Box Plot", "Violin Plot"])
                x_ax = st.selectbox("X-axis", numeric_cols)
                y_ax = None
                if "Histogram" not in p_type and len(numeric_cols) > 1:
                    y_ax = st.selectbox("Y-axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                color_v = st.selectbox("Group by color", ["None"] + categorical_cols)

            with right:
                color_p = None if color_v == "None" else color_v
                try:
                    if "Scatter" in p_type:
                        if y_ax is None:
                            st.warning("Scatter plots need two numeric variables.")
                        else:
                            fig = px.scatter(
                                df,
                                x=x_ax,
                                y=y_ax,
                                color=color_p,
                                template="plotly_white",
                                color_discrete_sequence=CUSTOM_SEQ,
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    elif "Histogram" in p_type:
                        fig = px.histogram(
                            df,
                            x=x_ax,
                            color=color_p,
                            template="plotly_white",
                            marginal="box",
                            color_discrete_sequence=CUSTOM_SEQ,
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif "Box" in p_type:
                        if y_ax is None:
                            st.warning("Box plots need a numeric Y-axis.")
                        else:
                            fig = px.box(
                                df,
                                x=color_p,
                                y=y_ax,
                                template="plotly_white",
                                color_discrete_sequence=CUSTOM_SEQ,
                            )
                            st.plotly_chart(fig, use_container_width=True)

                    elif "Violin" in p_type:
                        if y_ax is None:
                            st.warning("Violin plots need a numeric Y-axis.")
                        else:
                            fig = px.violin(
                                df,
                                x=color_p,
                                y=y_ax,
                                box=True,
                                template="plotly_white",
                                color_discrete_sequence=CUSTOM_SEQ,
                            )
                            st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Visualization error: {e}")

            st.markdown("#### Correlation Heatmap")
            if len(numeric_cols) >= 2:
                try:
                    corr = df[numeric_cols].corr()
                    fig_corr = px.imshow(
                        corr,
                        text_auto=".2f",
                        color_continuous_scale=[(0, SOFT_BLUE), (0.5, MINT), (1, PRIMARY_BLUE)],
                        template="plotly_white",
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
                except Exception as e:
                    st.error(f"Correlation heatmap error: {e}")
            else:
                st.info("At least two numeric columns are needed for a correlation heatmap.")
        else:
            st.warning("No numeric columns were found for visualization.")

    with tabs[2]:
        st.markdown("### Hypothesis Testing Engine")
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.markdown("#### 1. Independent Samples T-Test")
            if numeric_cols and categorical_cols:
                n_var = st.selectbox("Numeric variable", numeric_cols, key="t_num")
                c_var = st.selectbox("Grouping variable", categorical_cols, key="t_cat")
                if st.button("Run T-Test"):
                    groups = df[c_var].dropna().unique()
                    if len(groups) == 2:
                        g1 = df[df[c_var] == groups[0]][n_var].dropna()
                        g2 = df[df[c_var] == groups[1]][n_var].dropna()

                        if len(g1) < 2 or len(g2) < 2:
                            st.error("Each group needs at least two valid values.")
                        else:
                            t_stat, p_val = stats.ttest_ind(g1, g2)
                            st.write(f"T-Statistic: `{t_stat:.4f}`")
                            st.write(f"P-Value: `{p_val:.4e}`")
                            if p_val < 0.05:
                                st.success("The difference is statistically significant.")
                            else:
                                st.info("The difference is not statistically significant.")
                    else:
                        st.error("The grouping variable must contain exactly two categories.")
            else:
                st.warning("T-Test requires one numeric variable and one categorical variable.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.markdown("#### 2. Pearson Correlation")
            if len(numeric_cols) >= 2:
                v1 = st.selectbox("First variable", numeric_cols, key="p_x")
                v2 = st.selectbox("Second variable", numeric_cols, key="p_y")
                if st.button("Calculate Correlation"):
                    clean_pair = df[[v1, v2]].dropna()
                    if len(clean_pair) < 2:
                        st.error("Not enough matching data after removing missing values.")
                    else:
                        try:
                            r, p = stats.pearsonr(clean_pair[v1], clean_pair[v2])
                            st.write(f"Correlation Coefficient (r): `{r:.4f}`")
                            st.write(f"P-Value: `{p:.4e}`")
                            if abs(r) >= 0.7:
                                strength = "strong"
                            elif abs(r) >= 0.4:
                                strength = "moderate"
                            elif abs(r) >= 0.2:
                                strength = "weak"
                            else:
                                strength = "very weak"
                            direction = "positive" if r > 0 else "negative"
                            st.success(f"The relationship is {direction} and {strength}.")
                        except Exception as e:
                            st.error(f"Correlation calculation failed: {e}")
            else:
                st.warning("Pearson correlation requires at least two numeric variables.")
            st.markdown("</div>", unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("### Automated Technical Summary")

        report_lines = [
            f"Analysis Report for: {st.session_state.filename}",
            f"Scientific Domain: {domain}",
            "",
            f"Rows: {df.shape[0]}",
            f"Columns: {df.shape[1]}",
            f"Missing cells: {int(df.isnull().sum().sum())}",
            f"Data integrity: {integrity:.2f}%",
            "",
            "Key notes:",
        ]

        if numeric_cols:
            for col in numeric_cols[:3]:
                report_lines.append(
                    f"- {col}: mean={df[col].mean():.2f}, max={df[col].max():.2f}, min={df[col].min():.2f}"
                )
        else:
            report_lines.append("- No numeric columns available for summary statistics.")

        if len(numeric_cols) >= 2:
            corr = df[numeric_cols].corr().abs()
            corr = corr.mask(np.eye(len(corr), dtype=bool), 0)
            if not corr.empty and not corr.isna().all().all():
                max_corr = corr.max().max()
                if not pd.isna(max_corr):
                    loc = np.where(corr == max_corr)
                    if len(loc[0]) > 0:
                        a = corr.index[loc[0][0]]
                        b = corr.columns[loc[1][0]]
                        report_lines.append(f"- Strongest correlation: {a} vs {b} = {max_corr:.4f}")

        report_text = "\n".join(report_lines)

        st.markdown(
            f"""
            <div class="stat-card">
                <h4>Report Summary</h4>
                <p><b>Dataset:</b> {st.session_state.filename}</p>
                <p><b>Domain:</b> {domain}</p>
                <p><b>Rows:</b> {df.shape[0]}</p>
                <p><b>Columns:</b> {df.shape[1]}</p>
                <p><b>Data Integrity:</b> {integrity:.2f}%</p>
                <p>This summary is generated automatically from the available data.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button("Download Full Report", report_text, file_name="analysis_report.txt")

else:
    st.markdown(
        """
        <div style='margin-top: 80px; text-align: center; padding: 50px; border-radius: 22px; border: 1px dashed rgba(11,93,170,0.18); background: linear-gradient(135deg, #FFFFFF, #F4F8FC);'>
            <h1 style='color: #0B5DAA; font-size: 4.5rem; margin-bottom: 0.2rem;'>📥</h1>
            <h2 style='color: #223042;'>Awaiting Dataset Upload</h2>
            <p style='color: #7B8794;'>Please upload a CSV or Excel file from the sidebar to start the analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    f"<br><hr style='opacity: 0.12;'><p style='text-align: center; color: {TEXT_MUTED}; font-size: 0.85rem;'>Statistical Analysis Framework v2.1 | Professional Series</p>",
    unsafe_allow_html=True,
)
