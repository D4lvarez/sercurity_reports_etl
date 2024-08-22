import re

from bs4 import BeautifulSoup, Tag

from utils import FileUtils


class TenasusReportHTML:
    def __init__(self, path: str) -> None:
        self.path = path
        self.regex = r"[\n\t\s]+"

    def process_file(self) -> dict[str, dict]:
        content = FileUtils.read_file(self.path)

        html_document = BeautifulSoup(content, "lxml")

        # Summary
        summary_table = html_document.find("table", {"class": "summary"})
        summary = self._process_summary_table(summary_table)

        # Alerts Table
        alerts_table = html_document.find("table", {"class": "alerts"})
        alerts = self._process_alerts_table(alerts_table)

        # Vulnerabilities Details
        details_tables = html_document.find_all("table", {"class": "results"})
        vulnerabilities_details = self._process_details_tables(details_tables)

        return {
            "summary": summary,
            "alerts": alerts,
            "alert_detail": vulnerabilities_details,
        }

    def _process_summary_table(self, table: Tag) -> dict[str, int]:
        risk_levels: list[Tag] = table.find_all("a")
        number_of_alerts: list[Tag] = table.find_all("td", {"align": "center"})

        content: dict[str, int] = {}

        for risk in risk_levels:
            risk_level: str = self._clean_string(risk.get_text())
            alert_instances: str | None = None

            for counter in number_of_alerts:
                alert_instances: str = self._clean_string(counter.get_text())

            content[risk_level] = int(alert_instances)

        return content

    def _process_alerts_table(self, table: Tag) -> dict[str, dict[str, int]]:
        rows: list[Tag] = table.find_all("tr", {"bgcolor": "#e8e8e8"})

        content: dict[str, dict[str, int]] = {}

        for row in rows:
            columns = row.find_all("td")

            vulnerability_name = self._clean_string(columns[0].text)
            level = self._clean_string(columns[1].text)
            instances = self._clean_string(columns[2].text)

            content[vulnerability_name] = {"level": level, "instances": int(instances)}

        return content

    def _process_details_tables(self, tables: list[Tag]) -> list[dict[str, str | int]]:
        content: list[dict[str, str | int]] = []

        for detail_table in tables:
            value = {}
            location = {"url": [], "method": [], "evidence": [], "parameter": []}

            table_headers: list[Tag] = detail_table.find_all("th")
            table_cells_titles = detail_table.find_all("td", {"width": "20%"})
            table_cells_values = detail_table.find_all("td", {"width": "80%"})

            vulnerability_name = table_headers[1].get_text()
            value["vulnerability_name"] = self._clean_string(vulnerability_name)
            value["locations"] = []

            for i in range(len(table_cells_titles)):
                title = table_cells_titles[i].get_text()
                detail = table_cells_values[i].get_text()

                # Format string
                title = self._clean_string(title)
                detail = self._clean_string(detail)

                # Validations for locations object
                if title.lower() == "url":
                    location["url"].append(detail)

                if title.lower() == "method":
                    location["method"].append(detail)

                if title.lower() == "evidence":
                    location["evidence"].append(detail)

                if title.lower() == "parameter":
                    location["parameter"].append(detail)

                value["locations"].append(location)
                value[title] = detail

            locations = []

            last_item_location = value["locations"].pop(-1)

            urls = last_item_location["url"]
            methods = last_item_location["method"]
            evidences = last_item_location["evidence"]
            parameter = last_item_location["parameter"]

            for i in range(len(urls)):
                location_formatted = {
                    "url": urls[i],
                    "methods": methods[i],
                    "evidences": evidences[i] if i < len(evidences) else None,
                    "parameter": parameter[i] if i < len(parameter) else None,
                }
                locations.append(location_formatted)

            value["locations"] = locations
            content.append(value)

        return content

    def _clean_string(self, text: str) -> str:
        return re.sub(self.regex, " ", text).strip()


class TenasusReportJSON:
    def __init__(self, path: str) -> None:
        self.path = path
        self.regex = r"[\n\t\s]+"

    def process_file(self):
        print()
