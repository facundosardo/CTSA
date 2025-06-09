import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# CSV filenames
MASTER_FILE = "ctsa.csv"
NEW_FILE = "ctsa_newprof.csv"

# List of target cities to filter professionals
TARGET_CITIES = [
    "Ansonia", "Beacon Falls", "Bethany", "Branford", "Cheshire", "Derby",
    "East Haven", "Guilford", "Hamden", "Madison", "Meriden", "Middlebury",
    "New Haven", "North Branford", "North Haven", "Orange", "Oxford", "Prospect",
    "Seymour", "Shelton", "Southbury", "Wallingford", "Waterbury", "West Haven",
    "Woodbridge", "Bethel", "Bridgeport", "Brookfield", "Danbury", "Darien",
    "Easton", "Fairfield", "Greenwich", "Monroe", "New Canaan", "Newtown",
    "Norwalk", "Redding", "Ridgefield", "Shelton", "Sherman", "Stamford",
    "Stratford", "Trumbull", "Weston", "Westport", "Wilton", "New Fairfield",
]

def main():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)

    # Open practitioners page
    driver.get("https://www.ctacupuncturists.org/practitioners/")

    # Set location input to "Fairfield, CT"
    location_input = wait.until(EC.element_to_be_clickable((By.ID, "wpsl-search-input")))
    location_input.clear()
    location_input.send_keys("Fairfield, CT")
    time.sleep(1)

    # Set search radius to 100 miles
    search_radius_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wpsl-radius .wpsl-selected-item")))
    search_radius_dropdown.click()
    time.sleep(1)
    option_100_radius = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='wpsl-radius']//li[@data-value='100']")))
    option_100_radius.click()
    time.sleep(1)

    # Set results count to 100
    results_dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wpsl-results .wpsl-selected-item")))
    results_dropdown.click()
    time.sleep(1)
    option_100_results = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='wpsl-results']//li[@data-value='100']")))
    option_100_results.click()
    time.sleep(1)

    # Click the Search button
    search_button = wait.until(EC.element_to_be_clickable((By.ID, "wpsl-search-btn")))
    search_button.click()
    time.sleep(3)  # Wait for results to load

    # Scroll down multiple times to load all results
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Extract professionals container elements
    professionals = driver.find_elements(By.CSS_SELECTOR, "div.wpsl-store-location")

    # Load existing professionals to avoid duplicates
    existing_keys = set()
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, "r", encoding="utf-8") as f_master:
            reader = csv.reader(f_master)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    key = (row[0], row[1], row[2])  # Name, Address, City
                    existing_keys.add(key)

    new_pros = []
    all_pros = []

    # Process each professional entry
    for prof in professionals:
        # Extract name with fallback if needed
        name = ""
        try:
            name = prof.find_element(By.CSS_SELECTOR, "strong > a").text.strip()
        except:
            try:
                name = prof.find_element(By.CSS_SELECTOR, "strong").text.strip()
            except:
                name = "Name not found"

        # Extract address
        try:
            address = prof.find_element(By.CSS_SELECTOR, "span.wpsl-street").text.strip()
        except:
            address = ""

        # Extract city by checking presence of cities of interest in the full text
        container_text = prof.text
        city_name = None
        for city in CITIES_OF_INTEREST:
            if city.lower() in container_text.lower():
                city_name = city
                break

        # Skip if city not in cities of interest
        if not city_name:
            print(f"Skipping professional '{name}' due to city not in list.")
            continue

        # Extract email and phone
        email = ""
        phone = ""
        try:
            contact_spans = prof.find_elements(By.XPATH, ".//p[@class='wpsl-contact-details']/span")
            for span in contact_spans:
                text = span.text.strip()
                if text.startswith("Email"):
                    email = text.replace("Email:", "").strip()
                elif text.startswith("Phone"):
                    phone = text.replace("Phone:", "").strip()
        except:
            pass

        # Create a unique key to check duplicates
        key = (name, address, city_name)

        # Add to all professionals list
        all_pros.append([name, address, city_name, email, phone])

        # Add to new professionals if not already present
        if key not in existing_keys:
            existing_keys.add(key)
            new_pros.append([name, address, city_name, email, phone])

    # Save master CSV (overwrite all data)
    with open(MASTER_FILE, "w", newline="", encoding="utf-8") as f_master:
        writer = csv.writer(f_master)
        writer.writerow(["Name", "Address", "City", "Email address", "Phone number"])
        writer.writerows(all_pros)

    # Save new professionals only
    with open(NEW_FILE, "w", newline="", encoding="utf-8") as f_new:
        writer = csv.writer(f_new)
        writer.writerow(["Name", "Address", "City", "Email address", "Phone number"])
        writer.writerows(new_pros)

    print(f"Extracted {len(all_pros)} professionals, {len(new_pros)} new.")

    driver.quit()

if __name__ == "__main__":
    main()