import json






infojson = '2020-03-10 02:39:43\xa0\xa0最高全站日排行30'

print(infojson)

infojson1 = infojson[infojson.find('20'):infojson.find('最高')]

print(infojson1)