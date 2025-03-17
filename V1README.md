## V1 Overview
**Version 1** tries to fetche public GitHub repositories, generates a brief summary along with an image, and posts them to Instagram. If posting fails, it sends an email notification.

## Features
- Fetches public repositories from GitHub.
- Generates a summary of the repository.
- Creates an image with repository details.
- Posts the image and summary to Instagram.
- Sends an email notification if Instagram posting fails.

## Technologies Used
- **Python**
- **GitHub API** (via `PyGithub`)
- **Instagram Private API** (via `instagram_private_api`)
- **Pillow (PIL)** (for image generation)
- **Selenium WebDriver** (for Instagram automation fallback)
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
3. Create a `config.json` file in the root directory and add the following details:
   ```json
   {
       "github_token": "your_github_personal_access_token",
       "instagram_username": "your_instagram_username",
       "instagram_password": "your_instagram_password",
       "email_sender": "your_email@example.com",
       "email_receiver": "receiver_email@example.com",
       "email_password": "your_email_password"
   }
   ```

## Usage
Run the script with:
```sh
python main.py
```

## How It Works
1. **Fetch GitHub Repositories**
   - The script connects to the GitHub API using `PyGithub`.
   - It retrieves all public repositories from the authenticated user.

2. **Generate Repository Summary**
   - Extracts repository details (name, description, language, URL).
   - Limits long descriptions to 40 words.

3. **Create an Image**
   - Generates a 1080x1080px image using Pillow.
   - Displays repository name, short description, and main language.

4. **Post to Instagram**
   - Tries to post using `instagram_private_api`.
   - If API posting fails, falls back to Selenium WebDriver.

5. **Email Notification**
   - If Instagram posting fails, an email is sent to notify the user.

## Troubleshooting
- **Instagram login issues?** Check if Instagram requires additional verification.
- **GitHub API errors?** Ensure your access token has the correct permissions.
- **Email not sending?** Verify SMTP credentials and server settings.

## Contributing
Feel free to open issues and submit pull requests to improve this project.
