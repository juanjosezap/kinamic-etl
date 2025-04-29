from scrapy import Item, Field

class ArtworkItem(Item):
    url = Field()
    artist = Field()
    title = Field()
    image = Field()
    height = Field()
    width = Field()
    description = Field()
    categories = Field()
    price = Field()
    dated = Field()
    medium = Field()
    dimensions = Field()
    date_added = Field()
    location = Field()

    properties_mapping = {
        "Price": "price",
        "Dated": "dated",
        "Medium": "medium",
        "Dimensions": "dimensions",
        "Date Added": "date_added",
        "Location": "location"
    }