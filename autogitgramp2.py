import requests
import json
import os
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configuration
GITHUB_USERNAME = "your_github_username"
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
INSTAGRAM_USERNAME = "your_instagram_username"
INSTAGRAM_PASSWORD = "your_instagram_password"
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "your_email@gmail.com"

# Step 1: Fetch Public GitHub Repositories
def fetch_github_repos():
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        repos = response.json()
        return [repo for repo in repos if not repo['private']]
    return []

# Step 2: Generate Repository Summary
def generate_summary(repo):
    name = repo['name']
    description = repo['description'] or "No description provided."
    return f"{name}: {description[:47]}..." if len(description) > 50 else f"{name}: {description}"

# Step 3: Generate Image with Summary
def generate_image(summary, repo_name):
    img = Image.new('RGB', (500, 250), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((20, 100), summary, fill=(0, 0, 0), font=font)
    img_path = f"{repo_name}.png"
    try:
        img.save(img_path)
        return img_path
    except Exception as e:
        print(f"Image generation failed: {e}")
        return None

# Step 4: Send Email Notification if Image Generation Fails
def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

# Step 5: Post to Instagram (Using Selenium as Fallback)
def post_to_instagram(image_path, caption):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)
        
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(INSTAGRAM_USERNAME)
        password_input.send_keys(INSTAGRAM_PASSWORD)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        # Implement posting logic here (e.g., navigating to post section)
        print("Instagram posting logic needed.")
        driver.quit()
    except Exception as e:
        print(f"Instagram post failed: {e}")

# Main function to orchestrate the workflow
def main():
    repos = fetch_github_repos()
    for repo in repos:
        summary = generate_summary(repo)
        image_path = generate_image(summary, repo['name'])
        if image_path:
            post_to_instagram(image_path, summary)
        else:
            send_email("Image Generation Failed", f"Failed to generate image for {repo['name']}. Please upload manually.")

if __name__ == "__main__":
    main()
