import os
from tableauscraper import TableauScraper as TS


URL = "https://results.mo.gov/t/COVID19/views/VaccinationsDashboard/Vaccinations"
DATA_STORAGE_PATH = 'data'


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


def main():

    if not os.path.isdir(DATA_STORAGE_PATH):
        os.mkdir(DATA_STORAGE_PATH)

    for ws in get_worksheets():
        download_worksheet_csv(ws)


if __name__ == "__main__":
    main()
