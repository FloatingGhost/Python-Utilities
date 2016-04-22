#Python utils

Hannah's personal python utils repo - for anything I use a lot.

Like Machine learning stuff, or whatever else.

##Installation

```bash
$ sudo python setup.py install
```

##Utils:
* aiutils - Machine learning classes
  * class NGram, for models of language
* chan - 4chan API
  * class Board, for scraping from a specific 4chan board
* commandprocessor - A generic utility to parse commands
  * class CommandProcessor 
* reddit - A wrapper to Praw (python reddit API)
  * class Reddit
* skype - A wrapper to Skype4Py
  * class Chat - an easy class to manage skype bots with
* conf - A configuration file parser
  * class Conf - Simple conf file parser
  * class YamlConf - Calls PYaml and provides easy access
* twitter - A wrapper to Tweepy
  * class Twitter - Provides a simple way to retrieve tweets
* log - A wrapper to logging
  * class Log - Basic setup and usage of logging
* Package games
  * GUI - A wrapper to curses

Individual usages are listed in doc

##Tests

Run ./tests.py - calls nose

###Licence

See LICENCE
