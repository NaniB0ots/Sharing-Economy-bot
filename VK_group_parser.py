import requests
version = '5.110'
domain = 'sharingfood'
city = 'Москва'
count = 20
def vk_pars(token,version,domain,city,count=10):
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
        if city in data['response']['items'][i]['text']:
            print('+')
            back.append(data['response']['items'][i])
    return back
back = vk_pars(token,version,domain,city)
print(back)
print(1)
