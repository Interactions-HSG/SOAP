import os
import sqlite3
import time

from dotenv import load_dotenv
from tikapi import TikAPI, ValidationException, ResponseException

class TikTokManager:
    """
    A class to manage TikTok high-score interpretations and interactions using TikAPI.
    Instead of reading .env variables internally, we accept them as parameters.
    """

    def __init__(
        self,
        master_api_key,
        account_key,
        tiktok_username,
        db_path="TikTok_data.db"
    ):
        """
        :param master_api_key: Your overall TikAPI key (TIKAPI_KEY).
        :param account_key: The TikAPI account key (TIKAPI_ACCOUNT_KEY).
        :param tiktok_username: Which TikTok username to focus on (TIKTOKUSERNAME).
        :param db_path: Path to your local SQLite database.
        """
        # Optional: still load .env if you rely on other variables or secrets
        load_dotenv()

        self.master_api_key = master_api_key
        self.account_key = account_key
        self.tiktok_username = tiktok_username

        # Initialize TikAPI
        self.client = TikAPI(self.master_api_key)
        self.user = self.client.user(accountKey=self.account_key)

        # Connect to your SQLite database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def get_high_score_interpretations(self):
        """
        Fetch pk_ids with high score (>3) interpretations that have not been 'liked' yet (liked=0)
        for the given username.
        """
        query = """
            SELECT DISTINCT TikTokInterpretation.pk_id
            FROM TikTokInterpretation
            JOIN TikTokPost ON TikTokInterpretation.pk_id = TikTokPost.pk_id
            WHERE score > 3
              AND liked = 0
              AND username = ?
        """
        self.cursor.execute(query, (self.tiktok_username,))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]

    def fetch_videos_for_high_scores(self):
        """
        For each pk_id that meets the criteria, fetch the video details via TikAPI.
        (Optionally, you can like, comment, etc. based on your needs.)
        """
        pk_ids = self.get_high_score_interpretations()
        for pk_id in pk_ids:
            try:
                # Example: fetch the video details for this pk_id
                response = self.user.posts.video(id=str(pk_id))
                #data = response.json()
                #print(f"[TikTokManager] Data for pk_id={pk_id}: {data}")

                # Example: if you wanted to 'like' the video, you'd uncomment below:
                response_like = self.user.posts.like(media_id=str(pk_id))
                like_data = response_like.json()
                print(f"Like response for pk_id={pk_id}: {like_data}")
                time.sleep(1)  # Sleep a second to avoid rate limits



                # If you wanted to post a comment:
                # response_comment = self.user.posts.comments.post(
                #     id=str(pk_id),
                #     text="Interessant! 🚀"
                # )
                # comment_data = response_comment.json()
                # print(f"Comment response for pk_id={pk_id}: {comment_data}")

                # Update DB if you wanted to mark them as 'liked' to prevent re-liking:
                update_query = "UPDATE TikTokInterpretation SET liked = 1 WHERE pk_id = ?"
                self.cursor.execute(update_query, (pk_id,))
                self.conn.commit()
                print(f"pk_id={pk_id} marked as liked=1 in DB")

            except ValidationException as e:
                print("Validation error:", e, e.field)
            except ResponseException as e:
                print("Response error:", e, e.response.status_code)
            except Exception as ex:
                print(f"Error fetching pk_id={pk_id}:", ex)

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def run(self):
        """
        Main method to fetch and handle videos based on high score interpretations.
        """
        self.fetch_videos_for_high_scores()
        self.close_connection()


if __name__ == "__main__":
    # Example usage or test scenario:
    load_dotenv()

    # Read from .env or hardcode for testing:
    master_api_key = os.getenv("TIKAPI_KEY")
    account_key = os.getenv("TIKAPI_ACCOUNT_KEY1")
    tiktok_username = os.getenv("TIKTOKUSERNAME1")
    db_path = "TikTok_data.db"

    manager = TikTokManager(
        master_api_key=master_api_key,
        account_key=account_key,
        tiktok_username=tiktok_username,
        db_path=db_path
    )
    manager.run()
