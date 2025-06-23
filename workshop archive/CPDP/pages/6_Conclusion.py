import streamlit as st
import pandas as pd
import plotly.express as px
from database.poll_responses.session_management import initialize_session, save_poll_response, get_response_for_poll

# Initialize user session
user_id = initialize_session()

st.set_page_config(
    page_title="Reflections & Wrap-up | Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide"
)

st.title("6. Reflections & Wrap-up")
st.subheader("Evaluating trade-offs and considering the future of platform auditing")

# Introduction
st.markdown("""
As we conclude this workshop on social media platform auditing, let's reflect on what we've learned
about the various methods available, their trade-offs, and the broader implications for researchers,
civil society, platforms, and regulators.
""")

# Key reflections
st.header("Key Workshop Insights")

reflections = {
    "Mixed-Methods Approach": "No single data source or methodology provides a complete picture of algorithm behavior. Combining official and alternative methods creates a more comprehensive understanding.",
    
    "Legal-Technical Balance": "Platform auditing exists at the intersection of legal frameworks and technical capabilities. Researchers must balance innovative methods with legal and ethical considerations.",
    
    "Stakeholder Perspectives": "Different stakeholders (researchers, platforms, regulators) have legitimate but sometimes conflicting interests in the transparency ecosystem.",
    
    "Evidence Standards": "Different contexts (regulatory enforcement, academic publication, public advocacy) require different standards of evidence and methodological approaches."
}

# Create expandable sections for each reflection
for topic, description in reflections.items():
    with st.expander(f"**{topic}**", expanded=True):
        st.markdown(description)



# Policy gaps discussion
st.subheader("Addressing Policy Gaps")

st.markdown("""
Our workshop has highlighted several gaps in the current regulatory and policy framework around platform auditing:
""")

policy_gaps = [
    "Limited access rights for non-academic researchers and journalists",
    "Unclear legal status of web scraping for research purposes",
    "Inadequate mechanisms to verify platform transparency claims",
    "Insufficient standardization of data formats across platforms",
    "Limited enforcement mechanisms for transparency obligations"
]

for gap in policy_gaps:
    st.markdown(f"- {gap}")

# Participant reflection
st.header("Your Reflections")

st.markdown("""
Take a moment to reflect on what you've learned in this workshop and how it might apply to your work:
""")

col1, col2 = st.columns(2)

# Get previous responses if available
prev_learning = get_response_for_poll("workshop_learning")
prev_application = get_response_for_poll("workshop_application")

with col1:
    # Pre-fill with previous response if available
    learning = st.text_area(
        "What was your most valuable insight from this workshop?", 
        value=prev_learning if prev_learning else ""
    )
    
    # Save response when it changes
    if learning and learning != prev_learning:
        save_poll_response("workshop_learning", "conclusion", learning)
    
with col2:
    # Pre-fill with previous response if available
    application = st.text_area(
        "How might you apply these methods in your work?",
        value=prev_application if prev_application else ""
    )
    
    # Save response when it changes
    if application and application != prev_application:
        save_poll_response("workshop_application", "conclusion", application)


# Workshop evaluation
st.header("Workshop Evaluation")

st.markdown("Please take a moment to provide feedback on this workshop:")

# Get previous feedback response
prev_evaluation = get_response_for_poll("workshop_evaluation")
if prev_evaluation and isinstance(prev_evaluation, dict):
    prev_feedback = prev_evaluation.get("feedback", "")
else:
    prev_feedback = ""

feedback = st.text_area("Your feedback and suggestions:", value=prev_feedback)

# Save feedback response when the button is clicked
if st.button("Submit Feedback"):
    evaluation_data = {
        "feedback": feedback
    }
    
    # Save the feedback data
    save_poll_response("workshop_evaluation", "conclusion", evaluation_data)
    
    st.success("Thank you for your feedback!")
    st.balloons()

# Final note
st.info("""
**Thank you for participating in this workshop!**

We hope you've gained valuable insights into the tools and methods available for platform auditing,
as well as the legal and ethical considerations involved. As the regulatory landscape continues to evolve,
your work in this field will help shape how algorithms and platforms are held accountable.

For additional questions or to access workshop materials, please contact the workshop facilitator.
""")

# Navigation button
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    prev_button = st.button("← Previous: Group Simulation")
    if prev_button:
        st.switch_page("pages/5_Legal_Uncertainties.py")

with col2:
    home_button = st.button("Return to Workshop Overview")
    if home_button:
        st.switch_page("app.py")