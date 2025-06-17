import os
import csv
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# ==============================================================================
# 1. USER CONFIGURATION - EDIT THIS SECTION
# ==============================================================================

# --- Add details for each submission system you want to track ---
# You can add multiple dictionaries to this list.
# - URL: The login page of the submission system.
# - userid: Your username for the system.
# - password: Your password for the system.
# - cc: (Optional) A list of email addresses to be CC'd on notifications.
system_dicts = [
    {
        "URL": "https://mc.manuscriptcentral.com/tip-ieee",  # journal URL
        "userid": "***",  # user ID
        "password": "***",  # passwd
        "cc": [
            "***",
        ],  # cc email (optional)
    },
    {
        "URL": "https://mc.manuscriptcentral.com/tifs-ieee",  
        "userid": "***",  
        "password": "***",  
        "cc": [
            "***",
        ],  
    },

]

# --- Email Configuration ---
# IMPORTANT: You may need to generate an "App Password" for your email account
# instead of using your regular login password, especially for Gmail, QQ, etc.
SENDER_EMAIL = "***"  # Your sending email address (e.g., QQ, 163, Gmail)
SENDER_PASSWORD = "***"  # Your email app password
RECEIVER_EMAIL = "***"  # The email address to receive notifications
SMTP_SERVER = "smtp.qq.com"  # SMTP server for your email provider (e.g., smtp.qq.com, smtp.gmail.com)
SMTP_PORT = 587  # 587 for TLS, 465 for SSL


# ==============================================================================
# END OF USER CONFIGURATION
# ==============================================================================

def get_paper_status(system_dict):
    """Logs into the submission system and scrapes paper statuses."""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    # Uncomment the next line to run Chrome in the background without a visible window
    # chrome_options.add_argument("--headless")

    # Initialize browser
    # Assumes chromedriver.exe is in the same directory or in system PATH
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(300)

    all_papers = []
    try:
        print(f"Connecting to {system_dict['URL']}...")
        driver.get(system_dict["URL"])
    except TimeoutException:
        print(f"Page load timed out: {system_dict['URL']}")
        driver.quit()
        return []

    try:
        # Login
        print("Logging in...")
        driver.find_element(By.ID, "USERID").send_keys(system_dict["userid"])
        driver.find_element(By.ID, "PASSWORD").send_keys(system_dict["password"])
        time.sleep(1)  # Short delay to ensure elements are ready
        driver.find_element(By.ID, "logInButton").send_keys(Keys.ENTER)
        time.sleep(5)  # Wait for the login process to complete

        # Navigate to the author dashboard/submissions page
        # This CSS selector might need adjustment for different journal systems.
        print("Navigating to author dashboard...")
        driver.find_element(
            By.CSS_SELECTOR, "#header .nav-collapse.toplvlnav ul li:nth-child(2) a"
        ).send_keys(Keys.ENTER)
        time.sleep(5)

        def extract_paper_info(rows):
            """Extracts paper details from table rows."""
            papers = []
            for row in rows:
                try:
                    status = row.find_element(By.CSS_SELECTOR, 'td[data-label="status"] .pagecontents').text
                    id_ = row.find_element(By.CSS_SELECTOR, 'td[data-label="ID"]').text
                    title = \
                    row.find_element(By.CSS_SELECTOR, 'td[data-label="title"]').get_attribute("innerHTML").split(
                        "<br>")[0].strip()
                    papers.append((status, id_, title))
                    print(f"Found Paper -> ID: {id_}, Status: {status}, Title: {title}")
                except Exception:
                    # This row doesn't contain a paper, skip it.
                    continue
            return papers

        # Extract info from different sections (e.g., 'Submissions Being Processed', 'Manuscripts with Decisions')
        # sections_to_check = ['Submissions Being Processed', 'Manuscripts I Have Co-Authored',
        #                      'Manuscripts with Decisions', 'Awaiting Final Files']

        sections_to_check = ['Submissions Being Processed']
        for i, section_name in enumerate(sections_to_check):
            if i > 0:  # For sections after the first one, we need to click to navigate
                try:
                    print(f"Checking section: '{section_name}'...")
                    link = driver.find_element(By.LINK_TEXT, section_name)
                    link.send_keys(Keys.ENTER)
                    time.sleep(5)
                except Exception:
                    print(f"Could not find or navigate to section: '{section_name}'")
                    continue

            # These selectors might need to be adjusted based on the specific website's structure
            rows = driver.find_elements(By.CSS_SELECTOR, "#authorDashboardQueue_wrapper tbody tr")
            if not rows:  # Fallback selector
                rows = driver.find_elements(By.CSS_SELECTOR, "#authorDashboardQueue tbody tr")

            all_papers.extend(extract_paper_info(rows))

    except Exception as e:
        print(f"An error occurred while scraping: {e}")
    finally:
        print("Closing browser.")
        driver.quit()

    # Remove duplicate entries that might be found in multiple sections
    return list(set(all_papers))


