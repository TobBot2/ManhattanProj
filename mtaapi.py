import os
import dotenv

from nyct_gtfs import NYCTFeed

dotenv.load_dotenv()
MTA_API_KEY: str = os.getenv('MTA_API_KEY')

feed: NYCTFeed = NYCTFeed("1", api_key=MTA_API_KEY)

print(len(feed.trips))