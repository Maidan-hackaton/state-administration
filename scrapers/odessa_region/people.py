#encoding=utf-8
from pupa.scrape import Scraper
from pupa.scrape.helpers import Organization
from pupa.scrape.popolo import Person
import logging
import lxml.html


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MEMBERLIST = 'http://oblrada.odessa.gov.ua/index.php?option=com_content&view=article&id=1054&Itemid=266&lang=uk'


def parse_date(date_string):
    day, month, year, _ = date_string.split(' ')
    month_number = {'січня': 1, 'лютого': 2, 'березня': 3, 'квітня': 4, 'травня': 5, 'червня': 6, 'липня': 7, 'серпня': 8, 'вересня': 9, 'жовтня': 10, 'листопада': 11, 'грудня': 12}.get(month)
    year = int(year)
    day = int(day)
    return '%04d-%02d-%02d' % (year, month_number, day)


class OdessaOblRadaPersonScraper(Scraper):

    def lxmlize(self, url):
        entry = self.urlopen(url)
        page = lxml.html.fromstring(entry)
        page.make_links_absolute(url)
        return page

    def scrape_person_details(self, url, name, post):
        page = self.lxmlize(url)
        article = page.xpath("//div[@class='art-article']")[0]
        birthdate = ''
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
                birthdate_string = 'Дата народження: '
                if text.startswith(birthdate_string):
                    birthdate = parse_date(text.replace(birthdate_string, ''))
                logger.info(text)
        else:
            img_url = ''
        p = Person(name=name, image=img_url, birth_date=birthdate)
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
                a_link = name.xpath("./p/span/span/span/a")[0]
                url = a_link.attrib["href"]
            else:
                a_link = name.xpath("./p/span/a")[0]
                url = a_link.attrib["href"]
            name3 = name.xpath("./p/span")[0].text_content()
            post = post.xpath("./p/span/span/a")
            if post:
                post = post[0].text_content()
            else:
                post = ''

            yield self.scrape_person_details(url, name3, post)
