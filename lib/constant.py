import os


# folder
IMG = 'img'
RAW = 'raw'
DATA = 'data'
CONF = 'config'
CONT = 'content'
NOVELWEBSITE = 'novelwebsite'
CONF_NOVELWEBSITE = os.path.join(CONF, NOVELWEBSITE)

# file
GLOBALS_YAML = os.path.join(CONF, 'globals.yaml')
AOZORA_YAML = os.path.join(CONF, 'aozora.yaml')
DATABASES_YAML = os.path.join(CONF, 'database.yaml')

# keys in novel_downloader
K_CHAPTER = 'chapter'
K_TITLE = 'title'
K_URL = 'url'
K_DATE = 'date'
K_BODY ='body'

# keys in config/database.yaml
K_BOOKNAME = 'bookname'
K_AUTHOR = 'author'
K_URL = 'url'
K_CHAPS = 'chaps'
K_CHAPS_OLD = 'chaps_old'
K_UPTIME = 'update_time'
K_LTUPTIME = 'last_update'
K_LTCHK = 'last_check'
K_ID = 'id'
K_DIR = 'dir'
K_COVER = 'cover'

# keys in config/novelwebsite/*.yaml
K_DOWNLOADER = 'Downloader'
K_NOVELDOWNLOADER = 'NovelDownloader'
K_WEBSITE = 'Website'

