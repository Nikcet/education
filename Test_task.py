from requests import get
from json import loads
from os import mkdir, chdir, getcwd, listdir, rename
from datetime import datetime as dt
from copy import deepcopy
from os.path import getctime

response = get("https://jsonplaceholder.typicode.com/todos")
todos = loads(response.text)
response = get("https://jsonplaceholder.typicode.com/users")
users = loads(response.text)

os_path = '/tasks'
list_of_tasks = list()
list_of_false_tasks = list()

# Создание директории 'tasks'
if os_path != getcwd():
    try:
        mkdir('tasks')
        chdir('tasks')
    except FileExistsError:
        chdir('tasks')


# Вытягивает из json'а список завершенных задач.
def task_completed(task, userId):
    if task['completed'] and task['userId'] == userId['id']:
        list_of_tasks.append(check_len(task['title']))
    return list_of_tasks


# Вытягивает из  json'а список НЕ завершенных задач.
def no_task_completed(task, userId):
    if not task['completed'] and task['userId'] == userId['id']:
        list_of_false_tasks.append(check_len(task['title']))
    return list_of_false_tasks


# Проверяет длину названия задач и если он слишком длинный, обрезает.
def check_len(index):
    num_symbs = 48
    if len(index) >= num_symbs:
        title = f"{index[:num_symbs]}..."
    else:
        title = index
    return str(title)


# Формирует список завершенных задач отдельно для каждого человека.
def list_of_completed_tasks(todo_userId, user):
    task_completed(todo_userId, user)
    if list_of_tasks:
        completed_answer = deepcopy(list_of_tasks)
        list_of_tasks.clear()
        return completed_answer


# Формирует список НЕ завершенных задач отдельно для каждого человека.
def list_of_not_completed_tasks(todo_userId, user):
    no_task_completed(todo_userId, user)
    if list_of_false_tasks:
        no_completed_answer = deepcopy(list_of_false_tasks)
        list_of_false_tasks.clear()
        return no_completed_answer


# Чистит список от лишних элементов типа None.
def clear_list(amazing_list):
    copy_list = list()
    for i in amazing_list:
        if i is not None:
            copy_list.append(i[0])
    return copy_list


# Чистит список от лишних знаков препинания
def beauty_output(arg_list):
    return '\n'.join(arg_list)

# "Если файл для пользователя уже существует,
# то существующий файл переименовать, добавив в него время составления
# этого старого отчёта в формате "old_Antonette_2020-09-23T15:25.txt""
if len(listdir()) > 0:
    for file in listdir():
        if 'old_' not in file:
            # В условии задания указано, что время в файле должно быть указано
            # в формате HH:MM, но Windows не допускает содержания знака ":"
            # в названии файлов или папок.
            date = dt.fromtimestamp(getctime(file)).strftime('%Y-%m-%dT%H_%M')
            new_name = f"old_{file[:-4]}_{date}.txt"
            try:
                rename(file, new_name)
                # В условии задания не обговорено,
                # но я добавлял возможность многократного обновления отчетов.
                # Но, по какой-то причине, отчеты обновляются только 1 раз
                # из-за FileExistsError.
                # При этом я проверил, что при попытке переименовать файл
                # старое и новое названия отличаются.
                # Официальная документация функции rename и форумы не ответили
                # на мой вопрос по данной проблеме.
            except FileExistsError:
                print(file, '- Старый вариант этого файла уже существует.')

for user in users:
    with open(f"{user['username']}.txt", "w", encoding="utf8") as data_file:
        date = dt.now()  # Дата
        # Формирование текущей даты
        now_date = (
            f"{date.day}.{date.month}.{date.year} {date.hour}:{date.minute}"
        )

        # Вывод названия компании
        data_file.writelines([f"Отчет для {user['company']['name']}. \n"])

        # Вывод имени, электронной почты и времени составления отчета
        data_file.writelines(
            [user['name'], f" <{user['email']}> {now_date} \n"]
        )
        data_file.writelines('\n')

        # Формирование списка завершенных задач
        completed_tasks = clear_list(
            [list_of_completed_tasks(todo_userId, user)
             for todo_userId in todos]
        )

        # Формирование списка НЕ завершенных задач
        not_completed_tasks = clear_list(
            [list_of_not_completed_tasks(todo_userId, user)
             for todo_userId in todos]
        )

        ct = completed_tasks  # В угоду PEP8 :)
        n_ct = not_completed_tasks  # В угоду PEP8 :)

        # Вывод общего кол-ва задач
        data_file.writelines(
            [f'Всего задач: {len(ct) + len(n_ct)}']
        )
        data_file.writelines('\n' * 2)

        # Вывод списка завершенных задач
        data_file.writelines(
            [f"Завершенные задачи ({len(ct)}): \n{beauty_output(ct)}"]
        )
        data_file.writelines('\n' * 2)

        # Вывод списка оставшихся задач
        data_file.writelines(
            [f"Оставшиеся задачи ({len(n_ct)}): \n{beauty_output(n_ct)}"]
        )
