#games.ai

##Helper script for processing plaintext files into usable JSON

Intended for user with [Phaser](http://www.phaser.io), but probably can be
used wherever you want with a bit of work.

###Usage 

```bash
$ ./ai.py enemy.ai --obj enemy --out enemy.json
```

####Language Specification

```
[AI_Phase]
function args
function args
function args

[AI_Phase]
...
```

```
letter ::- A-Z | a-z | 0-9 | _ 
identifier ::- [letter] | [letter][identifier]
AI_Phase ::- [identifier]
prefefined_function ::- (anything defined in the object's code, object.func)
function ::- move | [predefined_function]
args ::- [letter] | [letter][args] | [args] [args] | (empty)
```
