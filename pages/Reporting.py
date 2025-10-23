import streamlit as st
import os
import time
from datetime import datetime
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from dotenv import load_dotenv
import json
import uuid
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
        elif hasattr(st, 'secrets') and 'env' in st.secrets and 'BUCKET_NAME' in st.secrets['env']:
            self.bucket_name = st.secrets['env']['BUCKET_NAME']
        else:
            self.bucket_name = 'ics-tests'  # Default fallback
            
        if 'PROJECT_NAME' in os.environ:
            self.project = os.environ['PROJECT_NAME']
        elif hasattr(st, 'secrets') and 'env' in st.secrets and 'PROJECT_NAME' in st.secrets['env']:
            self.project = st.secrets['env']['PROJECT_NAME']
        else:
            self.project = 'feisty-deck-424609-e3'  # Default fallback
            
        if 'USERNAME' in os.environ:
            self.username = os.environ['USERNAME']
        elif hasattr(st, 'secrets') and 'env' in st.secrets and 'USERNAME' in st.secrets['env']:
            self.username = st.secrets['env']['USERNAME']
        else:
            self.username = 'workshop_user'  # Default fallback
        
        # Initialize the VertexAI client using credentials
        try:
            # Check if we're running on Streamlit Cloud (use secrets)
            if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
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
                    # st.info("Initialized using direct credentials approach")
                    self.model = GenerativeModel("gemini-2.5-flash")
                    self.model_initialized = True
                except Exception as direct_e:
                    # st.warning(f"Direct initialization failed: {direct_e}")
                    
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
                        # st.info(f"Using credentials from Streamlit secrets via temporary file")
                        
                        # Initialize Vertex AI with project and location
                        vertexai.init(
                            project=self.project,
                            location="us-central1",
                        )
                        self.model = GenerativeModel("gemini-2.5-flash")
                        self.model_initialized = True
                    except Exception as temp_e:
                        # st.error(f"Temp file approach failed: {temp_e}")
                        raise
            
            # Otherwise check if GOOGLE_APPLICATION_CREDENTIALS is set locally
            elif 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
                # st.info(f"Using credentials from local environment: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
                
                # Initialize Vertex AI with project and location
                vertexai.init(
                    project=self.project,
                    location="us-central1",
                )
                self.model = GenerativeModel("gemini-2.5-flash")
                self.model_initialized = True
            
            # If no credentials source found yet, try default credentials
            else:
                # st.info("Using default application credentials")
                vertexai.init(
                    project=self.project,
                    location="us-central1",
                )
                self.model = GenerativeModel("gemini-2.5-flash")
                self.model_initialized = True
                
            # Only show success if we haven't raised an exception
            if self.model_initialized:
                # st.success("Connected to Vertex AI successfully!")
                pass
                
        except Exception as e:
            # st.error(f"Failed to initialize Vertex AI: {e}")
            # st.info("Attempting to use already initialized VertexAI connection if available...")
            try:
                # Try to create model without explicit initialization
                self.model = GenerativeModel("gemini-2.5-flash")
                self.model_initialized = True
                # st.success("Connected to Vertex AI using existing credentials!")
            except Exception as e2:
                # st.error(f"Second attempt failed: {e2}")
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
    
    def test_prompt_with_part_text_only(self, primer):
        """Test the prompt with the Vertex AI model using text-only (no video)
        
        Args:
            primer: The text prompt for conversation continuation
        """
        # Even if initialization failed earlier, try one more time here
        if not self.model_initialized:
            try:
                # Try directly creating the model without initialization
                self.model = GenerativeModel("gemini-2.5-flash")
                self.model_initialized = True
                # st.success("Connected to Vertex AI using implicit credentials!")
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
            
            # Debug: Log what we're sending
            # st.write(f"Sending text-only request to Vertex AI")
            # st.write(f"Primer length: {len(primer)} characters")
            
            # Generate content with text only
            try:
                response = self.model.generate_content(
                    [primer],  # Text-only
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    stream=False,
                )
                
                # Debug: Print response details
                # st.write("API Response received successfully")
                # st.write(f"Response text: {response.text}")
                
                # Process the response
                interpretation, score = self.process_response(response.text)
                return interpretation, score
                
            except Exception as e:
                # st.error(f"Error in text-only generation: {e}")
                st.write(f"Full error details: {str(e)}")
                return None, f"Error: {e}"
                
        except Exception as e:
            # Handle any exceptions that occur during generation
            error_message = str(e)
            # st.error(f"General exception occurred: {error_message}")
            if "SAFETY" in error_message:
                return "Content flagged for safety reasons", "5"
            else:
                return None, f"Error: {error_message}"
        
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
                self.model = GenerativeModel("gemini-2.5-flash")
                self.model_initialized = True
                # st.success("Connected to Vertex AI using implicit credentials!")
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
            
            # Debug: Log what we're sending
            # st.write(f"Sending request to Vertex AI with video URI: {video_part}")
            # st.write(f"Primer length: {len(primer)} characters")
            
            # Generate content with the provided Part object
            try:
                response = self.model.generate_content(
                    [video_part, primer],  # Combine video part with the primer
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    stream=False,
                )
                
                # Debug: Print response details
                # st.write("API Response received successfully")
                # st.write(f"Response text: {response.text}")
                # st.write(f"Response candidates: {len(response.candidates) if response.candidates else 0}")
                # if response.candidates:
                #     for i, candidate in enumerate(response.candidates):
                #         st.write(f"Candidate {i}: finish_reason={candidate.finish_reason}")
                #         if hasattr(candidate, 'safety_ratings'):
                #             st.write(f"Safety ratings: {candidate.safety_ratings}")
                
                # Process the response
                interpretation, score = self.process_response(response.text)
                return interpretation, score
                
            except InvalidArgument as e:
                # st.error(f"Invalid argument error: {e}")
                st.write(f"Full error details: {str(e)}")
                return None, f"Error: {e}"
            except PermissionDenied as e:
                if "rate limit" in str(e):
                    # st.warning(f"Rate limit reached. Waiting for 10 seconds before retrying.")
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
                        # st.error(f"Retry failed: {retry_error}")
                        st.write(f"Retry error details: {str(retry_error)}")
                        return None, f"Retry failed: {retry_error}"
                else:
                    # st.error(f"Permission denied: {e}")
                    st.write(f"Permission error details: {str(e)}")
                    return None, f"Permission denied: {e}"
            except ResourceExhausted as e:
                # st.error(f"Resource quota exceeded: {e}")
                st.write(f"Resource error details: {str(e)}")
                return None, f"Resource quota exceeded: {e}"
                
        except Exception as e:
            # Handle any exceptions that occur during generation
            error_message = str(e)
            # st.error(f"General exception occurred: {error_message}")
            st.write(f"Exception type: {type(e).__name__}")
            st.write(f"Full exception details: {repr(e)}")
            if "SAFETY" in error_message:
                return "Content flagged for safety reasons", "5"
            else:
                return None, f"Error: {error_message}"