def send_email(data, rows=[], cc=None):
    """Sends an email notification about the status change."""
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Status Update for Paper {data[2]}"
    message["From"] = formataddr(("Paper Status Tracker", SENDER_EMAIL))
    message["To"] = RECEIVER_EMAIL
    if cc:
        message["Cc"] = ", ".join(cc)

    # Find previous statuses for the same paper ID
    logs_text = ""
    previous_logs = sorted([row for row in rows if row[2] == data[2]], key=lambda x: x[0])
    if previous_logs:
        logs_text = "<table border='1' style='border-collapse: collapse; width:100%;'><tr><th style='padding:5px;'>Date</th><th style='padding:5px;'>Status</th></tr>"
        for log in previous_logs:
            logs_text += f"<tr><td style='padding:5px;'>{log[0][:10]}</td><td style='padding:5px;'>{log[1]}</td></tr>"
        # Add the current status to the history table
        logs_text += f"<tr><td style='padding:5px;'><b>{data[0][:10]}</b></td><td style='padding:5px;'><b>{data[1]}</b></td></tr></table>"

    html = f"""
    <html>
    <body>
        <p>Hi,</p>
        <p>The status of your paper has been updated in the system.</p>
        <table border="0" style="border-collapse: collapse; margin-bottom: 20px;">
        <tr><th style="text-align:left; padding-right:10px;">Time</th><td>{data[0]}</td></tr>
        <tr><th style="text-align:left; padding-right:10px;">Status</th><td style="color:red; font-weight:bold;">{data[1]}</td></tr>
        <tr><th style="text-align:left; padding-right:10px;">ID</th><td>{data[2]}</td></tr>
        <tr><th style="text-align:left; padding-right:10px;">Title</th><td>{data[3]}</td></tr>
        </table>
    """
    if logs_text:
        html += f"<h3>Status History</h3>{logs_text}"

    html += "</body></html>"
    message.attach(MIMEText(html, "html"))

    try:
        print(f"Sending email notification to {RECEIVER_EMAIL}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        recipients = [RECEIVER_EMAIL] + (cc if cc else [])
        server.sendmail(SENDER_EMAIL, recipients, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def update_csv(data, file_path, cc=None):
    """Writes the new status to the CSV file and triggers email if changed."""
    file_exists = os.path.exists(file_path)
    header = ["Time", "Status", "ID", "Title"]
    rows = []

    if file_exists:
        with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            try:
                # Skip header
                next(reader)
                rows = list(reader)
            except StopIteration:
                # File is empty
                pass

    # Find the last known status for this specific paper ID
    last_row_for_id = None
    for row in reversed(rows):
        if row and row[2] == data[2]:
            last_row_for_id = row
            break

    # If the status is new or different, add it and send an email
    if not last_row_for_id or last_row_for_id[1] != data[1]:
        print(f"Status changed for paper {data[2]} to '{data[1]}'. Updating records.")
        rows.append(data)

        # Sort rows by ID, then by time
        rows.sort(key=lambda x: (x[2], x[0]))

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(rows)

        send_email(data, rows, cc=cc)
    else:
        print(f"No status change for paper {data[2]}. Current status is '{data[1]}'.")


# --- Main Execution Block ---
if __name__ == "__main__":
    for system in system_dicts:
        print("-" * 50)
        print(f"Checking system: {system.get('URL')}")

        # Make sure login details are not the default ones
        if "your_username_here" in system["userid"] or "your_password_here" in system["password"]:
            print(
                "\n!!! WARNING: Please update the placeholder userid and password in the 'system_dicts' list before running!\n")
            continue

        paper_status_list = get_paper_status(system)

        if not paper_status_list:
            print("No paper information was retrieved.")
            continue

        for status, paper_id, title in paper_status_list:
            query_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            csv_file_path = "paper_status_history.csv"
            update_csv(
                (query_time, status, paper_id, title),
                csv_file_path,
                cc=system.get("cc", None),
            )
    print("-" * 50)
    print("Script finished.")
