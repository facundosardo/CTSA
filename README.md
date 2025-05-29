# 📝 CT Acupuncturists Scraper

This script scrapes acupuncturist professional data from the **Connecticut Acupuncturists Association** website for professionals located in selected Connecticut cities.

---

## 📁 **Generated Files**  
- **ctsa.csv:** Master database containing all professionals collected without duplicates.  
- **ctsa_newprof.csv:** Contains only newly detected professionals during each run (empty if none found).  

---

## ⚙️ **Requirements**  
- **Python 3.x**  
- **Google Chrome**  
- **Selenium and WebDriver Manager:**  
    ```bash
    pip install selenium webdriver-manager
    ```  

---

## 🚀 **How to Use**  
1. **Clone or download the script.**  
2. **Install dependencies:**  
    ```bash
    pip install selenium webdriver-manager
    ```  
3. **Run the script:**  
    ```bash
    python ctsa.py
    ```  

---

## 🌐 **Script Details**  
- Automatically sets search location to **Fairfield, CT**.  
- Sets search radius and results per page to **100** each.  
- Scrolls the page to load all professionals.  
- Extracts these fields per professional:  
  - Name  
  - Address  
  - City (only selected CT cities included)  
  - Email address  
  - Phone number  
- Filters professionals by a predefined list of Connecticut cities only.  
- Prevents duplicates by checking the master file (`ctsa.csv`).  
- Saves new professionals found during the run to `ctsa_newprof.csv`.

---

## 🎯 **Cities of Interest**

Bethel, Bridgeport, Brookfield, Danbury, Darien, Easton, Fairfield, Greenwich, Monroe, New Canaan, Newtown, Norwalk, Redding, Ridgefield, Shelton, Sherman, Stamford, Stratford, Trumbull, Weston, Westport, Wilton, New Fairfield

---

## 🤖 **Customization**  
To change the list of target cities, edit the `cities_of_interest` list inside the script.

---

## 📌 **Notes**  
- Outputs CSV files with columns:  
  `Name`, `Address`, `City`, `Email address`, `Phone number`  
- Some professionals might lack email or phone data; those fields remain empty.  
- Make sure ChromeDriver version matches your installed Chrome browser.  
- Running multiple times only appends newly discovered professionals to the new professionals CSV.

