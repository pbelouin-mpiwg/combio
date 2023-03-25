import scrapy
from combio_app.models import Record


class WellcomeTrustSpider(scrapy.Spider):
    # records model from Django
    print(Record.objects.all())
    name = "wellcome_trust"
    allowed_domains = ["qmro.qmul.ac.uk"]
    start_urls = [
        "https://qmro.qmul.ac.uk/xmlui/handle/123456789/12359/browse?rpp=100&sort_by=2&type=dateissued&offset=0&etal=-1&order=ASC"
    ]

    def parse(self, response):
        # products = response.xpath("//*[contains(@class, 'ph-summary-entry-ctn')]/a/@href").extract()
        histories = response.json()
        for h in histories["results"]:
            url = "https://wellcomecollection.org/api/works/" + h["id"]
            # print(url);
            # url = urljoin(response.url, h)
            yield scrapy.Request(url, callback=self.parse_oral_history)
            # yield scrapy.Request(url, callback=self.save_pdf)

    # def parse_oral_history(self, response):
    #    page = response.url.split("/")[-2]
    #    filename = f'quotes-{page}.html'
    #    with open(filename, 'wb') as f:
    #        f.write(response.body)
    #    self.log(f'Saved file {filename}')

    def parse_oral_history(self, response):
        # self.server.start()
        item = {}
        scrapedData = response.json()
        title = scrapedData["title"]

        # this checks to see if the entity exists and needs to be moved if you are updating the db
        eCheck = requests.get(
            'http://127.0.0.1:8080/combiodb/oral_histories?filter={"title":"' + title + '"}&keys={"_id":1}'
        )
        # id = eCheck.json()[0]["_id"]["$oid"]
        # print(id)
        if len(eCheck.json()) == 0:
            # if True:
            item["title"] = title
            print("HERE IS THE TITLE")
            print(title)
            metadata = {}
            metadata_other = defaultdict(list)
            metadata_dc = {}
            metadata_combio = {}
            metadata_dc["subjects"] = [subject["label"] for subject in scrapedData["subjects"]]
            metadata_dc["contributors"] = [contributor["agent"]["label"] for contributor in scrapedData["contributors"]]
            metadata_combio["collection"] = "Wellcome Trust Seminars"
            # item['transcript_text'] = "";
            # print(scrapedData['items'][0]['locations'][1]["license"]["label"])
            locations = scrapedData["items"][0]["locations"]
            wtItemURL = None
            license = None
            for location in locations:
                try:
                    license = [location["license"]["label"]]
                    metadata_dc["license"] = license
                except:
                    print("no license here")

                try:
                    wtItemURL = location["url"]
                except:
                    print("no url here")

                if (wtItemURL != None) and (license != None):
                    break
            metadata["other"] = metadata_other
            metadata["dc"] = metadata_dc
            metadata["combio"] = metadata_combio
            item["metadata"] = metadata
            item["permalink"] = response.url.replace("api/", "")
            # wtItemURL = scrapedData['items'][0]['locations'][1]["url"]

            # try:
            #     yield scrapy.Request(
            #         wtItemURL, callback=self.parse_wt_item, cb_kwargs={"item": item}
            #     )
            # except:
            #     print("no pdf here")
            #     yield item
            yield item
            # interrupt scrape
            raise scrapy.exceptions.CloseSpider(reason="first loop")
        else:
            return

    def parse_wt_item(self, response, item):
        scrapedData = response.json()
        for ms in scrapedData["mediaSequences"]:
            for elem in ms["elements"]:
                pdfURL = elem["@id"]
                if pdfURL.split(".")[-1] == "pdf":
                    yield scrapy.Request(pdfURL, callback=self.save_pdf, cb_kwargs={"item": item})
