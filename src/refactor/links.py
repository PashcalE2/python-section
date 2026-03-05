from dataclasses import dataclass
import datetime
from datetime import date

from bs4 import BeautifulSoup, ResultSet, Tag


@dataclass
class DatedUrl:
    date: date
    url: str


class LinksParser:
    __results: list[DatedUrl]
    # TODO: Возможно стоит перенести параметры в конструктор
    __target_links_class = "accordeon-inner__item-title link xls"
    __target_href_prefix = "/upload/reports/oil_xls/oil_xls_"
    __href_https_domen = "https://spimex.com"

    def __init__(self, html: str, verbose=True) -> None:
        self.__html = html
        self.__verbose = verbose

        self.__build()

    def __build(self):
        self.__results = []
        self.__soup = BeautifulSoup(self.__html, "html.parser")
        self.__links: ResultSet[Tag] = self.__soup.find_all(
            "a", class_=self.__target_links_class)

    def __print(self, *args, **kwargs):
        # TODO: Добавить префикс
        # TODO: Использовать лог
        if self.__verbose:
            print(*args, **kwargs)

    def __is_good_href(self, href: str):
        return self.__target_href_prefix in href and href.endswith(".xls")

    def __add_one_result(self, href: str, start_date: date, end_date: date):
        # TODO: Слишком много ответственности
        try:
            href_date = href.split(self.__target_href_prefix)[1][:8]
            file_date = datetime.datetime.strptime(href_date, "%Y%m%d").date()
        except Exception as e:
            # TODO: Слишком общий класс
            raise Exception(f"Не удалось извлечь дату из ссылки `{href}`: {e}")

        if not start_date <= file_date <= end_date:
            # TODO: Слишком общий класс
            raise Exception(f"Ссылка `{href}` вне диапазона дат")

        url = href if href.startswith(
            "http") else f"{self.__href_https_domen}{href}"
        self.__results.append(DatedUrl(url=url, date=file_date))

    def __parse_one_link(self, link: Tag, start_date: date, end_date: date):
        href_attribute = link.get("href")
        if not href_attribute:
            # TODO: Exception под этот случай
            return

        href = str(href_attribute).split("?", maxsplit=1)[0]
        if not self.__is_good_href(href):
            # TODO: Exception под этот случай
            return

        self.__add_one_result(href, start_date, end_date)

    def parse_links(self, start_date: date, end_date: date) -> list[DatedUrl]:
        # TODO: Возможно стоит перенести start_date и end_date в конструктор
        """
        Парсит ссылки на бюллетени с одной страницы:
        <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
        """
        for link in self.__links:
            try:
                self.__parse_one_link(link, start_date, end_date)
            except Exception as e:
                self.__print(e)

        return self.__results


data = """<a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>"""
parser = LinksParser(data)

print(parser.parse_links(date(2023, 2, 1), date(2025, 1, 1)))

print(parser.parse_links(date(2024, 2, 1), date(2025, 1, 1)))

data = """<a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_202401.xls">link1</a>"""
parser = LinksParser(data)

print(parser.parse_links(date(2023, 2, 1), date(2025, 1, 1)))
