import json
import sys
import os
import onnxruntime
from .env import CONFIG_FILE_PATH as __CONFIG_FILE_PATH__
from .output.consolePrint import (p_info, p_error)


# Config dosyası oluşturmak için basit bir şema kullanır 
# python3 -m lib.make_config şeklinde çağrılırsa otomatik çalışır 
# config/config.json oluşturur.
# gerekli paket: colorama 



__MODULE_LOG_NAME__ = "MAKE_CONFIG_SCHEMA"
__BASE_DIR__ = os.getcwd() + os.path.sep
__TEMP_DIR__ = __BASE_DIR__ + "tmp" + os.path.sep
__DATA_DIR__ = __BASE_DIR__ + "data" + os.path.sep
__SQL_SCHMEA_PATH__ = __BASE_DIR__ + "sql" + os.path.sep + "postgresql_schema.sql"
#__URL_FILE = __BASE_DIR__ + "defaults" + os.path.sep + "url.txt"
#__FLASK_DATA_DIR__ = __BASE_DIR__ + "flask_data" + os.path.sep 

__CONFIG_FILE_DATA__ = {
    
    "vendor":"SiberGüvenlikTurkey",
    "name":"TeleOsintBot",
    "version":"1.5.0",
    "base_dir":__BASE_DIR__,
    "temp_dir":__TEMP_DIR__,
    "data_dir":__DATA_DIR__,
    "bot_token":"",
    "vt_api_key":"",
    "ai_mode":False,
    "tokenizer_path":__DATA_DIR__ + "models" + os.path.sep +"tokenizer.json",
    "anti_illegal_model":__DATA_DIR__ + "models" + os.path.sep +"anti_illegal.h5",
    "web_requests":{
      "timeout":10,
      "random_user_agent":True,
      "ssl_verification":True,  
    },
    "insightface":{
        "prepare":{
        "ctx_id":-1,
        "det_thresh":0.5,
        "det_size":(640,640),
        },
        "main":{
            "providers":onnxruntime.get_available_providers(),
            "model":"buffalo_l"
        }
    },
        
    
    "insightface_min_verification_sim":0.50,
    "similarity_calculator":"consine_sim",    
    
    
}



if __name__ == "__main__":

    os.makedirs(f"{__BASE_DIR__+'config'}",exist_ok=True)
    try:
        with open(__CONFIG_FILE_PATH__,"w+") as conf_file:
            json.dump(__CONFIG_FILE_DATA__,conf_file,indent=4)
        
    except Exception as err:
        p_error(f"Failed to crate {__CONFIG_FILE_PATH__}, {err}",__MODULE_LOG_NAME__)
        sys.exit(-1)        

    p_info(f"{__CONFIG_FILE_PATH__} successfuly generated.",__MODULE_LOG_NAME__)
    sys.exit(0)














