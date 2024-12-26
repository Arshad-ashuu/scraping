# import requests
# from bs4 import BeautifulSoup
# import json

# def amazon(part_name):

#   url = f"https://www.amazon.in/s?k={part_name}"
#   response = requests.get(url)
#   soup = BeautifulSoup(response.text, 'html.parser')

#   results = soup.findAll("div", {"class": "sg-col-inner"})
#   shirt_data = []

#   for item in results:
    
#     try:
#       title = item.find("h2", {"class": "a-size-base-plus a-spacing-none a-color-base a-text-normal"}).get_text().strip()
#       price = item.find("span", {"class": "a-price-whole"}).get_text().strip()
#       link = "https://amazon.in" + item.find("a", {"class": "a-link-normal a-text-normal"})['href'].strip()
#       img_link = item.find("img")['src']

#       if "shirt".lower() in title.lower():
#         shirt_data.append({
#           "title": title,
#           "price": price,
#           "link": link,
#           "image_link": img_link
#         })

#     except Exception as e:
#       continue  # Handle exceptions gracefully

#   return json.dumps(shirt_data) 

# # Example usage
# shirts_json = amazon("shirts")
# print(shirts_json)


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_souled_store_products(url, num_pages=1, driver=None):

    if not driver:
        raise ValueError("WebDriver instance is required")
        
    product_names = []
    product_prices = []

    for page in range(num_pages):
        # Add page parameter to URL if needed
        page_url = f"{url}?page={page + 1}" if page > 0 else url
        driver.get(page_url)
        
        # Wait for dynamic content to load
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find all product cards
        # Note: You may need to update these selectors based on the website's structure
        products = soup.find_all('div', class_='sg-col-inner')
        
        for product in products:
            # Extract product name
            name_elem = product.find('h2', class_='a-size-base-plus a-spacing-none a-color-base a-text-normal')
            if name_elem:
                product_names.append(name_elem.text.strip())
            else:
                product_names.append(None)
            
            # Extract product price
            price_elem = product.find('span', class_='a-price-whole')
            if price_elem:
                # Clean up price text (remove currency symbol and convert to float)
                price_text = price_elem.text.strip().replace('₹', '').replace(',', '')
                try:
                    price = float(price_text)
                    product_prices.append(price)
                except ValueError:
                    product_prices.append(None)
            else:
                product_prices.append(None)

    # Create DataFrame
    product_df = pd.DataFrame({
        'Product Name': product_names,
        'Price': product_prices
    })
    
    return product_df

def get_valid_input():
    """Gets valid user input for scraping parameters."""
    while True:
        try:
            print("\nSouled Store Scraper Parameters:")
            print("--------------------------------")
            url = input("Enter the Souled Store URL to scrape: ").strip()
            if not url:
                print("URL cannot be empty!")
                continue
            
            if not url.startswith("https://www.amazon.in/s?k=shirt"):
                print("Please enter a valid Souled Store URL!")
                continue
                
            num_pages = int(input("Enter the number of pages to scrape: "))
            if num_pages <= 0:
                print("Number of pages must be greater than 0!")
                continue
                
            return url, num_pages
        except ValueError:
            print("Please enter a valid number for pages!")

def save_data(product_data):
    """Saves the scraped data to CSV file."""
    try:
        product_data.to_csv("souled.csv", index=False)
        print("Product data saved to souled_store_products.csv")
    except PermissionError:
        print("Could not save to souled_store_products.csv - file may be open in another program")
        try:
            product_data.to_json("souled_store_products_new.csv", index=False)
            print("Product data saved to souled_store_products_new.csv instead")
        except:
            print("Could not save data to CSV")

def main():
    driver = None
    product_data = None
    
    try:
        # Get user input
        url, num_pages = get_valid_input()

        # Set up Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()

        # Fetch product data
        try:
            product_data = fetch_souled_store_products(url, num_pages, driver)
            if product_data is not None and not product_data.empty:
                print("\nFetched Product Data Preview:")
                print(product_data.head())
                
                # Save data to CSV
                save_data(product_data)
                
                # Display some basic statistics
                print("\nProduct Statistics:")
                print(f"Total products found: {len(product_data)}")
                print(f"Average price: ₹{product_data['Price'].mean():.2f}")
                print(f"Price range: ₹{product_data['Price'].min():.2f} - ₹{product_data['Price'].max():.2f}")
            else:
                print("No product data was fetched.")
                
        except Exception as e:
            print(f"An error occurred while fetching data: {str(e)}")

    finally:
        # Clean up
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    main()