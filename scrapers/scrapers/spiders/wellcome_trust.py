from urllib.parse import urljoin
import scrapy
from scrapy.http import Request
from collections import defaultdict

import os
from dataclasses import dataclass, field
from typing import Any, Callable

# from pdfminer.high_level import extract_text

# from rich.progress import track
# from spacy.tokens import Doc, Token, Span

# from spacypdfreader.console import console
# from spacypdfreader.parsers import pdfminer
# from spacypdfreader.parsers.base import BaseParser
# from spacypdfreader._utils import _filter_doc_by_page, _get_number_of_pages
# import spacy
# from spacypdfreader import pdf_reader

import requests
from requests.auth import HTTPBasicAuth


# nlp = spacy.load("en_core_web_sm")

"""
def pdf_to_str(
    pdf_path: str,
    pdf_parser: BaseParser = pdfminer.PdfminerParser,
    verbose: bool = False,
    **kwargs: Any,
) -> str:
    if verbose:
        console.print(f"PDF to text engine: [blue bold]{pdf_parser.name}[/]...")

    pdf_path = os.path.normpath(pdf_path)
    num_pages = _get_number_of_pages(pdf_path)

    # Convert pdf to text.
    if verbose:
        console.print(f"Extracting text from {num_pages} pdf pages...")
    texts = ""
    for page_num in range(1, num_pages + 1):
        parser = pdf_parser(pdf_path, page_num)
        text = parser.pdf_to_text(**kwargs)
        texts = texts + " " + text;

    return texts
"""


class Wellcome_Trust_Spider(scrapy.Spider):
    name = "wellcome_trust"

    start_urls = [
        "https://api.wellcomecollection.org/catalogue/v2/works?partOf.title=Wellcome+witnesses+to+twentieth+century+medicine&pageSize=52"
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

    def save_pdf(self, response, item):
        # response.css("tr.ds-table-row"):
        path = "wellcome_trust_pdfs/" + response.url.split("/")[-1]
        print(path)
        self.logger.info("Saving PDF %s", path)
        # name = path.split('?')[0].replace('%20', '_').replace('%2C', '')
        with open(path, "wb") as f:
            f.write(response.body)

        # doc = pdf_reader(path, nlp);
        # item['transcript_text'] = doc.text;

        # item['transcript_text'] = pdf_to_str(path);

        item["transcript_text"] = textract.process(path)

        yield item
