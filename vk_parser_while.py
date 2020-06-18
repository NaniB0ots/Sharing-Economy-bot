import token_VK
import requests
import json
import time
#https://nanib0ots.pythonanywhere.com/bot/post

def vk_respons(domain,token,version,count = 1,offset = 1):
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

while (True):
    #stop = input()
    data = [
        {'title': 'Хелпфуд. Фудшеринг. Санкт-Петербург.', 'city': 'Санкт-Петербург', 'group_id': 'club_helpfoodspb'},
        {'title': 'Фудшеринг Отдам даром еду', 'city': ['Санкт-Петербург', 'Москва'], 'group_id': 'sharingfood'},
        {'title': 'Фудшеринг Отдам даром в Иркутске', 'city': 'Иркутск', 'group_id': 'sharingfood_irk'}
        ]
    def vk_pars_func(data, count = 1):
        token = token_VK.token
        version = token_VK.version
        for i in range(len(data)):
            print(i)
            domain = data[i]['group_id']
            vk_answer = vk_respons(domain,token,version)
            post_id = vk_answer
            send = {'link': 'https://vk.com/sharingfood?w=wall-'+domain+'_'+str(vk_answer['response']['items'][0]['id']),'category':'Da her prossish:(', 'city': data[i]['city']}
            bot_send = json.dumps(send)
            print(bot_send)
            requests.post('https://nanib0ots.pythonanywhere.com/bot/post', bot_send)
    vk_pars_func(data)
    time.sleep(0.5)



    #vk_pars_func(data)