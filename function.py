import os
from io import StringIO
from tableauscraper import TableauScraper as TS
from s3 import write_to as write_to_s3


URL = "https://results.mo.gov/t/COVID19/views/VaccinationsDashboard/Vaccinations"


def get_worksheets():
    ts = TS()
    ts.loads(URL)
    dashboard = ts.getDashboard()

    return dashboard.worksheets


def format_worksheet_name(name):
    return name \
        .replace("%", "pct") \
        .replace(" - ", "-") \
        .replace(" ", "-") \
        .lower() \


def download_worksheet_csv(worksheet):
    formatted_name = format_worksheet_name(worksheet.name)
    file_path = f"{DATA_STORAGE_PATH}/{formatted_name}.csv"

    return worksheet.data.to_csv(file_path)


def write_worksheet_to_csv_on_s3(worksheet):
    key = f'{format_worksheet_name(worksheet.name)}.csv'

    csv_buffer = StringIO()
    worksheet.data.to_csv(csv_buffer, index=False)

    return write_to_s3(key, csv_buffer.getvalue(), "text/csv")


def main():
    for ws in get_worksheets():
        write_worksheet_to_csv_on_s3(ws)


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()
