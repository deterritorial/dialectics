#print(__file__,'imported')
import os,sys
from pathlib import Path
PATH_USER_HOME = str(Path.home())
PATH_HOME = os.path.join(PATH_USER_HOME,'intertxt')
PATH_DATA = os.path.join(PATH_HOME,'data')
PATH_CONFIG = os.path.join(PATH_HOME,'config')
PATH_CORPORA = os.path.join(PATH_HOME,'corpora')
TO_SCREEN = True
TO_FILE = True

SERVERS=[
    'http://128.232.229.63:8529'
]
COL_ID='id'
COL_ADDR='_addr'
COL_CORPUS='_corpus'
IDSEP_START='_'
IDSEP='/'
IDSEP_DB=')('
MATCHRELNAME='rdf:type'
DEFAULT_COMPAREBY=dict(author=0.9, title=0.9, year=1.0)

INIT_DB_WITH_CORPORA = {
	# 'bpo',
	'chadwyck',
	'chicago',
	'markmark',
	'txtlab',
	'tedjdh',
	'gildedage',
	# 'canon_fiction',
	'clmet',
	'dta',
	'dialnarr',
	'estc',
	'eebo_tcp',
	'ecco_tcp',
	'ecco',
	'evans_tcp',
	'litlab',
	# 'ravengarside',
	'semantic_cohort',
	'spectator'
}

OK_META_KEYS={
'_id',
'_key',
'_addr',
'_corpus',
'_au',
'_ti',
'_yr',
'id',
}




### stdlib
import tempfile
from zipfile import BadZipFile
import shutil
import tempfile,sys,shutil,os,random


## external
import pandas as pd
import numpy as np
import humanize



## me
from intertxt.utils.logs import *
with Log('booting'):
	from intertxt.utils import *
	from intertxt.database import *
	from intertxt.texts import *
	from intertxt.corpora import *
	from intertxt.models import *

