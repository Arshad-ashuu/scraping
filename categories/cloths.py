parts_sites = {
    "%20": [("www.amazon.in", "https://www.amazon.in/s?k=item goes here"), ("www.souledStore.com", "https://www.souledStore.com/search/result?q=item goes here"), ("www.souledStore.com", "https://www.shoppersstop.com/search/result?q=item goes here")],
}

def scrape_site(site, part_name, soup):
    '''
    Function to call Parts Scraper for respective Site
    It returns list of Part objects corresponding to the given part name in a respective site
    It takes arguments site name, part name, BeautifulSoup object of site
    '''
    if site == "www.amazon.in":
        site_function = amazon
    elif site == "www.souledStore.com":
        site_function = souledStore
    elif site == "www.shoppersstop.com":
        site_function = shoppersStop
    part_list = site_function(soup, part_name, site)
    return part_list


def amazon(soup, part_name, site):
    '''
    Function to scrape Part from amazon.in
    It returns a list of Part objects satisfying the part name
    It takes Arguments BeautifulSoup object of amazon.in part search, part name
    '''
    results = soup.findAll("div", {"class": "sg-col-inner"})
    part_list = []
    for item in results:
        try:
            title = item.find(
                "span", {"h2": "a-size-base-plus a-spacing-none a-color-base a-text-normal"}).get_text().strip()
            price = item.find(
                "span", {"span": "a-price-whole"}).get_text().strip()
            link = "https://amazon.in" + \
                item.find(
                    "a", {"class": "a-link-normal a-text-normal"})['href'].strip()
            img_link = item.find(
                "div", {"class": "s-image"}).img["src"]
            flag = 0
            for word in part_name.split(" "):
                if(word not in title.lower().split()):
                    flag = 1
                    break
            if(flag == 0):
                part_list.append((title, price, link, img_link, site))
        except:
            continue
    return part_list

def souledStore(soup, part_name, site):
    '''
    Function to scrape Part from souledStore.com
    It returns a list of Part objects satisfying the part name
    It takes Arguments BeautifulSoup object of the souledStore.com part search, part name
    '''
    results = soup.findAll("div", {"class": "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"})
    part_list = []
    for item in results:
        try:
            title = item.find(
                "h5", {"class": "text-left"}).get_text().strip()
            price = item.find(
                "span", {"class": "offer fsemibold"}).get_text().strip()
            link = "https://www.souledstore.com" + \
                item.find(
                    "a", {"class": "a-link-normal a-text-normal"})['href'].strip()
            img_link = item.find(
                "img", {"class": "customFade custom-border img-auto gm-added"})["src"]
            flag = 0
            for word in part_name.split(" "):
                if(word not in title.lower().split()):
                    flag = 1
                    break
            if(flag == 0):
                part_list.append((title, price, link, img_link, site))
        except:
            continue
    return part_list

def shoppersStop(soup, part_name, site):
    '''
    Function to scrape Part from shoppersstop.com
    It returns a list of Part objects satisfying the part name
    It takes Arguments BeautifulSoup object of shoppersstop.com part search, part name
    '''
    results = soup.findAll("div", {"class": "product-item"}) # Placeholder class
    part_list = []
    for item in results:
        try:
            title = item.find("a", {"class": "product-name"}).text.strip() # Placeholder selectors
            price = item.find("span", {"class": "product-price"}).text.strip() # Placeholder selectors
            link = "https://www.shoppersstop.com" + item.find("a")["href"] # Placeholder selectors
            img_link = item.find("img")["src"] # Placeholder selectors
            flag = 0
            for word in part_name.split(" "):
                if word not in title.lower().split():
                    flag = 1
                    break
            if flag == 0:
                part_list.append((title, price, link, img_link, site))
        except:
            continue
    return part_list
