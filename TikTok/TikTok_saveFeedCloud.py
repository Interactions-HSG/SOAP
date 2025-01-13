import os
import glob
import time
import sqlite3
import tempfile
from random import randint

# If you still rely on .env for anything else, you can keep this:
from dotenv import load_dotenv

from google.cloud import storage
import pyktok as pyk


class SaveFeedCloudTikTok:
    def __init__(
            self,
            tiktok_username,
            bucket_name,
            db_path="/Users/lukabekavac/PycharmProjects/SOAP-private/TikTok/TikTok_data.db",
            specify_pyktok_browser="chrome"
    ):
        """
        Initialize the class with explicit parameters rather than relying on environment variables.

        Args:
            tiktok_username (str): The TikTok username to process.
            bucket_name (str): The GCS bucket name where files should be uploaded.
            db_path (str): Path to the local SQLite database. Defaults to your existing path.
            specify_pyktok_browser (str): If using Pyktok, specify which browser to mimic ("chrome" by default).
        """
        # Optional: still load .env if you want to read other environment variables or secrets
        load_dotenv()

        self.tiktok_username = tiktok_username
        self.bucket_name = bucket_name
        self.db_path = db_path

        # (Optional) Initialize Pyktok with a browser cookie to reduce captcha/ban risk
        pyk.specify_browser(specify_pyktok_browser)

    def upload_to_gcs(self, destination_blob_name, file_path):
        """
        Uploads a file to the specified Google Cloud Storage (GCS) bucket.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(str(file_path))
        print(f"File {file_path} uploaded to {destination_blob_name} in bucket {self.bucket_name}.")

    def download_video_with_pyktok(self, tiktok_url, metadata_file='metadata.csv'):
        """
        Uses Pyktok to download a single TikTok video to the current directory.
        Pyktok doesn't return a file path, so we have to find the newest .mp4 file.
        """
        # Before calling Pyktok, record the current .mp4 files so we can detect new ones
        existing_mp4s = set(glob.glob("*.mp4"))

        # Download the TikTok video, appending metadata to a CSV
        pyk.save_tiktok(tiktok_url, True, metadata_file)

        # Sleep briefly to mitigate scraping detection and let the file finalize
        time.sleep(2)

        # Find the newly created mp4 file by comparing against the old list
        current_mp4s = set(glob.glob("*.mp4"))
        new_files = current_mp4s - existing_mp4s

        if not new_files:
            return None  # Something failed or Pyktok changed naming convention

        # Typically Pyktok generates exactly one new file
        downloaded_file = new_files.pop()
        return downloaded_file

    def process_and_upload_media(self):
        """
        Fetches rows from the DB, downloads each video with Pyktok, then uploads to GCS.
        Implements a fallback to @tiktok if the username fails (e.g., 'playAddr' error).
        """
        conn = None
        try:
            # Connect to local SQLite DB
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Fetch rows from TikTokPost table where is_uploaded = 0
            cursor.execute(
                "SELECT pk_id, nickname FROM TikTokPost WHERE is_uploaded = 0 AND username = ?",
                (self.tiktok_username,)
            )
            rows = cursor.fetchall()

            for (pk_id, nickname) in rows:
                if not nickname or not pk_id:
                    print(f"Skipping row with pk_id={pk_id} due to missing nickname or pk_id.")
                    continue

                # Define the sequence of nicknames to try: original nickname and fallback 'tiktok'
                nicknames_to_try = [nickname, 'tiktok']
                success = False  # Flag to indicate successful processing

                for current_nickname in nicknames_to_try:
                    try:
                        # Build a TikTok URL from the current_nickname + pk_id
                        video_url = f"https://www.tiktok.com/@{current_nickname}/video/{pk_id}"
                        print(f"Processing video URL: {video_url}")

                        # Download via Pyktok
                        downloaded_file = self.download_video_with_pyktok(video_url, 'tiktok_data.csv')
                        if not downloaded_file:
                            print(f"Failed to find a downloaded file for {video_url}.")
                            raise Exception("Download failed.")

                        # Rename to pk_id.mp4 for clarity
                        new_name = f"{pk_id}.mp4"
                        try:
                            os.rename(downloaded_file, new_name)
                            print(f"Renamed {downloaded_file} to {new_name}.")
                        except Exception as rename_error:
                            print(f"Failed to rename {downloaded_file} to {new_name}: {rename_error}")
                            raise

                        # Use a temporary directory to keep the working directory clean
                        with tempfile.TemporaryDirectory() as tmpdir:
                            local_tmp_path = os.path.join(tmpdir, new_name)
                            try:
                                os.rename(new_name, local_tmp_path)
                                print(f"Moved {new_name} to temporary directory {local_tmp_path}.")
                            except Exception as move_error:
                                print(f"Failed to move {new_name} to temporary directory: {move_error}")
                                raise

                            # Upload to GCS
                            destination_blob_name = f"{self.tiktok_username}/{new_name}"
                            try:
                                self.upload_to_gcs(destination_blob_name, local_tmp_path)
                            except Exception as upload_error:
                                print(f"Failed to upload {new_name} to GCS: {upload_error}")
                                raise

                        # Mark DB as uploaded
                        try:
                            cursor.execute(
                                "UPDATE TikTokPost SET is_uploaded = 1 WHERE pk_id = ?",
                                (pk_id,)
                            )
                            conn.commit()
                            print(f"Marked pk_id={pk_id} as uploaded in the database.")
                        except Exception as db_error:
                            print(f"Failed to update database for pk_id={pk_id}: {db_error}")
                            raise

                        print(f"Successfully uploaded ID={pk_id} to GCS.")
                        success = True
                        break  # Exit the nickname loop on success

                    except Exception as e:
                        error_message = str(e)
                        print(
                            f"Unexpected error processing {pk_id} with nickname '{current_nickname}': {error_message}")

                        # Check if the error is related to 'playAddr' or invalid URL
                        if current_nickname == nickname and (
                                'playAddr' in error_message or "Invalid URL" in error_message):
                            print(
                                f"Error related to 'playAddr' or invalid URL for pk_id={pk_id}. "
                                f"Attempting fallback with '@tiktok'."
                            )
                            continue  # Try the next nickname
                        else:
                            # For other errors like 'itemInfo', do not attempt fallback
                            print(f"Non-recoverable error for pk_id={pk_id}. Continuing to next video.")
                            break  # Skip to the next video

                if not success:
                    print(f"Failed to process video with pk_id={pk_id} after attempting all nicknames.")

        except sqlite3.Error as db_conn_error:
            print(f"Database connection error: {db_conn_error}")
        finally:
            if conn:
                conn.close()
                print("Closed database connection.")

        print("All media processed.")

    def run(self):
        """
        Main entry point to process and upload.
        """
        self.process_and_upload_media()


if __name__ == "__main__":
    # Example usage (for testing):
    load_dotenv()  # If we want to read default env vars here

    # Read from .env or pass in manually
    username = os.getenv("TIKTOKUSERNAME", "someDefaultUser")
    bucket = os.getenv("BUCKET_NAME_TIKTOK", "default-bucket-name")
    db_path = "/Users/lukabekavac/PycharmProjects/SOAP-private/TikTok/TikTok_data.db"

    save_feed_cloud = SaveFeedCloudTikTok(
        tiktok_username=username,
        bucket_name=bucket,
        db_path=db_path
    )
    save_feed_cloud.run()
