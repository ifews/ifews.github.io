from dotenv import load_dotenv
import os
import urllib.request
import pandas as pd
from io import StringIO
load_dotenv()
API_key = os.getenv('API_KEY')

class c_usda_quick_stats:

    def __init__(self):
        # Set the USDA QuickStats API key and API base URL.
        self.api_key = API_key
        self.base_url_api_get = 'http://quickstats.nass.usda.gov/api/api_GET/?key=' + self.api_key + '&'

    def get_data(self, parameters):
        # Call the api_GET API with the specified parameters.
        # Retrieve the data from the Quick Stats server.
        full_url = self.base_url_api_get + parameters
        s_result = urllib.request.urlopen(full_url)
        s_text = s_result.read().decode('utf-8')

        # Parse the CSV data into a DataFrame.
        df = pd.read_csv(StringIO(s_text))

        return df    