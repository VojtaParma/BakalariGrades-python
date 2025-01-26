from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options

# URL stránky pro přihlášení a známky
LOGIN_URL = "https://bakalari.gslapanice.cz/login"
GRADES_URL = "https://bakalari.gslapanice.cz/next/prubzna.aspx?s=chrono"

# Přihlašovací údaje
USERNAME = "ParmaV23Z"
PASSWORD = "2010K@pr"

# Nastavení Chrome pro headless režim
chrome_options = Options()
chrome_options.add_argument("--headless")  # Spustí prohlížeč bez GUI
chrome_options.add_argument("--disable-gpu")  # Zakáže použití GPU, což může pomoci v některých případech
chrome_options.add_argument("--no-sandbox")  # Potřebné pro některé verze Chrome

# Inicializace Selenium WebDriveru s headless režimem
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1. Otevři stránku pro přihlášení
    driver.get(LOGIN_URL)
    print("Načtena přihlašovací stránka.")

    # 2. Najdi pole pro uživatelské jméno a heslo a vyplň je
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    print("Vyplněny přihlašovací údaje.")

    # 3. Najdi tlačítko pro přihlášení a klikni na něj
    login_button = driver.find_element(By.ID, "loginButton")
    login_button.click()
    print("Kliknuto na tlačítko přihlášení.")

    # 4. Počkej 5 sekund (nebo dokud se stránka plně nenačte)
    time.sleep(5)
    print("Po 5 vteřinách přecházím na stránku se známkami...")

    # 5. Přesměruj na stránku se známkami
    driver.get(GRADES_URL)
    print("Jsem u známek.")

    # 6. Najdi tabulku se známkami
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Vynecháme hlavičku tabulky

    # 7. Zpracuj data z tabulky
    grades = []
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        grade = columns[2].text.strip()  # Změň index podle struktury stránky
        grades.append(grade)

    # Seznam všech známek (1 až 5)
    ALL_GRADES = ["1", "2", "3", "4", "5"]

    # Spočítej výskyt známek
    grade_counts = {grade: grades.count(grade) for grade in ALL_GRADES}

    # Přidej 0 pro známky, které nejsou přítomné
    for grade in ALL_GRADES:
        if grade not in grade_counts:
            grade_counts[grade] = 0

    # Výpis výsledků
    print("\nVýsledky (počet výskytů každé známky):")
    for grade, count in grade_counts.items():
        print(f"Známka {grade}: {count}x")

    # Ulož data do Excelu (volitelné)
    df = pd.DataFrame(list(grade_counts.items()), columns=["Známka", "Počet výskytů"])
    df.to_excel("znamky_pocet.xlsx", index=False)
    print("Data byla uložena do souboru 'znamky_pocet.xlsx'.")

except Exception as e:
    print(f"Nastala chyba: {e}")
    print("Prohlížeč zůstává otevřený pro ladění.")
finally:
    driver.quit()  # Ukončí Selenium WebDriver po dokončení úkolu
