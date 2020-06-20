import token_VK
import requests
import json
import time
import img_processing


# https://nanib0ots.pythonanywhere.com/bot/post
# vk_answer['response']['items'][0]['date']
# vk_answer['response']['items'][0]['owner_id']
# https://nanib0ots.pythonanywhere.com/bot/post

def write_json(post_id, owner_id):
    post_id = str(post_id)
    owner_id = str(owner_id)
    flag = False
    try:
        json_d = json.load(open('groups.json'))
    except:
        json_d = {}
    if owner_id in json_d.keys():
        if json_d[owner_id] != post_id:
            flag = True
            json_d[owner_id] = post_id
            with open('groups.json', 'w') as file:
                json.dump(json_d, file, indent=2, ensure_ascii=False)
    else:
        json_d[owner_id] = post_id
        flag = True
        with open('groups.json', 'w') as file:
            json.dump(json_d, file, indent=2, ensure_ascii=False)
    return flag


def vk_respons(domain, token, version, count=1, offset=1):
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': count,
                                'offset': offset
                            }
                            )
    vk_answer = response.json()
    return vk_answer


def vk_pars_func(data, count=1):
    token = token_VK.token2


def vk_pars_func(data):
    token = token_VK.token4
    version = token_VK.version
    for i in range(len(data)):
        domain = data[i]['group_id']
        vk_answer = vk_respons(domain, token, version)
        post_id = vk_answer['response']['items'][0]['id']
        owner_id = vk_answer['response']['items'][0]['owner_id']
        writer = write_json(post_id, owner_id)
        if writer:
            send = {'link': 'https://vk.com/' + domain + '?w=wall' + str(owner_id) + '_' + str(post_id),
                    'category': 'Da her prossish:(', 'city': data[i]['city']}
            bot_send = json.dumps(send)
            print(bot_send)
            requests.get('https://nanib0ots.pythonanywhere.com/bot/post', send, cookies={'parser_key': '12345678'})
            for n in range(vk_answer['response']['items'][0]['attachments'].__len__()):
                path = './imgs/' + str(owner_id) + '_' + str(post_id) + '(' + str(n) + ').jpg'
                url = vk_answer['response']['items'][0]['attachments'][0]['photo']['sizes'][2]['url']
                img_processing.downlaod_img(url, path)


def main():
    while (True):
        try:
            response = requests.get('https://nanib0ots.pythonanywhere.com/bot/get_data', cookies={'parser_key': '12345678'})
            if response.status_code != 200:
                print(response)
                time.sleep(5)
                main()
            data = json.loads(response.content)
            print('from db: ', data)
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            time.sleep(40)
            main()
        vk_pars_func(data)
        time.sleep(40)


if __name__ == '__main__':
    main()
