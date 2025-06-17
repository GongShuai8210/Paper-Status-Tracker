# Paper Status Tracker

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/Paper-Status-Tracker?style=social)

An automation tool designed for researchers, students, and academics to free you from the endless cycle of manually refreshing submission systems and anxiously waiting for status updates.


## 😫 Sound Familiar?

-   Is the first thing you do every morning opening multiple journal submission portals, only to see the same "With Editor" status?
-   Do you find your workflow constantly interrupted by the nagging urge to check for updates, killing your productivity?
-   Are you tired of juggling numerous accounts and passwords for different submission systems?

**`Paper Status Tracker`** was built to solve these exact pain points. It acts as a tireless academic assistant, silently performing all the repetitive checks for you in the background. The moment a status changes, you'll be the first to know via email, allowing you to focus on what truly matters: your research.

## ✨ Features

-   ✅ **Automated Tracking**: Logs in and scrapes the latest manuscript status automatically, 24/7.
-   ✅ **Multi-System Support**: Easily configure and track submissions across major systems (e.g., Editorial Manager, ScholarOne).
-   ✅ **Real-time Email Notifications**: Get instant, detailed email alerts המmoment your manuscript's status is updated.
-   ✅ **Status History Logging**: Every status change is logged locally in a `paper_status_history.csv` file for easy tracking and review.
-   ✅ **Highly Configurable**: Manage multiple accounts and manuscripts across different journals simultaneously.
-   ✅ **Cross-Platform**: Runs smoothly on Windows, macOS, and Linux.

## 🚀 Getting Started

### 1. Prerequisites

-   [Python 3.8](https://www.python.org/) or higher installed.
-   [Google Chrome](https://www.google.com/chrome/) browser installed.
-   [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) matching your Chrome version downloaded. **Place the `chromedriver.exe` (or equivalent) executable in the project's root directory.**

### 2. Installation & Setup

**A. Clone the Repository**
```bash
git clone [https://github.com/YOUR_USERNAME/Paper-Status-Tracker.git](https://github.com/YOUR_USERNAME/Paper-Status-Tracker.git)
cd Paper-Status-Tracker
```

**B. Install Dependencies**
The project's dependencies are listed in `requirements.txt`. Install them with pip:
```bash
pip install -r requirements.txt
```

**C. Configure Your Details**
Open the main script file (e.g., `paper_tracker.py`) and modify the configuration section at the top with your personal information.

**Configure Submission Systems:**
```python
# --- Add each submission system you want to track ---
# You can add as many dictionaries to this list as you need
system_dicts = [
    {
        "URL": "[https://www.editorialmanager.com/journal-A/](https://www.editorialmanager.com/journal-A/)", # Required: Login URL for Journal A
        "userid": "your_username_for_journal_A",             # Required: Your username for Journal A
        "password": "your_password_for_journal_A",           # Required: Your password for Journal A
        "cc": ["coauthor1@example.com"],                     # Optional: List of emails for CC
    },
    {
        "URL": "[https://mc.manuscriptcentral.com/journal-B](https://mc.manuscriptcentral.com/journal-B)", # Required: Login URL for Journal B
        "userid": "your_username_for_journal_B",             # Required: Your username for Journal B
        "password": "your_password_for_journal_B",           # Required: Your password for Journal B
        "cc": [],                                            # Optional: No CC emails
    },
]
```

**Configure Email Notifications:**
```python
# --- Email Configuration ---
# IMPORTANT: It is highly recommended to use an "App Password" instead of your regular password.
SENDER_EMAIL = "your_sender_email@gmail.com"     # Required: The email address that sends notifications
SENDER_PASSWORD = "your_email_app_password"      # Required: The password or App Password for the sender email
RECEIVER_EMAIL = "your_receiver_email@outlook.com" # Required: The email address that receives notifications
SMTP_SERVER = "smtp.gmail.com"                   # Required: The SMTP server address for your sender email
SMTP_PORT = 587                                  # Required: The SMTP port (587 for TLS, 465 for SSL)
```

### 3. Running the Script

Once everything is configured, simply run the main script from your terminal:
```bash
python paper_tracker.py
```
The script will immediately perform a check. The first run will populate the CSV file with the current status of all manuscripts. Subsequent runs will only send an email if a status has changed.

### 4. Setting up Automation

To achieve true 24/7 automation, you should set up a scheduled task.
-   **On Windows**: Use the built-in **Task Scheduler**.
-   **On macOS / Linux**: Use **cron** to schedule the script to run at regular intervals.

## 🤝 Contributing

Contributions of all kinds are welcome! Feel free to open an issue if you find a bug or have a feature suggestion, or make a pull request.

1.  **Fork** the repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a **Pull Request**

## 📄 License

This project is distributed under the [MIT License](LICENSE). See the `LICENSE` file for more information.

---
*If you find this project helpful, please consider giving it a ⭐️ star! It's a great encouragement for me.*