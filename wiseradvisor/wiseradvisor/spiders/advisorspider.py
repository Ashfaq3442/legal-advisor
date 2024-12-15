import scrapy


class AdvisorspiderSpider(scrapy.Spider):
    name = "advisorspider"
    allowed_domains = ["www.wiseradvisor.com"]
    start_urls = ["https://www.wiseradvisor.com/financial-advisors.asp/"]

    def parse(self, response):
        links=response.css('ul.bullet_list.directory li a::attr(href)').getall()
        for link in links:
            joint_link=response.urljoin(link)
            yield response.follow(joint_link,callback=self.parse_)
            

    def parse_(self, response):
        rows = response.css("tbody tr")  # Select all rows within the tbody tag
        for row in rows:
            # Extract the advisor's name
            name = row.css("div.firm-advisor b a::text").get()

            # Extract the firm name by joining all text within the div.firm-advisor
            firm_info = row.css("div.firm-advisor::text").getall()
            firm_name = " ".join([text.strip() for text in firm_info if text.strip()])

            # Extract the full address
            address_parts = row.css("div.firm-advisor span span::text").getall()
            full_address = ", ".join([part.strip() for part in address_parts if part.strip()])

            # Extract other table data
            experience = row.css('td[data-label="Experience"] .table-txt::text').get()
            aum = row.css('td[data-label="AUM"] .table-txt::text').get()
            min_assets = row.css('td[data-label="Minimum Assets"] .table-txt::text').get()
            fee_structure = row.css('td[data-label="Fee Structure"] .table-txt::text').get()

            # Yield the scraped data
            yield {
                'Name': name,
                'Firm Name': firm_name,
                'Address': full_address,
                'Experience': experience,
                'AUM': aum,
                'Minimum Assets': min_assets,
                'Fee Structure': fee_structure,
            }
