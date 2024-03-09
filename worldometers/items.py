# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CovidCountryItem(scrapy.Item):
    country = scrapy.Field()
    totalCases = scrapy.Field()
    newCases = scrapy.Field()
    totalDeaths = scrapy.Field()
    newDeaths = scrapy.Field()
    totalRecovered = scrapy.Field()
    newRecovered = scrapy.Field()
    activeCases = scrapy.Field()
    critical = scrapy.Field()
    totalCasesPer1M = scrapy.Field()
    totalDeathsPer1M = scrapy.Field()
    TotalTests = scrapy.Field()
    TestsPer1M = scrapy.Field()
    population = scrapy.Field()
    caseEveryXPpl = scrapy.Field()
    deathEveryXPpl = scrapy.Field()
    testEveryXPpl = scrapy.Field()
    newCasesPer1M = scrapy.Field()
    newDeathsPer1M = scrapy.Field()
    activeCasesPer1M = scrapy.Field()

    def get_keys(self):
        return [
            'country',
            'totalCases',
            'newCases',
            'totalDeaths',
            'newDeaths',
            'totalRecovered',
            'newRecovered',
            'activeCases',
            'critical',
            'totalCasesPer1M',
            'totalDeathsPer1M',
            'TotalTests',
            'TestsPer1M',
            'population',
            'caseEveryXPpl',
            'deathEveryXPpl',
            'testEveryXPpl',
            'newCasesPer1M',
            'newDeathsPer1M',
            'activeCasesPer1M',
        ]
