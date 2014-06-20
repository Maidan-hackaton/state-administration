# encoding=utf-8
from pupa.scrape import Jurisdiction

from .people import OdessaOblRadaPersonScraper


class OdessaOblRada(Jurisdiction):
    classification = 'rada'
    division_id = 'ocd-division/country:ua/region:od/'
    name = 'Одеська обласна рада'
    url = 'http://oblrada.odessa.gov.ua/'
    scrapers = {
        "people": OdessaOblRadaPersonScraper
    }
    terms = [{
        'name': 'VI скликання',
        'sessions': ['VI-32'],
        'start_year': 2010,
        'end_year': 2014
    },{
        'name': 'V скликання',
        'sessions': ['V-12'],
        'start_year': 2006,
        'end_year': 2010
    }]
    parties = [
        {'name': 'Партія регіонов' },
        {'name': 'Народна партія' },
        {'name': 'Фронт змін' },
        {'name': 'Соціалістична партія України' },
        {'name': 'Комуністична партія України' },
        {'name': 'РОДИНА' },
        {'name': 'Батьківщина'}
    ]
    session_details = {
        'V-12': {'_scraped_name': 'V-12'},
        'VI-32': {'_scraped_name': 'VI-32'}
    }