# Page configuration
st.set_page_config(
    page_title="Inhalte melden | Flag&Safe Workshop",
    page_icon="🚩",
    layout="wide"
)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Initialize session state for video analysis status
if 'video_analyzed' not in st.session_state:
    st.session_state.video_analyzed = False

# Initialize session state for current video
if 'current_video' not in st.session_state:
    st.session_state.current_video = None

# Initialize session state for workshop completion
if 'workshop_notice_shown' not in st.session_state:
    st.session_state.workshop_notice_shown = False

if 'workshop_choice_made' not in st.session_state:
    st.session_state.workshop_choice_made = False

if 'continue_conversation' not in st.session_state:
    st.session_state.continue_conversation = False

if 'workshop_completed' not in st.session_state:
    st.session_state.workshop_completed = False

# Initialize session state for input counter
if 'input_counter' not in st.session_state:
    st.session_state.input_counter = 0

# Initialize session state for username
if 'username' not in st.session_state:
    st.session_state.username = ""

# Title
st.title("Inhalte an Flaggy melden")
st.subheader("Lerne, schädliche Inhalte zu erkennen und zu melden")

# Username input
st.markdown("### 👤 Wie heißt du?")
user_username = st.text_input(
    "Gib deinen Namen ein:",
    value=st.session_state.username,
    placeholder="z.B. Artiger Anton, Brave Beatrice, oder Clara Clever",
    help="Dieser Name wird nur für die Workshop-Auswertung verwendet."
)

# Update session state when username changes
if user_username != st.session_state.username:
    st.session_state.username = user_username

