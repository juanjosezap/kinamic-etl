from itemadapter import ItemAdapter
from datetime import datetime
import re
import requests
import mysql.connector
import os

class ArtworksPipeline:

    def process_artist(self, artists: str) -> [str]:
        artist_list = []

        if artists:
            split_artist_list = artists.split(";")

            for artist in split_artist_list:
                if artist == "":
                    continue
                if ":" in artist:
                    artist = artist.split(":")[1]
                
                artist_list.append(artist.strip())

        return artist_list

    def process_categories(self, categories: [str]) -> [str]:
        category_list = [] 

        for category in categories:
            if category == "":
                continue
            if "?" in category:
                category = category.split("?")[0]
            
            category_list.append(category)

        return category_list

    def process_date_added(self, date_added: str) -> str:
        # Remove "the" and trim spaces
        cleaned = date_added.replace(" the ", " ").strip()
        # Use regex to remove ordinal suffixes ONLY from the day (e.g., 1st → 1)
        cleaned = re.sub(r'(\d+)(st|nd|rd|th)\b', r'\1', cleaned)
        # Parse and format
        date_obj = datetime.strptime(cleaned, "%B %d, %Y")
        return date_obj.strftime("%Y-%m-%d")
        
    def process_price(self, price: str) -> float:
        try:
            return float(price.replace("$", ""))
        except:
            return 0


    def extract_cm_dimensions(self, dimensions: str):
        # Regex pattern to find all "X x Y cm" values inside parentheses
        pattern = r'\(\s*([\d.]+)\s*x\s*([\d.]+)\s*cm\s*\)'
        matches = re.findall(pattern, dimensions)
        # Convert matched strings to floats and return as tuples
        return [(float(w), float(h)) for w, h in matches]

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        artists_list = self.process_artist(adapter.get("artist"))
        
        if len(artists_list) > 0: 
            item["artist"] = artists_list

        item["categories"] = self.process_categories(adapter.get("categories"))

        item["date_added"] = self.process_date_added(adapter.get("date_added"))
        item["price"] = self.process_price(adapter.get("price"))

        dimensions = self.extract_cm_dimensions(adapter.get("dimensions"))
        if dimensions:
            item["width"] = dimensions[0][0]
            item["height"] = dimensions[0][1]

        return item

class ProxiesPipeline:
    def open_spider(self, spider):
        # Open the file when the spider starts
        current_path = os.getcwd()
        print(f'----> {current_path}')
        self.file = open('proxies.txt', 'w', encoding='utf-8')

    def close_spider(self, spider):
        # Close the file when the spider finishes
        self.file.close()

    def test_proxy(self, proxy: str):
        try:
            response = requests.get("https://httpbin.org/ip", 
                proxies={"http": proxy},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def process_last_checked(self, last_checked: str) -> str:
        
        last_checked = last_checked.replace(" ago", "").strip()
        number = int(last_checked.split(" ")[0])
        unit = last_checked.split(" ")[1]

        if unit == "mins":
            seconds = number * 60
        else:
            seconds = number

        if seconds <= 300:
            return True
        else:
            return False

    def process_item(self, item, spider):
        # Write the item data to the file
        if not self.process_last_checked(item["last_checked"]):
            return
        if not self.test_proxy(item["proxy"]):
            return
        line = f"{item['proxy']}\n"
        self.file.write(line)
        return item

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'scrapy',
            passwd = 'scrapy',
            database = 'scrapinghub_db'
        )
        self.curr = self.conn.cursor()

        # CREATE TABLE IF NOT EXISTS
        self.curr.execute("""
        CREATE TABLE IF NOT EXISTS artworks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) NOT NULL,
            artist VARCHAR(255) NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            image VARCHAR(255),
            categories VARCHAR(255),
            price DECIMAL(10, 2),
            dated VARCHAR(50),
            date_added VARCHAR(50),
            location VARCHAR(50),
            width DECIMAL(10, 2),
            height DECIMAL(10, 2),
            medium VARCHAR(100),
            dimensions VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)    


    def process_item(self, item, spider):
        if 'artist' not in item.keys() or item['artist'] == [] or item['artist'] == None:
            artist = ""
        else:
            artist = item['artist'][0]

        categories = "-".join(item['categories'])
        self.curr.execute("""
        INSERT INTO artworks (url, artist, title, description, image, categories, price, dated, date_added, location, width, height, medium, dimensions)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['url'],
            artist,
            item['title'],
            item['description'],
            item['image'],
            categories,
            item['price'],
            item['dated'],
            item['date_added'],
            item['location'],
            item['width'],
            item['height'],
            item['medium'],
            item['dimensions']
        ))
        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        self.curr.close()
        self.conn.close()