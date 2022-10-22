# Browsing the website

Like in most challenges, lets start by exploring the application like an average consumer would. CLick all buttons and explore all pages acessible to the normal user. It looks like a normal todo list. We can create, delete and complete elements in a todo list.

Lookig at the title "broken uthentication control" it seems like the vulnreability is located in the way the website identifys each user.
Opening a private browser windows we can see that we have another fresh new todo list. We need to explore how the websíte keeps track of the users.

# Analyzing the Source Code

Lets look at the source code. We found two files that appear to have inbteresiting comments.
We found a comment in index.thml: 

// don't use getstatus('all') until we get the verify_integrity() patched

We found a comment in routes.py: 

# TODO: There are not view arguments involved, I hope this doesn't break
# the authentication control on the verify_integrity() decorator

It seems like the vulnerability is in verify_integrity function in util.py.

# Page Source

// don't use getstatus('all') until we get the verify_integrity() patched
const update = () => getTasks('user4f375000')
update()
setInterval(update, 3000)

This piece of code that is running in the background is updating the todo list every 3 seconds.


fetch(`/api/list/${endpoint}/?secret=${secret}`)


The function getTasks uses the secret amd the endpoint(username) to fetch the todo items. The endpoint is used to go to the table and grab the items and the secret is used to verify the user.

# Verification function

Lets look at the file util.py where the verify_integrity functions is located.

Verify_integrity is divided in two functions check_secret and check_integrity. 
Trying to understand how function inside function work, if a function inside a function has @functools.wraps(func) then, you're replacing one function with another. When function verify_integrity is called before a request is sent in routes.py,

@api.before_request
@verify_integrity
def and_then(): pass

The function check_integrity is executed. What this function do is verify if the request has argumetns or a JSON and apply some filters to the valeus passed. In the end it will run check_secret function.

def check_secret(secret, name):
	if secret != todo.get_secret_from(name):
		return abort(403)

This function will take the values from the request, endpoint and secret and verify if the secret is from the user that is passed in the endpoint.

# Vulnerability

We can abuse the fact that the endpoint /list/all does not need to have a specific user to be passed to acess all todo list items from all users plus the fact that we can just use our secret whithout using arguments and json body, since it has no filter and the check_secret will always be true.

# Exploit

Lets make the following request.
Note: to get the secret go to the Network tab in browser and grab the secret value. 

/api/list/all/?secret=<your_seret>

And we get the flag.


