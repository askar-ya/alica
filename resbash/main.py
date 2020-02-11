import api
import json
from random import randint
from flask import Flask
from flask import request
app = Flask(__name__)

IMAGE_TOKEN = 'AgAAAAAkiWDYAAT7owzE7VLXTEEukUZVVqOY9No'


@app.route('/post', methods=['POST'])
def main():
    ## Создаем ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    ## Заполняем необходимую информацию
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res,req):
    if req['request']['type'] == 'ButtonPressed':
        if req['request']['payload']['text'] == 'Случайная новость':
            with open('out_pars.json') as f:
                pars_file = json.load(f)
            nams = randint(6,14)

            res['response'].update({'text':pars_file['news']['news-titel'][nams],'tts':pars_file['news']['news-titel'][nams]})
            image = {'card':{'button':{'text':'text','url':pars_file['news']['news-link'][nams]},
            'type':'BigImage',
            'image_id': pars_file['news']['news-imgId'][nams],
            'title': pars_file['news']['news-titel'][nams],
            'discription':pars_file['news']['news-titel'][nams]},}

            res['response'].update(image)
            
        elif req['request']['payload']['text'] == 'Последнии новости':
            with open('out_pars.json') as f:
                pars_file = json.load(f)
            last_news={'text':'Последнии новости',
                'card':{'type':'ItemsList','header':{'text':'Последнии новости'},'items':[]}
            }

            for i in range(5):
                k = {
                    'button':{'text':pars_file['news']['news-titel'][i],'url':pars_file['news']['news-link'][i]},
                    'title':pars_file['news']['news-titel'][i],
                    'tts':pars_file['news']['news-titel'][i],
                    'image_id':pars_file['news']['news-imgId'][i]}
                last_news['card']['items'].append(k)
            res['response'].update(last_news)

        elif req['request']['payload']['text'] == 'Смотреть номер':
            with open('out_pars.json') as f:
                pars_file = json.load(f)
            last_news={'text':'Последний номер',
                'card':{'type':'ItemsList','header':{'text':'Последний номер'},'items':[]}
            }
            if len(pars_file['stat']['stat-link'])>0:
                for i in range(5):
                    k = {
                        'button':{'text':pars_file['stat']['stat-titel'][i],'url':pars_file['stat']['stat-link'][i]},
                        'title':pars_file['stat']['stat-titel'][i],
                        'discription':pars_file['stat']['stat-lid'][i],
                        'tts': str(pars_file['stat']['stat-titel'][i])+'. '+str(pars_file['stat']['stat-lid'][i]),
                        'image_id':pars_file['stat']['stat-imgId'][i]}
                    last_news['card']['items'].append(k)
                res['response'].update(last_news)
            else:
                res['response']['text'] = 'Извините, номер ещё не готов😥'

    else:
        text = req['request']['original_utterance']
        if text == 'Случайная новость' or text == 'случайная новость' or text == 'Новость' or text == 'новость' or text == '🎲':

            with open('out_pars.json') as f:
                pars_file = json.load(f)
            nams = randint(6,14)

            res['response'].update({'text':pars_file['news']['news-titel'][nams],'tts':'text'})
            image = {'card':{'button':{'text':'text','url':pars_file['news']['news-link'][nams]},
            'type':'BigImage',
            'image_id': pars_file['news']['news-imgId'][nams],
            'title': pars_file['news']['news-titel'][nams],
            'discription':pars_file['news']['news-titel'][nams]},}

            res['response'].update(image)

        elif text == 'Последний номер' or text == 'номер' or text == 'Номер' or text == 'Покажи последний номер' or text == 'Раскажи последний номер' or text == 'Статьи' or text == 'статьи':
            with open('out_pars.json') as f:
                pars_file = json.load(f)
            last_news={'text':'Последний номер',
                'card':{'type':'ItemsList','header':{'text':'Последний номер'},'items':[]}
            }
            if len(pars_file['stat']['stat-link'])>0:
                for i in range(5):
                    k = {
                        'button':{'text':pars_file['news']['news-titel'][i],'url':pars_file['news']['news-link'][i]},
                        'title':pars_file['news']['news-titel'][i],
                        'tts':str(pars_file['stat']['stat-titel'][i])+'. '+str(pars_file['stat']['stat-lid'][i]),
                        'image_id':pars_file['news']['news-imgId'][i]}
                    last_news['card']['items'].append(k)
                res['response'].update(last_news)
            else:
                res['response']['text'] = 'Извините, номер ещё не готов😥'

        elif  text == 'Последнии новости' or text == 'последнии новости' or text == 'Новости' or text == 'новости'or text == 'Покажи последнии новости' or text == 'Раскажи последнии новости':
            with open('out_pars.json') as f:
                pars_file = json.load(f)
            last_news={'text':'Последнии новости',
                'card':{'type':'ItemsList','header':{'text':'Последнии новости'},'items':[]}
            }

            for i in range(5):
                k = {
                    'button':{'text':pars_file['news']['news-titel'][i],'url':pars_file['news']['news-link'][i]},
                    'title':pars_file['news']['news-titel'][i],
                    'tts':pars_file['news']['news-titel'][i],
                    'image_id':pars_file['news']['news-imgId'][i]}
                last_news['card']['items'].append(k)
            res['response'].update(last_news)

        elif text == '':
            ## Если это первое сообщение — представляемся
            hellp={'text':'Привет, я навык газетыРБ','card':{'type':'ItemsList','header':{'text':'Привет, я навык газетыРБ🔥🔥🔥','tts':'Привет, я навык газетыРБ'},
                'items':[
                    {'button':{'text':'Случайная новость','payload':{'text':'Случайная новость'}},
                        'title':'Случайная новость🎲',
                        'tts':'Случайная новость, показываает одну из последних новостей',
                    },
                    {'button':{'text':'Последнии новости','payload':{'text':'Последнии новости'}},
                        'title':'Последнии новости🕐',
                        'tts':'Последнии новости, покажет пять последних новостей',
                    },
                    {'button':{'text':'Смотреть номер','payload':{'text':'Смотреть номер'}},
                        'title':'Смотреть номер👀',
                        'tts':'Смотреть номер, зачитает загаловки самых интерсных статей из последнего номера',
                    },
                ]
            }}
            res['response'].update(hellp)
        else:
            ## Если не распознано
            hellp={'text':'Извините, я вас не понимаю','card':{'type':'ItemsList','header':{'text':'Извините, я вас не понимаю','tts':'Извините, я вас не понимаю'},
                'items':[
                    {'button':{'text':'Случайная новость','payload':{'text':'Случайная новость'}},
                        'title':'Случайная новость🎲',
                        'tts':'Случайная новость, показываает одну из последних новостей',
                    },
                    {'button':{'text':'Последнии новости','payload':{'text':'Последнии новости'}},
                        'title':'Последнии новости🕐',
                        'tts':'Последнии новости, покажет пять последних новостей',
                    },
                    {'button':{'text':'Смотреть номер','payload':{'text':'Смотреть номер'}},
                        'title':'Смотреть номер👀',
                        'tts':'Смотреть номер, зачитает загаловки самых интерсных статей из последнего номера',
                    },
                ]
            }}
            res['response'].update(hellp)

if __name__ == '__main__':
    app.run()