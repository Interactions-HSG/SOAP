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
    st.subheader("System for Observing and Analyzing Posts")

# Display the SOAP icon in the second column
with col2:
    soap_icon_path = os.path.join("data", "soap.png")
    if os.path.exists(soap_icon_path):
        image = Image.open(soap_icon_path)
        st.image(image, width=100)

# Introduction to SOAP
st.markdown("""
SOAP (System for Observing and Analyzing Posts) is a methodology that combines various techniques to enable direct audits of recommendation algorithms 
and social media platforms in ways that aren't possible through official data access methods. This approach allows researchers to observe how 
platforms behave in the wild, particularly how their algorithms respond to different user profiles and behaviors, providing unique visibility 
into the mechanisms that determine what content users see and why.

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

with st.expander("B. Personas & Sockpuppets", expanded=False):
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
    
    # Add prompt testing button
    prompt_testing_col1, prompt_testing_col2 = st.columns([3,1])
    
    with prompt_testing_col1:
        st.markdown("""
        ### Try It: Prompt Testing Tool
        
        Experiment with our tool for analyzing sock puppet data using Google's Vertex AI.
        Test different prompt structures to see how they can help analyze content shown to your sock puppets.
        """)
        
    with prompt_testing_col2:
        if st.button("Open Prompt Testing Tool"):
            # This will open the prompt testing page in the pages directory
            st.switch_page("pages/7_Prompt_Testing.py")

with st.expander("C. Limitations of SOAP", expanded=False):
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
# Systemic risks section
st.header("Using SOAP for Auditing Systemic Risks")

st.markdown("""
### Applying SOAP to Address DSA Systemic Risks

SOAP provides a robust framework for investigating the systemic risks identified under the Digital Services Act.
Below are key applications of SOAP methodology for specific risk areas:
""")

# Create tabs for different systemic risk scenarios
risk_tab1, risk_tab2, risk_tab3, risk_tab4 = st.tabs([
    "Illegal Content", 
    "Fundamental Rights", 
    "Civic Discourse & Elections",
    "Protection of Vulnerable Groups"
])

with risk_tab1:
    st.subheader("Dissemination of Illegal Content")
    
    # Container with custom styling using st.container() and CSS
    illegal_content_container = st.container()
    illegal_content_container.markdown("##### Case: Instagram's Algorithmic Amplification of Harmful Networks")
    
    with st.container():
        st.info("""
        SOAP enables comprehensive analysis of how illegal content (hate speech, incitement to violence, etc.) is disseminated on platforms. By simulating user behaviors, SOAP captures the pathways through which algorithms promote or amplify harmful materials.
        
        **Real-world example:** The Wall Street Journal's investigation revealed how Instagram's algorithms inadvertently connected users with harmful interests, creating vast networks facilitating illegal activities.
        
        **Why SOAP is essential:** Illegal and harmful content often resides at the "tail of the distribution" where official APIs restrict access. SOAP captures the full lifecycle of harmful content that platforms often hide from official research channels.
        """)
        
        st.markdown("**Key capabilities:**")
        st.markdown("""
        - Records how algorithms serve harmful content based on minor engagement signals
        - Tracks content from initial appearance through amplification
        - Documents platform moderation failures in real-time
        - Measures "algorithmic reinforcement" of harmful filter bubbles
        """)

with risk_tab2:
    st.subheader("Effects on Fundamental Rights")
    
    # Container with custom styling
    rights_container = st.container()
    rights_container.markdown("##### Case: Algorithmic Discrimination & Shadowbanning")
    
    with st.container():
        st.warning("""
        SOAP's diverse user profiles allow examination of bias in content moderation and recommendation systems, particularly how they may impact free expression and non-discrimination rights.
        
        **Real-world application:** Detecting "shadowbanning" - the practice where platforms limit content visibility without notifying creators, which disproportionately affects marginalized communities.
        
        **Why SOAP is essential:** Platforms lack transparency in communicating moderation decisions, leaving users to develop "folk theories" about algorithmic suppression. SOAP provides empirical evidence of these practices.
        """)
        
        st.markdown("**Key capabilities:**")
        st.markdown("""
        - Creates demographically diverse sock puppets to test content treatment
        - Compares engagement metrics across different user demographics
        - Identifies patterns of unexplained content suppression
        - Tests platform claims about equal treatment of diverse content
        """)

with risk_tab3:
    st.subheader("Effects on Civic Discourse & Elections")
    
    # Container with custom styling
    election_container = st.container()
    election_container.markdown("##### Case: Romanian Election Interference on TikTok")
    
    with st.container():
        st.error("""
        SOAP is particularly well-suited for studying algorithmic influences on electoral processes, like the Romanian presidential election case study we've examined.
        
        **Real-world application:** Investigating how platforms like TikTok may have amplified coordinated inauthentic behavior that promoted previously unknown candidates, as happened in Romania.
        
        **Why SOAP is essential:** Platforms like Instagram actively throttle political content, making it difficult to study through official channels. SOAP can empirically assess how platform policies affect political discourse.
        """)
        
        st.markdown("**Key capabilities:**")
        st.markdown("""
        - Simulates users with different political leanings to measure differential content exposure
        - Conducts real-time audits during election periods
        - Tests the effectiveness of platform election safeguards
        - Analyzes how algorithmic amplification impacts electoral information ecosystems
        - Identifies potential foreign interference through inauthentic content patterns
        """)
        
        st.caption("This approach could have provided early warning of the manipulation patterns seen in the Romanian election case.")

with risk_tab4:
    st.subheader("Protection of Vulnerable Groups")
    
    # Container with custom styling
    vulnerable_container = st.container()
    vulnerable_container.markdown("##### Case: Platform Safety Features for Minors")
    
    with st.container():
        st.success("""
        SOAP enables direct audits of recommendation algorithms and how they impact vulnerable populations, particularly minors at risk of harmful content exposure.
        
        **Research impact:** Investigations by Amnesty International revealed how TikTok's algorithms promote self-harm content to teens, while "Recommending Toxicity" showed amplification of misogynistic content.
        
        **Verification need:** With DSA prohibiting personalized ads for minors and platforms claiming safety features, SOAP provides the only independent verification method.
        """)
        
        st.markdown("**Key capabilities:**")
        st.markdown("""
        - Creating simulated teen accounts to test content exposure
        - Verifying DSA compliance on minor protections
        - Measuring harmful content reach
        - Evaluating platform safety claims
        """)

# Summary section on combining methods
st.subheader("Combining SOAP with DSA Tools")

st.markdown("""
The scenarios above demonstrate why SOAP provides critical insights that official data access methods cannot capture alone. 
The most effective research strategies combine SOAP with official DSA tools to create a more complete picture:
""")

# Create a comparison table for SOAP and DSA tools
st.markdown("### Complementary Approaches")
st.markdown("""
The recommended posts shown to sockpuppets can be directly compared with data provided through official DSA tools:
""")

comparison_df = pd.DataFrame({
    "DSA Tool": ["Ad Transparency Database", "Research APIs", "Transparency Reports/Database"],
    "What to Compare": [
        "Advertisements shown to sockpuppets vs. officially declared ads", 
        "Engagement metrics (likes, views) observed vs. reported metrics", 
        "Content moderation patterns observed vs. reported takedowns"
    ],
    "Research Value": [
        "Verify if all ads delivered to users are properly disclosed and labeled",
        "Validate accuracy of platform metrics and cross-check scraped variables with API-provided data",
        "Identify discrepancies in content moderation and understand what triggers enforcement actions"
    ]
})

st.table(comparison_df)



st.markdown("""
This combined methodology allows researchers to:

1. **Validate platform claims** by comparing what platforms say they do with what sockpuppets actually experience
2. **Identify blind spots** in official data access by discovering content or patterns not visible through DSA tools
3. **Strengthen research validity** through triangulation of multiple data sources
4. **Document platform behaviors** comprehensively using both insider and outsider perspectives
""")
# Alternative Data Access Tools section
st.header("Alternative Data Access Tools")
    
st.markdown("""
### Comprehensive Directory of Platform Research Tools

Below is an embedded directory of alternative tools for platform research beyond the official DSA mechanisms.
This resource, maintained by researchers studying platform transparency, provides up-to-date information on:

- Additional data access methods
- Tools for independent platform research 
- Community-developed resources for platform investigation
- Alternative APIs and documentation

Explore the directory to find tools that might be useful for your specific research questions:
""")

# Embed Airtable
st.components.v1.iframe(
    "https://airtable.com/embed/apphRmVsFpqb4xsbF/shr8tfiIMi7MafjXW/tblLtPvSzRqzk2med/viwbA8mzlE28qcI5l?blocks=hide", 
    height=600, 
    scrolling=True
)

st.caption("Source: Platform Research Tools Directory, maintained by the Digital Research Methods Consortium")



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