import bottle

secret = "Se3333KKKKKKAAAAIIIIILLLLovVVVVV3333YYYYoooouuu"
cookie = "!kElk5i80OuQFnxLryWYmoQ==?gAWVUQAAAAAAAACMB3Nlc3Npb26UfZSMBG5hbWWUXZSMCGJ1aWx0aW5zlIwEZXZhbJSTlIwcX19pbXBvcnRfXygib3MiKS5wb3BlbigibHMiKZSFlFKUYXOGlC4="
#cookie = "!o8siMrdaVf83giE8crJurg==?gAWVFwAAAAAAAACMBG5hbWWUfZRoAIwFZ3Vlc3SUc4aULg=="

exp = bottle.cookie_decode(cookie,secret)
print(exp)
