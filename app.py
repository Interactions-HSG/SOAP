import streamlit as st
import os
from PIL import Image, ImageOps # Import ImageOps
from io import BytesIO
import base64

# Page configuration
st.set_page_config(
    page_title="Flag&Safe Workshop",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display logos at the top
col1, col2, col3 = st.columns(3)
with col1:
    st.image("data/Logo_Université_de_Lausanne.png", width=250)
with col2:
    st.image("data/HSG_Logo_EN_RGB.svg.png", width=250)
with col3:
    st.image("data/Halden-logo.jpg", width=250)

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

# Remove logos section as it's not relevant for the new workshop

# Main title and introduction
st.title("Flag&Safe Workshop an der Pimarschule Halden")

st.subheader("Ein Workshop zu sicheren Online-Praktiken")

# Description
st.markdown("""
## Workshop-Überblick

Dieser Workshop konzentriert sich auf die Förderung sicheren Online-Verhaltens durch zwei Schlüsselaktivitäten: das Melden unangemessener Inhalte an Flaggy und das verantwortungsvolle Teilen von Inhalten mit Lehrern.

Die Teilnehmer lernen, schädliche Inhalte zu identifizieren und zu melden, sowie die Bedeutung des sicheren Teilens im Internet zu verstehen.

Für weitere Informationen besuche [www.flag-safe.ch](https://www.flag-safe.ch).
""")

# Remove presenters section

# Remove decorative elements and CoCoDa project section

# Workshop structure with links to subpages
st.header("Workshop Structure")

# Display the workshop sections with links
workshop_sections = {
    "1. Inhalte an Flaggy melden": {
        "description": "Wie man unangemessene Inhalte mit Flaggy meldet",
        "time": "15 min",
        "link": "Reporting"
    },
    "2. Inhalte mit Lehrern teilen": {
        "description": "Bewährte Praktiken für das sichere Teilen von Inhalten mit Lehrern",
        "time": "15 min",
        "link": "Sharing"
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
            st.markdown(f"[Go to section →]({details['link']})")
            st.divider()

# Remove headers for website and Git repo

# Brief explanation of the navigation
st.info("👈 Du kannst auch die Seitenleiste verwenden, um zwischen den Workshop-Abschnitten zu navigieren.")

# Footer with information about the data sources
st.markdown("---")
st.markdown("Für weitere Ressourcen besuche [www.flag-safe.ch](https://www.flag-safe.ch).")