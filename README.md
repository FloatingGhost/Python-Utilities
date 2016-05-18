#Python utils

Hannah's personal python utils repo - for anything I use a lot.

Like Machine learning stuff, or whatever else.

##Installation

```bash
$ sudo python setup.py install
```

##Modules:
* ai - Artificial Intelligence Utilities
  * ngram - for models of language
    * class NGram
  * knn - For K-Nearest-Neighbour calculations
    * class KNearest

* api - API Access to services
  * chan - 4chan API
    * class Board, for scraping from a specific 4chan board
  * reddit - A wrapper to Praw (python reddit API)
    * class Reddit
  * skype - A wrapper to Skype4Py
    * class Chat - an easy class to manage skype bots with
  * twitter - A wrapper to Tweepy
    * class Twitter - Provides a simple way to retrieve tweets

* games - Assistance with Game Dev (Not in current build)
  * GUI - A wrapper to curses

* network - Client/Server Utilities, With Authorization Built in
  * client - For interacting with Server
    * class Client - Performs 3-way handshake with server 
  * server
    * class Server - Wrapper to http.server, will handshake and serve POST
  * encryption
    * class LocalKeys - Wrapper to pyRSA, enables RSA encryption and hexlified versions
  * session
    * class Session - Simple tracking of a client's session
    * class SecureSession - Session, but with RSA encryption enabled
    * class SessionManager - Keeps track of multiple sessions
  * errors
    * class HFTPError
    * function code - Network errors, e.g FILE\_NOT\_FOUND
    * function error\_name - Reverse-lookup of code
    * function errorDesc - Human-Readable error description

* main package (floatingutils)
  * conf - A configuration file parser
    * class Conf - Simple conf file parser
    * class YamlConf - Calls PYaml and provides easy access
  * commandprocessor - A generic utility to parse commands
    * class CommandProcessor 
  * log - A wrapper to logging
    * class Log - Basic setup and usage of logging


Individual usages are listed in doc

##Tests

Run ./tests.py - calls nose

###Licence

See LICENCE
