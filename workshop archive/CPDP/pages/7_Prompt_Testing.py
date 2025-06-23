import streamlit as st
import os
import time
from datetime import datetime
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from dotenv import load_dotenv
import json
from google.api_core.exceptions import InvalidArgument, PermissionDenied, ResourceExhausted
from google.cloud import storage
from PIL import Image

class StreamlitPromptTester:
    """Class for testing Vertex AI prompts through a Streamlit interface"""
    
    def __init__(self):
        # Load environment variables - first try .env file, then Streamlit secrets
        load_dotenv()
        
        # Try to get from environment, otherwise from Streamlit secrets
        if 'BUCKET_NAME' in os.environ:
            self.bucket_name = os.environ['BUCKET_NAME']
        elif 'env' in st.secrets and 'BUCKET_NAME' in st.secrets['env']:
            self.bucket_name = st.secrets['env']['BUCKET_NAME']
        else:
            self.bucket_name = 'ics-tests'  # Default fallback
            
        if 'PROJECT_NAME' in os.environ:
            self.project = os.environ['PROJECT_NAME']
        elif 'env' in st.secrets and 'PROJECT_NAME' in st.secrets['env']:
            self.project = st.secrets['env']['PROJECT_NAME']
        else:
            self.project = 'feisty-deck-424609-e3'  # Default fallback
            
        if 'USERNAME' in os.environ:
            self.username = os.environ['USERNAME']
        elif 'env' in st.secrets and 'USERNAME' in st.secrets['env']:
            self.username = st.secrets['env']['USERNAME']
        else:
            self.username = 'workshop_user'  # Default fallback
        
        # Initialize the VertexAI client using credentials
        try:
            # Check if we're running on Streamlit Cloud (use secrets)
            if 'gcp_service_account' in st.secrets:
                import json
                import tempfile
                
                # Method 1: Try direct initialization with service account credentials
                try:
                    from google.oauth2 import service_account
                    
                    # Convert secrets to correct format if needed
                    if isinstance(st.secrets['gcp_service_account'], dict):
                        credentials = service_account.Credentials.from_service_account_info(
                            st.secrets['gcp_service_account']
                        )
                    else:
                        # Handle AttrDict or other types by converting to dict
                        cred_dict = {}
                        for key in st.secrets['gcp_service_account']:
                            cred_dict[key] = st.secrets['gcp_service_account'][key]
                        credentials = service_account.Credentials.from_service_account_info(cred_dict)
                    
                    # Initialize with credentials object directly
                    vertexai.init(
                        project=self.project,
                        location="us-central1",
                        credentials=credentials
                    )
                    st.info("Initialized using direct credentials approach")
                    self.model = GenerativeModel("gemini-1.5-flash")
                    self.model_initialized = True
                except Exception as direct_e:
                    st.warning(f"Direct initialization failed: {direct_e}")
                    
                    # Method 2: Try the temp file approach as fallback
                    try:
                        # Safely extract keys from credentials and recreate a clean dict
                        cred_dict = {}
                        for key, value in dict(st.secrets['gcp_service_account']).items():
                            if isinstance(value, (str, int, bool, list, dict)):
                                cred_dict[key] = value
                            else:
                                # Convert non-serializable types to string
                                cred_dict[key] = str(value)
                        
                        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp:
                            json.dump(cred_dict, temp)
                            temp_creds_path = temp.name
                        
                        # Set the credentials path in environment
                        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_creds_path
                        st.info(f"Using credentials from Streamlit secrets via temporary file")
                        
                        # Initialize Vertex AI with project and location
                        vertexai.init(
                            project=self.project,
                            location="us-central1",
                        )
                        self.model = GenerativeModel("gemini-1.5-flash")
                        self.model_initialized = True
                    except Exception as temp_e:
                        st.error(f"Temp file approach failed: {temp_e}")
                        raise
            
            # Otherwise check if GOOGLE_APPLICATION_CREDENTIALS is set locally
            elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
                st.info(f"Using credentials from local environment: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
                
                # Initialize Vertex AI with project and location
                vertexai.init(
                    project=self.project,
                    location="us-central1",
                )
                self.model = GenerativeModel("gemini-1.5-flash")
                self.model_initialized = True
            
            # If no credentials source found yet, try default credentials
            else:
                st.info("Using default application credentials")
                vertexai.init(
                    project=self.project,
                    location="us-central1",
                )
                self.model = GenerativeModel("gemini-1.5-flash")
                self.model_initialized = True
                
            # Only show success if we haven't raised an exception
            if self.model_initialized:
                st.success("Connected to Vertex AI successfully!")
                
        except Exception as e:
            st.error(f"Failed to initialize Vertex AI: {e}")
            st.info("Attempting to use already initialized VertexAI connection if available...")
            try:
                # Try to create model without explicit initialization
                self.model = GenerativeModel("gemini-1.5-flash")
                self.model_initialized = True
                st.success("Connected to Vertex AI using existing credentials!")
            except Exception as e2:
                st.error(f"Second attempt failed: {e2}")
                self.model_initialized = False
        
        # Clean up temporary file if it exists
        if 'temp_creds_path' in locals():
            try:
                os.unlink(temp_creds_path)
            except:
                pass

    def process_response(self, response):
        """Process the response from the generative model."""
        response = response.replace("\n", " ")
        if ":" in response:
            reversed_response = response[::-1]
            reversed_score, reversed_interpretation = reversed_response.split(":", 1)
            interpretation = reversed_interpretation[::-1].strip()
            score = reversed_score[::-1].strip()
        else:
            interpretation, score = response, "No score provided"
        return interpretation, score
    
    def upload_to_bucket(self, file_bytes, file_name):
        """Upload a file to Google Cloud Storage bucket"""
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket_name)
            blob_name = f"{self.username}/{file_name}"
            blob = bucket.blob(blob_name)
            
            # Upload the file to GCS
            blob.upload_from_string(file_bytes, content_type="video/mp4")
            
            # Return the GCS URI
            return f"gs://{self.bucket_name}/{blob_name}"
        except Exception as e:
            st.error(f"Error uploading to Google Cloud Storage: {e}")
            return None
        
    def test_prompt_with_part(self, primer, video_part):
        """Test the prompt with the Vertex AI model using a pre-created Part object
        
        Args:
            primer: The text prompt to analyze the video
            video_part: A Part object representing the video content
        """
        # Even if initialization failed earlier, try one more time here
        if not self.model_initialized:
            try:
                # Try directly creating the model without initialization
                self.model = GenerativeModel("gemini-1.5-flash")
                self.model_initialized = True
                st.success("Connected to Vertex AI using implicit credentials!")
            except Exception as e:
                return None, f"Failed to initialize model: {e}"
        
        try:
            # Set up the generation configuration
            generation_config = {
                "max_output_tokens": 2048,
                "temperature": 1,
                "top_p": 0.95,
            }
            
            safety_settings = {
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
            
            # Generate content with the provided Part object
            try:
                response = self.model.generate_content(
                    [video_part, primer],  # Combine video part with the primer
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    stream=False,
                )
                
                # Process the response
                interpretation, score = self.process_response(response.text)
                return interpretation, score
                
            except InvalidArgument as e:
                st.error(f"Invalid argument error: {e}")
                return None, f"Error: {e}"
            except PermissionDenied as e:
                if "rate limit" in str(e):
                    st.warning(f"Rate limit reached. Waiting for 10 seconds before retrying.")
                    time.sleep(10)
                    # Try again with a simplified request
                    try:
                        response = self.model.generate_content(
                            [primer],  # Text-only as fallback
                            generation_config=generation_config,
                            safety_settings=safety_settings,
                            stream=False,
                        )
                        interpretation, score = self.process_response(response.text)
                        return interpretation, score
                    except Exception as retry_error:
                        return None, f"Retry failed: {retry_error}"
                else:
                    return None, f"Permission denied: {e}"
            except ResourceExhausted as e:
                return None, f"Resource quota exceeded: {e}"
                
        except Exception as e:
            # Handle any exceptions that occur during generation
            error_message = str(e)
            if "SAFETY" in error_message:
                return "Content flagged for safety reasons", "5"
            else:
                return None, f"Error: {error_message}"
    
    def test_prompt(self, primer, video_file=None, video_path=None):
        """Test the prompt with the Vertex AI model
        
        Args:
            primer: The text prompt to analyze the video
            video_file: A Streamlit uploaded file object (has getvalue() method)
            video_path: String path to a video file on the filesystem
        """
        if not self.model_initialized:
            return None, "Model initialization failed. Check your credentials."
        
        try:
            # Set up the generation configuration
            generation_config = {
                "max_output_tokens": 2048,
                "temperature": 1,
                "top_p": 0.95,
            }
            
            safety_settings = {
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }
            
            # Prepare content for the model
            videos = []
            
            # Option 1: Process the uploaded file from Streamlit
            if video_file is not None:
                video_bytes = video_file.getvalue()
                video_name = f"test_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                
                # Upload to GCS
                gcs_uri = self.upload_to_bucket(video_bytes, video_name)
                
                if gcs_uri:
                    # Add the video to the content parts
                    videos.append(Part.from_uri(mime_type="video/mp4", uri=gcs_uri))
                else:
                    st.warning("Could not upload video from file upload. Using text-only prompt.")
            
            # Option 2: Process a video path from the filesystem
            elif video_path is not None and os.path.exists(video_path):
                # Read the video file
                with open(video_path, "rb") as f:
                    video_bytes = f.read()
                
                video_name = os.path.basename(video_path)
                gcs_uri = self.upload_to_bucket(video_bytes, video_name)
                
                if gcs_uri:
                    videos.append(Part.from_uri(mime_type="video/mp4", uri=gcs_uri))
                else:
                    st.warning("Could not upload video from path. Using text-only prompt.")
            
            # Option 3: Use a default video if nothing else is provided
            else:
                sample_video_path = os.path.join("data", "sample_video.mp4")
                if os.path.exists(sample_video_path):
                    # Upload sample video
                    with open(sample_video_path, "rb") as f:
                        video_bytes = f.read()
                    
                    video_name = "sample_video.mp4"
                    gcs_uri = self.upload_to_bucket(video_bytes, video_name)
                    
                    if gcs_uri:
                        videos.append(Part.from_uri(mime_type="video/mp4", uri=gcs_uri))
                    else:
                        st.warning("Could not upload sample video. Using text-only prompt.")
                else:
                    st.warning("No video provided and sample video not found. Using text-only prompt.")
            
            # Generate content
            try:
                response = self.model.generate_content(
                    videos + [primer],  # Combine videos with the primer
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    stream=False,
                )
                
                # Process the response
                interpretation, score = self.process_response(response.text)
                return interpretation, score
                
            except InvalidArgument as e:
                st.error(f"Invalid argument error: {e}")
                return None, f"Error: {e}"
            except PermissionDenied as e:
                if "rate limit" in str(e):
                    st.warning(f"Rate limit reached. Waiting for 10 seconds before retrying.")
                    time.sleep(10)
                    # Try again with a simplified request
                    try:
                        response = self.model.generate_content(
                            [primer],  # Text-only as fallback
                            generation_config=generation_config,
                            safety_settings=safety_settings,
                            stream=False,
                        )
                        interpretation, score = self.process_response(response.text)
                        return interpretation, score
                    except Exception as retry_error:
                        return None, f"Retry failed: {retry_error}"
                else:
                    return None, f"Permission denied: {e}"
            except ResourceExhausted as e:
                return None, f"Resource quota exceeded: {e}"
                
        except Exception as e:
            # Handle any exceptions that occur during generation
            error_message = str(e)
            if "SAFETY" in error_message:
                return "Content flagged for safety reasons", "5"
            else:
                return None, f"Error: {error_message}"


# Page configuration
st.set_page_config(
    page_title="Prompt Testing | Social Media Auditing Workshop",
    page_icon="🔬",
    layout="wide"
)

# Page title and header
st.title("7. Deductive Coding with Multimodal LLMs")
st.subheader("Testing Vertex AI Prompts for Social Media Analysis")

# Introduction to the prompt testing feature
st.markdown("""
This tool allows you to experiment with different primer prompts for deductive coding of social media content.
Enter your prompt below and see how the Vertex AI model interprets the provided test videos using your instructions.

Two videos are provided for testing your prompts: a dog video and a raccoon video. Select which video you want to analyze
and customize your prompt to see how the model responds to different instructions.
""")

# Create a row for the two columns layout
col1, col2 = st.columns([3, 1])

with col1:
    # Text area for entering the prompt
    primer_prompt = st.text_area(
        "Enter your primer prompt for content analysis:", 
        height=200,
        value="""Analyze this video with particular attention to the following:
1. Content type (informational, promotional, entertainment)
2. Target audience demographic
3. Main message or intent
4. Potential political alignment or bias (if any)
5. Emotional tone (positive, negative, neutral)

Rate the content on a scale of 1-5 for potential societal impact, where:
1 = Minimal impact
3 = Moderate impact
5 = Significant impact

Provide your interpretation first, followed by the numerical rating in this format:
[Your interpretation]: [rating 1-5]"""
    )

with col2:
    st.markdown("### Example Prompt Components")
    st.info("""
    Consider including:
    
    - Content categorization criteria
    - Emotional tone assessment
    - Political bias detection
    - Rating scale instructions
    - Specific output format
    """)

# Video selection for testing
st.subheader("Select Video for Testing")

# Define direct GCloud links to the videos
dog_video_gcs_uri = "gs://ics-tests/dog.mp4"
raccoon_video_gcs_uri = "gs://ics-tests/Racoon.mp4"

# Also keep local paths for displaying in the UI
dog_video_path = os.path.join("data", "ws-videos", "dog.mp4")
raccoon_video_path = os.path.join("data", "ws-videos", "Racoon.mp4")

# Create columns for the two videos
video_col1, video_col2 = st.columns(2)

# Set up the first video (dog)
with video_col1:
    st.markdown("### Dog Video")
    if os.path.exists(dog_video_path):
        st.video(dog_video_path)
    else:
        # If local file doesn't exist, show public link
        st.markdown("Video should be downloaded to `data/ws-videos/dog.mp4`")
        # Try alternate URL format
        try:
            st.video("https://storage.googleapis.com/ics-tests/dog.mp4")
        except Exception as e:
            st.error(f"Cannot display dog video: {e}")

# Set up the second video (raccoon)
with video_col2:
    st.markdown("### Raccoon Video")
    if os.path.exists(raccoon_video_path):
        st.video(raccoon_video_path)
    else:
        # If local file doesn't exist, show public link
        st.markdown("Video should be downloaded to `data/ws-videos/Racoon.mp4`")
        # Try alternate URL format
        try:
            st.video("https://storage.googleapis.com/ics-tests/Racoon.mp4")
        except Exception as e:
            st.error(f"Cannot display raccoon video: {e}")

# Radio button to select which video to test
selected_video = st.radio(
    "Select which video to test:",
    ["Dog Video", "Raccoon Video"],
    horizontal=True
)

# Set the selected video GCS URI based on user choice
if selected_video == "Dog Video":
    selected_video_gcs_uri = dog_video_gcs_uri
    st.info("Dog video selected for testing.")
else:
    selected_video_gcs_uri = raccoon_video_gcs_uri
    st.info("Raccoon video selected for testing.")

# Button to run the test
run_col1, run_col2 = st.columns([1, 2])
with run_col1:
    run_test = st.button("Test Prompt", type="primary")
    
if run_test:
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize the prompt tester
    tester = StreamlitPromptTester()
    
    # Display a loading message
    status_text.info("Initializing test...")
    progress_bar.progress(10)
    
    # Update progress
    status_text.info("Preparing video content...")
    progress_bar.progress(30)
    
    # Test the prompt
    with st.spinner(f"Processing {selected_video} with Vertex AI... this may take up to 30 seconds"):
        # Create a Part object directly from the GCS URI
        video_part = Part.from_uri(mime_type="video/mp4", uri=selected_video_gcs_uri)
        
        # Call a custom function that uses the Part directly
        interpretation, score = tester.test_prompt_with_part(primer_prompt, video_part)
    
    # Update progress
    progress_bar.progress(100)
    status_text.success("Analysis complete!")
    
    # Display the results
    st.subheader("Results")
    if interpretation:
        st.success(f"Content analyzed successfully!")
        
        results_col1, results_col2 = st.columns([3, 1])
        
        with results_col1:
            st.markdown("### Interpretation")
            st.write(interpretation)
        
        with results_col2:
            st.markdown("### Impact Score")
            
            # Try to convert score to numeric if possible
            try:
                numeric_score = float(score)
                st.metric("Rating", numeric_score, delta=None, delta_color="off")
            except ValueError:
                st.write(f"**Rating**: {score}")
        
        # Display the full raw response for debugging
        with st.expander("Raw Response"):
            st.code(f"{interpretation}: {score}")
            
        # Offer suggestions for improving the prompt
        st.subheader("Prompt Analysis")
        st.markdown("""
        ### Was the result what you expected?
        
        If not, consider:
        - Adding more specific rating criteria
        - Clarifying the output format requirements
        - Focusing on specific aspects of the content
        - Providing examples of good and bad analyses
        """)
    else:
        st.error(f"Failed to get a valid interpretation. Error: {score}")

# Tips section
with st.expander("Tips for Effective Prompts"):
    st.markdown("""
    ### Best Practices for Creating Effective Prompts
    
    1. **Be specific with your instructions**: Clearly state what aspects of the content you want analyzed
    2. **Define your rating scales**: Explain what each number on your rating scale represents
    3. **Specify the output format**: Tell the model exactly how you want the results structured
    4. **Include examples**: If possible, include examples of good analyses to guide the model
    5. **Consider the context**: Include relevant contextual information about the platform or content type
    
    Remember that the quality of the AI's analysis depends significantly on the clarity and specificity of your prompt.
    """)
    
# Information about the implementation
with st.expander("About this Tool"):
    st.markdown("""
    This tool uses Google's Vertex AI with the Gemini 1.5 Flash model to analyze social media content. 
    The tool is designed to help researchers develop and test prompts for deductive coding of platform content.
    
    In a real implementation, the tool would process actual videos from the platform rather than placeholders.
    
    For more information on how to use this in your research, refer to the workshop materials or contact the workshop facilitators.
    """)

# Navigation buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    prev_button = st.button("← Back to SOAP and Scraping")
    if prev_button:
        st.switch_page("pages/4_SOAP_and_Scraping.py")

with col2:
    next_button = st.button("Next: Legal Uncertainties →")
    if next_button:
        st.switch_page("pages/5_Legal_Uncertainties.py")
