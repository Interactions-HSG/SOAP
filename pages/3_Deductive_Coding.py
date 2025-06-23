import streamlit as st
import os
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Deductive Coding - SOAP Workshop",
    page_icon="🏷️",
    layout="wide"
)

st.title("3. Deductive Coding")
st.subheader("LLM-based deductive coding for systematic content analysis")

# Display SOAP system image
try:
    soap_image = Image.open("data/SOAP_system.png")
    st.image(soap_image, caption="SOAP System Architecture for Platform Auditing", use_container_width=True)
except FileNotFoundError:
    st.info("SOAP system diagram not found at data/SOAP_system.png")

# Deductive Coding Introduction
st.markdown("""
## Deductive Coding in SOAP

For SOAP to interact with posts and the platform beyond random interactions, it must understand and categorize the content it encounters to create highly homogeneous feeds or steer the algorithm in specific directions.

To achieve this, the system needs a method to determine whether a post belongs to a particular topic based on a **predefined codebook**, which includes an initial set of codes, descriptions, and examples aligned with the research focus or theoretical framework.

### LLM-Based Approach
SOAP employs an **LLM-based deductive coding approach** by including the multimodal LLM **Gemini 1.5 Flash**, which is capable of analyzing video and audio data alongside text. This LLM-based approach significantly enhances scalability and allows for more comprehensive analysis.

However, acknowledging the limitations of automatic deductive coding, we remain cautious about relying solely on automated processes and therefore employ **cross-validation techniques** to ensure the reliability and accuracy of our approach.
""")

# Sockpuppet Creation Section
st.markdown("""
## Sockpuppet Creation with Users

SOAP creates **sockpuppet accounts** - fake accounts designed to simulate real user behavior for research purposes. These accounts are used to systematically explore how platform algorithms respond to different user behaviors and content preferences.

### Account Creation Strategy
""")

# Display Bot accounts image
try:
    bot_image = Image.open("data/Bot_accounts_workshop_0.1.png")
    st.image(bot_image, caption="Bot Account Creation Process for Research", use_container_width=True)
except FileNotFoundError:
    st.info("Bot accounts diagram not found at data/Bot_accounts_workshop_0.1.png")

st.markdown("""
**Analysis of Results**:
The lower scores for conflict-related content stem largely from **topic ambiguity**: both human coders and the model sometimes disagreed on whether a post referred specifically to Palestine or Israel conflict. 

The LLM, in particular, tended to classify generic war-related imagery as "non-related" unless there was an explicit and identifiable link to the Palestine–Israel conflict. War footage alone was not sufficient for inclusion—the model required contextual cues to assign it to the topic category.

**Key Finding**: Even with lower κ values, the resulting content streams still evolved into clearly homogeneous bubbles. This indicates that **near-perfect label agreement is not a precondition** for SOAP to generate clear filter-bubble effects.

### Multimodal Analysis Capabilities
**Gemini 1.5 Flash** provides comprehensive analysis of social media content:

**Video Analysis**:
- Content object detection and classification
- Scene understanding and context analysis
- Movement and action recognition
- Visual sentiment analysis

**Audio Analysis**:
- Speech-to-text transcription
- Emotional tone detection
- Background audio classification
- Music and sound effect recognition

**Text Analysis**:
- Natural language understanding
- Sentiment and emotion classification
- Topic modeling and categorization
- Language detection and translation


### Deductive Coding Process
**1. Codebook Development**:
- Define categories based on research objectives
- Create clear descriptions and examples for each code
- Establish decision rules for boundary cases
- Test and refine categories on pilot data

**2. Multimodal Content Processing**:
- Extract text, image, video, and audio features
- Apply LLM analysis to all content modalities
- Generate comprehensive content descriptions
- Classify content according to predefined categories

**3. Quality Assurance**:
- Cross-validation with human coders
- Reliability testing across different content types
- Continuous monitoring of coding accuracy
- Regular updates to improve performance
""")

# Hands-On Prompt Testing Section  
st.markdown("""
---
## Hands-On: Prompt Testing with Multimodal Content

Now let's test the deductive coding approach with real videos using the kitten classification prompt developed for SOAP.

### Kitten Classification Prompt
This is the actual prompt used in our filter bubble experiments to classify content as kitten-related:
""")

