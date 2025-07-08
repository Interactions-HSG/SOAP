import streamlit as st
import os
from PIL import Image
import base64

# Page configuration
st.set_page_config(
    page_title="Introduction - SOAP Workshop",
    page_icon="📖",
    layout="wide"
)

st.title("Measuring Systemic Risks: SOAP")
st.subheader("The System for Observing and Analyzing Posts")

# Add navigation helper
st.info("📚 This workshop demonstrates SOAP, a techno-legal tool for investigating systemic risks on VLOPs.")

# Introduction
st.markdown("""
The current landscape of data access for investigating systemic risks on Very Large Online Platforms (VLOPs) is fraught with challenges. Official data access mechanisms under the DSA sometimes are not sufficient, providing static and limited data that hinders comprehensive investigations. Alternative methodologies, such as data scraping and black-box testing, offer potential solutions but are constrained by significant legal and technical barriers.

To address these challenges, we developed the **System for Observing and Analyzing Posts (SOAP)** - a novel tool designed to collect and analyze data from VLOPs. SOAP is specifically aimed at studying systemic risks at scale through sock-puppet auditing. While measuring systemic risks fulfills an important societal need, it must be done in adherence to legal and ethical standards. We present SOAP as a **techno-legal tool for investigating systemic risks**.
""")

# Understanding Personalized Recommendation Systems
st.header("The Challenge: Personalized Content & Filter Bubbles")

st.markdown("""
### Highly Personalized Content Delivery
Feeds and content reaching users are highly personalized through sophisticated recommendation algorithms:
""")

# Display recommendation system pipeline
try:
    recsys_image = Image.open("data/recsys-pipeline.png")
    st.image(recsys_image, caption="Recommendation System Pipeline: How platforms personalize content delivery", use_container_width=True)
except FileNotFoundError:
    st.info("Recommendation system diagram not found at data/recsys-pipeline.png")

st.markdown("""
### Filter Bubbles and Loss of Shared Worlds
Users can live in so-called filter bubbles, leading to a loss of shared worlds:
""")

# Display filter bubble concept
try:
    bubble_image = Image.open("data/Simpson_bubble.webp")
    st.image(bubble_image, caption="Filter Bubbles: How personalized content creates isolated information environments", use_container_width=True)
except FileNotFoundError:
    st.info("Filter bubble illustration not found at data/Simpson_bubble.webp")

st.markdown("""
These personalized recommendation systems create unique "information diets" for each user, potentially leading to:
- **Echo chambers** where users only see content that confirms their existing beliefs
- **Political polarization** through algorithmic amplification of divisive content
- **Reduced exposure to diverse perspectives** and shared societal discourse
- **Systemic risks** to democratic processes and public discourse

Understanding and measuring these effects requires sophisticated auditing tools like SOAP.
""")

# SOAP Overview Section
st.header("SOAP Overview")

st.markdown("""
SOAP is a framework for auditing personalized recommender systems on VLOPs. It leverages configurable sock-puppet accounts to simulate user behavior, measure content exposure, and evaluate how recommendation systems contribute to systemic risks—such as filter bubbles, political radicalization, or harmful content amplification.

SOAP is based on two key innovations:

**1. Active Puppets**: These extend traditional sock-puppet methods by dynamically adapting their behavior during runtime. Puppets are guided by a "primer prompt," which defines their topical interest (e.g., climate change denial or election misinformation) and steers their actions accordingly.

**2. Multimodal LLM Integration**: SOAP integrates large language models to analyze diverse content across text, image, and audio modalities. This automates the deductive coding process while maintaining human oversight of classification quality.

Unlike systems that merely collect content snapshots, SOAP tracks the evolution of personalized feeds over time. This enables causal experimentation and longitudinal analysis of algorithmic behavior.
""")

# Real-world examples section
st.header("Real-World SOAP Applications")

st.markdown("""
SOAP has been successfully deployed to investigate systemic risks across multiple platforms and contexts:
""")

# Use case columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("🗳️ German Election Study")
    
    
    st.markdown("""
    **The TikTok Party**: Investigation of political content exposure during Germany's 2024 elections.
    
    **Key Findings**:
    - Platform algorithms systematically amplified certain political perspectives
    - Created distinct "information diets" for different user groups
    
    [📄 Read the full investigation](https://www.zeit.de/digital/2025-02/rechts-tiktok-bundestagswahl-soziale-medien-afd)
    """)

