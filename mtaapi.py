import os
import dotenv
import sys

from nyct_gtfs import NYCTFeed

dotenv.load_dotenv()
MTA_API_KEY: str | None = os.getenv('MTA_API_KEY')

if not MTA_API_KEY:
    print("Error - API key not found")
    sys.exit(1)

feed: NYCTFeed = NYCTFeed("1", api_key=MTA_API_KEY)

print(len(feed.trips))