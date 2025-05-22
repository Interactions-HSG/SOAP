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
        # Load environment variables
        load_dotenv()
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.project = os.getenv('PROJECT_NAME')
        self.username = os.getenv('USERNAME', 'workshop_user')
        
        # Initialize the VertexAI client if credentials are available
        try:
            vertexai.init(project=self.project, location="us-central1")
            self.model = GenerativeModel("gemini-1.5-flash")
            self.model_initialized = True
            st.success("Connected to Vertex AI successfully!")
        except Exception as e:
            st.error(f"Failed to initialize Vertex AI: {e}")
            self.model_initialized = False

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
        
    def test_prompt(self, primer, video_file=None):
        """Test the prompt with the Vertex AI model"""
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
            
            # If we have a video file, process it
            if video_file is not None:
                # For a real file uploaded through Streamlit
                video_bytes = video_file.getvalue()
                video_name = f"test_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                
                # Upload to GCS
                gcs_uri = self.upload_to_bucket(video_bytes, video_name)
                
                if gcs_uri:
                    # Add the video to the content parts
                    videos.append(Part.from_uri(mime_type="video/mp4", uri=gcs_uri))
                else:
                    st.warning("Could not upload video. Using text-only prompt.")
            else:
                # Use a default video if available
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
                    st.warning("Sample video not found. Using text-only prompt.")
            
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


def display_prompt_testing_ui():
    """Display the Streamlit UI for testing prompts"""
    st.title("Deductive Coding with Multimodal LLMs")
    
    # Introduction to the prompt testing feature
    st.markdown("""
    This tool allows you to experiment with different primer prompts for deductive coding of social media content.
    Enter your prompt below and see how the Vertex AI model would interpret content using your instructions.
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
    
    # Options for testing
    st.subheader("Test Options")
    
    test_option = st.radio(
        "Choose a test method:",
        ["Use sample video", "Upload your own video"]
    )
    
    uploaded_video = None
    if test_option == "Upload your own video":
        uploaded_video = st.file_uploader("Upload a video file (MP4 format recommended)", type=["mp4", "mov", "avi"])
        
        if uploaded_video:
            st.video(uploaded_video)
            st.caption(f"File name: {uploaded_video.name}, Size: {round(uploaded_video.size/1024/1024, 2)} MB")
    else:
        st.info("The system will use a sample video from the workshop materials.")
        
        # Check if we have a sample video to display
        sample_video_path = os.path.join("data", "sample_video.mp4")
        if os.path.exists(sample_video_path):
            st.video(sample_video_path)
        else:
            st.warning("""
            No sample video is available. Please:
            1. Add a sample_video.mp4 file to the 'data' directory, or
            2. Upload your own video using the option above
            
            Without a video, the system will run in text-only mode, which may limit accuracy.
            """)
    
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
        with st.spinner("Processing with Vertex AI... this may take up to 30 seconds"):
            interpretation, score = tester.test_prompt(primer_prompt, uploaded_video)
        
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

if __name__ == "__main__":
    display_prompt_testing_ui()