with col2:
    st.subheader("🐦 Elon Musk's Feed Analysis")
    
    st.markdown("""
    **Algorithmic Influence on High-Profile Users**: Analysis of how recommendation algorithms shape content exposure for influential figures.
    
    **Key Findings**:
    - Even prominent users are subject to algorithmic filtering
    - Platform recommendations can amplify specific viewpoints
    - Personal feeds become increasingly homogeneous over time
    
    [📄 Read the full analysis](https://www.nytimes.com/interactive/2025/05/15/business/elon-musk-x-twitter-feed-following-followers.html)
    """)

# How SOAP Works Section
st.header("How SOAP Works")

st.markdown("""
The SOAP workflow demonstrates how algorithmic recommendations evolve over time, creating increasingly homogeneous content feeds.

### 1. System Interaction Timeline
""")

# Display timeline image
try:
    timeline_image = Image.open("data/timeline_aviation_bubble.png")
    st.image(timeline_image, caption="SOAP system starts interacting with posts and tracking algorithmic responses", use_container_width=True)
except FileNotFoundError:
    st.info("Timeline visualization not found at data/timeline_aviation_bubble.png")

st.markdown("""
### 2. Filter Bubble Formation
""")

# Display filter bubble formation image
try:
    aviation_image = Image.open("data/Aviation_Filter_bubble.png")
    st.image(aviation_image, caption="Timeline of sockpuppet entering an aviation-focused filter bubble", use_container_width=True)
except FileNotFoundError:
    st.info("Aviation filter bubble visualization not found at data/Aviation_Filter_bubble.png")

st.markdown("""
### 3. Multi-Topic Capability
""")

# Display multiple filter bubbles image
try:
    bubbles_image = Image.open("data/Filter_bubbles_compressed.png")
    st.image(bubbles_image, caption="SOAP can investigate filter bubble formation across diverse topics", use_container_width=True)
except FileNotFoundError:
    st.info("Filter bubbles overview not found at data/Filter_bubbles_compressed.png")

# SOAP Technical Features
st.header("SOAP Technical Features")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 Automated Sock-puppet Management")
    st.markdown("""
    - **Profile Creation**: Diverse demographic and behavioral profiles
    - **Behavioral Simulation**: Authentic user interaction patterns
    - **Primer Prompts**: Topic-specific guidance for puppet behavior
    - **Scalable Deployment**: Multiple puppets operating simultaneously
    """)
    
    st.subheader("🔍 Multimodal Content Analysis")
    st.markdown("""
    - **Text Analysis**: Natural language processing and sentiment analysis
    - **Image Recognition**: Visual content classification and OCR
    - **Video Processing**: Scene understanding and object detection
    - **Audio Analysis**: Speech-to-text and emotional tone detection
    """)

with col2:
    st.subheader("📊 Data Collection & Storage")
    st.markdown("""
    - **Feed Logging**: Complete timeline of recommended content
    - **Interaction Tracking**: User actions and platform responses
    - **Metadata Capture**: Timestamps, engagement metrics, algorithmic signals
    - **Privacy Protection**: Anonymized data handling
    """)
    
    st.subheader("📈 Analysis & Validation")
    st.markdown("""
    - **Filter Bubble Detection**: Statistical measures of content homogeneity
    - **Reliability Testing**: Inter-rater and intra-rater validation
    - **Temporal Analysis**: Long-term trend identification
    - **Bias Quantification**: Systematic differences across user groups
    """)

# Workshop Transition
st.header("🎯 Workshop Structure")

st.markdown("""
This workshop provides hands-on experience with SOAP's core capabilities:

1. **Data Scraping** → Learn systematic data collection from platforms
2. **Deductive Coding** → Develop frameworks for content analysis using LLMs
3. **Analysis** → Apply statistical methods to detect systemic risks

By the end, you'll understand how to deploy SOAP for independent platform auditing and systemic risk assessment.
""")



# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("")

with col2:
    st.markdown("<div style='text-align: center;'>**Current: Introduction**</div>", unsafe_allow_html=True)

with col3:
    if st.button("Next: Data Scraping →"):
        st.switch_page("pages/2_Data_Scraping.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
Part of the FAccT 2025 Workshop: "Auditing Social Media Platforms using SOAP"<br>
University of St. Gallen | CoCoDa Project
</div>
""", unsafe_allow_html=True)
