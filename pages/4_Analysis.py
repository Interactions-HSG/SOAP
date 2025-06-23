import streamlit as st
import os
from PIL import Image
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Analysis - SOAP Workshop",
    page_icon="📊",
    layout="wide"
)

st.title("4. Analysis & Interaction")
st.subheader("SOAP's interaction mechanisms and data analysis approach")

# Display SOAP system image
try:
    soap_image = Image.open("data/SOAP_system.png")
    st.image(soap_image, caption="SOAP System Architecture: Analysis and Interaction Components", use_container_width=True)
except FileNotFoundError:
    st.info("SOAP system diagram not found at data/SOAP_system.png")



# SOAP Interaction Mechanism
st.markdown("""
---
## SOAP Interaction Mechanism

After content collection and deductive coding, SOAP employs a **sophisticated interaction system** that operates within legal and ethical constraints while simulating authentic user behavior.

### Platform Restrictions and Legal Considerations

VLOPs implement numerous restrictions to prevent automated behavior, often extending beyond research concerns. SOAP navigates these challenges through careful design:

**Technical Challenges**:
- API limitations and rate limiting
- Account detection and flagging systems
- Platform countermeasures against automation
- Constant changes to platform configurations

**Legal Constraints**:
- **No commenting or content creation**: SOAP deliberately avoids actions that could violate platform terms
- **Passive interaction only**: Limited to viewing, liking, and saving content
- **Respect for intellectual property**: Careful handling of platform data and content
- **Privacy compliance**: Adherence to data protection regulations

**Research Justification**: 
Despite platform restrictions, SOAP's careful application remains crucial for academic research. The system uses libraries like Instagrapi and TikAPI in a deliberate and cautious manner, while some sockpuppet accounts may still be flagged or banned during operation despite ethical design standards.

### Interaction Pipeline

**Phase 3: Content Analysis**
- **Multimodal LLM Processing**: Gemini 1.5 Flash via Google Cloud Vertex AI analyzes each post
- **Relevance Rating**: Automatic scoring based on predefined primer prompts
- **Content Flagging**: Identification of posts matching target topics

**Phase 4: Interaction Execution**
- **Selective Engagement**: Interaction only with flagged relevant posts
- **Behavioral Simulation**: Actions include:
  - **Liking**: Primary engagement mechanism
  - **Viewing**: Extended viewing time for relevant content  
  - **Saving**: Bookmarking content of interest
- **Continuous Operation**: Process repeats for each feed reload until homogeneity threshold is reached

### Homogeneity Threshold

The system monitors **content homogeneity** defined as the ratio of posts matching the filter bubble topic to total posts. Once the feed becomes predominantly homogeneous (typically 75%+ relevant content), the filter bubble formation is considered successful.

**Example Thresholds Achieved**:
- **Aviation**: 75% homogeneity after ~100 posts (45 minutes)
- **Kittens**: 75% homogeneity after ~125 posts (60 minutes)  
- **Palestine/Israel**: 75% homogeneity after ~200 posts (1.5 hours)
""")


# Use Cases Section
st.markdown("""
## Auditing Systemic Risks Using SOAP
With its ability to analyze recommendation dynamics and simulate diverse user behaviors, SOAP allows researchers to explore systemic risks in detail. It addresses questions that remain challenging to tackle through existing data access methods under the DSA or conventional research APIs, offering a framework for studying the dissemination and amplification of systemic risks.

Building on existing methodologies for auditing systemic risks under the DSA, SOAP provides a framework for addressing key limitations in current approaches to measuring such risks. The following examples illustrate the tool's potential for empirical investigation:
""")

# Create columns for use cases
use_case_col1, use_case_col2 = st.columns(2)

with use_case_col1:
    st.markdown("""
    ### 🗳️ Electoral Processes & Political Content
    
    **German Federal Election Study (2025)**
    - Investigated content recommended to users expressing interest in the AfD party on TikTok
    - Measured political content exposure across different personas
    - Analyzed how platforms regulate or amplify political narratives
    
    *Research demonstrates SOAP's capability to study algorithmic influences on civic discourse and democratic processes.*
    """)
    
    st.markdown("""
    ### 🔍 Illegal Content Dissemination
    
    **Content Pathway Analysis**
    - Track how illegal content (hate speech, violence incitement) spreads through recommendation systems
    - Capture algorithmic amplification mechanisms
    - Measure exposure patterns in extremist filter bubbles
    
    *Addresses gaps where research APIs restrict access to flagged content.*
    """)

with use_case_col2:
    st.markdown("""
    ### 👶 Protection of Minors
    
    **Child Safety Auditing**
    - Simulate underage accounts to test platform protections
    - Verify compliance with DSA Article 28(2) (no personalized ads for minors)
    - Assess exposure to harmful content despite "Teen Safety" settings
    
    *Provides independent validation of platform safety claims.*
    """)
    
    st.markdown("""
    ### ⚖️ Fundamental Rights & Bias Detection
    
    **Algorithmic Fairness Assessment**
    - Examine biases in content moderation across demographics
    - Detect shadowbanning patterns with empirical evidence
    - Analyze differential content exposure by user characteristics
    
    *Offers evidence-based approach to validate user experiences of algorithmic discrimination.*
    """)

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("← Previous: Deductive Coding"):
        st.switch_page("pages/3_Deductive_Coding.py")

with col2:
    st.markdown("<div style='text-align: center;'>**Current: Analysis**</div>", unsafe_allow_html=True)

with col3:
    if st.button("Back to Home"):
        st.switch_page("app.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
Part of the FAccT 2025 Workshop: "Auditing Social Media Platforms using SOAP"<br>
University of St. Gallen | CoCoDa Project
</div>
""", unsafe_allow_html=True)