st.code('''
"Dustin_Henderson44": """You are analyzing Social Media videos that feature cute and adorable kittens.
    Post Description: {post_text}
    Username: {creator_id}
    Please answer the following questions:
    - On a scale of 0 to 5, how much does the video feature or relate to cute and adorable kittens? (0 being not at all and 5 being entirely focused on kittens)
    - What is your reasoning for the score?
    Consider the following topics and rate higher if the video prominently features:
    - Kitten antics (e.g., playful behavior, funny moments)
    - Kitten care (e.g., grooming tips, health advice, feeding information)
    - Kitten milestones (e.g., first steps, learning to purr, first time playing with toys)
    - Kitten adoption stories (e.g., rescue tales, adoption success stories)
    - Kitten interactions with humans and other animals (e.g., cuddling with owners, playing with other pets)
    - Kitten habitats (e.g., cozy beds, playful environments, safe outdoor explorations)
    For example:
    - A video showing kittens playing with each other should be rated higher.
    - A video providing tips on how to care for a new kitten should be rated higher.
    - A video showing a kitten being adopted into a loving home should be rated higher.
    - A video presenting a kitten's first time exploring a new environment should be rated higher.
    - A video exploring different types of kitten toys and how kittens interact with them should be rated higher.
    Give your answer precisely in the following format:
    "Score:Reasoning". For example, "5:The video is entirely about kittens playing and showing their adorable antics." Do not say 'Score' or 'Reasoning' in the answer."
    """
''', language='python')

st.markdown("""
### Test Videos
We'll use sample videos to demonstrate how this classification works in practice:
""")

# Video selection for testing
video_col1, video_col2, video_col3 = st.columns(3)

# Set up the first video (kitten)
with video_col1:
    st.markdown("#### Kitten Video")
    kitten_video_path = "data/kitten.mp4"
    if os.path.exists(kitten_video_path):
        st.video(kitten_video_path)
        st.success("**Expected Result**: Should score 4-5 (highly kitten-related)")
    else:
        st.warning("Kitten video not found. Expected at data/kitten.mp4")

# Set up the second video (dog)
with video_col2:
    st.markdown("#### Dog Video")
    dog_video_path = "data/ws-videos/dog.mp4"
    if os.path.exists(dog_video_path):
        st.video(dog_video_path)
        st.info("**Expected Result**: Should score 0-1 (not kitten-related)")
    else:
        st.warning("Dog video not found. Expected at data/ws-videos/dog.mp4")

# Set up the third video (raccoon)
with video_col3:
    st.markdown("#### Raccoon Video")
    raccoon_video_path = "data/ws-videos/Racoon.mp4"
    if os.path.exists(raccoon_video_path):
        st.video(raccoon_video_path)
        st.info("**Expected Result**: Should score 0-2 (possibly cute but not kittens)")
    else:
        st.warning("Raccoon video not found. Expected at data/ws-videos/Racoon.mp4")

st.markdown("""
### Interactive Testing

In a full implementation, you would:

1. **Load the video content** into the multimodal LLM (Gemini 1.5 Flash)
2. **Apply the kitten classification prompt** with the video as input
3. **Receive structured output** in the format "Score:Reasoning"
4. **Validate results** against human coding for reliability

**Sample Expected Outputs**:
- **Kitten Video**: "5:This video shows adorable kittens playing and displaying typical kitten behaviors. The content is entirely focused on kittens."
- **Dog Video**: "0:This video shows a dog, not a kitten. While the animal may be cute, it does not feature kittens at all."
- **Raccoon Video**: "1:This video shows a raccoon which, while potentially cute and small, is not a kitten. The content does not relate to kitten-specific topics."
""")

# Inter and Intra-Rater Reliability Testing
st.markdown("""
## Inter and Intra-Rater Reliability Testing

To safeguard the integrity of analysis and address limitations of automated coding, we tested the **intra- and inter-reliability** of the model (Gemini 1.5 Flash multimodal LLM) as a labeler.

### Intra-Reliability Validation
We assess the consistency of ratings for the same posts through an **adjusted Test-Retest Reliability procedure**.

**Methodology**:
- Selected **95 posts** from each Explore feed of a sockpuppet account
- Had the model rate each post **5 times**
- Total of **475 ratings per filter bubble**
- Calculated **Cronbach's Alpha** and 95% confidence interval

**Results**: The results demonstrate consistently high scores, indicating that the model reliably produced similar ratings across multiple iterations for the same content.
""")

