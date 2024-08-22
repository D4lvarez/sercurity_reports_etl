import re

from bs4 import BeautifulSoup, Tag

from utils import FileUtils


class TenableReportHTML:
    def __init__(self, path: str) -> None:
        self.path = path
        self.regex = r"[\n\t\s]+"
        self.base_url = "https://www.tenable.com/plugins/nessus/"

    def process_file(self) -> list[dict[str, str]]:
        content = FileUtils.read_file(self.path)

        html_document = BeautifulSoup(content, "lxml")

        tables = html_document.find_all("tr", {"class": "plugin-row"})

        severities = self._process_plugin_table(tables)
        return severities

    def _process_plugin_table(self, tables: list[Tag]) -> list[dict[str, str]]:
        content: list[dict[str, str]] = []

        # Remove last item
        tables.pop()

        for table in tables:
            columns = table.find_all("td")

            severity = self._clean_string(columns[1].get_text())
            cvss = self._clean_string(columns[3].get_text())
            vpr = self._clean_string(columns[5].get_text())
            plugin = self._clean_string(columns[7].get_text())
            name = self._clean_string(columns[8].get_text())
            url = f"{self.base_url}{plugin}"

            content.append(
                {
                    "severity": severity,
                    "cvss": cvss,
                    "vpr": vpr,
                    "plugin": plugin,
                    "name": name,
                    "url": url,
                }
            )

        return content

    def _clean_string(self, text: str) -> str:
        return re.sub(self.regex, " ", text).strip()