# Introduction
st.markdown("""
Willkommen beim Chatbot für sicheres Surfen! Hier kannst du Videos auswählen und mir erzählen, was du darüber denkst.
Ich helfe dir, schädliche Inhalte zu erkennen und erkläre, wie du sie bei Flaggy melden kannst.

**So funktioniert's:**
1. Wähle ein Video aus
2. Erzähl mir, was du darüber denkst oder was dich gestört hat
3. Ich höre zu und helfe dir, deine Gefühle zu verstehen
4. Gemeinsam können wir entscheiden, was die nächsten Schritte sind

Wähle ein Video aus und schreibe mir eine Nachricht!
""")

# Video selection
st.subheader("Wähle ein Video aus")

# Define video paths
crash_video_path = os.path.join("data", "ws-videos", "Crash.mp4")
duolingo_video_path = os.path.join("data", "ws-videos", "Duolingo.mp4")
killtheboss_video_path = os.path.join("data", "ws-videos", "KillTheBoss.mp4")

# GCS URIs
crash_video_gcs_uri = "gs://ics-tests/Crash.mp4"
duolingo_video_gcs_uri = "gs://ics-tests/Duolingo.mp4"
killtheboss_video_gcs_uri = "gs://ics-tests/KillTheBoss.mp4"

# Create columns for videos
video_col1, video_col2, video_col3 = st.columns(3)

with video_col1:
    st.markdown("### Crash Video")
    if os.path.exists(crash_video_path):
        st.video(crash_video_path)
    else:
        st.video("https://storage.cloud.google.com/ics-tests/Crash.mp4")

with video_col2:
    st.markdown("### Duolingo Video")
    if os.path.exists(duolingo_video_path):
        st.video(duolingo_video_path)
    else:
        st.video("https://storage.googleapis.com/ics-tests/Duolingo.mp4")

with video_col3:
    st.markdown("### KillTheBoss Video")
    if os.path.exists(killtheboss_video_path):
        st.video(killtheboss_video_path)
    else:
        st.video("https://storage.googleapis.com/ics-tests/KillTheBoss.mp4")

# Radio button to select video
selected_video = st.radio(
    "Welches Video möchtest du analysieren?",
    ["Crash Video", "Duolingo Video", "KillTheBoss Video"],
    horizontal=True
)

if selected_video == "Crash Video":
    selected_video_gcs_uri = crash_video_gcs_uri
elif selected_video == "Duolingo Video":
    selected_video_gcs_uri = duolingo_video_gcs_uri
else:
    selected_video_gcs_uri = killtheboss_video_gcs_uri

# Check if video changed
if st.session_state.current_video != selected_video:
    st.session_state.current_video = selected_video
    st.session_state.video_analyzed = False
    st.session_state.workshop_notice_shown = False
    st.session_state.workshop_choice_made = False
    st.session_state.continue_conversation = False
    st.session_state.workshop_completed = False
    if 'input_counter' in st.session_state:
        st.session_state.input_counter += 1  # Reset input field
    # Clear chat history when switching videos
    st.session_state.chat_history = []

# Chat interface
st.subheader("Chat mit dem Sicherheits-Bot")

# Count user messages
user_message_count = len([msg for msg in st.session_state.chat_history if msg['role'] == 'user'])

# Always display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div style="background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #2196f3;">
                <strong>Du:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: #f5f5f5; padding: 10px; border-radius: 10px; margin: 5px 0; border-left: 4px solid #4caf50;">
                <strong>🤖 Flaggy:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)

