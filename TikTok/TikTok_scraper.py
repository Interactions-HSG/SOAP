import datetime
import os
import sqlite3
import requests  # <-- New import for making a quick IP check
from dotenv import load_dotenv
from tikapi import TikAPI, ValidationException, ResponseException


class TikTokScraper:
    def __init__(
            self,
            master_api_key,  # The master TikAPI key
            account_key,  # The TikAPI accountKey for a specific sub-account
            tiktok_username,  # The TikTok username you want to scrape
            db_path="/Users/lukabekavac/PycharmProjects/SOAP-private/TikTok/TikTok_data.db"
    ):
        """
        Initializes with user-provided credentials, sets up database connections,
        and creates a TikAPI user instance.
        """
        load_dotenv()  # if needed

        self.master_api_key = master_api_key
        self.account_key = account_key
        self.tiktok_username = tiktok_username

        # Connect to SQLite database
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Initialize TikAPI
        self.api = TikAPI(self.master_api_key)
        self.user = self.api.user(accountKey=self.account_key)

        # Optional: create a directory to save videos if needed
        self.save_directory = "downloaded_videos"
        os.makedirs(self.save_directory, exist_ok=True)

    def run(self, count=30):
        """
        Fetches posts using TikAPI, extracts relevant nested details,
        and stores them in SQLite.

        Args:
            count (int): Number of posts to fetch.
        """
        try:
            # -- Quick IP check:
            # If your environment or session is set to use a proxy,
            # this will print the IP from which the request is made.
            ip_response = requests.get("https://ipv4.icanhazip.com", timeout=10)
            print(f"IP check before calling TikAPI: {ip_response.text.strip()}")

            # 1) Fetch posts from the user's explore feed
            response = self.user.posts.explore(count=count)
            posts = response.json().get("itemList", [])

            if not posts:
                print(f"No posts found for username={self.tiktok_username}.")
                return

            time_scraped = datetime.datetime.now().isoformat()  # Current time

            # 2) Iterate over each post and extract data
            for post in posts:
                pk_id = post.get("id")  # The main post ID
                if not pk_id:
                    print("Skipping post with missing pk_id.")
                    continue

                is_ad = post.get("isAd", False)
                nickname = post.get("author", {}).get("nickname", "")
                desc = post.get("desc", "")
                create_time = post.get("createTime", "")

                # Stats
                stats = post.get("stats", {})
                comment_count = stats.get("commentCount", 0)
                collect_count = stats.get("collectCount", 0)
                digg_count = stats.get("diggCount", 0)
                play_count = stats.get("playCount", 0)
                share_count = stats.get("shareCount", 0)

                # Video
                video = post.get("video", {})
                duration = video.get("duration", 0)
                format_ = video.get("format", "")
                download_url = video.get("downloadAddr", "")
                play_url = video.get("playAddr", "")
                video_url = download_url if download_url else play_url

                # Music
                music = post.get("music", {})
                music_id = music.get("id", "")
                music_title = music.get("title", "")

                # Author
                author = post.get("author", {})
                author_id = author.get("id", "")
                author_nickname = author.get("nickname", "")
                private_account = author.get("privateAccount", False)

                # Author Stats
                author_stats = post.get("authorStats", {})
                author_following_count = author_stats.get("followingCount", 0)
                author_follower_count = author_stats.get("followerCount", 0)
                author_heart_count = author_stats.get("heartCount", 0)
                author_video_count = author_stats.get("videoCount", 0)

                # 3) Insert data into SQLite database
                self.cursor.execute("""
                    INSERT INTO TikTokPost (
                        pk_id, isAd, nickname, desc, commentCount, createTime, collectCount,
                        diggCount, playCount, shareCount, duration, format, music_id,
                        music_title, author_id, author_nickname, privateAccount,
                        authorFollowingCount, authorFollowerCount, authorHeartCount,
                        authorVideoCount, time_scraped, username, video_url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pk_id, is_ad, nickname, desc, comment_count, create_time, collect_count,
                    digg_count, play_count, share_count, duration, format_, music_id,
                    music_title, author_id, author_nickname, private_account,
                    author_following_count, author_follower_count, author_heart_count,
                    author_video_count, time_scraped, self.tiktok_username, video_url
                ))

            # 4) Commit
            self.conn.commit()
            print(f"[{self.tiktok_username}] Successfully stored {len(posts)} posts in the database.")

        except ValidationException as e:
            print(f"Validation error: {e} (Field: {e.field})")
        except ResponseException as e:
            print(f"Response error: {e} (Status code: {e.response.status_code})")
        except Exception as general_error:
            print(f"An error occurred: {general_error}")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    load_dotenv()

    master_api_key = os.getenv("TIKAPI_KEY")
    account_key = os.getenv("TIKAPI_ACCOUNT_KEY")
    tiktok_username = os.getenv("TIKTOKUSERNAME")

    scraper = TikTokScraper(master_api_key, account_key, tiktok_username)
    scraper.run(count=30)
    scraper.close_connection()
