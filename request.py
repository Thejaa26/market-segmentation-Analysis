import requests

url = 'http://localhost:5000/predict-api'
r = requests.post(url,json={'yummy':'Yes','convenient':'Yes','spicy':'No'
                            'fattening':'No','greasy':'No','fast':'Yes',
                            'cheap':'Yes','tasty':'Yes','expensive'='No,
                            'healthy':'Yes','disgusting':'No','Age':30,
                            'Like':'3','VisitFrequency':'Once a week',
                            'Gender':'Female'})

print(r.json())