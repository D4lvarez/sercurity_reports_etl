from etl import TenasusReportHTML, TenasusReportJSON, TenableReportHTML

TENASUS_REPORT_HTML_PATH: str = (
    "C:\\Users\\dalvarez\\Desktop\\security_reports\\intelix.html"
)
TENASUS_REPORT_JSON_PATH: str = (
    "C:\\Users\\dalvarez\\Desktop\\security_reports\\intelix.json"
)

TENABLE_REPORT_HTML_PATH: str = (
    "C:\\Users\\dalvarez\\Desktop\\security_reports\\Valoracion_6noqof.html"
)


def process_tenasus_html():
    tenasus_html = TenasusReportHTML(TENASUS_REPORT_HTML_PATH)
    report = tenasus_html.process_file()
    print(report)


def process_tensasus_json():
    tenasus_json = TenasusReportJSON(TENASUS_REPORT_JSON_PATH)
    report = tenasus_json.process_file()
    print(report)


def process_tenable_html():
    tenable_html = TenableReportHTML(TENABLE_REPORT_HTML_PATH)
    report = tenable_html.process_file()
    print(report)


if __name__ == "__main__":
    process_tenasus_html()
    process_tensasus_json()
    process_tenable_html()