# Display intra-reliability results table
st.markdown("""
| Filter Bubble | Cronbach's Alpha | 95% Confidence Interval |
|---------------|------------------|-------------------------|
| Aviation | 0.979 | [0.972, 0.985] |
| Kitten | 0.998 | [0.997, 0.998] |
| Palestine/Israel | 0.975 | [0.966, 0.982] |
""")

st.markdown("""
### Inter-Reliability Validation  
We use **Human-to-Human** and **AI-to-Human** inter-rater reliability validation to determine if the model's labels align with human labels.

**Methodology**:
- **Two human labelers** and the model independently labeled the same set of **95 posts** from each sockpuppet account
- **Cohen's Kappa** calculated to compare ratings between:
  - Two human labelers
  - Human labelers and the LLM

**Results**: We observed *substantial* to *high* agreement in the Aviation and Kitten filter bubbles, and *moderate* to *substantial* agreement in the Palestine/Israel filter bubble.
""")



# Display inter-reliability results table
st.markdown("""
| Labelers | Aviation: κ | Kitten: κ | Palestine/Israel: κ |
|----------|-------------|-----------|-------------------|
| Human 1 - Human 2 | 0.9354 | 0.9794 | 0.7407 |
| AI-Human 1 | 0.7705 | 0.7357 | 0.4157 |
| AI-Human 2 | 0.7330 | 0.7158 | 0.5042 |
""")

# Limitations of Automated Deductive Coding
st.markdown("""
## Limitations of Automated Deductive Coding

While SOAP's multimodal LLM approach enables scalable content analysis, several limitations must be acknowledged:

### Behavioral Simulation Boundaries
SOAP does not replicate genuine human behavior. Sockpuppet accounts follow predefined interaction patterns designed for consistency, not behavioral realism. They lack the complex personal, social, and contextual signals used in real personalization algorithms (social graphs, emotional responses, multi-platform activity). Filter bubble effects observed represent system-level responses to controlled inputs, not realistic user experiences.

### Topic-Specific Coding Challenges
**Ambiguous Content**: Open-ended concepts like "woke" or "insulting" content are difficult to measure consistently. LLMs show documented political biases that may influence coding on sensitive topics.

**Harmful Content**: Safety filters in models like Gemini may block analysis of extremist content, limiting research into harmful material. Alternative approaches include using safety scores as indicators or self-hosted models without filters.

**Recent Events**: LLMs have knowledge cutoffs, making fact-checking of very recent events impossible.

### Multimodal LLM Limitations
- **Cultural Context**: Reduced accuracy across languages and underrepresented cultural contexts
- **Training Biases**: Systematic biases from training data affect content interpretation
- **Contextual Judgment**: Lack of nuanced understanding compared to human coders

### Mitigation Strategies
1. **Cross-validation**: Compare machine and human coding for reliability testing
2. **Human Oversight**: Complement automated coding with human annotation for ambiguous topics
3. **Domain Adaptation**: Adapt prompts to specific research domains
4. **Transparency**: Document all prompt templates and evaluation procedures

**Key Insight**: Even with lower coding precision (e.g., Palestine/Israel κ values), SOAP can still create effective filter bubbles, suggesting robustness to imperfect classification. However, findings should be interpreted with caution and supported by human validation.
""")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("← Previous: Data Scraping"):
        st.switch_page("pages/2_Data_Scraping.py")

with col2:
    st.markdown("<div style='text-align: center;'>**Current: Deductive Coding**</div>", unsafe_allow_html=True)

with col3:
    if st.button("Next: Analysis →"):
        st.switch_page("pages/4_Analysis.py")



# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.8em;'>
Part of the FAccT 2025 Workshop: "Auditing Social Media Platforms using SOAP"<br>
University of St. Gallen | CoCoDa Project
</div>
""", unsafe_allow_html=True)
