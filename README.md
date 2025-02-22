# AutoGitGram
Automation tool designed to bridge GitHub and Instagram seamlessly.

AutoGitGram is an automation tool designed to bridge GitHub and Instagram seamlessly. It monitors your public GitHub repositories for new additions, generates concise summaries of their content, creates an accompanying visual representation, and posts them directly to your Instagram page. If image generation fails, the tool sends an email prompt for manual image upload. This system is ideal for developers or tech enthusiasts who want to share their work effortlessly with their Instagram audience.

---

### **Features**:

1. **GitHub Integration**:
    - Fetches all public repositories from your GitHub account.
    - Generates a concise summary (≤ 50 words) of new repositories.
2. **Image Generation**:
    - Creates a simple, visually appealing image containing the repository summary.
3. **Instagram Posting**:
    - Posts the summary and image directly to your Instagram account.
    - Uses alternative methods like browser automation if API-based posting is not feasible.
4. **Email Notification**:
    - If image generation fails, it sends an email prompt to the user with repository details for manual posting.

---

### **Code Overview**:

### **1. Fetch Public GitHub Repositories**

A Python function retrieves public repositories from GitHub and filters them to exclude private repositories.

### **2. Generate Repository Summary**

A function composes a concise summary of each repository, including its name and description.

### **3. Image Generation**

Using the **Pillow** library, the tool generates a basic image containing the repository summary.

### **4. Email Notifications**

A fallback mechanism sends an email to the user for manual image upload if automated generation fails.

### **5. Instagram Posting**

The system integrates with:

- **Instagram Graph API** (preferred method for compliance).
- **Selenium-based browser automation** (alternative).

### **6. Automated Workflow**

All components are orchestrated in a main function to check GitHub repositories, generate content, and publish to Instagram or notify the user via email.
