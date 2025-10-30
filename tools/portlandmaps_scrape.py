import time
import os
import pandas as pd
import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.portlandmaps.com/advanced/?action=assessor"

def rename_latest_csv(download_dir, neighborhood, page_num):
    """Rename the most recently downloaded CSV file"""
    # Find the most recent CSV in downloads folder
    csv_files = glob.glob(os.path.join(download_dir, "*.csv"))
    if not csv_files:
        return None
    
    latest_file = max(csv_files, key=os.path.getctime)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create new filename
    new_filename = f"{neighborhood}_page{page_num}_{timestamp}.csv"
    new_path = os.path.join(download_dir, new_filename)
    
    # Rename the file
    os.rename(latest_file, new_path)
    print(f"    Renamed to: {new_filename}")
    return new_path

# Setup browser
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": os.getcwd() + "/downloads"}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "select")))

# Grab neighborhood names
select = Select(driver.find_element(By.TAG_NAME, "select"))
neighborhoods = [o.get_attribute("value") for o in select.options if o.get_attribute("value") != ""]

print(f"Found {len(neighborhoods)} neighborhoods")

os.makedirs("downloads", exist_ok=True)

# Check which neighborhoods already have downloads
existing_files = set()
if os.path.exists("downloads"):
    for f in os.listdir("downloads"):
        if f.endswith(".csv"):
            # Extract neighborhood name from filename (format: NEIGHBORHOOD_pageX_timestamp.csv)
            neighborhood_name = f.split("_page")[0] if "_page" in f else f.split("_")[0]
            existing_files.add(neighborhood_name.upper())

print(f"Found {len(existing_files)} neighborhoods already downloaded")

for hood in neighborhoods:
    if hood in existing_files:
        print(f"Skipping {hood} (already downloaded)")
        continue
        
    print(f"Processing: {hood}")

    # Select neighborhood
    select.select_by_value(hood)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]" )))
    driver.find_element(By.XPATH, "//button[contains(text(),'Search')]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'CSV')]" )))

    # Check if results exist and handle pagination
    try:
        page_num = 1
        
        # First, check if pagination exists by looking for page links
        has_pagination = False
        try:
            # Look for numbered page links (they're <a> tags, not buttons!)
            page_links = driver.find_elements(By.XPATH, "//a[text()='2' or text()='3' or text()='4' or text()='5']")
            if len(page_links) > 0:
                has_pagination = True
                print(f"  Found multiple pages for {hood}")
        except:
            pass
        
        if not has_pagination:
            # Single page - just download once
            print(f"  Single page result for {hood}")
            csv_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'CSV')]" )))
            csv_button.click()
            time.sleep(3) # Wait for download to initiate
            rename_latest_csv("downloads", hood, 1)
        else:
            # Multiple pages - download each page
            while True:
                print(f"  Downloading page {page_num} for {hood}")
                
                # Click CSV download for current page
                csv_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'CSV')]" )))
                csv_button.click()
                time.sleep(3)  # Wait for download to initiate
                rename_latest_csv("downloads", hood, page_num)
                
                # Try to find and click the next page link
                try:
                    # Look for <a> tag with title="Go to next page"
                    next_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Go to next page']")))
                    
                    print(f"  Moving to page {page_num + 1}")
                    next_link.click()
                    WebDriverWait(driver, 10).until(EC.staleness_of(next_link)) # Wait for the page to change
                    time.sleep(2) # Give a little extra time for content to load
                    page_num += 1
                        
                except:
                    # No next link found - we're on the last page
                    print(f"  Last page reached for {hood}")
                    break
                
    except Exception as e:
        print(f"No results or error for {hood}: {e}")

    # Reset
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Clear')]" ))).click()
    time.sleep(2)

driver.quit()

# Combine CSVs
files = [f"downloads/{f}" for f in os.listdir("downloads") if f.endswith(".csv")]
frames = []

for f in files:
    df = pd.read_csv(f)
    df["neighborhood"] = os.path.basename(f).replace(".csv","")
    frames.append(df)

combined = pd.concat(frames, ignore_index=True)
combined.to_csv("Portland_Assessor_AllNeighborhoods.csv", index=False)

print("✅ All done. Combined file ready.")
