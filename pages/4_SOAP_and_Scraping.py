import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
from PIL import Image

st.set_page_config(
    page_title="SOAP and Scraping | Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide"
)

# Create a row with two columns for the title and icon
col1, col2 = st.columns([6, 1])

# Display the title in the first column
with col1:
    st.title("4. SOAP and Scraping")
    st.subheader("Systematic Observation of Algorithms and Platforms")

# Display the SOAP icon in the second column
with col2:
    soap_icon_path = os.path.join("data", "soap.png")
    if os.path.exists(soap_icon_path):
        image = Image.open(soap_icon_path)
        st.image(image, width=100)

# Introduction to SOAP
st.markdown("""
SOAP (Systematic Observation of Algorithms and Platforms) is a methodology that combines various techniques to audit social media platforms
in ways that aren't possible through official data access methods. This approach allows researchers to observe how 
platforms behave in the wild, particularly how their algorithms respond to different user profiles and behaviors.

This section explores the key components of SOAP and how they can be implemented for platform research.
""")
# Show the SOAP system image
soap_image_path = os.path.join("data", "SOAP_system.png")
if os.path.exists(soap_image_path):
    image = Image.open(soap_image_path)
    st.image(image, caption="SOAP System Architecture", use_container_width=True)
else:
    st.info("SOAP system diagram not found. The diagram would show the architecture of a sock puppet auditing system.")

# Main sections as expandable elements
with st.expander("A. Scraping Techniques", expanded=False):
    st.header("Scraping Techniques")
    
    st.markdown("""
    ### Browser-based Scraping via Selenium
    
    Browser automation tools like Selenium allow researchers to programmatically interact with social media 
    platforms through a real browser interface. This approach:
    
    - Mimics genuine user interactions with the platform
    - Allows for structured data collection from the user interface
    - Can navigate complex, JavaScript-heavy interfaces
    - Provides access to content as it appears to real users
    """)
    
    # Zeeschuimer section
    st.subheader("Zeeschuimer - Browser Traffic Monitoring")
    
    st.markdown("""
    [Zeeschuimer](https://github.com/digitalmethodsinitiative/zeeschuimer) is a browser extension that monitors internet traffic while you are browsing a social media site, 
    and collects data about the items you see in a platform's web interface for later systematic analysis.
    
    This tool allows researchers to:
    
    - Capture API requests and responses while browsing
    - Collect structured data directly from the platform's internal APIs
    - Document the exact content shown to a specific user profile
    - Export data in formats suitable for systematic analysis
    
    **[Explore Zeeschuimer on GitHub](https://github.com/digitalmethodsinitiative/zeeschuimer)**
    """)
    
    # SOAP Deepdive - API calls
    st.subheader("SOAP Deepdive: Private API Calls")
    
    st.markdown("""
    ### Private API Access
    
    Beyond browser scraping, researchers can sometimes interact directly with platforms' private APIs.
    Tools like Instagrapi (for Instagram) provide programmatic access to platform functions through 
    reverse-engineered API endpoints.
    
    #### Key Components:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Authentication**
        
        - Cookie-based session management
        - Device fingerprinting simulation
        - Token management and refresh
        - Handling two-factor authentication
        """)
    
    with col2:
        st.markdown("""
        **Proxy Configuration**
        
        - Residential IP rotation
        - Geographic distribution
        - Rate limiting adherence
        - Traffic pattern naturalization
        """)
    
    st.markdown("""
    **Automated Behavior**
    
    When interacting with platforms through private APIs, researchers must carefully simulate natural user behavior:
    
    - Randomized timing between requests
    - Natural session durations and patterns
    - Gradual account growth and activity
    - Contextually appropriate interactions
    - Variation in device identifiers
    """)
    
    # Note about API implementation instead of code sample
    st.subheader("API Implementation")
    st.info("""
    **Implementation Note:** A typical API implementation would include:
    
    - Client initialization with appropriate device fingerprinting
    - Authentication handling with proxy support
    - Rate-limited data collection functions
    - Natural delay implementation between requests
    - Error handling for API changes and blocks
    - Data normalization and export functionality
    
    For specific code examples, please refer to documentation for tools like Instagrapi or check the workshop resources.
    """)

with st.expander("B. Deductive Coding", expanded=False):
    st.header("Deductive Coding")
    
    st.markdown("""
    ### The Role of Deductive Coding in SOAP
    
    Deductive coding is a systematic approach to analyzing platform behavior based on pre-defined 
    categories and hypotheses. In the context of SOAP, it helps researchers:
    
    - Identify patterns in algorithmic responses to specific behaviors
    - Categorize content recommendation strategies
    - Test hypotheses about platform algorithms
    - Quantify observed platform behaviors
    
    #### Coding Framework Development
    
    1. **Define Research Questions**: Start with clear questions about platform behavior
    2. **Develop Code Categories**: Create categories based on existing theories and knowledge
    3. **Set Coding Rules**: Establish clear criteria for categorizing observations
    4. **Test Reliability**: Ensure consistent application of codes across researchers
    5. **Implement Systematic Coding**: Apply framework to collected data
    6. **Analyze Patterns**: Identify significant patterns in coded data
    
    #### Example: Coding Political Content Recommendations
    
    | Code Category | Definition | Example |
    |---------------|------------|---------|
    | Political Alignment | Content presents clear partisan perspective | Pro-party X message |
    | Inflammatory | Content designed to provoke strong reactions | Outrage-focused political attack |
    | Informational | Neutral presentation of facts or events | Election date announcement |
    | Call to Action | Content urging specific political behavior | "Vote for candidate Y" |
    | Personalization | Content tailored to user's known views | "Because you follow Z..." |
    """)
    
    st.info("""
    Deductive coding provides the analytical framework that gives meaning to data collected through 
    scraping and sock puppet methods. Without this systematic approach, the data remains merely 
    observations without actionable insights.
    """)

