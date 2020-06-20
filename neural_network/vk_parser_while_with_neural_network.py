# -*- coding: utf-8 -*-
"""vk_parser_while.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UkBDShocbdq--K2nR6_3agB0poBV3Bfv

#Гугл диск
"""

from google.colab import drive
drive.mount('/content/drive')

"""#Нейросеть"""

import os, shutil
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten 
from tensorflow.keras.applications import ResNet152V2
from keras.preprocessing.image import ImageDataGenerator, load_img

"""##Константы"""

FAST_RUN = False
IMAGE_WIDTH=128
IMAGE_HEIGHT=128
IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS=3
input_shape = (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)
# определим batch_size
batch_size=15

"""##Загружаем предварительно обученную нейронную сеть ResNet152V2
Создадим экземпляр модели ResNet152V2
"""

ResNet152V2_net = ResNet152V2(weights='imagenet', 
                  include_top=False, 
                  input_shape=input_shape)

ResNet152V2_net.trainable = False

"""## Классификатор"""

model = Sequential()
# добавляем в модель сеть ResNet152V2 в качестве слоя
model.add(ResNet152V2_net)
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(9, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer="rmsprop", metrics=['accuracy'])

#model.load_weights("/content/drive/My Drive/Sharing-Economy-neural-network/model-cnn-1.h5")
#model.load_weights("/content/drive/My Drive/Sharing-Economy-neural-network/model-cnn-S1.h5")
model.load_weights("/content/drive/My Drive/Sharing-Economy-neural-network/model-cnn-S2.h5")

"""#Классификация

##Распределение по категориям
"""

!mkdir imgs

def distribution_by_category():
    test_filenames = os.listdir("/content/imgs/")
    test_df_img = pd.DataFrame({
        'filename': test_filenames
    })
    nb_samples = test_df_img.shape[0]
    test_df_img.head() 



    test_gen = ImageDataGenerator(rescale=1./255)
    test_generator = test_gen.flow_from_dataframe(
        test_df_img, 
        "/content/imgs", 
        x_col='filename',
        y_col=None,
        class_mode=None,
        target_size=IMAGE_SIZE,
        batch_size=batch_size,
        shuffle=False
    )


    predict = model.predict(test_generator, steps=np.ceil(nb_samples/batch_size))

    cat = {0:'Алкоголь', 1:'Готовые блюда', 2:'Консервы', 3:'Крупы', 4:'Молочка', 5:'Мясо рыба', 6:'Орехи фрукты овощи', 7:'Соки воды', 8:'Хлеб'}
    predict_index = np.argmax(predict, axis=-1)
    for index in predict_index:
      print(cat[index])
    return predict_index

"""#vk_parser"""

import requests
import json
import time

version = '5.110'
token = '06f914db06f914db06f914db67068b6414006f906f914db58235e27d29376af1fa9f903'

"""###img_processing"""

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

"""###parser"""

# https://nanib0ots.pythonanywhere.com


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


def vk_pars_func(data):
    for i in range(len(data)):
        domain = data[i]['group_id']
        cities = list(set(data[i]['city']))

        vk_answer = vk_respons(domain, token, version)
        print(vk_answer)
        post_id = vk_answer['response']['items'][0]['id']
        owner_id = vk_answer['response']['items'][0]['owner_id']
        writer = write_json(post_id, owner_id)
        if writer:
            print('link:', 'https://vk.com/' + domain + '?w=wall' + str(owner_id) + '_' + str(post_id))
            item = vk_answer['response']['items'][0]

            text = item['text']
            # Определение города
            print(cities)
            if len(cities) == 1:
                city = [cities[0]]
            else:
                city = cities
                for item_city in cities:
                    if item_city in text:
                       city = [item_city]
                       break



            # Определение категории
            neural_network = False
            if 'attachments' in item.keys():
                attachments = item['attachments']
                n = 0 # индекс изображени
                for att in attachments:
                    neural_network = True
                    # Проверяем есть ли во вложениях фото
                    if att['type'] == 'photo':
                        path = './imgs/' + str(owner_id) + '_' + str(post_id) + '(' + str(n) + ').jpg'
                        url = att['photo']['sizes'][2]['url']
                        n += 1
                        downlaod_img(url, path) # загрузка изображений
            
            # Нейросеть 
            category = [] 
            folder = './imgs/'
            if neural_network:          
                category_dict = {0:'Готовые блюда', 1:'Консервы', 2:'Крупы, макаронные изделия, чай и приправы', 
                      3:'Молочная продукция', 4:'Мясное, рыба', 5:'Овощи, фрукты, орехи', 6:'Реклама', 
                      7:'Соки, напитки', 8:'Хлебобулочные и кондитерские изделия'} 
                try:              
                    predict_index = distribution_by_category()
                    if not 6 in predict_index:
                        for index in predict_index:
                            category.append(category_dict[index])
                except Exception as e: 
                    print(e) 

            # отчищаем папку с загрузками
            folder = './imgs/' 
            for the_file in os.listdir(folder): 
                file_path = os.path.join(folder, the_file) 
                try: 
                    if os.path.isfile(file_path): 
                        os.unlink(file_path) 
                    elif os.path.isdir(file_path): 
                        shutil.rmtree(file_path) 
                except Exception as e: 
                    print(e) 

                  

            #  Отправка поста боту
            send = {'link': 'https://vk.com/' + domain + '?w=wall' + str(owner_id) + '_' + str(post_id),
                    'category': category, 'city': city}
            bot_send = json.dumps(send)
            print(bot_send)
            requests.get('https://nanib0ots.pythonanywhere.com/bot/post', send, cookies={'parser_key': '12345678'})
            


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

#!rm ./imgs/*.jpg
!rm ./groups.json