import streamlit as st
import altair as alt
import pandas as pd
import plotly.graph_objects as go

COLUMN_LABELS = {
    "pl_rade": "Planet Radius (Earth radii)",
    "pl_bmasse": "Planet Mass (Earth masses)",
    "pl_orbper": "Orbital Period (log days)",
    "pl_eqt": "Equilibrium Temp (K)",
    "st_teff": "Stellar Effective Temp (log K)",
    "st_rad": "Stellar Radius (Solar radii)"
}

FEATURE_EXPLANATIONS = {
    "pl_rade":
        "Planet Radius (Earth radii) – Physical size of the exoplanet relative to Earth. Larger values typically indicate gas giants, while smaller values suggest rocky or terrestrial planets.",

    "pl_bmasse":
        "Planet Mass (Earth masses) – Estimated planetary mass relative to Earth. Higher masses often correspond to gas giants or ice giants.",

    "pl_orbper":
        "Orbital Period (days) – Time the planet takes to complete one orbit around its host star. Longer periods generally indicate wider orbits.",

    "pl_eqt":
        "Equilibrium Temperature (K) – Estimated surface temperature assuming thermal balance with the host star. Higher values generally indicate closer orbits.",

    "st_teff":
        "Stellar Effective Temperature (K) – Surface temperature of the host star. Hotter stars emit more radiation, influencing planetary environments.",

    "st_rad":
        "Stellar Radius (Solar radii) – Size of the host star relative to the Sun. Larger stars tend to host warmer planetary systems."
}

st.header("Welcome to the Exoplanet Extravaganza. A look at known exoplanets using KMeans.")

with st.expander("Project Overview"):
    st.markdown("""
This project explores whether known exoplanets can be grouped into meaningful categories 
    based on their physical and orbital properties.

Using publicly available NASA / Caltech data, I applied dimensionality reduction and 
    clustering techniques to visualize patterns across multiple planetary features. 
    The goal was not to build a predictive model, but to better understand how 
    different types of exoplanets relate to one another in feature space.
""")

with st.expander("PCA? What's that about?"):
    st.markdown("""
The chart below shows a 2D projection of exoplanets based on their key features 
         (like radius, mass, temperature, and stellar properties). 
         Each point represents a planet, and planets that are closer together in this chart 
         are more similar to each other.

To make the comparison easier, Principal Component Analysis (PCA) was used. 
         PCA reduces many features into two main dimensions while keeping as much of the 
         variation in the data as possible. Think of it as compressing multiple 
         planet properties into a 2D map.
                
PCA Component 1 captured Planet-Star System Scale and Energy. It increases when Host Stars 
                are hotter and larger, and the exoplanets are more massive and have higher temperatures

PCA Component 2 is primarily driven by orbital period, separating our short and long-orbit planets.                               

Colors represent clusters discovered by KMeans (an Unsupervised Clustering Algorithm). 
         Planets in the same cluster share similar characteristics across the features used. 
         This helps identify groups like small rocky planets vs large gas giants.
""")

st.write("Hover your mouse over a planet to see some more about it!")
# Load planet_df
planet_df = pd.read_csv("data/processed/planet_df.csv")

# Scatter plot of PCA coordinates colored by cluster
st.subheader("PCA Scatter Plot of Exoplanets by Cluster")
chart = alt.Chart(planet_df).mark_circle(size=80).encode(
    x=alt.X('pca1', title='PCA component 1 (58% variance explained)'),
    y=alt.Y('pca2', title='PCA component 2 (21% variance explained)'),
    color='cluster:N',
    tooltip=['pl_name', 'cluster', 'pl_rade', 'pl_bmasse', 'pl_eqt']
)
st.altair_chart(chart, use_container_width=True)

with st.expander("Radar Chart? Tell me more!"):
    st.markdown("""
Below is a Radar chart. It displays a planets key characteristics all at once.
    Each axis represents a different feature, such as planet size, mass, temperature, 
    or properties of the host star.

The farther a point extends from the center, the larger that feature is relative 
    to other known exoplanets.
            
How to read the values:
    All features have been scaled to a common range from 0 to 1 so that no single feature 
    dominates the chart.
    The chart shows relative comparisons, not raw data.

How to explore:
    Select different planets from the dropdown to see how their shapes change.
    Select "Compare selected planet to Earth?" to see how the planet you chose compares to Earth.                     
""")

# Radar chart
# Load the pre-scaled radar CSV
planet_radar = pd.read_csv("data/processed/planet_df_radar.csv")

st.subheader("Planet Feature Radar Chart")

# Dropdown to select planet
selected_planet = st.selectbox(
    "Select a planet to visualize:",
    planet_radar['pl_name'].unique()
)

# Checkbox to show Earth for comparison
compare_to_earth = st.checkbox("Compare selected planet to Earth?")

# Get the data for the selected planet
planet_data = planet_radar[planet_radar['pl_name'] == selected_planet].iloc[0]

# Prepare radar chart
features = list(COLUMN_LABELS.keys())
values = [planet_data[f] for f in features]

fig = go.Figure()

# Plot selected planet on radar
fig.add_trace(go.Scatterpolar(
    r=values,
    theta=[COLUMN_LABELS[f] for f in features],
    fill='toself',
    name=selected_planet
))

# If user wants to see a comparison of the selected planet to Earth, plot Earth on radar
if compare_to_earth:
    earth_values = [-0.146906, 0.058306, 0.228154, -0.032176, -0.295485, 0.712823]
    earth_values = [max(v, 0.02) for v in earth_values]
    fig.add_trace(go.Scatterpolar(
        r=earth_values,
        theta=[COLUMN_LABELS[f] for f in features],
        fill='none',
        mode='markers+lines',
        line=dict(color='black', dash='dash'),
        marker=dict(color='red', size=8),
        name='Earth'
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1])
    ),
    showlegend=True,
    margin=dict(t=50, b=50, l=50, r=50)
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    """Radar charts are useful for comparing multiple features
    simultaneously and spotting overall similarity patterns at a glance.""")

# Data Dictionary for users
with st.expander("See explanations for each feature"):
    for key, explanation in FEATURE_EXPLANATIONS.items():
        st.markdown(f"**{COLUMN_LABELS[key]} ({key})**: {explanation}")

with st.expander("*Preprocessing"):
    st.write("""
To reduce skew and scale differences, selected features 
    (planet radius, planet mass, orbital period, and stellar radius) 
    were first log-transformed. All features were then standardized (standard scalar) 
    prior to Kmeans analysis and rescaled using Min-Max normalization before radar visualization.
""")

st.header("Summary")
st.write("""
In this project, I applied PCA and K-Means clustering to explore structure within 
    exoplanet data after cleaning and scaling the features. While the clustering reveals 
    groupings among planets, the results also highlight how detection methods and 
    observational bias influence the data we have available (larger, hotter things are much easier 
    to see!).

Overall, this project helped reinforce my understanding of unsupervised learning and 
    the importance of interpreting results in context, rather than treating clusters as 
    definitive classifications.
         
I hope you enjoyed exploring this data as much as I did!         
""")