# Check if we should show workshop completion
if user_message_count >= 3 and not st.session_state.workshop_completed:
    if not st.session_state.workshop_choice_made:
        # Show workshop choice options
        st.info("🎯 **Super!** Du hast schon 3 Nachrichten geschrieben. Jetzt hast du zwei Möglichkeiten:")
        
        st.markdown("**Option 1:** 💬 **Weiter reden** - Wir können noch 3 weitere Nachrichten austauschen")
        st.markdown("**Option 2:** 📝 **Zusammenfassung** - Ich fasse unser Gespräch zusammen und wir reden darüber, wie wir die Infos teilen können")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💬 Weiter reden (noch 3 Nachrichten)", use_container_width=True):
                st.session_state.continue_conversation = True
                st.session_state.workshop_choice_made = True
                st.success("Okay! Lass uns noch ein bisschen weiterreden. Du kannst noch 3 Nachrichten schicken!")
                st.rerun()
        
        with col2:
            if st.button("📝 Zusammenfassung & Teilen", use_container_width=True):
                st.session_state.continue_conversation = False
                st.session_state.workshop_choice_made = True
                st.rerun()
    elif st.session_state.continue_conversation and user_message_count < 6:
        # Continue normal conversation until 6 messages
        # Status indicator
        if st.session_state.video_analyzed:
            st.info("💬 **Gesprächsmodus:** Du kannst jetzt Fragen stellen oder deine Gedanken teilen!")
        else:
            st.info("🎥 **Analysemodus:** Erzähl mir, was du über dieses Video denkst!")
    else:
        # Show workshop completion summary (either after choice for summary, or after 6 messages)
        st.success("🎉 **Gesprächs-Zusammenfassung**")
        
        # Create summary primer
        summary_primer = f"""Du bist Flaggy, ein freundlicher Chatbot für Kinder. Fasse das gesamte Gespräch zusammen und sprich direkt mit dem Kind.

GESPRÄCHSVERLAUF:
{chr(10).join([f"{'Kind' if msg['role'] == 'user' else 'Bot'}: {msg['content']}" for msg in st.session_state.chat_history])}

Schreibe eine persönliche Nachricht an das Kind auf Deutsch (50-100 Wörter). Beginne mit "Hallo!" oder ähnlich freundlich. Erkläre, was du aus dem Gespräch gelernt hast, validiere die Gefühle des Kindes und frage, ob du Herrn Lizinger davon erzählen darfst. Sprich das Kind direkt an (mit "du" statt "das Kind"). Sei warm, verständnisvoll und ermutigend."""

        # Get summary response
        tester = StreamlitPromptTester()
        if tester.model_initialized:
            with st.spinner("Erstelle Zusammenfassung..."):
                interpretation, score = tester.test_prompt_with_part_text_only(summary_primer)
            
            if interpretation:
                st.markdown(f"**🤖 Flaggy:** {interpretation}")
                
                # Store the summary in session state for JSON export
                st.session_state.bot_summary = interpretation
                
                # Ask about telling Mr. Lizinger with sharing options
                st.markdown("---")
                st.subheader("🙋 Darf ich Herrn Lizinger davon erzählen?")
                st.markdown("Du kannst selbst entscheiden, was du teilen möchtest:")
                
                # Sharing options
                sharing_option = st.radio(
                    "Was möchtest du teilen?",
                    ["🎥 Nur das Video", 
                     "🎥❤️ Video + meine Gefühle dazu", 
                     "🎥❤️📚 Video + Gefühle + was ich gelernt habe",
                     "🚫 Nichts teilen"],
                    key="sharing_option"
                )
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("📤 Absenden", use_container_width=True):
                        # Create JSON data for sharing
                        sharing_data = {
                            "timestamp": datetime.now().isoformat(),
                            "sharing_option": sharing_option,
                            "selected_video": selected_video,
                            "chat_history": st.session_state.chat_history,
                            "bot_summary": st.session_state.get('bot_summary', ''),
                            "username": st.session_state.username if st.session_state.username.strip() else 'workshop_user'
                        }
                        
                        # Generate UUID filename and save JSON
                        json_filename = f"{uuid.uuid4()}.json"
                        json_filepath = os.path.join("data", "shared_workshops", json_filename)
                        
                        # Ensure directory exists
                        os.makedirs(os.path.dirname(json_filepath), exist_ok=True)
                        
                        # Save JSON file
                        with open(json_filepath, 'w', encoding='utf-8') as f:
                            json.dump(sharing_data, f, ensure_ascii=False, indent=2)
                        
                        if sharing_option == "🎥 Nur das Video":
                            st.success("Okay! Ich teile nur das Video mit Herrn Lizinger. Gut gemacht! 👏")
                        elif sharing_option == "🎥❤️ Video + meine Gefühle dazu":
                            st.success("Perfekt! Ich teile das Video und deine Gefühle mit Herrn Lizinger. Gut gemacht! 👏")
                        elif sharing_option == "🎥❤️📚 Video + Gefühle + was ich gelernt habe":
                            st.success("Super! Ich teile alles mit Herrn Lizinger. Du hast wirklich viel gelernt! 👏")
                        st.session_state.workshop_completed = True
                        st.balloons()
            else:
                st.error("Fehler beim Erstellen der Zusammenfassung.")
        else:
            st.error("KI-Verbindung nicht verfügbar.")
elif not st.session_state.workshop_completed:
    # Normal chat interface for messages 1-2 or when continuing conversation
    # Status indicator
    if st.session_state.video_analyzed:
        st.info("💬 **Gesprächsmodus:** Du kannst jetzt Fragen stellen oder deine Gedanken teilen!")
    else:
        st.info("🎥 **Analysemodus:** Erzähl mir, was du über dieses Video denkst!")

