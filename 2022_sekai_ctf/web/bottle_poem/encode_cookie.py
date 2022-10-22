import bottle

secret = "Se3333KKKKKKAAAAIIIIILLLLovVVVVV3333YYYYoooouuu"
cookie = ('name', {'name': 'admin'})

exp = bottle.cookie_encode(cookie,secret)
print(exp)
