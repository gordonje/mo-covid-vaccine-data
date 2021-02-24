import os
from io import StringIO
from tableauscraper import TableauScraper as TS
from s3 import write_to as write_to_s3
from s3 import read_all_files, read_object_versions
from jinja2 import Template, Environment, FileSystemLoader
import datetime
from pytz import *


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


def write_html_to_s3(filename, html_string):
    with open(f'templates/{filename}.html', 'w', encoding='utf-8') as f:
        f.write(html_string)
    with open(f'templates/{filename}.html', 'r', encoding='utf-8') as f:
        return write_to_s3(f'{filename}.html', f.read(), 'text/html')


def build_page():
    worksheets = []
    
    offset = datetime.timedelta(hours = 6)

    for file in read_all_files():
        if file['Key'].endswith('.csv'):
            file['Key'] = file['Key'].split('.')[0]

            file['LastModified'] = (file['LastModified'] - offset).strftime("%Y-%m-%d %H:%M:%S")

            worksheets.append(file)

    env = Environment(loader=FileSystemLoader('templates'))
    
    main_template = env.get_template('template.html')
    html_string = main_template.render(worksheets = worksheets)

    write_html_to_s3('index', html_string)

    version_template = env.get_template('version.html')
    for sheet in worksheets:
        versions = read_object_versions(sheet['Key'])['Versions']

        for version in versions:
            version['LastModified'] = (version['LastModified'] - offset).strftime("%Y-%m-%d %H:%M:%S")

        versions_html_string = version_template.render(versions = versions)

        write_html_to_s3(sheet['Key'], versions_html_string)


def main():
    for ws in get_worksheets():
        write_worksheet_to_csv_on_s3(ws)

    build_page()


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()
