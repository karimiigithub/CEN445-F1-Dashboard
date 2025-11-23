import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="F1 Performance Dashboard", layout="wide", page_icon="🏎️")

st.title("🏎️ Formula 1 Analysis & Prediction Dashboard")

st.markdown("""
This dashboard analyzes Formula 1 race results, driver performances, and track data.
**Students:** Yiğit Çetin, Ozan Dural, Seymen Bugay | **Course:** CEN445
""")

@st.cache_data
def load_and_prep_data():
    try:
        r_results = pd.read_csv('data/Race_Results.csv')
        drivers = pd.read_csv('data/Driver_Details.csv')
        teams = pd.read_csv('data/Team_Details.csv')
        schedule = pd.read_csv('data/Race_Schedule.csv')
        tracks = pd.read_csv('data/Track_Information.csv')

        for df in [r_results, drivers, teams, schedule, tracks]:
            df.columns = df.columns.str.lower().str.strip()

        race_key = 'raceid' if 'raceid' in r_results.columns else 'race_id'
        df = pd.merge(r_results, schedule, on=race_key, suffixes=('', '_sched'))

        driver_key = 'driverid' if 'driverid' in r_results.columns else 'driver_id'
        df = pd.merge(df, drivers, on=driver_key, suffixes=('', '_driver'))

        team_key = 'teamid' if 'teamid' in r_results.columns else 'constructorid'
        team_ref_key = 'teamid' if 'teamid' in teams.columns else 'constructorid'
        df = pd.merge(df, teams, left_on=team_key, right_on=team_ref_key, suffixes=('', '_team'))

        circuit_key = 'circuitid' if 'circuitid' in schedule.columns else 'circuit_id'
        track_ref_key = 'circuitid' if 'circuitid' in tracks.columns else 'circuit_id'
        df = pd.merge(df, tracks, left_on=circuit_key, right_on=track_ref_key, suffixes=('', '_track'))

        cols_to_numeric = ['points', 'grid', 'position']
        for col in cols_to_numeric:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        if 'surname' in df.columns:
            df['Driver Name'] = df['firstname'] + " " + df['surname'] if 'firstname' in df.columns else df['surname']
        else:
            df['Driver Name'] = df['driver']

        df['Team Name'] = df['name_team'] if 'name_team' in df.columns else df['name']

        return df

    except Exception as e:
        st.error(f"Data merging error: {e}")
        st.warning("Please ensure column names match the logic. Check the 'data' folder.")
        return pd.DataFrame()

df = load_and_prep_data()

if df.empty:
    st.stop()

st.sidebar.header("🔍 Filters")

years = sorted(df['year'].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Select Season", years, index=0)

season_df = df[df['year'] == selected_year]

teams_list = sorted(season_df['Team Name'].unique())
selected_teams = st.sidebar.multiselect("Filter Teams", teams_list, default=teams_list[:5])

if selected_teams:
    season_df = season_df[season_df['Team Name'].isin(selected_teams)]

tab1, tab2, tab3, tab4 = st.tabs(["🌍 Geography & Tracks", "🏎️ Driver Analysis", "🔧 Team Analysis", "🤖 AI (ML)"])

with tab1:
    st.subheader(f"{selected_year} Season Race Map")

    map_data = season_df.drop_duplicates(subset=['circuitid'])

    lat_col = 'lat' if 'lat' in map_data.columns else 'latitude'
    lng_col = 'lng' if 'lng' in map_data.columns else 'longitude'

    if lat_col in map_data.columns:
        fig_map = px.scatter_geo(map_data,
                                 lat=lat_col, lon=lng_col,
                                 hover_name="country",
                                 size="points",
                                 projection="natural earth",
                                 title="Global Race Locations",
                                 template="plotly_dark")
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Latitude/Longitude data not found.")

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        top_drivers = season_df.groupby('Driver Name')['points'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(top_drivers, x='Driver Name', y='points', color='points',
                         title="Top 10 Drivers of the Season", color_continuous_scale='Viridis')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_scatter = px.scatter(season_df, x='grid', y='position',
                                 color='Team Name', hover_data=['Driver Name'],
                                 title="Grid (Start) vs. Finishing Position Relationship",
                                 labels={'grid': 'Grid Position', 'position': 'Finishing Position'})
        fig_scatter.add_shape(type="line", x0=0, y0=0, x1=20, y1=20, line=dict(color="White", dash="dash"))
        st.plotly_chart(fig_scatter, use_container_width=True)

    season_df = season_df.sort_values(by='round')
    season_df['cumulative_points'] = season_df.groupby('Driver Name')['points'].cumsum()

    top_5_names = top_drivers['Driver Name'].head(5).tolist()
    filtered_line_df = season_df[season_df['Driver Name'].isin(top_5_names)]

    fig_line = px.line(filtered_line_df, x='round', y='cumulative_points', color='Driver Name',
                       title="Championship Race (Cumulative Points)", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with tab3:
    col3, col4 = st.columns(2)

    with col3:
        team_stats = season_df.groupby('Team Name')['points'].sum().reset_index()
        fig_tree = px.treemap(team_stats, path=['Team Name'], values='points',
                              title="Team Points Distribution (Treemap)", color='points')
        st.plotly_chart(fig_tree, use_container_width=True)

    with col4:
        winners = season_df[season_df['position'] == 1]
        win_counts = winners['Team Name'].value_counts().reset_index()
        win_counts.columns = ['Team Name', 'Win Count']

        fig_pie = px.pie(win_counts, values='Win Count', names='Team Name',
                         title="Distribution of Race Wins by Team", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    nat_col = 'nationality_team' if 'nationality_team' in season_df.columns else 'nationality'

    if nat_col in season_df.columns:
        fig_sun = px.sunburst(season_df, path=[nat_col, 'Team Name', 'Driver Name'],
                              title="Team and Driver Hierarchy (Sunburst)")
        st.plotly_chart(fig_sun, use_container_width=True)

with tab4:
    st.subheader("🤖 K-Means Clustering: Driver Performance Grouping")
    st.write("Grouping drivers based on their average 'Grid Position' and 'Points' using AI.")

    ml_data = df.groupby('Driver Name').agg({
        'points': 'mean',
        'grid': 'mean',
        'position': 'mean'
    }).reset_index()

    pilot_counts = df['Driver Name'].value_counts()
    active_pilots = pilot_counts[pilot_counts > 10].index
    ml_data = ml_data[ml_data['Driver Name'].isin(active_pilots)]

    ml_data = ml_data.dropna()

    if len(ml_data) > 3:
        kmeans = KMeans(n_clusters=3, random_state=42)
        ml_data['Cluster'] = kmeans.fit_predict(ml_data[['grid', 'points']])
        ml_data['Cluster'] = ml_data['Cluster'].astype(str)

        fig_ml = px.scatter(ml_data, x='grid', y='points', color='Cluster',
                            hover_name='Driver Name', size='points',
                            title="Driver Clusters (K-Means Result)",
                            labels={'grid': 'Avg Grid Position', 'points': 'Avg Points'})
        st.plotly_chart(fig_ml, use_container_width=True)

        st.info(
            "Clusters: Generally separates elite drivers (high points), mid-field contenders, and back-markers.")

        fig_box = px.box(ml_data, x='Cluster', y='position', color='Cluster',
                         title="Finishing Position Distribution by Cluster")
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.warning("Not enough data for clustering.")

st.markdown("---")
st.caption("Data Source: Kaggle Formula 1 Dataset | Project: Introduction to Data Visualization Assignment")