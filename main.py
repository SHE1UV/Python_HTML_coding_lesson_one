import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import argparse  
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--data-file', default='wine3.xlsx', help='Путь к файлу с данными')
args = parser.parse_args()

def calculate_company_age():
    delta_new = company_year % 100
    if 21 > delta_new > 4:
        return "лет"
    delta_new = company_year % 10
    if delta_new == 1:
        return "год"
    elif 1 < delta_new < 5:
        return "года"
    return "лет"


if __name__ == '__main__':
    foundation_year = 1920
    now_year = datetime.datetime.now().year
    company_year = now_year-foundation_year
    
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    excel_data_df = pandas.read_excel(args.data_file, na_values=' ', keep_default_na=False)  # Используйте аргумент командной строки
    wines = excel_data_df.to_dict(orient='records')
    sorted_wines = collections.defaultdict(list) 
    
    for wine in wines:
        sorted_wines[wine['Категория']].append(wine)

    rendered_page = template.render(
        age=company_year,
        years=years(),
        wines=sorted_wines
        
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
