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


# Data donation challenges section
st.header("Challenges with the Data Donation Approach")

st.markdown("""
While data donation provides valuable insights, it comes with several significant challenges:
""")

# Create two columns - one for the embed and one for the explanation
col1, col2 = st.columns([3, 5])

# LinkedIn post embed in the first column
with col1:
    st.components.v1.html("""
    <iframe src="https://www.linkedin.com/embed/feed/update/urn:li:share:7300850251601469440" 
            height="700" width="100%" frameborder="0" allowfullscreen="" 
            title="Embedded LinkedIn post about data donation challenges"></iframe>
    """, height=700)

# Explanation of challenges in the second column
with col2:
    st.markdown("""
    ### The Reality of Data Donation Challenges
    
    As illustrated in the post about TikTok:
    
    1. **Unpredictable Format Changes**: 
       - Platforms change data formats without notice (e.g., TikTok changing "Activities" to "Your Activities")
       - File names suddenly change (e.g., "Browsing History.txt" to "Watch History.txt")
       - These changes break research tools and invalidate donations
    
    2. **No Communication Channel**:
       - Platforms don't announce changes in advance
    
    3. **Privacy and Anonymization Challenges**:
       - Data contains highly sensitive personal information (private messages, locations)
       - Anonymization must happen client-side before researchers can access it
       - Cannot store raw data on research servers due to privacy regulations
    
    4. **Forced Client-Side Filtering**:
       - Processing must happen on user devices before data is donated
       - Any platform format change breaks these filtering tools
       - Requires constant maintenance of data processing scripts
    
    5. **Research Impact**:
       - As seen in the post, 80 donations were rendered useless by a simple format change
       - For data donation studies with limited samples, this is devastating
       - Undermines the reliability of the entire research approach
    
    These issues highlight why standardization of data formats and proper communication channels with platforms are urgently needed for data donation to become a reliable research method.
    """)

# Get previous data donation challenges response
prev_donation_challenges = get_response_for_poll("donation_challenges")



# Display text area with previous response
donation_challenges = st.text_area(
    "Your thoughts on adding specific technical details in Regualtions:", 
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