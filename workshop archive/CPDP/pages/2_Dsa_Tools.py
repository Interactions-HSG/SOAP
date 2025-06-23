import base64
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import numpy as np
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from PIL import Image
from database.poll_responses.session_management import initialize_session, save_poll_response, get_response_for_poll

# Initialize user session
user_id = initialize_session()

st.set_page_config(
    page_title="DSA Tools | Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide"
)

st.title("2. Tool Walkthrough (Official DSA Tools)")
st.subheader("Exploring DSA-compliant data access methods")

# Introduction to the section
st.markdown("""
In this section, we'll examine the official data access methods provided under the Digital Services Act (DSA),
including:

1. **DSA Ads Repository** - Public archive of political and issue-based advertisements
2. **DSA Transparency Database** - Platform disclosures on content moderation and risk assessments
3. **Research API** - Data access for vetted researchers under Article 40
""")

# Create tabs for the different tools
tab1, tab2, tab3 = st.tabs(["Ads Repository", "Transparency DB", "Research API"])

# Tab 1: Ads Repository
with tab1:
    st.header("DSA Ads Repository")
    
    st.markdown("""
    ### What is the DSA Ads Repository?
    
    Under Article 39 of the DSA, very large online platforms (VLOPs) must maintain repositories
    of all advertisements displayed on their platforms, including:
    
    - Content of the advertisement
    - Advertiser identity
    - Period of display
    - Targeting parameters used
    - Total number of recipients reached
    
    The TikTok Ad Library is an example of a DSA ad repository that researchers can use.
    """)
    
    # Add TikTok Ad Library link with screenshot
    st.subheader("TikTok Ad Library")
    
    st.markdown("""
    The TikTok Ad Library allows you to search for ads, view targeting parameters, and explore advertiser information.
    
    **[Open TikTok Ad Library in a New Tab](https://library.tiktok.com/ads)** 👈 Click here to explore the actual repository
    """)
    
    # Embed Airtable with list of ad repositories
    st.subheader("Comprehensive List of Ad Repositories")
    
    st.markdown("""
    Below is a curated database of all available ad repositories from major platforms. You can explore the features, 
    access requirements, and compare the data available from each platform.
    """)
    
    # Embed the Airtable
    st.components.v1.html("""
    <iframe class="airtable-embed" src="https://airtable.com/embed/appnk1UgP5Kojk2iv/shrG0v9iROVmAj8rR/tblQ1o24x5wvWryM6?viewControls=on" 
    frameborder="0" onmousewheel="" width="100%" height="533" style="background: transparent; border: 1px solid #ccc;"></iframe>
    """, height=550)
    
    # Add information about limitations
    st.markdown("""
    ### Key Limitations of Ad Repositories
    
    **Notable omissions in the ad repositories include:**
    
    - **No ephemeral data:** Stories and temporary ads are not consistently archived
    - **Influencer promotions:** Paid partnerships and influencer marketing often fall outside the scope
    - **Native advertising:** Content that resembles organic posts but is sponsored may be underrepresented
    
    These gaps highlight the need for complementary research methods to fully understand the advertising ecosystem on platforms.
    """)

    
    # Add TikTok DSA breach disclaimer box
    st.markdown("""
    <div style='background-color: #ffe8e8; border-left: 5px solid #ff6b6b; padding: 20px; border-radius: 5px; margin-bottom: 20px;'>
        <h4 style='color: #d32f2f; margin-top: 0;'>⚠️ European Commission finds TikTok's ad repository in breach of the Digital Services Act</h4>
        <p><strong>What's missing from TikTok's repository:</strong></p>
        <ul>
            <li>👉🏼 Info about ads content</li>
            <li>👉🏼 Targeted users</li>
            <li>👉🏼 Ads investors (who paid for the commercial content)</li>
            <li>👉🏼 A function that allows the public to search comprehensively for advertisement</li>
        </ul>
        <p><em>May 2025: The Commission has found TikTok's ad repository does not meet DSA requirements for transparency and data access.</em></p>
        <p><a href="https://digital-strategy.ec.europa.eu/en/news/commission-preliminarily-finds-tiktoks-ad-repository-breach-digital-services-act" target="_blank">Read the official Commission announcement</a></p>
    </div>
    """, unsafe_allow_html=True)

    

