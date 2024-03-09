import scrapy
import re
import numpy as np
import pandas as pd

class CovidSpider(scrapy.Spider):
    name = "covid"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/coronavirus/"]

    def get_td_content(self, td):
        anchor_text = td.xpath('.//a/text()').extract_first()
        if anchor_text:
            return anchor_text.strip()
        else:
            span_text = td.xpath('.//span/text()').extract_first()
            if span_text:
                return span_text.strip()
            else:
                td_text = td.xpath('text()').extract_first()
                if td_text:
                    return td_text.strip()
                else:
                    return ''

    def clean(self, txt):
        txt = np.nan if txt == 'N/A' or txt == '' else txt
        txt = int(txt.replace(',', '')) if isinstance(txt, str) and txt.replace(',', '').replace('+','').isdigit() else txt
        return txt

    def parse(self, response):
        columns_names = []
        for th in response.xpath('//*[@id="main_table_countries_today"]/thead/tr/th').extract()[1:]:
            cleaned_html = re.sub(r'<(br|/?(nobr))\s?/?>', ' ', th)
            columns_names.append(re.sub(r'\s+', ' ', scrapy.selector.unified.Selector(text=cleaned_html).xpath('//text()').extract_first().replace('\n','')))
        # columns_names = [item for item in columns_names if item.lower() != 'continent']
        columns_names[0] = columns_names[0].split(',')[0]
        tmp = []
        for tr in response.xpath("//*[@id=\"main_table_countries_today\"]/tbody[1]/tr[not(contains(@style, 'display: none'))]"):
            # item = CovidCountryItem()
            # td_elements = tr.xpath("td[not(contains(@style, 'display:none'))]")[1:]
            td_elements = tr.xpath("td")[1:]
            data = []
            for idx, td in enumerate(td_elements):
                txt = self.get_td_content(td)
                # item[item.get_keys()[idx]] = self.clean(txt)
                data.append(self.clean(txt))
            # yield item
            data_cleaned = [np.nan if value == 'N/A' or value == '' else value for value in data]
            data_cleaned = [
                int(value.replace(',', '')) if isinstance(value, str) and value.replace(',', '').isdigit() else value
                for value in data_cleaned]
            tmp.append(data_cleaned)

        df = pd.DataFrame(tmp, columns=columns_names)
        df.to_csv("data.csv", index=False)
