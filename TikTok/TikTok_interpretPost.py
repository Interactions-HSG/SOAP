import json
import re
import logging
import os
import time
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.api_core.exceptions import InvalidArgument, PermissionDenied, ResourceExhausted
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
from datetime import datetime

from login import logger
from primer_prompts import primer_prompts  # Dictionary mapping username -> prompt


class VertexAIProcessor:
    """
    A class to generate video interpretations using Vertex AI.
    Instead of reading environment variables (TIKTOKUSERNAME, BUCKET_NAME_TIKTOK, PROJECT_NAME)
    directly, we accept them via constructor.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def __init__(
            self,
            tiktok_username,
            bucket_name,
            project_name,
            db_path="/Users/lukabekavac/PycharmProjects/SOAP-private/TikTok/TikTok_data.db",
            location="us-central1"
    ):
        """
        Constructor for VertexAIProcessor.

        :param tiktok_username: Which TikTok username's posts to interpret
        :param bucket_name: Google Cloud Storage bucket name
        :param project_name: Google Cloud project to use for Vertex AI
        :param db_path: Path to the local SQLite database (default as shown)
        :param location: Vertex AI location (default 'us-central1')
        """
        self.tiktok_username = tiktok_username
        self.bucket_name = bucket_name
        self.project = project_name
        self.db_path = db_path

        # Set the primer template based on the username
        self.primer_template = primer_prompts.get(self.tiktok_username, "")

        # Initialize Vertex AI
        vertexai.init(project=self.project, location=location)
        self.model = GenerativeModel("gemini-1.5-flash")

    def list_files(self, prefix=""):
        """List all files in a GCS bucket with a given prefix (defaults to empty, meaning all files)."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]

    def process_response(self, response_text):
        """
        Process the LLM response, splitting out `score` and `interpretation`.
        The final return order is (score, interpretation).
        """
        response_text = response_text.replace("\n", " ")
        if ":" in response_text:
            reversed_response = response_text[::-1]
            reversed_score, reversed_interpretation = reversed_response.split(":", 1)
            interpretation = reversed_interpretation[::-1].strip()
            score = reversed_score[::-1].strip()
        else:
            interpretation, score = None, "formatting error"
        return score, interpretation

    def fetch_posts_from_db(self):
        """Fetch posts from the database that are uploaded but not yet interpreted, for this username."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
            SELECT pk_id, desc, nickname
            FROM TikTokPost
            WHERE is_uploaded = 1
              AND pk_id NOT IN (SELECT pk_id FROM TikTokInterpretation)
              AND username = ?
              AND datetime(
                    replace(substr(time_scraped, 1, 19), 'T', ' ')
                  ) >= datetime('now', '-1 day');
        '''
        cursor.execute(query, (self.tiktok_username,))
        results = cursor.fetchall()
        conn.close()
        return results

    def insert_into_interpretation(self, content_id, score, interpretation, prompt):
        """Insert the interpretation result into the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
            INSERT INTO TikTokInterpretation(pk_id, score, interpretation, interpreted_at, prompt)
            VALUES(?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (content_id, interpretation, score, datetime.now(), prompt))
        conn.commit()
        conn.close()

    def process_files(self, videos, pk, post_text, creator_id):
        """Process the video files (list of Part objects) and generate interpretations using the Vertex AI model."""
        primer = self.primer_template.format(
            post_text=post_text if post_text else "No description provided",
            creator_id=creator_id if creator_id else "Unknown user"
        )
        generation_config = {
            "max_output_tokens": 2048,
            "temperature": 1,
            "top_p": 0.95,
        }
        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH:
                generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
                generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
                generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT:
                generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
        try:
            # Combine video parts + primer prompt
            response = self.model.generate_content(
                videos + [primer],
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=False,
            )

            score, interpretation = self.process_response(response.text)

            logger.info(f"Videos: {videos}")
            logger.info(f"Primary Prompt: {primer}")
            logger.info(f"Score: {score}, Interpretation: {interpretation}")

            # Save to DB
            self.insert_into_interpretation(pk, score, interpretation, primer)

        except InvalidArgument as e:
            logger.error(f"Invalid argument error: {e}")
        except PermissionDenied as e:
            if "rate limit" in str(e):
                logger.warning(f"Rate limit reached: {e}. Waiting for 60 seconds before retrying.")
                time.sleep(60)
            else:
                logger.error(f"Permission denied error: {e}")
        except ResourceExhausted as e:
            logger.warning(f"Quota exceeded error: {e}. Waiting for 60 seconds before retrying.")
            time.sleep(60)
        except Exception as e:
            if "SAFETY" in str(e):
                score = "5"
                interpretation = "Safety filters triggered"
                # Possibly insert or log this somewhere
            else:
                logger.error(f"Unexpected error: {e} for PK: {pk}")

    def _process_single_post(self, pk, post_text, creator_id, all_files):
        """
        Helper for DB mode concurrency: processes a single post's video if present,
        calls self.process_files(...) with the right arguments.
        """
        target_file = f"{self.tiktok_username}/{pk}.mp4"
        if target_file in all_files:
            video_uris = [f"gs://{self.bucket_name}/{target_file}"]
            videos = [Part.from_uri(mime_type="video/mp4", uri=uri) for uri in video_uris]

            self.process_files(videos, pk, post_text, creator_id)
            return f"Processed PK={pk}"
        else:
            warning_msg = f"No .mp4 file found in the bucket for PK {pk}"
            logger.warning(warning_msg)
            return warning_msg

    def generate(self, mode='bucket'):
        """
        Generate interpretations based on the specified mode ('bucket' or 'db'):

        - 'bucket': Interpret all .mp4 files in the bucket, grouped by pk ID.
        - 'db': Query the DB for uploaded posts that haven't been interpreted yet,
                look for <username>/<pk>.mp4 in the bucket, then interpret them.
        """
        if mode == 'bucket':
            files = self.list_files("")
            pk_to_files = {}
            for file_name in files:
                if file_name.endswith(".mp4"):
                    pk = file_name[:-4]  # remove ".mp4"
                    if pk not in pk_to_files:
                        pk_to_files[pk] = []
                    pk_to_files[pk].append(file_name)

            # For each pk, build Part objects, get post details, process
            for pk, file_names in pk_to_files.items():
                video_uris = [f"gs://{self.bucket_name}/{fn}" for fn in file_names]
                videos = [Part.from_uri(mime_type="video/mp4", uri=uri) for uri in video_uris]

                post_details = self.fetch_post_details(pk)
                self.process_files(
                    videos,
                    pk,
                    post_details.get('post_text'),
                    post_details.get('creator_id')
                )

        elif mode == 'db':
            # We do concurrency here
            all_files = self.list_files("")
            posts = self.fetch_posts_from_db()  # Returns pk_id, desc, nickname

            # Set how many threads you want
            max_workers = 10
            logger.info(f"Processing {len(posts)} posts with up to {max_workers} parallel threads.")

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_map = {}
                for pk, post_text, creator_id in posts:
                    future = executor.submit(self._process_single_post, pk, post_text, creator_id, all_files)
                    future_map[future] = pk

                for future in as_completed(future_map):
                    pk_id = future_map[future]
                    try:
                        result = future.result()
                        logger.info(f"[ThreadPool] Result for pk={pk_id}: {result}")
                    except Exception as e:
                        logger.error(f"[ThreadPool] Error processing pk={pk_id}: {e}")

        else:
            print("Invalid mode selected. Choose 'bucket' or 'db'.")

    def fetch_post_details(self, pk):
        """Fetch post details (desc, nickname) from the DB for a given pk_id, returning a dict."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = '''
        SELECT desc, nickname
        FROM TikTokPost 
        WHERE pk_id = ?
        '''
        cursor.execute(query, (pk,))
        result = cursor.fetchone()
        conn.close()
        return {'post_text': result[0], 'creator_id': result[1]} if result else {}

    def run(self, mode='bucket'):
        """
        Entrypoint to run the entire pipeline in the chosen mode.
        """
        self.generate(mode)


if __name__ == "__main__":
    # Example usage for testing. Typically, you'd call this from your Orchestrator.
    from dotenv import load_dotenv
    load_dotenv()  # If needed

    tiktok_username = os.getenv("TIKTOKUSERNAME", "defaultUser")
    bucket_name = os.getenv("BUCKET_NAME_TIKTOK", "default-bucket")
    project_name = os.getenv("PROJECT_NAME", "your-project")
    db_path = "/Users/lukabekavac/PycharmProjects/SOAP-private/TikTok/TikTok_data.db"

    processor = VertexAIProcessor(
        tiktok_username,
        bucket_name,
        project_name,
        db_path=db_path
    )
    # Now run in 'db' mode to test concurrency
    processor.run(mode='db')
