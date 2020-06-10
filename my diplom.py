import requests
import time
import json
from tqdm import tqdm

user = 171691064
TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


def get_friends(user_id):
    print('Получаем список друзей пользователя: ', user)

    friends_params = {
        'user_id': user_id,
        'order': 'name',
        'access_token': TOKEN,
        'v': '5.89'
    }

    friends_json = requests.get('https://api.vk.com/method/friends.get', friends_params)
    friends_dict = friends_json.json()['response']
    return set(friends_dict['items'])



def get_groups(user_id):
    print('Получаем список групп пользователя: ', user)

    group_params = {
        'user_id': user_id,
        'count': '1000',
        'access_token': TOKEN,
        'v': '5.89'
    }
    group_json = requests.get('https://api.vk.com/method/groups.get', group_params)
    group_dict = group_json.json()['response']
    return set(group_dict['items'])


def get_friends_groups(friends_set, group_set):
    print('Ищем совпадения')

    for friend in tqdm(friends_set):  # добавлен прогресс бар, выводит проценты построчно
        time.sleep(1)
        print('Проверяем https://vk.com/id{}'.format(friend))
        friend_params = {
            'user_id': friend,
            'count': '1000',
            'access_token': TOKEN,
            'v': '5.89'
        }

        group_json = requests.get('https://api.vk.com/method/groups.get?', friend_params)
        try:
            group_dict = group_json.json()['response']
            group_users = set(group_dict['items'])
            group_set = group_set - group_users
        except KeyError:
            error = group_json.json()['error']
            print('Ошибка № {0} {1}'.format(error['error_code'], error['error_msg']))

    return group_set


def json_group(group_user_set):
    print('Формируем json-файл')

    group_list = []

    for group in group_user_set:

        time.sleep(1)
        params = {
            'group_id': group,
            'fields': 'members_count',
            'access_token': TOKEN,
            'v': '5.89'
        }

        group_json = requests.get('https://api.vk.com/method/groups.getById', params)
        group_dict = group_json.json()['response']

        print('Собираем информацию о группе', group_dict[0]['name'])

        group_list.append({
            'name': group_dict[0]['name'],
            'gid': group_dict[0]['id'],
            'members_count': group_dict[0]['members_count']
        })

    with open('groups.json', 'w', encoding='utf8') as f:
        json.dump(group_list, f, ensure_ascii=False, indent=2)

    print('Файл groups.json сформирован и заполнен')

#
# print(get_friends('171691064'))
# print(get_groups('171691064'))


def search_groups(user_id):
    friends_set = get_friends(user_id)
    print('Колличество друзей получено')
    print(len(friends_set), 'человек')
    group_set = get_groups(user_id)
    print('Колличество групп получено')
    print(len(group_set), 'групп')
    group_user_set = get_friends_groups(friends_set, group_set)
    print(group_user_set)
    print('Результат получен:')
    print(len(group_user_set), 'групп')
    json_group(group_user_set)
    print('Выполнение программы завершено')

search_groups(user)
