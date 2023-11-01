# -*- coding: utf-8 -*-
import scrapy
import datetime
import os

class ResolucoesSpider(scrapy.Spider):
    name = 'resolucoes'
    allowed_domains = ['ifce.edu.br']
    start_urls = [
        'https://ifce.edu.br/instituto/documentos-institucionais/resolucoes/']

    def parse(self, response):
        now = datetime.datetime.now()
        for resolucao_ano in range(2010, now.year):
            self.logger.info(f'Resoluções de {str(resolucao_ano)}')

            url = 'https://ifce.edu.br/instituto/documentos-institucionais/resolucoes/' + \
                    str(resolucao_ano)

            yield scrapy.Request(
                url=url,
                callback=self.parse_ano,
                meta={'resolucao_ano': resolucao_ano}
            )

    def parse_ano(self, response):
        links = response.xpath(
            '//div[@id="content"]//article//a/@href').getall()
        self.logger.info(str(links))
        for link in links:
            self.logger.info(f'Doc {str(link)}')
            yield scrapy.Request(
                url=response.urljoin(link.replace('/view', '')),
                callback=self.save_pdf,
                meta={'resolucao_ano': response.meta['resolucao_ano']}
            )

    def save_pdf(self, response):
        ano = str(response.meta['resolucao_ano'])
        if not os.path.exists(ano):
            os.makedirs(ano)

        path = str(response.meta['resolucao_ano']) + '/' + response.url.split('/')[-1]
        if not path.endswith('.pdf'):
            path = f'{path}.pdf'
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
