## V2 Overview
**Version 2** tries to fetch public GitHub repositories, generates a brief summary along with an image, and posts them to Instagram. If posting fails, it sends an email notification.

## Features
- Fetches public repositories from GitHub.
- Generates a summary of the repository.
- Creates an image with repository details.
- Posts the image and summary to Instagram using Selenium WebDriver.
- Sends an email notification if image generation or Instagram posting fails.

## Technologies Used
- **Python**
- **GitHub API** (via `requests`)
- **Pillow (PIL)** (for image generation)
- **Selenium WebDriver** (for Instagram automation)
- **SMTP (smtplib)** (for email notifications)

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Chrome WebDriver (for Selenium automation)
- Required Python libraries

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/AutoGitGram.git
   cd AutoGitGram
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure environment variables or modify the script to include:
   ```python
   GITHUB_USERNAME = "your_github_username"
   INSTAGRAM_USERNAME = "your_instagram_username"
   INSTAGRAM_PASSWORD = "your_instagram_password"
   EMAIL_SENDER = "your_email@gmail.com"
   EMAIL_RECEIVER = "receiver_email@gmail.com"
   EMAIL_PASSWORD = "your_email_password"
   ```

## Usage
Run the script with:
```sh
python main.py
```

## How It Works
1. **Fetch GitHub Repositories**
   - The script connects to the GitHub API using `requests`.
   - It retrieves all public repositories for the specified username.

2. **Generate Repository Summary**
   - Extracts repository details (name, description).
   - Limits long descriptions to 50 characters.

3. **Create an Image**
   - Generates a 500x250px image using Pillow.
   - Displays repository name and short description.

4. **Post to Instagram**
   - Uses Selenium WebDriver to log in and post the image.
   - Requires a valid Instagram username and password.

5. **Email Notification**
   - If image generation or Instagram posting fails, an email is sent to notify the user.

## Troubleshooting
- **Instagram login issues?** Ensure credentials are correct and two-factor authentication is disabled.
- **GitHub API errors?** Verify that the username exists and API rate limits are not exceeded.
- **Email not sending?** Ensure SMTP credentials and server settings are correct.
