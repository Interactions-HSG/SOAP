import streamlit as st
import pandas as pd
from PIL import Image
import os
from database.poll_responses.session_management import initialize_session, save_poll_response, get_response_for_poll

# Initialize user session
user_id = initialize_session()

st.set_page_config(
    page_title="Introduction | Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide"
)

st.title("1. Introduction to Social Media Research")
st.subheader("Understanding the Digital Services Act & Researcher Access")

# Load images
image_path = os.path.join("data", "cpdp2025-long.svg")
if os.path.exists(image_path):
    st.image(image_path, width=600)

# Short introduction
st.markdown("""
Welcome to our workshop on **Social Media Research Under the Digital Services Act (DSA)**. 
This session explores how researchers can investigate algorithmic systems while navigating
legal and technical constraints.
""")

# Poll about familiarity with DSA
st.header("Before we begin...")

# --- New: Two-column layout for participant info ---
left_col, right_col = st.columns([1, 1])

# --- LEFT COLUMN: Background & Years of Experience ---
with left_col:
    # Background
    background_options = [
        "CS", "Legal & Law", "Political Science", "Social Science", "Other"
    ]
    prev_background = get_response_for_poll("background")
    background = st.selectbox(
        "What is your background?",
        options=background_options,
        index=background_options.index(prev_background) if prev_background in background_options else 0
    )
    # If 'Other', show text input
    background_other = ""
    if background == "Other":
        background_other = st.text_input(
            "Please specify your background:",
            value=prev_background if prev_background not in background_options and prev_background else ""
        )
        background_value = background_other if background_other else "Other"
    else:
        background_value = background
    # Save response
    if prev_background != background_value and background_value:
        save_poll_response("background", "introduction", background_value)

    # Years of experience
    exp_options = ["0-3", "3-5", "5-10", "10+"]
    prev_years_exp = get_response_for_poll("years_experience")
    years_exp = st.selectbox(
        "Years of experience in research or relevant field:",
        options=exp_options,
        index=exp_options.index(prev_years_exp) if prev_years_exp in exp_options else 0
    )
    if prev_years_exp != years_exp:
        save_poll_response("years_experience", "introduction", years_exp)

# --- RIGHT COLUMN: DSA familiarity & research experience ---
with right_col:
    # Get previous DSA familiarity response
    prev_dsa_familiarity = get_response_for_poll("dsa_familiarity")
    dsa_options = [
        "Never heard of it", 
        "Heard of it but don't know details", 
        "Familiar with basic provisions",
        "Very familiar with researcher-specific provisions", 
        "Expert who has applied for/used DSA data access"
    ]
    dsa_familiarity = st.radio(
        "How familiar are you with the Digital Services Act?", 
        options=dsa_options,
        index=dsa_options.index(prev_dsa_familiarity) if prev_dsa_familiarity and prev_dsa_familiarity in dsa_options else 0
    )
    if dsa_familiarity != prev_dsa_familiarity:
        save_poll_response("dsa_familiarity", "introduction", dsa_familiarity)

    # Get previous social media research response
    prev_research_exp = get_response_for_poll("research_experience")
    research_options = [
        "No experience", 
        "Limited experience (e.g., social media analytics)", 
        "Some experience with platform APIs",
        "Significant experience with social media research", 
        "Expert in algorithmic auditing"
    ]
    research_exp = st.radio(
        "What is your experience level with social media research?",
        options=research_options,
        index=research_options.index(prev_research_exp) if prev_research_exp and prev_research_exp in research_options else 0
    )
    if research_exp != prev_research_exp:
        save_poll_response("research_experience", "introduction", research_exp)



# Add the real-world case study
st.header("Real-World Case Study: Election Interference in Romania")

