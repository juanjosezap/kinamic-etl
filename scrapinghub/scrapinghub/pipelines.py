from itemadapter import ItemAdapter
from datetime import datetime
import re
class ArtworksPipeline:

    def process_artist(self, artists: str) -> list[str]:
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
        return float(price.replace("$", ""))


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
        else:
            item.pop("artist")

        item["categories"] = self.process_categories(adapter.get("categories"))

        item["date_added"] = self.process_date_added(adapter.get("date_added"))
        item["price"] = self.process_price(adapter.get("price"))

        dimensions = self.extract_cm_dimensions(adapter.get("dimensions"))
        if dimensions:
            item["width"] = dimensions[0][0]
            item["height"] = dimensions[0][1]

        return item