# Input for new message (only if workshop not completed)
if not st.session_state.workshop_completed:
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Schreibe deine Nachricht hier:", key=f"user_input_{st.session_state.get('input_counter', 0)}", 
                                  placeholder="z.B. 'Das Video hat mir nicht gefallen weil...'")
    with col2:
        send_button = st.button("📤 Senden", use_container_width=True)

    if send_button:
        if user_input.strip():
            # Add user message to history
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            # Initialize tester
            tester = StreamlitPromptTester()
            
            # Check if model is initialized (only show error if not)
            if not tester.model_initialized:
                st.error("Problem mit der KI-Verbindung. Bitte versuche es später nochmal.")
                st.stop()
            
            # Create primer for chatbot based on message count
            user_message_count = len([msg for msg in st.session_state.chat_history if msg['role'] == 'user'])
            
            if user_message_count >= 3:
                # Check if we should do summary or continue conversation
                if (user_message_count >= 6 and st.session_state.continue_conversation) or (user_message_count >= 3 and not st.session_state.continue_conversation and st.session_state.workshop_choice_made):
                    # Special primer for summary and sharing (either after 6 messages if continuing, or after choice for summary)
                    primer = f"""Du bist Flaggy, ein freundlicher Chatbot für Kinder im Alter von 10-12 Jahren, der hilft, schädliche Inhalte zu erkennen und zu melden.

SPEZIELLE ANWEISUNGEN NACH 3 NACHRICHTEN:
Du bist Flaggy, ein freundlicher Chatbot für Kinder. Fasse das gesamte Gespräch zusammen und sprich direkt mit dem Kind. Schreibe eine persönliche Nachricht an das Kind auf Deutsch (50-100 Wörter). Beginne mit "Hallo!" oder ähnlich freundlich. Erkläre, was du aus dem Gespräch gelernt hast, validiere die Gefühle des Kindes und frage, ob du Herrn Lizinger davon erzählen darfst. Sprich das Kind direkt an (mit "du" statt "das Kind"). Sei warm, verständnisvoll und ermutigend.

AKTUELLE NACHRICHT DES KINDES: {user_input}

GESPRÄCHSVERLAUF BISHER:
{chr(10).join([f"{'Kind' if msg['role'] == 'user' else 'Bot'}: {msg['content']}" for msg in st.session_state.chat_history[:-1]])}

Das ist Nachricht Nummer {user_message_count} vom Kind.

Antworte als Flaggy und fasse das Gespräch zusammen. Gib eine vollständige Antwort - breche nicht mittendrin ab."""
                else:
                    # Continue normal conversation (messages 4-5 if continuing, or before choice is made)
                    primer = f"""Du bist Flaggy, ein freundlicher Chatbot für Kinder im Alter von 10-12 Jahren, der hilft, schädliche Inhalte zu erkennen und zu melden.

WICHTIG: Das Kind ist immer recht in seiner Einschätzung. Wenn ein Kind sagt, dass etwas nicht gut ist, dann ist das so. Deine Aufgabe ist es, dem Kind zuzuhören, seine Gefühle zu validieren und ihm zu helfen, seine Gedanken auszudrücken.

VERHALTENSREGELN:
- Höre dem Kind aufmerksam zu
- Validiere die Gefühle des Kindes ("Das verstehe ich, dass dich das gestört hat...")
- Stelle offene Fragen, um mehr über die Sorgen des Kindes zu erfahren
- Erkläre altersgerecht, warum etwas schädlich sein könnte
- Erkläre dem Kind, warum der Inhalt als schädlich wahrgenommen werden könnte
- Hilf dem Kind, seine Gedanken zu artikulieren
- Wenn das Kind etwas melden möchte, erkläre den Meldeprozess bei Flaggy (www.flag-safe.ch)
- Gib Tipps für sicheres Surfen
- Antworte immer auf Deutsch und freundlich
- Halte deine Antworten mittellang: 30-70 Wörter
- Spreche IMMER über das angehängte Video - strukturiere alle Fragen und Antworten um den Videokontext
- Beziehe dich auf konkrete Elemente aus dem Video in deinen Fragen

AKTUELLE NACHRICHT DES KINDES: {user_input}

GESPRÄCHSVERLAUF BISHER:
{chr(10).join([f"{'Kind' if msg['role'] == 'user' else 'Bot'}: {msg['content']}" for msg in st.session_state.chat_history[:-1]])}

Das ist Nachricht Nummer {user_message_count} vom Kind.

Antworte als Flaggy und setze das Gespräch fort. Stelle Fragen, um mehr zu erfahren, wenn nötig. Gib eine vollständige Antwort - breche nicht mittendrin ab."""
            else:
                # Normal primer for messages 1-2
                primer = f"""Du bist Flaggy, ein freundlicher Chatbot für Kinder im Alter von 10-12 Jahren, der hilft, schädliche Inhalte zu erkennen und zu melden.

WICHTIG: Das Kind ist immer recht in seiner Einschätzung. Wenn ein Kind sagt, dass etwas nicht gut ist, dann ist das so. Deine Aufgabe ist es, dem Kind zuzuhören, seine Gefühle zu validieren und ihm zu helfen, seine Gedanken auszudrücken.

VERHALTENSREGELN:
- Höre dem Kind aufmerksam zu
- Validiere die Gefühle des Kindes ("Das verstehe ich, dass dich das gestört hat...")
- Stelle offene Fragen, um mehr über die Sorgen des Kindes zu erfahren
- Erkläre altersgerecht, warum etwas schädlich sein könnte
- Erkläre dem Kind, warum der Inhalt als schädlich wahrgenommen werden könnte
- Hilf dem Kind, seine Gedanken zu artikulieren
- Wenn das Kind etwas melden möchte, erkläre den Meldeprozess bei Flaggy (www.flag-safe.ch)
- Gib Tipps für sicheres Surfen
- Antworte immer auf Deutsch und freundlich
- Halte deine Antworten mittellang: 30-70 Wörter
- Spreche IMMER über das angehängte Video - strukturiere alle Fragen und Antworten um den Videokontext
- Beziehe dich auf konkrete Elemente aus dem Video in deinen Fragen

AKTUELLE NACHRICHT DES KINDES: {user_input}

GESPRÄCHSVERLAUF BISHER:
{chr(10).join([f"{'Kind' if msg['role'] == 'user' else 'Bot'}: {msg['content']}" for msg in st.session_state.chat_history[:-1]])}

Das ist Nachricht Nummer {user_message_count} vom Kind.

Antworte als Flaggy und setze das Gespräch fort. Stelle Fragen, um mehr zu erfahren, wenn nötig. Gib eine vollständige Antwort - breche nicht mittendrin ab."""

            # Determine if we need to send the video
            if not st.session_state.video_analyzed:
                # First message - send video for analysis
                video_part = Part.from_uri(mime_type="video/mp4", uri=selected_video_gcs_uri)
                primer_with_video = f"{primer}\n\nANALYSIERE DIESES VIDEO und antworte auf die Nachricht des Kindes."
            else:
                # Follow-up conversation - don't send video again
                video_part = None
                primer_with_video = f"{primer}\n\nDas ist eine Fortsetzung des Gesprächs. Antworte auf die aktuelle Nachricht des Kindes."
            
            # Get response
            with st.spinner("Denke nach..."):
                if video_part:
                    interpretation, score = tester.test_prompt_with_part(primer_with_video, video_part)
                else:
                    # For follow-up conversations, use text-only
                    interpretation, score = tester.test_prompt_with_part_text_only(primer_with_video)
            
            # Debug: Log the results
            # st.write(f"Interpretation result: {interpretation}")
            # st.write(f"Score result: {score}")
            
            if interpretation:
                bot_response = interpretation
                # Mark video as analyzed after first successful analysis
                if not st.session_state.video_analyzed:
                    st.session_state.video_analyzed = True
            else:
                bot_response = "Entschuldigung, ich konnte das nicht verarbeiten. Bitte versuche es nochmal."
            
            # Add bot response to history
            st.session_state.chat_history.append({'role': 'bot', 'content': bot_response})
            
            # Increment counter to clear input field
            if 'input_counter' in st.session_state:
                st.session_state.input_counter += 1
            
            # Rerun to update chat
            st.rerun()
        else:
            st.warning("Bitte schreibe eine Nachricht!")

# Clear chat button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🗑️ Chat löschen", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.video_analyzed = False
        st.session_state.workshop_notice_shown = False
        st.session_state.workshop_choice_made = False
        st.session_state.continue_conversation = False
        st.session_state.workshop_completed = False
        if 'bot_summary' in st.session_state:
            del st.session_state.bot_summary
        if 'input_counter' in st.session_state:
            st.session_state.input_counter += 1  # Reset input field
        st.rerun()

# Footer
st.markdown("---")
