import streamlit as st
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Data Scraping - SOAP Workshop",
    page_icon="🔍",
    layout="wide"
)

st.title("2. Data Scraping")
st.subheader("Techniques for collecting social media data")

# Display SOAP system image
try:
    soap_image = Image.open("data/SOAP_system.png")
    st.image(soap_image, caption="SOAP System Architecture for Platform Auditing", use_container_width=True)
except FileNotFoundError:
    st.info("SOAP system diagram not found at data/SOAP_system.png")

# 1. Private APIs - The Foundation of SOAP Data Collection
st.markdown("""
## Unofficial Private API Libraries

**Primary Tools Used in SOAP**: Instagrapi, TikAPI

**What are Private APIs?**
These are the same API calls that the official mobile apps make to platform servers. Unlike public research APIs, private APIs provide access to the full range of data and functionality available to regular users.

### Instagrapi for Instagram
- **GitHub**: [https://github.com/subzeroid/instagrapi](https://github.com/subzeroid/instagrapi)
- **Capabilities**: OAuth authentication, session management, challenge handling
- **Data Access**: Posts, stories, albums, Reels, Explore Feed content
- **Interactions**: Like, follow, comment, save, report posts
- **Authentication**: Username/password or session ID login

### TikAPI for TikTok  
- **GitHub**: [https://github.com/tikapi-io/tiktok-api](https://github.com/tikapi-io/tiktok-api)
- **Data Richness**: Access to 845+ variables vs. 32 variables in official research API
- **Comprehensive Access**: Full user profiles, video metadata, engagement metrics
- **Real-time Data**: Live recommendation feeds, trending content

### Why Private APIs?
- **Complete Data Access**: Unlike research APIs with limited data fields
- **Real User Experience**: Same data that actual users see
- **No Rate Limits**: Avoid restrictive quotas of official APIs
- **Dynamic Content**: Access to recommendation algorithms in real-time
""")

# 2. Types of data that can be scraped
st.markdown("""
## Types of Data Available for Scraping

### 1. Content Data
- **Posts/Videos**: Text, images, videos shared on platforms
- **Metadata**: Timestamps, engagement metrics, hashtags
- **Comments**: User interactions and discussions

### 2. Recommendation Data
- **Feed Content**: What appears in user timelines/feeds
- **Search Results**: Platform responses to specific queries
- **Suggested Content**: "Related" or "You might also like" sections

### 3. User Profile Data (Public)
- **Profile Information**: Publicly visible user details
- **Following/Followers**: Network connections (where public)
- **Activity Patterns**: Posting frequency, engagement behavior
""")

# 3. Account creation and management
st.markdown("""
## Account Creation

### Sockpuppet Account Strategy
SOAP uses carefully created **sockpuppet accounts** - fake accounts designed to simulate real user behavior for research purposes.

#### Account Creation Process:
1. **Demographic Diversity**: Create accounts representing different user demographics
2. **Realistic Profiles**: Use believable names, photos, and basic information  
3. **Gradual Activation**: Slowly build account history before data collection
4. **Geographic Distribution**: Accounts from different locations to test regional differences

#### Proxy Infrastructure
**Why Proxies Are Essential**:
- **Geographic Diversity**: Simulate users from different countries/regions
- **IP Rotation**: Prevent detection of coordinated behavior
- **Rate Limit Distribution**: Spread requests across multiple IP addresses
- **Account Isolation**: Prevent linking multiple research accounts

**SOAP's Proxy Implementation**:
- **Residential Proxies**: Use real user IP addresses to appear authentic
- **Location-Based**: Match proxy location with account geographic profile
- **Rotation Strategy**: Automatic IP switching to maintain anonymity
- **Quality Monitoring**: Continuous testing of proxy reliability and speed

#### Account Behavior Simulation
**Human-Like Patterns**:
- **Variable Timing**: 1-3 second delays between interactions
- **Natural Engagement**: Gradual increase in activity over time
- **Realistic Limits**: Maximum 300 posts per session (~2 hours scrolling)
- **Mindless Scrolling**: Continuous, unstructured browsing patterns

**Authentication Methods**:
- **Session Management**: Use session IDs for consistent login
- **Challenge Handling**: Automated responses to platform security checks
- **Login Verification**: Multiple authentication options (username/password, sessions)
""")

# 4. Platform detection and countermeasures
st.markdown("""
## Platform Detection and Countermeasures

### Detection Challenges
Platforms actively monitor for automated behavior and implement sophisticated detection systems:

#### Common Detection Methods:
- **Interaction Patterns**: Unusual speed or regularity of actions
- **IP Analysis**: Multiple accounts from same IP address
- **Device Fingerprinting**: Browser and device characteristic analysis
- **Behavioral Analysis**: Deviation from typical user patterns

#### Platform Responses:
- **Account Warnings**: Notifications about detected automated behavior
- **Rate Limiting**: Temporary restrictions on account activity
- **Account Suspension**: Temporary or permanent account blocks
- **CAPTCHA Challenges**: Human verification requirements

### SOAP's Countermeasures

#### Built-in Library Features:
- **Session Persistence**: Maintain consistent login sessions
- **Challenge Handling**: Automated responses to platform security measures
- **Rate Limiting**: Built-in delays and request throttling
- **User-Agent Rotation**: Vary browser identification strings

#### Additional Safeguards:
- **Proxy Integration**: Residential IP addresses for geographic authenticity
- **Timing Randomization**: Variable delays between interactions (1-3 seconds)
- **Activity Limits**: Respect platform usage patterns (300 posts/session)
- **Behavioral Mimicry**: Simulate realistic user engagement patterns

### Example Warning Response
When platforms detect automated behavior:
> "We've detected automated behavior on your account. This could be because you're using third-party apps that violate our Terms of Service."

""")

