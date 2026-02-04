import streamlit as st

st.set_page_config(
    page_title="Caleb Combs | Data Science Portfolio",
    page_icon="📊",
    layout="wide"
)

# about
st.title("Hi, I'm Caleb")
st.subheader("Data Science & Machine Learning Student")

st.write(
    """
    I'm a student interested in data science, machine learning, and scientific data analysis.
    This portfolio highlights projects I've worked on using real-world datasets, 
    with a focus on learning, exploration, and clear communication.

    This portfolio is part of my learning journey and will grow as I complete more projects.
    """
)
st.markdown("---")

with st.expander("Project List"):
    with st.expander("Exoplanet Extravaganza!"):
        st.markdown("""
    ### Exoplanet Extravaganza!
**Goal:**  
Explore worlds far beyond our own.

**Key Concepts:**
- KMeans clustering analysis
- Feature exploration
- Dimensionality reduction using PCA for visualization
- Public TAP API data ingestions (NASA Exoplanet Archive)

**Tools Used:**
- Python
- Pandas & NumPy
- Scikit-Learn
- Matplotlib / Seaborn
- Plotly

""")
 
st.markdown("---")
st.header("Connect with me:")

st.markdown(
    """
    - **GitHub:** https://github.com/caparcom
    - **LinkedIn:** https://www.linkedin.com/in/calebcombscaparcom/
    - **Email:** caleb_combs@yahoo.com
    """
)

