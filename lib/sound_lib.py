#!/usr/bin/env python3 
from pydub import AudioSegment
import os 
import random
import speech_recognition as sr




def voice2text(target_file_path):
    target_file_path = str(target_file_path)

    try:
        recognizator = sr.Recognizer()
        with sr.AudioFile(target_file_path) as sound_file:
            audio_is = recognizator.record(sound_file)
            finaly_text_is = recognizator.recognize_google(audio_data=audio_is,language="tr-TR")
            return [ "true" , finaly_text_is ]
    
    except Exception as err_msg:
        return ["false", f"Hata: {str(err_msg)}"]
    






# SES DEN METNE FONKSIYONUNDA GOOGLE API ICIN * FORMATDAN VAW FORMATINA CEVIRME FONKSIYONIU 
def ConvertAnyAudio_to_wav(target_file_path:str, temp_dir_path:str):
    """ Desteklenen formatlardaki ses dosyalarını vaw foarmatına dönüştütüt
        Desteklenen formatlar -> "MP3","OGG","FLAC","AAC","AIFF","WMA","WAV"

    Args:
        target_file_path (str): hedef dosyanın dosya yolu 
        temp_dir_path (str, optional): final olarak oluşan *.vaw dosyasının kayıt konumu. Defaults to TEMP_DIR.

    Returns:
        dict: key: success -> true,false eğer urum başarılı ise success:true ve path döner değilse code:hata durumu
    """
    
    TARGET_FILE_FORMAT = "wav"
    
    if not os.path.exists(target_file_path) or not os.path.exists(temp_dir_path):
        return {"success":"false", "code":"invaid path"}
    
    target_file_extensions = target_file_path.split(".")
    target_file_extensions = target_file_extensions[len(target_file_extensions)-1]

    supported_formats = ["MP3","OGG","FLAC","AAC","AIFF","WMA","WAV"]
    
    if target_file_extensions.upper() not in supported_formats:
        return {"success":"false", "code":"not supported file extensions"}

    LoadedAudio = AudioSegment.from_file(target_file_path, format=target_file_extensions)
    export_name = temp_dir_path+"exported_file_"+str(random.randint(1,999))+"."+TARGET_FILE_FORMAT
    
    # dosyanın export edilmesi 
    LoadedAudio.export(export_name, format=TARGET_FILE_FORMAT)

    if os.path.exists(export_name):
        return {"success":"true", "path":str(export_name)}
    else:
        return { "success":"false", "code":"export error"}




# SES DEN METNE FONKSIYONUNDA GOOGLE API ICIN * FORMATDAN VAW FORMATINA CEVIRME FONKSIYONIU 
def GenericAudioConverter(target_file_path:str, temp_dir_path:str, TARGET_FILE_FORMAT="mp3") -> list:
    """ Desteklenen formatlardaki ses dosyalarını vaw foarmatına dönüştütüt
        Desteklenen formatlar -> "MP3","OGG","FLAC","AAC","AIFF","WMA","WAV"

    Args:
        target_file_path (str): hedef dosyanın dosya yolu 
        temp_dir_path (str, optional): final olarak oluşan *.vaw dosyasının kayıt konumu. Defaults to TEMP_DIR.

    Returns:
        dict: key: success -> true,false eğer urum başarılı ise success:true ve path döner değilse code:hata durumu
    
    
    UYARI: geri döndürülen path kendisi silinmez
    
    """
    
    
    if not os.path.exists(target_file_path) or not os.path.exists(temp_dir_path):
        return {"success":"false", "code":"invaid path"}
    
    target_file_extensions = target_file_path.split(".")
    target_file_extensions = target_file_extensions[len(target_file_extensions)-1]

    supported_formats = ["MP3","OGG","FLAC","AAC","AIFF","WMA","WAV"]
    
    if target_file_extensions.upper() not in supported_formats:
        return {"success":"false", "code":"not supported file extensions"}

    LoadedAudio = AudioSegment.from_file(target_file_path, format=target_file_extensions)
    export_name = temp_dir_path+"exported_file_"+str(random.randint(1,999))+"."+TARGET_FILE_FORMAT
    
    # dosyanın export edilmesi 
    LoadedAudio.export(export_name, format=TARGET_FILE_FORMAT)

    if os.path.exists(export_name):
        return {"success":"true", "path":str(export_name)}
    else:
        return { "success":"false", "code":"export error"}