# Tab 2: Transparency Database
with tab2:
    st.header("DSA Transparency Database")
    
    st.markdown("""
    ### What is the DSA Transparency Database?
    
    The DSA requires VLOPs to publish transparency reports and risk assessments.
    This database includes:
    
    - Content moderation statistics
    - Risk assessment documentation
    - Platform policies and their application
    - Information on recommender systems
    
    You can access the actual DSA Transparency Database to see real compliance statements from platforms.
    """)
    
    # Add DSA Transparency Database link
    st.subheader("Official DSA Transparency Database")
    
    st.markdown("""
    The European Commission maintains an official repository of transparency statements from designated platforms.
    
    **[Open DSA Transparency Database in a New Tab](https://transparency.dsa.ec.europa.eu/statement)** 👈 Click here to explore the actual repository
    """)
    
   
    # Add information about the tradeoffs
    st.markdown("""
    ### Public Accessibility vs. Complete Information
    
    The Transparency Database represents a tradeoff between:
    - Making information publicly available and easy to access
    - Providing complete technical details on platform operations
    
    While the public database gives a high-level overview, researchers can request more detailed non-public data under Article 40(4) of the DSA to hold platforms accountable and verify their compliance claims.
    """)
    
    # Create information boxes for key insights about the Transparency Database
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: #f0f7fb; border-left: 5px solid #2196F3; padding: 20px; border-radius: 5px; margin-bottom: 20px;'>
            <h4 style='color: #0d47a1; margin-top: 0;'>Academic Analysis: Kaushal et al.</h4>
            <p>Research reveals that despite transparency gains, compliance remains problematic:</p>
            <ul>
                <li>99.8% of removals are based on Terms of Service rather than illegal content (0.2%)</li>
                <li>Appeals status for content moderation decisions is not reported</li>
                <li>Lack of standardization makes extracting meaningful insights difficult</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style='background-color: #fff8e1; border-left: 5px solid #ffc107; padding: 20px; border-radius: 5px; margin-bottom: 20px;'>
            <h4 style='color: #ff6f00; margin-top: 0;'>Key Findings: Trujillo et al.</h4>
            <p>Critical shortcomings identified include:</p>
            <ul>
                <li>Platforms adhere only partially to the database's intended structure</li>
                <li>Database structure is inadequate for platforms' reporting needs</li>
                <li>Substantial differences exist in moderation actions across platforms</li>
                <li>Significant fraction of data is inconsistent</li>
                <li>Platform X presents the most inconsistencies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Full-width box for strategic approach
    st.markdown("""
    <div style='background-color: #e8f5e9; border-left: 5px solid #4caf50; padding: 20px; border-radius: 5px; margin-bottom: 20px;'>
        <h4 style='color: #2e7d32; margin-top: 0;'>Strategic Approach: Leveraging Transparency Tools</h4>
        <p><strong>Demonstration of necessity for data access requests:</strong></p>
        <p>You can leverage all available transparency tools (ad-targeting databases, content moderation databases) to hold platforms accountable as part of data access requests under Article 40(4).</p>
        <p><strong>Example Application:</strong> Animal rights researchers could log all entries related to "Animal Welfare" from eBay on the DSA Transparency database and subsequently hold the platform accountable to providing the exact amount of data they reported (e.g., 4,205 posts).</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add Terms and Conditions Database box
    st.markdown("""
    <div style='background-color: #e3f2fd; border-left: 5px solid #1976d2; padding: 20px; border-radius: 5px; margin-bottom: 20px;'>
        <h4 style='color: #1565c0; margin-top: 0;'>DSA Terms and Conditions Database</h4>
        <p>The European Commission now hosts a GitLab repository with a database of platform Terms and Conditions.</p>
        <p><strong><a href="https://code.europa.eu/dsa/terms-and-conditions-database/vlops-and-vloses/vlop-vlose-versions" target="_blank">Access the Terms and Conditions Database</a></strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different types of transparency information with mock examples
    
# Tab 3: Research API
with tab3:
    st.header("DSA Research API")
    
    st.markdown("""
    ### What is the Research API?
    
    Article 40 of the DSA requires VLOPs to provide data access to vetted researchers investigating systemic risks.
    This API provides structured access to:
    
    - Content data (posts, videos, comments)
    - Interaction data (likes, shares)
    - Recommendation data (what content was shown to whom)
    
    TikTok has implemented a Research API that provides access to platform data for qualified researchers.
    """)
    
    # Add TikTok Research API link
    st.subheader("TikTok Research API")
    

    # Add DSA40 Data Access Tracker
    st.subheader("DSA40 Data Access Tracker")
    
    st.markdown("""
    The **[DSA40 Data Access Tracker](https://www.soscisurvey.de/DSA40applications/)** is an initiative by the #DSA40 Data Access Collaboratory, 
    a joint project of the European New School in Frankfurt/Oder and the Weizenbaum Institute in Berlin.
    
    It is meant to inform the scientific community about the developments regarding the platform data access of researchers under Article 40 of the DSA.
    
    👉 **[Access the DSA40 Data Access Tracker](https://www.soscisurvey.de/DSA40applications/)**
    """)
    
    
    st.markdown("""
    ### Requirements for API Access
    
    To access the TikTok Research API, researchers must:
    
    1. Be affiliated with an academic institution or research organization
    2. Have a clear research proposal focused on understanding systemic risks
    3. Apply through TikTok's researcher verification process
    4. Comply with data security and privacy requirements
    5. Agree to the API terms of service
    
    **Recent Changes:** Ethics committee approval is no longer required for the application process.
    """)
    
    # Add VLOP-vetting-process image
    vetting_process_path = os.path.join("data", "VLOP-vetting-process.jpg")
    if os.path.exists(vetting_process_path):
        st.image(vetting_process_path, width=800, caption="VLOP vetting process for researcher access under Article 40 DSA (Source: Democracy Reporting International, 2024)")
        st.markdown("""
        <small>Source: <a href="https://digitalmonitor.democracy-reporting.org/data-access/#section2-tab1" target="_blank">Digital Monitor by Democracy Reporting International (2024)</a></small>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Access Timeline
    
    From our experience, the access granting process typically takes:
    - 2-4 weeks for...
    """)

    # Create tabs for data limitations and VDE
    st.markdown("## Data Access Limitations")
    st.subheader("TikTok Research API")
    st.markdown("[Comparison of TikTok Research API with other data access methods](https://github.com/mrtn3000/tiktok-audit/tree/main/Data%20Access)")
    api_limitations_tab1, api_limitations_tab2 = st.tabs(["Platform-specific Limitations", "Virtual Data Enclaves (VDE)"])
    
    with api_limitations_tab1:
        st.subheader("Platform-specific Data Limitations")
        
        st.markdown("""
        ### TikTok Limitations
        - **No data for users under the age of 18**
        - No ephemeral content (stories, expired content)
        - Limited historical data range
        - Aggregated engagement metrics in many cases
        
        ### Meta (Facebook/Instagram) Limitations
        - **No data for users with fewer than 25,000 followers or 1,000 followers** (depending on content type)
        - No ephemeral data (stories, expired content)
        - Limited breakdown of algorithmic recommendation factors
        - Restricted access to certain engagement signals
        
        ### Common Limitations Across Platforms
        - Sampling methods not fully transparent
        - Limited visibility into content moderation processes
        - Restricted data granularity for sensitive topics
        - Significant technical barriers to working with the data
        """)
        
        # Add VLOP-provided-data image
        vlop_data_path = os.path.join("data", "VLOP-provided-data.jpg")
        if os.path.exists(vlop_data_path):
            st.image(vlop_data_path, width=800, caption="Types of data provided by VLOPs under Article 40 DSA (Source: Democracy Reporting International, 2024)")
            st.markdown("""
            <small>Source: <a href="https://digitalmonitor.democracy-reporting.org/data-access/#section2-tab1" target="_blank">Digital Monitor by Democracy Reporting International (2024)</a></small>
            """, unsafe_allow_html=True)
    
    with api_limitations_tab2:
        st.subheader("Virtual Data Enclaves (VDE)")
        
        st.markdown("""
        ### Highly Restrictive Environment
        
        Many platforms provide access through Virtual Data Enclaves (VDEs), which impose significant restrictions:
        
        - Data cannot leave the platform's controlled environment
        - Limited computational resources
        - Pre-approved analysis tools only
        - Output review processes before exporting results
        - No raw data exports allowed
        - Monitored usage and activity logs
        
        ### Example Workflow in a VDE
        
        1. **Preparation**: Develop and test code outside VDE with synthetic data
        2. **Access**: Log into the highly secured environment
        3. **Analysis**: Run approved analyses on the platform's data
        4. **Review**: Submit results for platform review
        5. **Export**: Receive approved aggregated results and visualizations
        6. **Publication**: Cite data according to platform requirements
        
        This restrictive approach significantly limits research flexibility and increases the time required for analysis.
        """)
       
    # Limitations section
    st.markdown("""
    ### Limitations of Research API Access
    
    Research API access under the DSA has significant limitations:
    
    - Lengthy vetting process for researchers
    - Restricted to officially recognized research institutions
    - Limited historical data access
    - Aggregation that may obscure important patterns
    - Rate limits and query constraints
    - No ability to study algorithm behavior dynamically
    """)

# Navigation buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    prev_button = st.button("← Previous: Introduction")
    if prev_button:
        st.switch_page("pages/1_Introduction.py")

with col2:
    next_button = st.button("Next: Challenges & Discussion →")
    if next_button:
        st.switch_page("pages/3_GDPR_Tools.py")