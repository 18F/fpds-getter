import requests
import xmltodict
import json
from urllib.parse import urlparse, parse_qs


class FPDS:
    def get_data_from_fpds(self, start_date, end_date):
        """
        The powerhouse of the FPDS class. This iterates through the FPDS pages and returns a dict with all of the entries for a date range.
        """
        d = self._get_data_from_url(start_date, end_date, offset=0)

        # Here, we should call the generator to cycle through the range
        pages = range(int(parse_qs(urlparse(d["feed"]["link"][2]["@href"]).query)["start"][0]), int(parse_qs(urlparse(d["feed"]["link"][1]["@href"]).query)["start"][0]), 10)
        results = []

        for page in pages:
            # I *think* this is where we can take advantage of parallel processing...
            d = self._get_data_from_url(start_date, end_date, page)
            # This is where the XML for the page comes in... at this point, it's possible to do things like save data to file or do additional processing.
            results.append([entry for entry in d["feed"]["entry"]])
        return results

    def _get_data_from_url(self, start_date, end_date, offset):
        """
        Private method to get a page from FPDS.
        Returns a dict from the FPDS XML
        """

        baseurl = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
        params = "LAST_MOD_DATE:[%s,%s]" % (start_date, end_date)
        r = requests.get(baseurl, params={"q": params, "start": offset})

        # Convert the XML into a JSON object
        d = xmltodict.parse(r.text)
        return d


if __name__ == '__main__':
    d = FPDS().get_data_from_fpds(start_date="2016/01/01", end_date="2016/01/01")
    with open('results.json', 'w') as f:
        f.write(json.dumps(d))