# 5. Legal considerations
st.markdown("""
## Legal Considerations

#### 1. **Publicly Available Data Only**
- SOAP accesses only publicly available data from VLOPs
- Content made publicly accessible by data subjects themselves
- No "reasonable expectation" of privacy for fully public platform content

#### 2. **Copyright and Text/Data Mining Exceptions**
- **Germany's 2017 Copyright Act (§ 60d)**: Allows automatic data collection for research corpus creation
- **EU Digital Single Market Directive (Article 3)**: Mandates text and data mining exceptions for scientific research

#### 3. **Data Protection Considerations**
- **GDPR Compliance**: Focuses on manifestly publicly accessible data
- **Data Minimization**: Collect only necessary data for research objectives

#### 4. **Platform Terms of Service (ToS)**
- **Academic Freedom Defense**: European Convention on Human Rights (Article 10) protects research expression
- **Balancing Interests**: Research value vs. contractual restrictions
- **Council of Europe Support**: Recognizes "societal role of academia in producing independent research"

#### 5. **Passive Research Approach**
- **Non-Intrusive**: Mimics natural user behavior (viewing, liking)
- **No Active Discourse**: No commenting, sharing, or messaging
- **Societal Benefit**: Research on polarization and systemic risks outweighs ToS concerns

### Best Practices for Compliance:
- ✅ **Transparency**: Document methodology and legal analysis
- ✅ **Data Minimization**: Collect only necessary research data
- ✅ **Public Interest**: Focus on systemic risks and societal impact
- ✅ **Passive Observation**: Avoid active platform engagement
- ✅ **Academic Purpose**: Non-commercial research objectives only
""")

# 6. SOAP's Complete Data Collection Pipeline
st.markdown("""
## SOAP's Complete Data Collection Pipeline

The **System for Observing and Analyzing Posts (SOAP)** implements a comprehensive approach to platform auditing through systematic data collection:

### Infrastructure Setup
**Proxy Network Configuration**:
- Residential proxy pool for geographic diversity
- IP rotation system for account isolation
- Location-based proxy assignment matching account profiles

**Account Management System**:
- Automated sockpuppet account creation and session persistence
- Diverse demographic profile generation
- Account behavior tracking and adjustment

### Data Collection Workflow
**Phase 1**: Account Preparation → **Phase 2**: Data Gathering → **Phase 3**: Quality Assurance

**API Library Integration with Cloud Storage**:

The following code demonstrates SOAP's data collection workflow with Google Cloud Storage integration:
""")

# Display code block using st.code to avoid markdown syntax conflicts
st.code("""
# Example SOAP data collection flow with Google Cloud Storage
from instagrapi import Client
from tiktok_api import TikTokApi
from google.cloud import storage
import requests
import os

# Initialize cloud storage client
storage_client = storage.Client()
bucket = storage_client.bucket('soap-media-data')

# Initialize with proxy and session management
cl = Client()
cl.set_proxy(proxy_url)
cl.login_by_sessionid(session_id)

# Collect Explore Feed data
explore_feed = cl.explore_feed()
for post in explore_feed:
    # Extract comprehensive metadata
    post_data = extract_full_metadata(post)
    
    # Handle media files (images, videos)
    if post_data.get('media_url'):
        media_filename = f"{post_data['id']}.{post_data['media_type']}"
        cloud_url = upload_media_to_cloud(
            post_data['media_url'], 
            media_filename,
            bucket
        )
        post_data['cloud_media_url'] = cloud_url
        # Remove local URL to save storage
        del post_data['media_url']
    
    # Store metadata with cloud reference
    store_with_metadata(post_data, collection_context)
""", language="python")

st.markdown("""
**Media Storage Architecture**: 3.8TB daily collection capacity with organized cloud storage structure for images and videos from Instagram and TikTok.

**Scale and Performance**:
- **Session Limits**: 300 posts per account per session
- **Multi-Platform**: Simultaneous Instagram and TikTok auditing  
- **Scalability**: Architecture supports scaling of accounts

**Built-in Compliance Features**:
- **Public Data Only**: Automated filtering for publicly accessible content
- **Data Minimization**: Configurable collection scope based on research needs
- **Audit Trail**: Comprehensive logging for transparency and accountability
""")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("← Previous: Introduction"):
        st.switch_page("pages/1_Introduction.py")

with col2:
    st.markdown("<div style='text-align: center;'>**Current: Data Scraping**</div>", unsafe_allow_html=True)

with col3:
    if st.button("Next: Deductive Coding →"):
        st.switch_page("pages/3_Deductive_Coding.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
Part of the FAccT 2025 Workshop: "Auditing Social Media Platforms using SOAP"<br>
University of St. Gallen | CoCoDa Project
</div>
""", unsafe_allow_html=True)
