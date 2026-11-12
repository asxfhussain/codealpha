from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Job Market Analyzer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #08080f; color: #e2e2ee; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 4rem; max-width: 1200px; }
.hero { text-align: center; padding: 3rem 0 2rem; }
.hero h1 {
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(135deg, #fff 30%, #60a5fa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -1.5px; margin-bottom: 0.5rem;
}
.hero p { color: #52526e; font-size: 1.05rem; }
.divider { border: none; border-top: 1px solid #16162a; margin: 2rem 0; }
.metric-card {
    background: #0f0f1a; border: 1px solid #1a1a30;
    border-radius: 16px; padding: 1.5rem; text-align: center;
}
.metric-value { font-size: 2rem; font-weight: 800; color: #60a5fa; }
.metric-label { font-size: 11px; font-weight: 600; letter-spacing: 2px;
    text-transform: uppercase; color: #3d3d5c; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# load data
df = pd.read_csv(Path(__file__).parent / 'Cleaned_DS_Jobs.csv')



# clean salary
df['avg_salary'] = pd.to_numeric(df['avg_salary'], errors='coerce')
df = df.dropna(subset=['avg_salary'])

df['job_state'] = df['job_state'].str.strip()

state_names = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'Washington DC'
}



df['state_name'] = df['job_state'].map(state_names).fillna(df['job_state'])

# sidebar filter
st.sidebar.header("Filters")
roles = ['All'] + sorted(df['job_simp'].dropna().unique().tolist())
selected_role = st.sidebar.selectbox("Job Role", roles)

states = ['All'] + sorted(df['state_name'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("State", states)

if selected_role != 'All':
    df = df[df['job_simp'] == selected_role]
if selected_state != 'All':
    df = df[df['state_name'] == selected_state]

# hero
st.markdown("""
<div class="hero">
    <h1>Job Market Analyzer</h1>
    <p>Explore data science job trends, salaries, and in-demand skills.</p>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Job Postings</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${df["avg_salary"].mean():.0f}k</div><div class="metric-label">Avg Salary</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{df["job_state"].nunique()}</div><div class="metric-label">States Hiring</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{df["Company Name"].nunique()}</div><div class="metric-label">Companies</div></div>', unsafe_allow_html=True)


st.markdown('<hr class="divider">', unsafe_allow_html=True)

# skills demand
st.subheader("Most In-Demand Skills")
skills = ['python', 'excel', 'hadoop', 'spark', 'aws', 'tableau', 'big_data']
skill_counts = df[skills].sum().sort_values(ascending=True).reset_index()
skill_counts.columns = ['skill', 'count']
fig1 = px.bar(skill_counts, x='count', y='skill', orientation='h',
              color='count', color_continuous_scale='Blues',
              template='plotly_dark')
fig1.update_layout(paper_bgcolor='#0f0f1a', plot_bgcolor='#0f0f1a', showlegend=False, coloraxis_showscale=False)
st.plotly_chart(fig1, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# salary by role
st.subheader("Average Salary by Job Role")
salary_role = df.groupby('job_simp')['avg_salary'].mean().sort_values(ascending=False).reset_index()
salary_role.columns = ['role', 'avg_salary']
fig2 = px.bar(salary_role, x='role', y='avg_salary',
              color='avg_salary', color_continuous_scale='Blues',
              template='plotly_dark')
fig2.update_layout(paper_bgcolor='#0f0f1a', plot_bgcolor='#0f0f1a', showlegend=False, coloraxis_showscale=False)
st.plotly_chart(fig2, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# top states
st.subheader("Top Hiring States")
top_states = df['state_name'].value_counts().head(10).reset_index()
top_states.columns = ['state', 'count']
fig3 = px.bar(top_states, x='state', y='count',
              color='count', color_continuous_scale='Blues',
              template='plotly_dark')
fig3.update_layout(paper_bgcolor='#0f0f1a', plot_bgcolor='#0f0f1a', showlegend=False, coloraxis_showscale=False)
st.plotly_chart(fig3, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# salary distribution
st.subheader("Salary Distribution")
fig4 = px.histogram(df, x='avg_salary', nbins=30,
                    color_discrete_sequence=['#60a5fa'],
                    template='plotly_dark')
fig4.update_layout(paper_bgcolor='#0f0f1a', plot_bgcolor='#0f0f1a')
st.plotly_chart(fig4, use_container_width=True)    

