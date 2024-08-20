
"""
? Enviroments File ?

! DONT CHANGE IT !

"""

import os

# Gerekli global değişkenlerin en baştan set edilmesi bunların değiştirilmesi sistemi bozacaktır 
# Bilgili değilseniz ellemeniz tavsiye edilmez 

CONFIG_FILE_NAME = "config.json"
APPLICATION_BASE_DIR = os.getcwd().split(os.path.sep)[-1]
CONFIG_FILE_PATH = "config" + os.path.sep + "config.json"
DEFAULT_CHARSET = "utf-8"