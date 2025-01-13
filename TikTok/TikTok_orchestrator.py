import os
import time
import logging
import requests
from dotenv import load_dotenv

# Import your pipeline classes
from TikTok_scraper import TikTokScraper
from TikTok_saveFeedCloud import SaveFeedCloudTikTok
from TikTok_interpretPost import VertexAIProcessor
from TikTok_interactPost import TikTokManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        """
        1) Load environment variables.
        2) Collect multiple account credentials from .env using a chronological numbering approach.
        """
        load_dotenv()  # Load all .env variables
        self._enable_proxy_if_configured()  # Optionally set HTTP/HTTPS_PROXY env vars

        # Shared (master) TikAPI key
        self.master_api_key = os.getenv("TIKAPI_KEY")

        # Gather environment settings for GCS + Vertex AI
        self.bucket_name = os.getenv("BUCKET_NAME_TIKTOK")
        self.project = os.getenv("PROJECT_NAME")

        # Build a list of (accountKey, username) pairs
        self.accounts = []
        self._collect_chronological_accounts()

    def _enable_proxy_if_configured(self):
        """
        Check if the user provided PROXY_HOST, PROXY_PORT, and optionally PROXY_USER / PROXY_PASS
        in the .env. If so, set HTTP_PROXY and HTTPS_PROXY environment variables.
        """
        proxy_host = os.getenv("PROXY_HOST")
        proxy_port = os.getenv("PROXY_PORT")
        proxy_user = os.getenv("PROXY_USER")
        proxy_pass = os.getenv("PROXY_PASS")

        if proxy_host and proxy_port:
            auth_part = ""
            if proxy_user and proxy_pass:
                auth_part = f"{proxy_user}:{proxy_pass}@"

            proxy_url = f"http://{auth_part}{proxy_host}:{proxy_port}"

            os.environ["HTTP_PROXY"] = proxy_url
            os.environ["HTTPS_PROXY"] = proxy_url

            logger.info(f"Proxy environment variables set to {proxy_url}")
        else:
            logger.info("No proxy configuration found in environment variables. Skipping proxy setup.")

        # Log what we ended up with (might be None if not set)
        logger.info(f"HTTP_PROXY={os.environ.get('HTTP_PROXY')}")
        logger.info(f"HTTPS_PROXY={os.environ.get('HTTPS_PROXY')}")

    def _collect_chronological_accounts(self):
        """
        Looks for TIKAPI_ACCOUNT_KEY1, TIKTOKUSERNAME1,
                   TIKAPI_ACCOUNT_KEY2, TIKTOKUSERNAME2, etc.
        Continues incrementing the index until one variable is missing.
        """
        idx = 1
        while True:
            account_key = os.getenv(f"TIKAPI_ACCOUNT_KEY{idx}")
            username = os.getenv(f"TIKTOKUSERNAME{idx}")
            if account_key and username:
                self.accounts.append((account_key, username))
                idx += 1
            else:
                break

        if not self.accounts:
            logger.warning("No chronological TikAPI accounts found in the .env file!")

    def _test_proxy_ip(self, step_name):
        """
        Make a quick request to https://ipv4.icanhazip.com to see what IP we have,
        after finishing a pipeline step.
        """
        test_url = "https://ipv4.icanhazip.com"
        try:
            r = requests.get(test_url, timeout=10)
            logger.info(f"[{step_name}] Proxy test -> IP: {r.text.strip()}")
        except Exception as e:
            logger.error(f"[{step_name}] Could not complete proxy test request: {e}")

    def run_all_accounts(self):
        """
        Run the entire pipeline for each account in self.accounts.
        Each iteration calls:
          1) TikTokScraper
          2) SaveFeedCloudTikTok
          3) VertexAIProcessor
          4) TikTokManager
        Then after each step, we run a proxy test to confirm the IP.
        """
        if not self.accounts:
            logger.info("No valid accounts to process.")
            return

        logger.info(f"Starting pipeline for {len(self.accounts)} accounts.")
        logger.info(f"Following accounts will be processed: {self.accounts}")

        db_path = "/Users/lukabekavac/PycharmProjects/SOAP-private/TikTok/TikTok_data.db"

        for (acc_key, username) in self.accounts:
            logger.info(f"=== Starting pipeline for username='{username}' ===")
            overall_start = time.time()

            # STEP 1: SCRAPER
            scraper_start = time.time()
            scraper = TikTokScraper(
                master_api_key=self.master_api_key,
                account_key=acc_key,
                tiktok_username=username,
                db_path=db_path,
            )
            scraper.run(count=30)
            scraper.close_connection()
            scraper_end = time.time()
            logger.info(f"1) TikTokScraper finished in {scraper_end - scraper_start:.2f}s")
            self._test_proxy_ip("TikTokScraper")  # Test after scraper

            # STEP 2: SAVE FEED CLOUD
            save_feed_start = time.time()
            save_feed_cloud = SaveFeedCloudTikTok(
                tiktok_username=username,
                bucket_name=self.bucket_name
            )
            save_feed_cloud.run()
            save_feed_end = time.time()
            logger.info(f"2) SaveFeedCloudTikTok finished in {save_feed_end - save_feed_start:.2f}s")
            self._test_proxy_ip("SaveFeedCloudTikTok")  # Test after save feed cloud

            # STEP 3: VERTEX AI
            vertex_ai_start = time.time()
            vertex_ai = VertexAIProcessor(
                tiktok_username=username,
                bucket_name=self.bucket_name,
                project_name=self.project,
                db_path=db_path
            )
            vertex_ai.run(mode='db')  # or 'bucket', as you prefer
            vertex_ai_end = time.time()
            logger.info(f"3) VertexAIProcessor finished in {vertex_ai_end - vertex_ai_start:.2f}s")
            self._test_proxy_ip("VertexAIProcessor")  # Test after Vertex AI

            # STEP 4: TIKTOK MANAGER
            manager_start = time.time()
            manager = TikTokManager(
                master_api_key=self.master_api_key,
                account_key=acc_key,
                tiktok_username=username,
                db_path=db_path
            )
            manager.run()
            manager.close_connection()
            manager_end = time.time()
            logger.info(f"4) TikTokManager finished in {manager_end - manager_start:.2f}s")
            self._test_proxy_ip("TikTokManager")  # Test after manager

            overall_end = time.time()
            total = overall_end - overall_start
            logger.info(f"=== Finished pipeline for '{username}' in {total:.2f}s ===\n")


if __name__ == "__main__":
    orchestrator = Orchestrator()
    orchestrator.run_all_accounts()