st.markdown("""
### TikTok Manipulation in Romanian Presidential Elections
<small>*Source: Goanta, Catalina, et al. "The Great Data Standoff: Researchers vs. Platforms Under the Digital Services Act." arXiv preprint arXiv:2505.01122 (2025). [View Paper](https://arxiv.org/abs/2505.01122)*</small>


The Romanian presidential election campaign (October 25 - November 24, 2024) revealed concerning patterns of platform 
manipulation. According to investigative journalists and Romanian intelligence agencies, TikTok became a central tool 
for influencing voters through coordinated tactics that promoted a previously unknown right-wing candidate.

In a matter of weeks, this candidate rose from obscurity to become the most popular candidate in the first voting 
round. Due to suspected manipulation and possible foreign interference, Romania's Constitutional Court ultimately 
annulled the election results, and the European Court of Human Rights refused the candidate's request to suspend this decision.

""", unsafe_allow_html=True)

# --- Key Mechanisms of Manipulation ---
st.subheader("Key Mechanisms of Manipulation")

mechanisms = [
    ("Inauthentic Behavior", "A coordinated network of promotion accounts generated fake engagement that triggered TikTok's search recommendations"),
    ("Political Influencer Marketing", "Non-disclosed micro-influencer campaigns promoted an \"ideal candidate\" without transparent disclosure"),
    ("Livestream Monetization", "TikTok's streaming gifts and coins were used to amplify undisclosed political advertising and content"),
]
cols = st.columns(3)
for i, (title, desc) in enumerate(mechanisms):
    with cols[i % 3]:
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <h4 style='color: #1e3a8a;'>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

# --- Systemic Risks Under DSA ---
st.subheader("Systemic Risks Under DSA")

risks = [
    ("Election Interference", "Coordinated manipulation of platform mechanisms to influence electoral outcomes (Art. 34(1)(c))"),
    ("Hidden Advertising", "Undisclosed political advertising masquerading as organic content (Art. 34(1)(a))"),
    ("Hate Speech", "Amplification of content involving fascism, misogyny, racism, and fundamental rights rejections (Art. 34(1)(b))"),
    ("Conspiracy Theories", "Promotion of conspiracy theories with potential public health impacts (Art. 34(1)(d))"),
    ("Recommender System Design", "TikTok's search recommendations further amplified problematic content (Art. 34(2))"),
]
cols = st.columns(3)
for i, (title, desc) in enumerate(risks):
    with cols[i % 3]:
        st.markdown(f"""
        <div style='background-color: #fef3c7; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
            <h4 style='color: #92400e;'>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)


# Workshop overview
st.header("Data Access Overview")

# Add the complete data access graphic
dsa_tools_path = os.path.join("data", "DSATools_0.4(1).png")
if os.path.exists(dsa_tools_path):
    st.image(dsa_tools_path, width=1000, caption="Complete Data Access Overview")

st.markdown("""
In order to investigate those claims, we will use all available data access methodologies.
""")
# Group discussion
st.header("Quick Discussion")

# Get previous discussion response
prev_discussion = get_response_for_poll("intro_discussion")

# Display text area with previous response
discussion_notes = st.text_area(
    "What specific algorithmic behaviors or systems are you most interested in studying?", 
    value=prev_discussion if prev_discussion else "",
    height=150
)

# Save response when it changes
if discussion_notes and discussion_notes != prev_discussion:
    save_poll_response("intro_discussion", "introduction", discussion_notes)

# Show institutions
st.header("Presented by")

col1, col2, col3, col4 = st.columns(4)

# Maastricht University logo
maastricht_path = os.path.join("data", "Maastricht_University_logo.svg.png")
if os.path.exists(maastricht_path):
    with col1:
        st.image(maastricht_path, width=200)
        st.caption("Maastricht University")

# HSG logo
hsg_path = os.path.join("data", "HSG_Logo_EN_RGB.svg.png")
if os.path.exists(hsg_path):
    with col2:
        st.image(hsg_path, width=200)
        st.caption("University of St. Gallen")

# Lausanne logo
unil_path = os.path.join("data", "Logo_Université_de_Lausanne.png")
if os.path.exists(unil_path):
    with col3:
        st.image(unil_path, width=200)
        st.caption("University of Lausanne")


# Navigation
st.markdown("---")
next_button = st.button("Next: DSA Tools →")
if next_button:
    st.switch_page("pages/2_Dsa_Tools.py")