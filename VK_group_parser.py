import requests
version = '5.110'
domain = 'sharingfood'
city = {'Москва','Санкт-Петербург','Иркутск'}
count = 20
def vk_pars(token,version,domain,city,count=20):
    back = []
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': count
                            }
                            )
    data = response.json()
    print(data)
    for i in range(data['response']['items'].__len__()):
        temp_data = data['response']['items'][i]['text'].replace(',','').replace('.','').replace('!','').replace('?','').split()
        for j in temp_data:
            if j in city:
                print('+')
                back.append(data['response']['items'][i])
                break
    return back
back = vk_pars(token,version,domain,city)
print(back)
print(1)
