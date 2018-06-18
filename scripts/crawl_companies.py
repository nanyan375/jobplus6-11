import json
from scrapy.http import HtmlResponse

def spider():
    body = open('test.html').read()
    response = HtmlResponse(url='http://example.com', body=body.encode('utf-8'))
    results = []

    for company in response.xpath('//div[@class="media"]'):
        middle = company.xpath('.//li[@class="text-muted"]\
                                /span/text()').extract()[1:]
        result = dict(
            title = company.xpath('.//h4[@class="media-heading"]\
                                /a/text()').extract_first(),
            site = company.xpath('.//a[@class="company-site"]\
                                /@href').extract_first(),
            logo = company.xpath('.//div[@class="img-warp"]/a[@class= \
                    "company-logo"]/@style').re_first\
                    ("background-image: url\('(.+)'\)"),
            desc = company.xpath('.//p[@class="company-desc"]\
                                /text()').extract_first(),
            location = company.xpath('.//li[@class="text-muted "]\
                                /span/text()').extract_first(),
            field = middle[0] if middle else ''
        )
        results.append(result)
    with open('../datas/companies.json', 'w') as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    spider()
