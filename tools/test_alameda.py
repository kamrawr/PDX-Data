import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.portlandmaps.com/advanced/?action=assessor"

# Setup browser
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": os.getcwd() + "/downloads"}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)
time.sleep(4)

# Select Alameda
select = Select(driver.find_element(By.TAG_NAME, "select"))
select.select_by_value("ALAMEDA")
time.sleep(1)

# Click search
driver.find_element(By.XPATH, "//button[contains(text(),'Search')]").click()
time.sleep(4)

print("Search completed. Looking for pagination buttons...\n")

# Get page source and extract pagination HTML
page_source = driver.page_source

# Look for pagination patterns in HTML
import re
patterns_to_search = [
    r'<button[^>]*>[\s]*[12345][\s]*</button>',
    r'<button[^>]*>[\s]*&gt;[\s]*</button>',
    r'<button[^>]*>[\s]*>[\s]*</button>',
    r'<div[^>]*pagination[^>]*>.*?</div>',
    r'<ul[^>]*pagination[^>]*>.*?</ul>',
]

print("=== SEARCHING HTML FOR PAGINATION PATTERNS ===")
for pattern in patterns_to_search:
    matches = re.findall(pattern, page_source, re.DOTALL | re.IGNORECASE)
    if matches:
        print(f"\nPattern '{pattern}':")
        for match in matches[:5]:  # Show first 5 matches
            print(f"  {match[:200]}")

# Find all buttons
print("\n=== ALL BUTTONS ON PAGE ===")
buttons = driver.find_elements(By.TAG_NAME, "button")
for i, btn in enumerate(buttons):
    text = btn.text.strip()
    if text:  # Only show buttons with text
        outer_html = btn.get_attribute('outerHTML')[:150]
        print(f"{i}: text='{text}'")
        print(f"   HTML: {outer_html}")
        print()

print("\nKeep browser open to inspect visually...")
input("Press Enter to close browser...")
driver.quit()
