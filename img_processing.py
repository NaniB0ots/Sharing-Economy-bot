import requests
import token_VK

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

def downlaod_img(img,path):
    p = requests.get(img)
    out = open(path, "wb")
    out.write(p.content)
    out.close()
# name = 'img1.jpg'
# path = '../imgs/'+name
# downlaod_img('https://sun4-15.userapi.com/rT2PGPaYQETVJClKWc65dX2_Zj87hx-xsKcE9w/26XbpiTEEqU.jpg',path)

def tests_preparing(groups):
    for i in range(len(groups)):
        domain = groups[i]
        token = token_VK.token4
        version = token_VK.version
        count = 100
        vk_answer = vk_respons(domain,token,version,count)
        for j in range(vk_answer['response']['items'].__len__()):
            post_id = vk_answer['response']['items'][j]['id']
            owner_id = vk_answer['response']['items'][j]['owner_id']
            if 'attachments' in vk_answer['response']['items'][j].keys():
                for n in range(vk_answer['response']['items'][i]['attachments'].__len__()):
                    try:
                        if 'photo' in vk_answer['response']['items'][j]['attachments'][n].keys():
                            path = '../test_imgs/'+str(owner_id)+'_'+str(post_id)+'('+str(n)+').jpg'
                            url = vk_answer['response']['items'][j]['attachments'][n]['photo']['sizes'][2]['url']
                            downlaod_img(url, path)
                    except:
                        pass
#groups = ['club_helpfoodspb','sharingfood','sharingfood_irk','foodsharing_minsk','food_sharing_spb']
#tests_preparing(groups)

