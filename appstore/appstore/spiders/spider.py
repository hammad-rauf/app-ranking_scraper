from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from datetime import date

from ..items import AppstoreItem

class AppStoreSpider(CrawlSpider):

    name = "appranking"
    start_urls = [
                "https://apps.shopify.com/browse/all?app_integration_kit=off&app_integration_pos=off&pricing=all&requirements=off&sort_by=installed",
                "https://apps.shopify.com/browse/all?app_integration_kit=off&app_integration_pos=off&pricing=all&requirements=off&sort_by=relevance",
                "https://apps.shopify.com/browse/all?app_integration_kit=off&app_integration_pos=off&pricing=all&requirements=off&sort_by=newest"
    ]


    categorys = ["all","store-design","sales-and-conversion-optimization","marketing","orders-and-shipping","customer-support","inventory-management",
                "reporting","productivity","finding-and-adding-products","finances","trust-and-security","places-to-sell"
    ]

    typee = ["installed","relevance","newest"] 

    rules = (
        Rule(LinkExtractor(restrict_css=("#CategoriesFilter .search-filter-group.accordion-item")),callback="parse_product"),
        Rule(LinkExtractor(restrict_css=(".search-pagination.display--mobile.text-center .search-pagination__next-page-text")),callback="parse_product"), 
    )


    today_date = date.today()

    def parse_product(self,response):

        links = response.css(".ui-app-card::attr(data-target-href)").extract()

        next_page = response.css(".search-pagination.display--mobile.text-center .search-pagination__next-page-text::attr(href)").extract_first()
        
        for link in links:
            product = AppstoreItem()

            for data in self.typee:
                if data in response.url:
                    product["type"] = data

            yield Request(url = link,callback=self.product,meta={"product":product})

        yield response.follow(url = next_page,callback=self.parse_product)

    def product(self, response):

        product = response.meta["product"]

        product["date"] = self.today_date

        for category in self.categorys:
            if category in response.url:
                product["category"] = category


        ranking = response.url

        start_page = ranking.index("position=") + 9
        end_page = ranking.index("&surface_intra_position")


        start = ranking.index("&surface_intra_position=") + 24
        end = ranking.index("&surface_type=")

        rank = 0

        if int(ranking[start_page:end_page]) > 1:
            rank = int(ranking[start_page:end_page]) - 1
            rank = rank * 24
            rank = rank + int(ranking[start:end])
        else:
            rank = rank + int(ranking[start:end])

        product["ranking"] = rank

        try :

            sub_category = response.url
            sub_start = sub_category.index(f'{product["category"]}-') + len(product["category"]) + 1
            sub_end = sub_category.index("&surface_inter")

            product["subcategory"] = response.url[sub_start:sub_end]

        except ValueError:

            product["subcategory"] = product["category"]

        if product["subcategory"] == "in-one?surface_detail=all":
            product["subcategory"] = product["category"]



        product["app_name"] = response.css(".heading--2.ui-app-store-hero__header__app-name::text").extract_first()
        product["app_link"] = response.url
        product["app_link"] = product["app_link"].split("?")[0]

        yield product

