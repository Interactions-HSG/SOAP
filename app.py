import streamlit as st
import os
from PIL import Image
from database.poll_responses.session_management import initialize_session

# Initialize user session - this creates or retrieves a unique user ID
user_id = initialize_session()

# Page configuration
st.set_page_config(
    page_title="Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display centered CPDP logo at the top
if os.path.exists("data/cpdp2025-long.svg"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("data/cpdp2025-long.svg", width=600)

# Display university logos in a row
col1, col2, col3 = st.columns(3)
with col1:
    if os.path.exists("data/Logo_Université_de_Lausanne.png"):
        st.image("data/Logo_Université_de_Lausanne.png", width=200)
with col2:
    if os.path.exists("data/HSG_Logo_EN_RGB.svg.png"):
        st.image("data/HSG_Logo_EN_RGB.svg.png", width=200)
with col3:
    if os.path.exists("data/Maastricht_University_logo.svg.png"):
        st.image("data/Maastricht_University_logo.svg.png", width=200)

# Main title and introduction
st.title("Auditing Social Media Platforms Workshop")
st.subheader("Public, Non-Public, and Alternative Data Access Methods under the DSA & GDPR")

# Description
st.markdown("""
## Workshop Overview

This 80-minute workshop guides participants through auditing social media platforms using both 
official DSA-compliant methods and alternative data access techniques. Our CoCoDa project 
focuses on opening up the concentration and control of data by VLOPs and VLOSEs.

### Use Case: 
*Examining how political content is amplified and moderated on social media platforms during election periods.*

This interactive application provides tools and demonstrations for each phase of the workshop.
""")

# Presenters section - moved up and styled artistically
st.markdown("""
<div style="padding: 20px 0; text-align: center;">
    <div style="height: 2px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(0,0,120,0.75), rgba(255,255,255,0)); margin: 20px 0;"></div>
    <h2 style="text-align: center; font-family: 'Georgia', serif;">Workshop Presenters</h2>
    <div style="height: 2px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(120,0,0,0.75), rgba(255,255,255,0)); margin: 20px 0;"></div>
</div>
""", unsafe_allow_html=True)

# Display presenters with photos in 2 rows of 2 columns with equal sizing
col1, col2 = st.columns(2)

image_height = 200  # Fixed height for all images

with col1:
    with st.container():
        st.subheader("Contact Person")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            if os.path.exists("data/aurelia.jpg"):
                st.image("data/aurelia.jpg", width=image_height)
        with col_info:
            st.markdown("**Prof. Dr. Aurelia Tamo-Larrieux**")
            st.markdown("University of Lausanne (Switzerland)")
            st.markdown("Email: aurelia.tamo-larrieux@unil.ch")

with col2:
    with st.container():
        st.subheader("Facilitator")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            if os.path.exists("data/Konrad.jpeg"):
                st.image("data/Konrad.jpeg", width=image_height)
        with col_info:
            st.markdown("**Prof. Dr. Konrad Kollnig**")
            st.markdown("Maastricht University (Netherlands)")

col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.subheader("Host")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            if os.path.exists("data/Luka.jpg"):
                st.image("data/Luka.jpg", width=image_height)
        with col_info:
            st.markdown("**Luka Bekavac**")
            st.markdown("University of St. Gallen (Switzerland)")

with col4:
    with st.container():
        st.subheader("Facilitator")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            if os.path.exists("data/Simon.png"):
                st.image("data/Simon.png", width=image_height)
        with col_info:
            st.markdown("**Prof. Dr. Simon Mayer**")
            st.markdown("University of St. Gallen (Switzerland)")

# Add a Picasso-inspired decorative element
st.markdown("""
<div style="padding: 10px 0; margin: 20px 0; text-align: center;">
    <div style="height: 3px; background: linear-gradient(90deg, rgba(0,0,255,0.5), rgba(255,0,0,0.5), rgba(0,255,0,0.5), rgba(255,255,0,0.5)); margin: 10px 0;"></div>
    <div style="height: 2px; background: linear-gradient(90deg, rgba(255,0,0,0.5), rgba(0,0,255,0.5), rgba(255,255,0,0.5), rgba(0,255,0,0.5)); margin: 8px 0;"></div>
</div>
""", unsafe_allow_html=True)

# Link to CoCoDa project
st.markdown("""
## CoCoDa Project
Our work is part of the [CoCoDa project](https://snsf-cocoda.github.io/), which builds tools to open up 
the concentration and control of data by VLOPs and VLOSEs.
""")

# Workshop structure with links to subpages
st.header("Workshop Structure")

# Display the workshop sections with links
workshop_sections = {
    "1. Introduction": {
        "description": "Set the scene: systemic risk, DSA/GDPR goals, the election use case",
        "time": "10 min",
        "link": "Introduction"
    },
    "2. DSA Tools": {
        "description": "Explore data from DSA Ads Repository, Transparency DB, and Research API",
        "time": "20 min",
        "link": "Dsa_Tools"
    },
    "3. GDPR Tools": {
        "description": "Leveraging Data Rights for Research through data donation methods",
        "time": "10 min",
        "link": "GDPR_Tools"
    },
    "4. SOAP and Scraping": {
        "description": "Systematic Observation of Algorithms and Platforms through sockpuppets and scraping",
        "time": "20 min",
        "link": "SOAP_and_Scraping"
    },
    "5. Legal Uncertainties": {
        "description": "Navigating legal tensions in platform auditing research",
        "time": "15 min",
        "link": "Legal_Uncertainties"
    },
    "6. Conclusion": {
        "description": "Reflections, trade-offs and next steps",
        "time": "5 min",
        "link": "Conclusion"
    }
}

# Display the workshop structure as cards
col1, col2 = st.columns(2)
for i, (section, details) in enumerate(workshop_sections.items()):
    # Alternate between columns
    with col1 if i % 2 == 0 else col2:
        with st.container():
            st.subheader(section)
            st.markdown(f"**Time**: {details['time']}")
            st.markdown(f"**Description**: {details['description']}")
            # Create a button that would typically link to the subpage
            # In Streamlit, we don't need explicit links as the pages are in the sidebar automatically
            st.markdown(f"[Go to section →]({details['link']})")
            st.divider()

# Brief explanation of the navigation
st.info("👈 You can also use the sidebar to navigate between workshop sections.")

# Footer with information about the data sources
st.markdown("---")
st.markdown("### Data Sources")
st.markdown("""
This workshop uses both real and simulated data to demonstrate auditing techniques:
- Sample data from TikTok and other platforms
- Simulated DSA transparency database entries
- Mock API responses based on real platform behaviors
- SOAP (Sock Puppet Auditing Protocol) demonstration results
""")