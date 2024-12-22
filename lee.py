from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time
import csv
from datetime import datetime


class LinkedInEmailScraper:
    def __init__(self):
        # Initialize Chrome options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless=new")  # Updated headless mode
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

        # Initialize the driver with Service
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)

    def search_linkedin_profiles(self, search_query, num_pages=3):
        emails = []

        try:
            # Go to Google
            self.driver.get("https://www.google.com")
            time.sleep(2)  # Wait for page to fully load

            # Handle cookie consent - multiple possible button texts
            consent_buttons = [
                "//button[contains(., 'Accept all')]",
                "//button[contains(., 'I agree')]",
                "//button[contains(., 'Agree')]",
                "//div[contains(., 'Accept all')]/ancestor::button",
            ]

            for button_xpath in consent_buttons:
                try:
                    consent = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, button_xpath))
                    )
                    consent.click()
                    time.sleep(1)
                    break
                except Exception:
                    continue

            # Find and interact with search box using JavaScript
            search_query = f"site:linkedin.com {search_query} email"
            self.driver.execute_script(
                f'document.querySelector("input[name=\'q\']").value = "{search_query}"'
            )
            time.sleep(1)

            # Submit the form using JavaScript
            self.driver.execute_script(
                "document.querySelector(\"input[name='q']\").form.submit()"
            )

            # Wait for search results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )

            # Process multiple pages of results
            for page in range(num_pages):
                # Wait for results to load
                time.sleep(2)

                # Get page source and parse with BeautifulSoup
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                search_results = soup.find_all("div", class_="g")

                # Extract emails from each result
                for result in search_results:
                    text_content = result.get_text()
                    # Look for email patterns
                    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
                    email_matches = re.findall(email_pattern, text_content)
                    emails.extend(email_matches)

                # Try to go to next page
                try:
                    next_button = self.driver.find_element(By.ID, "pnnext")
                    next_button.click()
                except Exception as e:
                    print(f"Could not find next button: {e}")
                    break

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            return list(set(emails))  # Remove duplicates

    def save_results(self, emails, search_query):
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/srch_res_{timestamp}.csv"

        # Save results to CSV
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Search Query", "Email"])
            for email in emails:
                writer.writerow([search_query, email])

    def close(self):
        self.driver.quit()


def main():
    scraper = LinkedInEmailScraper()
    search_query = input("Enter search terms (e.g., 'python developer new york'): ")

    try:
        emails = scraper.search_linkedin_profiles(search_query)
        if emails:
            print(f"\nFound {len(emails)} unique email addresses:")
            for email in emails:
                print(email)
            scraper.save_results(emails, search_query)
        else:
            print("No email addresses found.")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
