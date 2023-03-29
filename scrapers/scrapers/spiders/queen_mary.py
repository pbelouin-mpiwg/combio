from urllib.parse import urljoin
import scrapy
from scrapy.http import Request
from scrapy import crawler


class QueenMarySpider(scrapy.Spider):
    name = "queen_mary"

    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapers.pipelines.ComBioScrapersPipeline": 300,
        }
    }

    def start_requests(self):
        urls = [
            "https://qmro.qmul.ac.uk/xmlui/handle/123456789/12359/browse?rpp=100&sort_by=2&type=dateissued&offset=0&etal=-1&order=ASC"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.css)
        histories = response.css("div.artifact-description a::attr(href)").getall()

        print(histories)
        for h in histories:
            #     print(h)
            url = urljoin(response.url, h) + "?show=full"
            print(url)
            yield scrapy.Request(url, callback=self.parse_oral_history)
            # interrupt scrape
            raise scrapy.exceptions.CloseSpider(reason="first loop")

    def parse_oral_history(self, response):
        item = {}
        # id = eCheck.json()[0]["_id"]["$oid"]
        # print(id)

        item = {}
        metadata_dc = {}
        metadata_combio = {}
        metadata_dc["contributors"] = []
        for index, data in enumerate(response.css("tr.ds-table-row")):
            field = data.css("td.label-cell::text").get().split(".")
            if len(field) == 2:
                field = field[1]
            else:
                field = field[1] + " (" + field[2] + ")"
            val = data.css("td.word-break::text").get()
            # yield {
            if field == "title":
                item["title"] = val
            elif field == "identifier (uri)":
                item["permalink"] = val
            elif field == "rights":
                metadata_dc["license"] = val
            else:
                if field == "contributor":
                    # print("###########CONTRIBUTORS ARRAY##############")
                    metadata_dc["contributors"].append(val)
                    if index == 0:
                        metadata_combio["interviewers"] = [val]
                    if index == 1:
                        metadata_combio["interviewees"] = [val]
                else:
                    # print("-----FIELD-----")
                    # print(field)
                    # print("----VAL----")
                    # print(val)
                    metadata_dc[field] = [val]

                # url=response.urljoin(href),
                # callback=self.save_pdf
            # }

        pdfURL = response.css("meta[content*=pdf]::attr(content)").get()
        metadata_dc["pdf"] = pdfURL.split("/")[-1].split("?")[0]
        item["metadata"] = {}
        item["metadata"]["dc"] = metadata_dc
        metadata_combio[
            "collection"
        ] = "Queen Mary University of London History of Modern Biomedicine Interviews (Digital Collection)"
        item["metadata"]["combio"] = metadata_combio
        # item['transcript_text'] = "";
        metadata_combio = {}

        yield item
        # yield scrapy.Request(pdfURL, callback=self.save_pdf, cb_kwargs={'item': item})
