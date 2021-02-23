import requests
from flask import Flask, render_template, redirect, request


#url -> new https://hn.algolia.com/api/v1/search_by_date?tags=story
#url -> popular https://hn.algolia.com/api/v1/search?tags=story
#url -> id http://hn.algolia.com/api/v1/items/{id}

#rotas
#"/" -> popular
# /?order_by=popular -> popular
# /?order_by=new -> new
# se não for passado nada redireciona para o "/"

app = Flask("Hacker_News")

@app.route('/')
def start():
  order_by = request.args.get('order_by')
  if order_by == 'new':
    new_info = new_news()
    return render_template('index.html', datas=new_info)
  else:
    new_info = popular_news()
    return render_template('index.html',order='popular',datas=new_info)


@app.route('/id')
def publication():
  id_by = request.args.get('id')
  id_info, comentarios = id_new(id_by)
  return render_template('id.html',header=id_info, comments=comentarios)




def new_news():
  new_json = requests.get("https://hn.algolia.com/api/v1/search_by_date?tags=story").json()
  news = []
  for new in new_json['hits']:
    info = {
      'titulo': new['title'],
      'Link_Acess': new['url'],
      'Autor': new['author'],
      'Pontos': new['points'],
      'Num_Coments': new['num_comments'],
      'Code_Id': new['objectID']
      }
    news.append(info)
  return news



def popular_news():
    new_json = requests.get("https://hn.algolia.com/api/v1/search?tags=story").json()
    news = []
    for new in new_json['hits']:
        info = {
            'titulo': new['title'],
            'Link_Acess': new['url'],
            'Autor': new['author'],
            'Pontos': new['points'],
            'Num_Coments': new['num_comments'],
            'Code_Id': new['objectID']
        }
        news.append(info)
    return news
    
def id_new(id):
  new_json = requests.get(f"http://hn.algolia.com/api/v1/items/{id}").json()
  info_header = {
    'titulo': new_json['title'],
    'autor' : new_json['author'],
    'link': new_json['url'],
    'pontos': new_json['points']
  }
  comments = []
  for comment in new_json['children']:
    if comment['author'] == None:
      continue
    else:
      info_comments = {
        'autor' : comment['author'],
        'texto' : comment['text']
      }
      comments.append(info_comments)
  return info_header, comments



app.run(host='0.0.0.0')