import os
import requests
from PIL import Image, ImageDraw, ImageFont
from github import Github
from instagram_private_api import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from typing import List, Dict, Optional
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AutoGitGram:
    def __init__(self, config_path: str = "config.json"):
        """Initialize AutoGitGram with configuration."""
        self.config = self._load_config(config_path)
        self.github_client = Github(self.config["github_token"])
        self.logger = self._setup_logging()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found at {config_path}")

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='autogitgram.log'
        )
        return logging.getLogger('AutoGitGram')

    def fetch_public_repos(self) -> List[Dict]:
        """Fetch public repositories from GitHub."""
        try:
            user = self.github_client.get_user()
            repos = []
            for repo in user.get_repos():
                if not repo.private:
                    repos.append({
                        'name': repo.name,
                        'description': repo.description,
                        'url': repo.html_url,
                        'created_at': repo.created_at,
                        'language': repo.language
                    })
            return repos
        except Exception as e:
            self.logger.error(f"Error fetching repositories: {str(e)}")
            raise

    def generate_summary(self, repo: Dict) -> str:
        """Generate a concise summary of the repository."""
        summary = f"🚀 New Project: {repo['name']}\n\n"
        if repo['description']:
            # Truncate description to ensure total summary is ≤ 50 words
            words = repo['description'].split()
            if len(words) > 40:  # Leave room for name and other elements
                description = ' '.join(words[:40]) + '...'
            else:
                description = ' '.join(words)
            summary += f"{description}\n\n"
        
        summary += f"💻 Main language: {repo['language'] or 'Various'}\n"
        summary += f"🔗 {repo['url']}"
        return summary

    def generate_image(self, repo: Dict, summary: str) -> Optional[str]:
        """Generate an image containing the repository summary."""
        try:
            # Create a new image with a gradient background
            width, height = 1080, 1080  # Instagram square format
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)

            # Load a font (you'll need to provide the path to a font file)
            try:
                font = ImageFont.truetype("arial.ttf", 48)
                small_font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()

            # Draw text
            margin = 50
            y_position = margin
            
            # Repository name
            draw.text((margin, y_position), repo['name'], fill='black', font=font)
            y_position += 100

            # Description
            if repo['description']:
                words = repo['description'].split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    if len(' '.join(current_line)) > 40:  # Character limit per line
                        lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                if current_line:
                    lines.append(' '.join(current_line))

                for line in lines:
                    draw.text((margin, y_position), line, fill='black', font=small_font)
                    y_position += 50

            # Save the image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"repo_image_{timestamp}.png"
            image.save(filename)
            return filename
        except Exception as e:
            self.logger.error(f"Error generating image: {str(e)}")
            return None

    def post_to_instagram(self, image_path: str, caption: str) -> bool:
        """Post to Instagram using either API or browser automation."""
        try:
            # First attempt: Instagram Graph API
            if self._post_via_api(image_path, caption):
                return True
            
            # Fallback: Browser automation
            return self._post_via_selenium(image_path, caption)
        except Exception as e:
            self.logger.error(f"Error posting to Instagram: {str(e)}")
            return False

    def _post_via_api(self, image_path: str, caption: str) -> bool:
        """Post to Instagram using the Graph API."""
        try:
            api = Client(
                username=self.config["instagram_username"],
                password=self.config["instagram_password"]
            )
            api.post_photo(image_path, caption=caption)
            return True
        except Exception as e:
            self.logger.error(f"API posting failed: {str(e)}")
            return False

    def _post_via_selenium(self, image_path: str, caption: str) -> bool:
        """Post to Instagram using Selenium browser automation."""
        try:
            driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
            driver.get("https://www.instagram.com")
            
            # Login
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            ).send_keys(self.config["instagram_username"])
            
            driver.find_element(By.NAME, "password").send_keys(
                self.config["instagram_password"]
            )
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            # Navigate to create post
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Create']"))
            ).click()

            # Upload image and add caption
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(os.path.abspath(image_path))
            
            caption_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Write a caption...']"))
            )
            caption_input.send_keys(caption)

            # Share
            driver.find_element(By.XPATH, "//button[text()='Share']").click()
            
            driver.quit()
            return True
        except Exception as e:
            self.logger.error(f"Selenium posting failed: {str(e)}")
            driver.quit()
            return False

    def send_email_notification(self, repo: Dict, summary: str) -> None:
        """Send email notification for manual posting."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email_from"]
            msg['To'] = self.config["email_to"]
            msg['Subject'] = f"AutoGitGram: Manual Posting Required - {repo['name']}"

            body = f"""
            AutoGitGram failed to automatically post about your repository.
            
            Repository Details:
            Name: {repo['name']}
            Description: {repo['description']}
            URL: {repo['url']}
            
            Generated Summary:
            {summary}
            
            Please create and post an image manually to Instagram.
            """
            
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.config["email_username"], self.config["email_password"])
            server.send_message(msg)
            server.quit()
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")

    def run(self) -> None:
        """Main execution flow."""
        try:
            # Fetch repositories
            repos = self.fetch_public_repos()
            
            # Process each repository
            for repo in repos:
                # Check if repository was already processed
                if self._is_repo_processed(repo):
                    continue
                
                # Generate summary
                summary = self.generate_summary(repo)
                
                # Generate image
                image_path = self.generate_image(repo, summary)
                
                if image_path:
                    # Try posting to Instagram
                    if self.post_to_instagram(image_path, summary):
                        self._mark_repo_processed(repo)
                        self.logger.info(f"Successfully posted {repo['name']} to Instagram")
                    else:
                        self.send_email_notification(repo, summary)
                else:
                    self.send_email_notification(repo, summary)
        except Exception as e:
            self.logger.error(f"Error in main execution: {str(e)}")

    def _is_repo_processed(self, repo: Dict) -> bool:
        """Check if repository was already processed."""
        try:
            with open('processed_repos.json', 'r') as f:
                processed = json.load(f)
                return repo['url'] in processed
        except FileNotFoundError:
            return False

    def _mark_repo_processed(self, repo: Dict) -> None:
        """Mark repository as processed."""
        try:
            try:
                with open('processed_repos.json', 'r') as f:
                    processed = json.load(f)
            except FileNotFoundError:
                processed = []
            
            processed.append(repo['url'])
            
            with open('processed_repos.json', 'w') as f:
                json.dump(processed, f)
        except Exception as e:
            self.logger.error(f"Error marking repo as processed: {str(e)}")

if __name__ == "__main__":
    auto_git_gram = AutoGitGram()
    auto_git_gram.run()