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
    
    The TikTok Ad Library is a real example of a DSA-compliant ad repository that researchers can use.
    """)
    
    # Add TikTok Ad Library link with screenshot
    st.subheader("TikTok Ad Library")
    
    st.markdown("""
    The TikTok Ad Library allows you to search for ads, view targeting parameters, and explore advertiser information.
    
    **[Open TikTok Ad Library in a New Tab](https://library.tiktok.com/ads)** 👈 Click here to explore the actual repository
    """)
    
    # Display an image of the TikTok Ad Library instead of embedding it
    st.markdown("### Screenshot of TikTok Ad Library")
    
    # Check if we have a screenshot image in the data folder, if not display a placeholder
    tiktok_screenshot_path = os.path.join("data", "tiktok_ad_library.png")
    if os.path.exists(tiktok_screenshot_path):
        image = Image.open(tiktok_screenshot_path)
        st.image(image, caption="TikTok Ad Library Interface", use_container_width=True)
    else:
        st.info("""
        **TikTok Ad Library Screenshot**
        
        A screenshot would normally appear here showing the TikTok Ad Library interface. 
        
        You can visit https://library.tiktok.com/ads to explore the actual repository.
        """)
    
    # Add information about limitations
    st.markdown("""
    ### Key Limitations of Ad Repositories
    
    **Notable omissions in the ad repositories include:**
    
    - **No ephemeral data:** Stories and temporary ads are not consistently archived
    - **Influencer promotions:** Paid partnerships and influencer marketing often fall outside the scope
    - **Native advertising:** Content that resembles organic posts but is sponsored may be underrepresented
    
    These gaps highlight the need for complementary research methods to fully understand the advertising ecosystem on platforms.
    """)
    
    st.markdown("""
    ### How to Use the Ad Library
    
    1. Use the search bar to find specific advertisers or ad content topics
    2. Apply filters for date ranges, countries, and ad types
    3. Click on individual ads to see details about targeting parameters and reach
    4. Use the "Download" feature to export data for offline analysis
    
    ### Key Research Applications
    
    - Monitoring political ad spending during election periods
    - Analyzing targeting strategies by different political actors
    - Comparing ad messaging across different demographic targets
    - Tracking issue-based advocacy campaigns
    """)
    
    st.markdown("""
    ### Workshop Exercise: Exploring Political Ads
    
    For this workshop, try the following exercise:
    
    1. Visit the [TikTok Ad Library](https://library.tiktok.com/ads)
    2. Search for terms like "election," "vote," "democracy," or "politics"
    3. Filter for ads in your country or region
    4. Examine the targeting parameters of political advertisements
    5. Note what information is available and what seems to be missing
    
    ### Limitations of Ads Repository Data
    
    While valuable, ad repository data has several limitations:
    
    - Limited historical data (usually 1-2 years)
    - Inconsistent reporting formats across platforms
    - No interaction data (likes, comments, shares)
    - No information about organic content recommendations
    - Limited details on actual audience reached vs targeting parameters
    - No access to ad performance metrics like click-through rates
    - Limited ability to observe personalization effects
    """)

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
    
    # Display an image or placeholder for the Transparency Database
    st.markdown("### Screenshot of DSA Transparency Database")
    
    # Check if we have a screenshot image in the data folder, if not display a placeholder
    transparency_screenshot_path = os.path.join("data", "dsa_transparency_database.png")
    if os.path.exists(transparency_screenshot_path):
        image = Image.open(transparency_screenshot_path)
        st.image(image, caption="DSA Transparency Database Interface", use_container_width=True)
    else:
        st.info("""
        **DSA Transparency Database Screenshot**
        
        A screenshot would normally appear here showing the DSA Transparency Database interface.
        
        You can visit https://transparency.dsa.ec.europa.eu/statement to explore the actual repository.
        """)
    
    # Add information about the tradeoffs
    st.markdown("""
    ### Public Accessibility vs. Complete Information
    
    The Transparency Database represents a tradeoff between:
    - Making information publicly available and easy to access
    - Providing complete technical details on platform operations
    
    While the public database gives a high-level overview, researchers can request more detailed non-public data under Article 40(4) of the DSA to hold platforms accountable and verify their compliance claims.
    
    ### Workshop Exercise: Exploring Platform Transparency Statements
    
    For this workshop, try the following exercise:
    
    1. Visit the [DSA Transparency Database](https://transparency.dsa.ec.europa.eu/statement)
    2. Browse statements from different platforms (TikTok, Facebook, X/Twitter, etc.)
    3. Compare how different platforms disclose their content moderation practices
    4. Note what information is consistently provided and what varies between platforms
    """)
    
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
    
    st.markdown("""
    The TikTok Research API provides structured data access for qualified academic researchers.
    
    **[Open TikTok Research API Documentation in a New Tab](https://developers.tiktok.com/products/research-api/)** 👈 Click here to explore the actual API documentation
    """)

    # Add DSA40 Data Access Tracker
    st.subheader("DSA40 Data Access Tracker")
    
    st.markdown("""
    The **[DSA40 Data Access Tracker](https://www.soscisurvey.de/DSA40applications/)** is an initiative by the #DSA40 Data Access Collaboratory, 
    a joint project of the European New School in Frankfurt/Oder and the Weizenbaum Institute in Berlin.
    
    It is meant to inform the scientific community about the developments regarding the platform data access of researchers under Article 40 of the DSA.
    
    👉 **[Access the DSA40 Data Access Tracker](https://www.soscisurvey.de/DSA40applications/)**
    """)
    
    # Display an image or placeholder for the Research API
    st.markdown("### Screenshot of TikTok Research API Documentation")
    
    # Check if we have a screenshot image in the data folder, if not display a placeholder
    api_screenshot_path = os.path.join("data", "tiktok_research_api.png")
    if os.path.exists(api_screenshot_path):
        image = Image.open(api_screenshot_path)
        st.image(image, caption="TikTok Research API Documentation", use_container_width=True)
    else:
        st.info("""
        **TikTok Research API Screenshot**
        
        A screenshot would normally appear here showing the TikTok Research API documentation.
        
        You can visit https://developers.tiktok.com/products/research-api/ to explore the actual API documentation.
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
    
    ### Access Timeline
    
    From our experience, the access granting process typically takes:
    - 2-4 weeks for...
    """)

    # Create tabs for data limitations and VDE
    st.markdown("## Data Access Limitations")
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