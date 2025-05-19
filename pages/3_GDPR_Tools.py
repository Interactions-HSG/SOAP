import streamlit as st
import os
from PIL import Image
from database.poll_responses.session_management import initialize_session, save_poll_response, get_response_for_poll

# Initialize user session
user_id = initialize_session()

st.set_page_config(
    page_title="GDPR Tools | Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide"
)

st.title("3. GDPR Tools")
st.subheader("Leveraging Data Rights for Research")

# Introduction to GDPR Tools
st.markdown("""
While the DSA provides new data access mechanisms, the General Data Protection Regulation (GDPR) 
has been providing individuals with data rights since 2018. These rights can be leveraged 
for research purposes through structured data donation approaches.

In this section, we'll explore how researchers can use GDPR data rights to conduct platform audits
and the initiatives that facilitate this research approach.
""")

# Data Donation Methods
st.header("Data Donation Methods")

st.markdown("""
### What is Data Donation?

Data donation is a process where individuals exercise their right to access their personal data 
from platforms (under GDPR Article 15) and donate this data to research initiatives. This approach:

- Provides authentic user experiences rather than platform-curated data
- Captures personalization aspects that are often missing from official APIs
- Allows for a broader range of research questions
- Empowers users to contribute directly to platform accountability
""")

# Data Donation Projects
st.subheader("Notable Data Donation Projects")

# Bundeswahl Project
with st.expander("Dein Feed, Deine Wahl - German Election Project", expanded=True):
    st.markdown("""
    ### Dein Feed, Deine Wahl (Your Feed, Your Choice)
    
    This project collected donated TikTok data during the German federal election (Bundeswahl) to analyze 
    how algorithms influenced political content distribution.
    
    **[Visit Project Website](https://dein-feed-deine-wahl.de/)**
    
    #### Key Features:
    - Collected feed data from real TikTok users
    - Analyzed political content exposure across different user groups
    - Provided insights into algorithmic influence on election information
    - Created transparency around content recommendation patterns
    
    The project demonstrated how individual data access rights can be aggregated for meaningful algorithm research.
    """)
    
    # Display project image if available
    project_image_path = os.path.join("data", "dein-feed-deine-wahl.png")
    if os.path.exists(project_image_path):
        st.image(project_image_path, caption="Dein Feed, Deine Wahl Project", use_container_width=True)

# Data Donation Lab
with st.expander("Data Donation Lab & Weizenbaum Institute", expanded=True):
    st.markdown("""
    ### Data Donation Lab & Weizenbaum Institute
    
    The Data Donation Lab at the Weizenbaum Institute has pioneered methods for collecting and analyzing 
    data donations for algorithm research.
    
    #### Key Initiatives:
    - Development of secure data donation infrastructure
    - Creation of browser extensions for simplified data donation
    - Standardized protocols for handling sensitive personal data
    - Cross-platform comparison studies
    
    Their work has established methodological standards for conducting research through data donations while
    maintaining privacy and research ethics.
    """)

# How to request your data
st.header("How to Request Your Data")

st.markdown("""
### Step-by-Step Guide to Data Access Requests

Under GDPR Article 15, platforms must provide users with a copy of their personal data upon request.
Here's how to request your data:
""")

# Create tabs for different platforms
platform_tab1, platform_tab2 = st.tabs(["Instagram Data Request", "TikTok Data Request"])

with platform_tab1:
    st.subheader("Requesting Data from Instagram")
    
    st.markdown("""
    ### Instagram Data Download Process
    
    1. **Open Instagram settings**
       - Go to your profile
       - Tap the menu icon (≡) in the top right
       - Select "Settings and privacy"
    
    2. **Access data download tools**
       - Scroll down to "Data and history"
       - Select "Download your information"
    
    3. **Configure your request**
       - Select data types (photos, messages, profile info, etc.)
       - Choose date range
       - Select format (HTML recommended for readability, JSON for analysis)
    
    4. **Submit and wait**
       - Request processing may take up to 14 days
       - You'll receive a notification when your data is ready
       - Download within 4 days before link expires
    
    5. **Analyze the data**
       - Extract insights about content you've been shown
       - Identify patterns in algorithmic recommendations
       - Look for metadata about why content was recommended
    """)
    
with platform_tab2:
    st.subheader("Requesting Data from TikTok")
    
    st.markdown("""
    ### TikTok Data Download Process
    
    1. **Open TikTok settings**
       - Go to your profile
       - Tap the three-line menu icon in the top right
       - Select "Settings and privacy"
    
    2. **Access data download tools**
       - Tap "Privacy"
       - Select "Download your data"
    
    3. **Configure your request**
       - Choose between TXT or JSON format (JSON recommended for research)
       - Request will include:
         - Profile information
         - Video browsing history
         - Comment history
         - Interaction data
    
    4. **Submit and wait**
       - Processing typically takes 1-4 days
       - You'll receive an in-app notification
       - Download link valid for 4 days
    
    5. **TikTok Together initiative**
       - Consider contributing to "TikTok Together" for research
       - Provides more structured way to donate your data
       - Helps create a broader understanding of the platform
    """)

# Collaborative tools for data donation
st.header("Collaborative Data Donation Tools")

st.markdown("""
### Streamlining the Data Donation Process

Several initiatives have developed tools to make data donation easier for both users and researchers:

* **Browser Extensions**: Simplify the extraction of key data points
* **Data Donation Platforms**: Secure infrastructures for collecting and analyzing donations
* **Standardized Formats**: Tools that convert diverse platform data into consistent formats
* **Anonymization Tools**: Protect donor privacy while preserving research value
""")

# Example Data Analysis
st.subheader("Sample Insights from Data Donations")

st.markdown("""
### What Can We Learn From Donated Data?

Analysis of donated data has revealed important insights about algorithmic systems:

1. **Content Exposure Patterns**:
   - Which topics appear most frequently in different user feeds
   - How user behavior influences content recommendations
   - Differences in political content exposure across user groups

2. **Platform Behavior Variations**:
   - How the same user profile is treated differently across platforms
   - Temporal changes in recommendation algorithms
   - A/B testing detected through aggregate donation analysis
""")

# Data donation challenges section
st.header("Challenges with the Data Donation Approach")

# Get previous data donation challenges response
prev_donation_challenges = get_response_for_poll("donation_challenges")

st.markdown("""
Despite its advantages, data donation comes with significant challenges:

* **Selection Bias**: Donors may not represent average platform users
* **Incomplete Data**: Platforms may not provide all relevant data
* **Format Complexity**: Donated data often requires significant processing
* **Privacy Concerns**: Balancing research needs with donor privacy
* **Scale Limitations**: Difficult to achieve sample sizes comparable to API access

**Group Discussion Question**: How might data donation approaches complement official DSA data access methods?
""")

# Display text area with previous response
donation_challenges = st.text_area(
    "Your thoughts on combining data donation with DSA tools:", 
    value=prev_donation_challenges if prev_donation_challenges else "",
    height=150,
    key="donation_challenges"
)

# Save response when it changes
if donation_challenges and donation_challenges != prev_donation_challenges:
    save_poll_response("donation_challenges", "gdpr_tools", donation_challenges)



# Navigation
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    prev_button = st.button("← Back: DSA Tools")
    if prev_button:
        st.switch_page("pages/2_Dsa_Tools.py")
with col2:
    next_button = st.button("Next: Alternative Methods →")
    if next_button:
        st.switch_page("pages/4_SOAP_and_Scraping.py")