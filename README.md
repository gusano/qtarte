# QtArte

This program allows recording videos from [arte+7](http://videos.arte.tv) website (in german).

This is a git conversion of [~arte+7recorder/+junk/qtarte](https://launchpad.net/~arte+7recorder/+archive/ppa) bzr repository (which
does not seem to be maintained anymore).

![QtArte screenshot](http://www.yvanvolochine.com/media/images/qtarte.gif)

## Dependencies

 - python >= 2.7 (does not work with python3 yet)
 - PyQt >= 4.4
 - [flvstreamer](http://savannah.nongnu.org/projects/flvstreamer)
 - [urllib2](http://docs.python.org/2/library/urllib2.html)
 - [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4)

## Usage

Assuming you have dependencies installed:

 - `$ git clone git://github.com/gusano/qtarte.git`
 - `$ cd qtarte`
 - `$ ./arte7recorder.py`

Optionally you can pass a language option (`fr` or `de`, default is `fr`):

 - `$ ./arte7recorder.py -l de` or `$ ./arte7recorder.py --lang=de`

Show help:

 - `$ ./arte7recorder -h`

## Authors

 - Yvan Volochine <contact@yvanvolochine.com>
 - Vincent Vande Vyvre <vins@swing.be>