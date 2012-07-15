#!/usr/bin/python
"""
Python wrapper for the CRM114 Classifier (http://crm114.sourceforge.net/).

Requires the crm command to be installed in your command path or be specified in the cfg file.

Uses an ini style config file.

To use the module, create an instance of the Classifier class, giving it a path to the config file.
Alternatively a space delimited list of categories can be passed in and
the a crm.cfg file will be loaded from or created in the current dir.

e.g:
	c = Classifier("/path/to/mycrm.cgf") #to load a config file
	c = Classifier("good bad ugly")      #to create a config in the current dir with defaults

To teach the classifier object about some text, call the learn method passing in a category
(on of the ones that you provided originally OR a new category),
and the text.

e.g:
	c.learn("good", "some good text")
	c.learn("bad", "some bad text")
	c.learn("ugly","SoMee Uggly tExT")
	
To find out what the classifier things about some text, call the classify method passing in the text.
The result of this method is a tuple -
  1. the category best matching the text,
  2. the probability of the match
  3. the pR (see crm114 docs).

e.g:
	(classification, probability, pR) = c.classify("some text")

"""

__version__ = "1.1.0dev"

__license__ = """
Copyright (C) 2005 Sam Deane, 2007 Sam Deane, Phil Cooper.
MIT LICENSE http://www.opensource.org/licenses/mit-license.php
"""

import os
import re
import logging
from ConfigParser import ConfigParser
import subprocess

#logFormat = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s#%(lineno)s %(message)s')
logFormat = logging.Formatter('%(asctime)s %(levelname)-8s  %(message)s')
log = logging.getLogger('crm.Classifier')

crmDEFAULTS = """[crm]
# command path where the crm executable is found
cmdpath = crm

# directory where all classification(css) files are
# %(here)s is replaced with the directory of this file
#dir = %(here)s/data
dir = %(here)s

# classifier to use if this changes the css files need to be recreated
classifier = osb unique microgroom
extension = .css

# space delimited list of possible classes 
#classes = spam ham

logfile = %(here)s/learning.log
"""

crmLearnCommand = "%s -u %s '-{ learn <%s> ( %s ) }'"
crmClassifyCommand = "%s -u %s '-{ isolate (:stats:); classify <%s> ( %s ) (:stats:);output /:*:stats:/}'"
	

# wrapper for crm114
class Classifier:

	def __init__( self, file_or_classes ):
		# Must be initialized with either classes or a config file with the classes
		classes=file_or_classes.split()
		if len(classes) > 1:
			# if there is no config file, find it or make it
			cfgFile='crm.cfg'
			if not os.path.exists(cfgFile):
				open(cfgFile,'w').write(crmDEFAULTS)
		elif len(classes) == 1:
			# if there is one then treat it as the config file name
			cfgFile = classes[0]
			classes=''
		config=ConfigParser({'here':os.path.dirname(os.path.abspath(cfgFile))})
		config.read(cfgFile)
		self.categories = classes or config.get('crm','classes').split()
		self.path = os.path.expanduser(config.get('crm','dir'))
		self.CmdPath = config.get('crm','cmdpath')
		self.Classifier = config.get('crm','classifier')
		self.Extension = config.get('crm','extension')
		if config.has_option('crm','logfile'):
			logfile = os.path.expanduser(config.get('crm','logfile'))
			loghandler = logging.FileHandler(logfile)
			loghandler.setFormatter(logFormat)
			loghandler.setLevel(logging.INFO)
			log.setLevel(logging.INFO)
			log.addHandler(loghandler)
		self.makeFiles()
		
	# learn the classifier what category some new text is in 
	def learn( self, category, text ):
		command = crmLearnCommand % (self.CmdPath, self.path, self.Classifier, category + self.Extension )
		log.debug("Learn: "+command)
		pipe = os.popen( command, 'w' )
		pipe.write( text )
		pipe.close()
		if len(text):
			log.info('Learn: %s <%s>'% ( category,text ))
	
	# ask the classifier what category best matches some text	
	def classify( self, text, choices='' ):
                """Given a string of text will return the classification
                    returns (catetory, probability, pR) tuple"""
		choices = choices.split() or self.categories
		files = [cat+self.Extension for cat in choices]
		command = crmClassifyCommand % (self.CmdPath, self.path, self.Classifier , ' '.join(files))
		log.debug("Classify: %s" % (command))
#		(fin, fout) = os.popen2( command )
                p = subprocess.Popen([ command ], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
                (fout, fin) = (p.stdout, p.stdin)
		fin.write( text )
		fin.close()
		stats = fout.read()
		fout.close()
                # lets parse the result
		pattern = r"Best match to file .. \(.*?([a-zA-Z0-9_-]+)%s\) +prob: *([0-9.]+) +pR: *([0-9.-]+)" % (self.Extension)
		statsfound = re.search(pattern,stats)
		if statsfound:
		    cat, prob, pR = statsfound.groups()
		    return (cat, float(prob), float(pR))
		else:
		    raise RuntimeError(stats)

	# ensure that data files exist, by calling learn with an empty string
	def makeFiles( self ):
		# make directory if necessary
		if not os.path.exists( self.path ):
				os.mkdir( self.path )

		# make category files
		for category in self.categories:
			self.learn( category, "" )
