import streamlit as st
import os
from PIL import Image, ImageOps # Import ImageOps
from io import BytesIO
import base64
from database.poll_responses.session_management import initialize_session

# Initialize user session - this creates or retrieves a unique user ID
user_id = initialize_session()

# Page configuration
st.set_page_config(
    page_title="Social Media Auditing Workshop",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load and style images
def load_styled_image(image_path, size=150, border_radius="50%", vertical_shift_px=0): # Added vertical_shift_px
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            img_w, img_h = img.size
            target_s = float(size)

            # Determine scaled dimensions and excess for centering adjustment
            img_aspect = img_w / img_h
            target_aspect = 1.0 # Target is square

            centering_y = 0.5 # Default vertical centering

            if vertical_shift_px != 0:
                # Apply shift only if image is taller than target aspect (vertical cropping occurs)
                if img_aspect < target_aspect: 
                    # Image is scaled based on width to target_s
                    # scaled_w = target_s
                    scaled_h = img_h * (target_s / img_w)
                    if scaled_h > target_s: # Check if there's excess height to crop
                        excess_h = scaled_h - target_s
                        if excess_h > 0: # Avoid division by zero if somehow excess_h is not positive
                            centering_y = 0.5 + (vertical_shift_px / excess_h)
            
            # Clamp centering_y to be between 0.0 and 1.0
            centering_y = max(0.0, min(1.0, centering_y))
            
            centering_tuple = (0.5, centering_y) # Horizontal centering remains 0.5

            # Resize and crop image to fit while maintaining aspect ratio, using adjusted centering
            img = ImageOps.fit(img, (size, size), Image.Resampling.LANCZOS, centering=centering_tuple)
            
            # Convert image to base64
            buffered = BytesIO()
            img.save(buffered, format="PNG") # Save as PNG to support transparency if any
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # HTML for styled image
            return f'<img src="data:image/png;base64,{img_str}" style="width:{size}px; height:{size}px; border-radius:{border_radius}; object-fit:cover;">' # Removed extra_style from f-string
        except Exception as e:
            return f"Error loading image {image_path}: {e}"
    return ""

# Display centered CPDP logo at the top
if os.path.exists("data/cpdp2025-long.svg"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("data/cpdp2025-long.svg", width=600)

# Display university logos in a row
col1, col2, col3 = st.columns(3)
with col1:
    if os.path.exists("data/Logo_Université_de_Lausanne.png"):
        st.image("data/Logo_Université_de_Lausanne.png", width=200)
with col2:
    if os.path.exists("data/HSG_Logo_EN_RGB.svg.png"):
        st.image("data/HSG_Logo_EN_RGB.svg.png", width=200)
with col3:
    if os.path.exists("data/Maastricht_University_logo.svg.png"):
        st.image("data/Maastricht_University_logo.svg.png", width=200)

# Main title and introduction
st.title("Auditing Social Media Platforms Workshop")
st.subheader("Public, Non-Public, and Alternative Data Access Methods under the DSA & GDPR")

# Description
st.markdown("""
## Workshop Overview

This 80-minute workshop guides participants through auditing social media platforms using both 
official DSA-compliant methods and alternative data access techniques. The aim is to give Participants a hollistic overview of current data access methodologies used by researchers and the public for auditing Social Media Platforms.""")

# Presenters section - moved up and styled artistically
st.markdown("""
<div style="padding: 20px 0; text-align: center;">
    <div style="height: 2px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(0,0,120,0.75), rgba(255,255,255,0)); margin: 20px 0;"></div>
    <h2 style="text-align: center; font-family: 'Georgia', serif;">Workshop Presenters</h2>
    <div style="height: 2px; background: linear-gradient(90deg, rgba(255,255,255,0), rgba(120,0,0,0.75), rgba(255,255,255,0)); margin: 20px 0;"></div>
</div>
""", unsafe_allow_html=True)

# Display presenters with photos in 2 rows of 2 columns with equal sizing
col1, col2 = st.columns(2)

image_display_size = 150 # Define a common size for styled images

with col1:
    with st.container():
        st.subheader("Contact Person")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            styled_image_html = load_styled_image("data/aurelia.jpg", size=image_display_size)
            if styled_image_html:
                st.markdown(styled_image_html, unsafe_allow_html=True)
        with col_info:
            st.markdown("**Prof. Dr. Aurelia Tamo-Larrieux**")
            st.markdown("University of Lausanne (Switzerland)")
            st.markdown("Aurelia Tamò-Larrieux is an Associate Professor at the University of Lausanne (UNIL), Faculty of Law, heading the team of Digital and Computational Law and leading the Legal Design & Code Lab. She is also a lecturer at EPFL, teaching Law and Computation to engineers and computer scientists.")
            st.markdown("[Profile](https://www.cpdpconferences.org/persons/aurelia-tamo-larrieux-university-of-lausanne) | [LinkedIn](https://www.linkedin.com/in/aurelia-tamo-larrieux-81a31130b/) | [Website](https://wp.unil.ch/legaldesignandcodelab/)")

with col2:
    with st.container():
        st.subheader("Facilitator")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            styled_image_html = load_styled_image("data/Konrad.jpeg", size=image_display_size)
            if styled_image_html:
                st.markdown(styled_image_html, unsafe_allow_html=True)
        with col_info:
            st.markdown("**Prof. Dr. Konrad Kollnig**")
            st.markdown("Maastricht University (Netherlands)")
            st.markdown("Konrad Kollnig is assistant professor at the Law & Tech Lab of Maastricht University’s Law Faculty. He particularly focuses on the future of AI regulation (in leading the RegTech4AI project with 5 researchers), holding online platforms to account (in the co-leading the CoCoDa project across the UK, Switzerland and the EU) and building a more resilient digital infrastructure (in his latest book).")
            st.markdown("[Profile](https://www.cpdpconferences.org/persons/konrad-kollnig-maastricht-university) | [LinkedIn](https://www.linkedin.com/in/kkollnig/)")

col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.subheader("Host")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            styled_image_html = load_styled_image("data/Luka.jpg", size=image_display_size)
            if styled_image_html:
                st.markdown(styled_image_html, unsafe_allow_html=True)
        with col_info:
            st.markdown("**Luka Bekavac**")
            st.markdown("University of St. Gallen (Switzerland)")
            st.markdown("Luka Bekavac is a doctoral candidate at the University of St. Gallen. His research focuses on understanding and addressing the systemic risks posed by Very Large Online Platforms, combining methods from computer science, tech law and social sciences to study how platforms personalized recommender systems influence us, while developing tools to enhance transparency and accountability in their operation.")
            st.markdown("[Profile](https://www.cpdpconferences.org/persons/luka-bekavac-university-of-st-gallen) | [LinkedIn](https://www.linkedin.com/in/luka-bekavac-80285a1b2/)")

with col4:
    with st.container():
        st.subheader("Facilitator")
        col_img, col_info = st.columns([1, 2])
        with col_img:
            # Apply vertical_shift_px to Simon Mayer's image
            styled_image_html = load_styled_image("data/Simon.png", size=image_display_size, vertical_shift_px=-20)
            if styled_image_html:
                st.markdown(styled_image_html, unsafe_allow_html=True)
        with col_info:
            st.markdown("**Prof. Dr. Simon Mayer**")
            st.markdown("University of St. Gallen (Switzerland)")
            st.markdown("Simon Mayer is a Full Professor in Computer Science at the University of St. Gallen (HSG). He is fascinated by the integration of concepts and approaches from across the fields of pervasive computing, hypermedia, human-computer interaction, and embedded systems to realize ideal interfaces between machines and animals.")
            st.markdown("[Profile](https://www.cpdpconferences.org/persons/simon-mayer-university-of-st-gallen) | [Website](https://ics.unisg.ch/chairs/simon-mayer-interaction-and-communication-based-systems/)")

# Add a Picasso-inspired decorative element
st.markdown("""
<div style="padding: 10px 0; margin: 20px 0; text-align: center;">
    <div style="height: 3px; background: linear-gradient(90deg, rgba(0,0,255,0.5), rgba(255,0,0,0.5), rgba(0,255,0,0.5), rgba(255,255,0,0.5)); margin: 10px 0;"></div>
    <div style="height: 2px; background: linear-gradient(90deg, rgba(255,0,0,0.5), rgba(0,0,255,0.5), rgba(255,255,0,0.5), rgba(0,255,0,0.5)); margin: 8px 0;"></div>
</div>
""", unsafe_allow_html=True)

# Link to CoCoDa project
st.markdown("""
## CoCoDa Project
Our work is part of the [CoCoDa project](https://snsf-cocoda.github.io/), which builds tools to open up 
the concentration and control of data by VLOPs and VLOSEs.

The project aims to:
- Combine technical data access methods with legal innovations like the Digital Services Act.
- Develop techno-legal tools that empower researchers, regulators, and civil society.
- Focus on real-world use cases in social media and mobile apps.
""")

# Workshop structure with links to subpages
st.header("Workshop Structure")

# Display the workshop sections with links
workshop_sections = {
    "1. Introduction": {
        "description": "Set the scene: systemic risk, DSA/GDPR goals, the election use case",
        "time": "10 min",
        "link": "Introduction"
    },
    "2. DSA Tools": {
        "description": "Explore data from DSA Ads Repository, Transparency DB, and Research API",
        "time": "20 min",
        "link": "Dsa_Tools"
    },
    "3. GDPR Tools": {
        "description": "Leveraging Data Rights for Research through data donation methods",
        "time": "10 min",
        "link": "GDPR_Tools"
    },
    "4. SOAP and Scraping": {
        "description": "Systematic Observation of Algorithms and Platforms through sockpuppets and scraping",
        "time": "20 min",
        "link": "SOAP_and_Scraping"
    },
    "5. Legal Uncertainties": {
        "description": "Navigating legal tensions in platform auditing research",
        "time": "15 min",
        "link": "Legal_Uncertainties"
    },
    "6. Conclusion": {
        "description": "Reflections, trade-offs and next steps",
        "time": "5 min",
        "link": "Conclusion"
    }
}

# Display the workshop structure as cards
col1, col2 = st.columns(2)
for i, (section, details) in enumerate(workshop_sections.items()):
    # Alternate between columns
    with col1 if i % 2 == 0 else col2:
        with st.container():
            st.subheader(section)
            st.markdown(f"**Time**: {details['time']}")
            st.markdown(f"**Description**: {details['description']}")
            # Create a button that would typically link to the subpage
            # In Streamlit, we don't need explicit links as the pages are in the sidebar automatically
            st.markdown(f"[Go to section →]({details['link']})")
            st.divider()

# Brief explanation of the navigation
st.info("👈 You can also use the sidebar to navigate between workshop sections.")

# Data Collection Disclaimer
st.markdown("""
## Data Collection & Privacy

During this workshop, we will be collecting some data through interactive polls and surveys. 

- **All data collected is anonymized.** We do not link your responses to any personal identifiers.
- **Your participation is voluntary.** If you prefer not to have your data collected, you can simply choose not to fill out the surveys or polls presented during the workshop.
- **Please keep this website open** throughout the workshop to ensure your anonymous session remains active and any contributions you choose to make are recorded correctly.
- At the end of the workshop, there will be an **option to provide your email address if you would like to share feedback or get in touch** with the presenters. This is entirely optional.

Your engagement helps us understand the effectiveness of these tools and methods. Thank you for your participation!
""")

# Footer with information about the data sources
st.markdown("---")

