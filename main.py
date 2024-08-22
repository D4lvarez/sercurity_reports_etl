from etl import TenasusReportHTML

TENASUS_REPORT_HTML_PATH: str = (
    "C:\\Users\\dalvarez\\Desktop\\security_reports\\intelix.html"
)
TENASUS_REPORT_JSON_PATH: str = (
    "C:\\Users\\dalvarez\\Desktop\\security_reports\\intelix.json"
)

if __name__ == "__main__":
    tenasus_html = TenasusReportHTML(TENASUS_REPORT_HTML_PATH)
    report = tenasus_html.process_file()
    print(report)
