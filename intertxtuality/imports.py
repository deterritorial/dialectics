SERVERS=[
    'http://128.232.229.63:8529'
]
COL_ID='id'
COL_ADDR='_id'
COL_CORPUS='_corpus'
IDSEP_START='_'
IDSEP='/'
IDSEP_DB='__'


import os,sys,random
from .logs import *


from .utils import *

log = Log(
	to_screen=True,
	to_file=False,
	# fn=PATH_LLTK_LOG_FN,
	force=True,
	# verbose=LOG_VERBOSE_JUPYTER if in_jupyter() else LOG_VERBOSE_TERMINAL
)
log.info('booting')


from .models import *
from .database import *
from .text import *
from .corpus import *
from .rels import *
from .database import _ADB_ as db,_ADB_CLIENT as client,_ADB_SYSDB as sysdb


log.info('ready')