with st.expander("C. Personas & Sockpuppets", expanded=False):
    st.header("Personas & Sockpuppets")
    
    st.markdown("""
    ### Using Simulated Users for Platform Auditing
    
    Sock puppets (or simulated user accounts) allow researchers to observe how platforms respond 
    to different user characteristics and behaviors. This is a critical component of SOAP methodology.
    """)
    
    # Display the bot accounts workshop image
    bot_image_path = os.path.join("data", "Bot_accounts_workshop_0.1.png")
    if os.path.exists(bot_image_path):
        image = Image.open(bot_image_path)
        st.image(image, caption="Bot Accounts for Research", use_container_width=True)
    else:
        st.warning("Bot accounts workshop image not found.")
    
    st.markdown("""
    ### Persona Development
    
    Creating effective sock puppets requires careful persona development:
    
    1. **Demographic Profile**: Age, location, gender, education level
    2. **Interest Graph**: Topics, accounts, and hashtags to follow
    3. **Interaction Patterns**: How the account will engage with content
    4. **Growth Strategy**: How the account will develop over time
    5. **Activity Schedule**: When and how often the account will be active
    
    ### Sockpuppet Implementation
    
    Practical implementation of sockpuppets typically involves:
    
    - Creating accounts across multiple research devices
    - Establishing VPN connections from appropriate locations
    - Gradually building account history and engagement
    - Documenting all account activities and platform responses
    - Following specific interaction protocols based on research questions
    """)
    
    # Note about cloud implementation instead of code sample
    st.subheader("Scaling Sock Puppet Research")
    st.info("""
    **Cloud Infrastructure:** For larger-scale sockpuppet research, cloud infrastructure can help manage:
    
    - Centralized puppet account management
    - Scheduled activities across personas
    - Secure storage of session data
    - Coordinated multi-device interactions
    - Automated data collection and analysis
    
    This approach allows researchers to create a network of diverse personas with consistent behavior patterns.
    """)

with st.expander("D. Limitations of SOAP", expanded=False):
    st.header("Limitations of SOAP")
    
    st.markdown("""
    ### Key Limitations of the SOAP Methodology
    
    While SOAP provides valuable insights into platform behavior, it has significant limitations:
    
    #### Technical Limitations
    
    - **Detection Risk**: Platforms actively detect and block automated activity
    - **Scale Limitations**: Cannot easily match the scale of official data access
    - **Technical Maintenance**: Requires constant updates as platforms change
    - **Resource Intensity**: High computational and human resource requirements
    
    #### Methodological Limitations
    
    - **Generalizability Issues**: Small samples may not reflect broader platform behavior
    - **Algorithmic Changes**: Platform algorithms change frequently, limiting study longevity
    - **Baseline Comparison**: Difficult to establish true "neutral" baselines
    - **Replication Challenges**: Hard for other researchers to independently verify results
    
    #### Ethical and Legal Limitations
    
    - **Terms of Service**: Often violates platform terms of service
    - **Legal Gray Areas**: Potential legal risks in certain jurisdictions
    - **Deception Concerns**: Involves creating fictitious accounts and personas
    - **Potential Harm**: Risk of unintended consequences in platform ecosystems
    
    #### Data Quality Limitations
    
    - **Missing Context**: Limited visibility into why algorithms make certain decisions
    - **Incomplete Data**: Cannot access all variables influencing recommendations
    - **Selection Biases**: Sock puppets may receive atypical recommendations
    - **Historical Limitations**: Difficult to study past platform behaviors
    """)
    
    st.warning("""
    Given these limitations, SOAP methods should be seen as complementary to official 
    data access methods rather than replacements. The most robust research combines 
    multiple approaches to overcome the limitations of each individual method.
    """)


# Combining methods section
st.header("Integrating SOAP with Official Methods")

st.markdown("""
### A Comprehensive Approach to Platform Auditing

The most effective auditing strategies combine SOAP methods with official DSA data access
and GDPR data donations to create a more complete picture of platform behavior:

| Research Question | SOAP Methods | Official Methods | Combined Approach |
|-------------------|-------------|------------------|-------------------|
| Content Amplification | Observe what specific personas are shown | Access aggregate recommendation data | Compare actual delivery to stated policies |
| User Profiling | Test how behaviors affect recommendations | Request data processing documentation | Map actual profiling against disclosed practices |
| A/B Testing | Detect different treatments across accounts | Access platform experimentation data | Verify completeness of disclosed experiments |
| Election Integrity | Monitor election content exposure | Analyze platform transparency reports | Compare claimed vs. observed safeguards |
""")

# Navigation buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    prev_button = st.button("← Previous: GDPR Tools")
    if prev_button:
        st.switch_page("pages/3_GDPR_Tools.py")

with col2:
    next_button = st.button("Next: Legal Uncertainties →")
    if next_button:
        st.switch_page("pages/5_Legal_Uncertainties.py")