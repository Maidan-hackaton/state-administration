#encoding=utf-8
from pupa.scrape import Scraper
from pupa.scrape.helpers import Legislator, Organization
import logging
import lxml.html


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MEMBERLIST = 'http://oblrada.odessa.gov.ua/index.php?option=com_content&view=article&id=1054&Itemid=266&lang=uk'


class OdessaOblRadaPersonScraper(Scraper):

    def lxmlize(self, url):
        entry = self.urlopen(url)
        page = lxml.html.fromstring(entry)
        page.make_links_absolute(url)
        return page

    def scrape_person_details(self, url, name, post):
        page = self.lxmlize(url)
        article = page.xpath("//div[@class='art-article']")[0]
        if not article.text_content().strip() == u'Інформіція відсутня' and not article.text_content().strip() == name:
            items = article.xpath("./p/span")
            img = article.xpath("./p//img")
            if img:
                img_url = img[0].attrib['src']
            else:
                img_url = ''
            logger.info(img_url)
            for item in items:
                if not item.text_content().strip():
                    continue
                text = item.text_content()
                logger.info(text)
        else:
            img_url = ''
        p = Legislator(name=name, district=None, image=img_url)
        p.add_source(MEMBERLIST)
        p.add_source(url)
        return p


    def scrape(self):
        page = self.lxmlize(MEMBERLIST)
        article = page.xpath("//div[@class='art-article']")[0]
        cells = article.xpath("./table//tr")
        for cell in cells:
            _, name, post = cell.xpath("./td")
            name1 = name.xpath("./p/span/a/span/span")
            if not name1:
                continue
            name2 = name1[0].text_content()
            if not name2:
                name1 = name.xpath("./p/span/span/span/a")
                name2 = name1[0].text_content()
                url = name.xpath("./p/span/span/span/a")[0].attrib["href"]
            else:
                url = name.xpath("./p/span/a")[0].attrib["href"]
            post = post.xpath("./p/span/span/a")
            if post:
                post = post[0].text_content()
            else:
                post = ''

            yield self.scrape_person_details(url, name2, post)
