import requests
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

print("\nEnter a Kilonova profile and the number of the page to scrap submissions from\n")
user_input = input()
profile = user_input.split()[0]
page = user_input.split()[1]

url = f"https://kilonova.ro/profile/{profile}/submissions?page={page}"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.content, 'html.parser')

# local for first page
# html = open(f'Past submissions_Problem {profile}.html', encoding="utf-8").read()
# soup = BeautifulSoup(html, 'html.parser')

kn_table_rows = soup.find_all('tr', class_='kn-table-row')

submissions = []

for kn_table_row in kn_table_rows:
    submission = {}

    id_element = kn_table_row.find('th', class_='text-center')
    id = id_element.text
    submission['id'] = id

    author_element = id_element.find_next_sibling()
    author = author_element.text
    submission['author'] = author

    upload_date_element = author_element.find_next_sibling()
    raw_timestamp = upload_date_element.find('server-timestamp').get('timestamp')
    ro_tz = ZoneInfo("Europe/Bucharest")
    date = datetime.fromtimestamp(int(raw_timestamp) / 1000, tz=ro_tz)
    formatted_date = date.strftime("%d/%m/%Y %H:%M")
    submission['upload_date'] = formatted_date

    problem_element = upload_date_element.find_next_sibling()
    problem = problem_element.text
    submission['problem'] = problem

    time_element = problem_element.find_next_sibling()
    time = time_element.text
    submission['time'] = time

    memory_element = time_element.find_next_sibling()
    memory = memory_element.text
    submission['memory'] = memory

    status_element = memory_element.find_next_sibling()
    status = status_element.text
    submission['status'] = status

    submissions.append(submission)

space_manager = {
    'index': 2,
    'id': 7,
    'author': 10,
    'upload_date': 16,
    'problem': 10,
    'time': 7,
    'memory': 10,
    'status': 19,
    'space': 5
}


def get_space(key, val):
    val = str(val)
    return space_manager['space'] + space_manager[key] - len(val)


def print_helper(key, val, restriction):
    val = str(val)
    if restriction == 1:
        val = val[:space_manager[key]]
    else:
        val = val.capitalize()
    if key == 'index':
        if val != 'Index':
            print(val, ".", get_space(key, val) * " ", end="", sep="")
        else:
            print(val, (get_space(key, val) + 1) * " ", end="", sep="")
    else:
        print(val, get_space(key, val) * " ", end="", sep="")


print(f"\nScraped the {page}th page of submissions and found {len(submissions)} submissions:\n")

if len(submissions):
    for key in space_manager:
        if key != 'space':
            print_helper(key, key, 0)
    print()

for index, submission in enumerate(submissions):
    print_helper('index', index + 1, 1)
    for key, val in submission.items():
        print_helper(key, val, 1)
    print()