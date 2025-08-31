import csv
import os
import re
import time, zoneinfo
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class FlipkartScraper:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def get_top_review(self, product_url, count=2):
        """Get the top reviews for a product"""
        options = uc.ChromeOptions()
        options.add_argument("--no--sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = uc.Chrome(options=options, use_subprocess=True)

        if not product_url.startswith("http"):
            return "No reviews found"
        
        try:
            driver.get(product_url)
            time.sleep(4)
            try:
                driver.find_element(By.XPATH,"//button[contains(text(),'X')]").click()
                time.sleep(1)
            except Exception as e:
                print(f"Error occurred while closing popup: {e}")

            for _ in range(4):
                ActionChains(driver).send_keys(Keys.END).perform()
                time.sleep(1.5)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            review_blocks = soup.select("div._27M-vq, div.col.EPCmJX,div._6K-7Co")
            seen = set()
            reviews =[]

            for block in review_blocks:
                text = block.get_text(separator=" ", strip=True)
                if text and text not in seen:
                    reviews.append(text)
                    seen.add(text)
                if len(reviews) >=count:
                    break
        except Exception as e:
            reviews =[]
        driver.quit()
        return " || ".join(reviews) if reviews else "No reviews found"


    def scrape_flipkart_products(self):
        """Scrape fligkart products based on a search query"""
        pass

    def save_to_csv(self, data, filename="product_reviews.csv"):
        """Save the scraped product reviwes to a CSV file"""
        pass
    