# external library's 
import os   # işletim sistemi operasyonları için
import sys   # sistemsel işlemler içim
import transformers # metin özetleme için 
import keras    # Antiİllegal model'i kullanmak için
import time     # Zamansal işlemler için Uyku bekleme vs
import json     # Config dosyasını yüklemek için
import random   # Dosya adlarını benzersiz random sayılar için
import telebot  # Telegram api
from telebot import types   # fotoğraf vs göndermek için 
import threading    # arkplanda çalışma için

# local library's 
from lib.sound_lib import   *   # ses işlemleri
from lib.load_config import load_config_from_file   # config yükleme 
from lib.output.banner import makeFigletBanner  # banner 
from lib.output.consolePrint import p_error,p_info,p_warn,p_title   # print fonksiyonları
from lib.tokenizer import tokenize  # tokenizer oluşturucu
from lib.virus_total import is_url,virustotal_url_response_handler,virustotal_url_scanner # VirüsTotal
from lib.init_insightface import initilate_insightface  # insightface yüz tanıma sistemi 
from lib.face_identify import insightface_method    # Yüz tanma otomatik sistem

# Config dosyasını yükler 
MainConfig = load_config_from_file()

# Config yükleme durumunu kontrol eder 
if MainConfig[0] == False:
    p_error(f"Failed to load config from file: {str(MainConfig[1])}")
    sys.exit(1)
    

# Config listesi küçültülür 
MainConfig = MainConfig[1]



def printBannerAndInfo():
    """
    Vendor ve Version bilgileri ekrana verilir 
    """
    print(makeFigletBanner(MainConfig["vendor"]))
    print()
    print()
    print(f"* Version:\t{MainConfig['version']}")


# tokenizer datasının yüklenmesi 
with open(str(MainConfig["tokenizer_path"]),"r") as target:
    TOKENIZER_IS = json.load(target)


# Gerekli küresel değişkenler 

# anti illegal keras modeli 
ANTI_ILLEGAL_MODEL = keras.saving.load_model(MainConfig["anti_illegal_model"])

# metin özetleme transformers | tensorflow modeli 
TEXT_SUMMARYZATION_MODEL = transformers.pipeline("summarization",model="facebook/bart-large-cnn")

# Virüstotal api keyinin config dosyasından yüklenmesi
VIRUSTOTAL_API_KEY = MainConfig["vt_api_key"]

# Yüz tanıma sistemi için max file size belirlenmesi
YUZ_TANIMA_MAX_IMAGE_SIZE = (5 *1024) * 1024

# Temp'dir in config dosyasından alınması
TEMP_DIR = MainConfig["temp_dir"]

# Yüz tanıma sistemi yardım mesajları
YUZ_KARSILASTIRMA_HELP_TEXT__FACE = """❔ InsightFace Yüz Karşılaştırma Sistemi Kullanımı❔

➡️ Telegrama 1 adet yüz içeren (1 tane yüz içermeli) fotoğraf atın ve yanıtlayarak /yüz1 yazın

➡️ Telegrama 1 adet daha resim atın yanıtlayın ve /yüz2 yazın.

➡️ Final olarak /karsilastir yazarak sonucu görebilirsiniz.


➡️ Bu sistem InsightFace buffalo_l modeli ile yüzleri tespit eder kosinüs benzerliği ile benzerlik oranını hesaplar.

"""
YUZ_KARSILASTIRMA_HELP_TEXT__COMPARE = YUZ_KARSILASTIRMA_HELP_TEXT__FACE



# Yüz tanıma sistemi başlatılır 
insightfaceApp = initilate_insightface([True, MainConfig])
FaceAnalysisToolkit = insightface_method.FaceAnlyser(insightFaceAnalyserUI=insightfaceApp)



# banner ve version bilgisini yazdırır 
printBannerAndInfo()

# Gerekli dizinler oluşturulur 
os.makedirs(TEMP_DIR, exist_ok=True)





try:
    # Telegram botunun set edilmesi
    CyberBot = telebot.TeleBot(token=MainConfig["bot_token"])
    
except Exception as err: # olası token hatalarını yakalamak için | kullanıcı bazlı hatalar mesela 
    p_error(f"Failed to start telegram bot: {err}")
    sys.exit(2)
    
    

# anti illegal modeli için mesaj yakalama özelliği 
@CyberBot.message_handler(["ai"])
def calculate_ai(msg):    
    
    # debugger bilgisi 
    p_info("New requests anti illegal model!")
    
    
    # komutu al 
    command_is = msg.text
    command_is = str(command_is).replace("/ai", "")

    command_is = str(command_is).strip().replace("\n"," ")       
    current_line = ""
    
    # metni temizle ve güvenli hale getir 
    for char in command_is:
        if str(char).isalpha() or char == " " or str(char).isnumeric():
            current_line += char
    if str(current_line) == "None" or len(str(current_line)) == 0 or len(str(current_line)) < 5:
        CyberBot.reply_to(msg, "Geçersiz mesaj!")
        return
    
    # boşlukları temizle 
    if current_line.startswith(" "):
        current_line = current_line[1:]

    # model ile tahmin işlemi yapıp yanıtla 
    results = ANTI_ILLEGAL_MODEL.predict(tokenize(TOKENIZER_IS,[current_line]))
    CyberBot.reply_to(msg,f"Mesaj illegallik oranı: %{str(int(results[0][0]*100))}")


# metin özetleme 
@CyberBot.message_handler(["ozet"])
def text_summary(msg):
    
    # debugger bilgisi 
    p_info("New requests for text summaryzatiın!")
    
    # olası sistemsel hataları yakalama için try blogu
    try:
        # mesaj bir yanıt mı kontrol edilir 
        if msg.reply_to_message == None:
            CyberBot.reply_to(msg,f"!Lütfen bir mesaj yanıtlayarak bu komutu çalıştırın!")
            return
        
        # metin set edilir 
        target_text = msg.reply_to_message.text

        # mesaj parcalanır ve kontrolden geçer 
        parcalanmis_mesaj = str(target_text).split(" ")
        if len(parcalanmis_mesaj) > 400 or len(parcalanmis_mesaj) < 50:
            CyberBot.reply_to(msg,f"!400 karakterden uzun veya 50 karakterden kısa mesajlar yanıtlanamazaz!")
            return

        # ek temizlik 
        prepared_text = str(target_text).replace("\n", " ")
        finaly_text = ""

        # karakter kontrolü sağla 
        for char in prepared_text:
            if char.isalpha() or char == " " or char in [",",".","!","?","!"] or char.isnumeric():
                finaly_text += char

        # bozuk kelimeleri temizle 
        finaly_text_2 = ""
        for kelime in finaly_text.split(" "):
            if len(kelime) >= 15:
                continue
            else:
                finaly_text_2 += " " + kelime
            
        


        # özeti oluştur 
        results_is = TEXT_SUMMARYZATION_MODEL(finaly_text_2,max_length=200,min_length=30, do_sample=False)

        # özet bilgisini al ve kullanıcıya ilet 
        CyberBot.reply_to(msg, f"🌟OZET🌟:\n\n{str(results_is[0]['summary_text'])}")
        return
    except Exception as err: # olası hataların yakalandıgı kısım | ve geri bildirim 
        CyberBot.reply_to(msg, f"❌ Özet oluşturma esnasında hata oluştu")



# help ve start mesajları
@CyberBot.message_handler(["help", "start"])
def send_help_message(msg):
    HELP_TEXT = f"""Merhaba ben {str(MainConfig["vendor"])} tarafından üretilmiş bir botun komutlarım şu şekilde

🔗 /ai <metin>   ➡️ Bir mesaj illegalmi diye Yapay Zeka sorusu
🔗 /url <url>  ➡️ Bir url hakkında VirüsTotal sorgusu
🔗 /ozet  ➡️ Bir metnin özetini çıkartırım (yavaş)
🔗 /cevir ➡️ Bir metni türkçe diline çeviririm (yakında)
🔗 /karsilastir ➡️ Yüz karşılaştırma sistemi.
"""
    CyberBot.reply_to(msg, HELP_TEXT)


# VirüsTotal URL tarama sistemi
@CyberBot.message_handler(["url"])
def scan_url(msg):
    # komut bir mesajı yanıtlayarakmı çalıştırılmış kontrol ediliyor 
    if msg.reply_to_message != None:

        # öyle iste hedef olarak yanıtlanan mesaj seçiliyor 
        target_text = msg.reply_to_message.text        
        target_url_is = target_text
        
    # Eğer yanıtlama olarak değil ise komuttan sonra url verildiği varsayılacak
    else:
            
        # hedef olarak komutun verildiği mesaj seçildi 
        target_text = msg.text
        # mesaj " " boşluklar referans alınarak bölündü 
        str_data = target_text.split(" ")

        # mesajın yapısı kontrol edildi ve uygun değilse geri bildirim verilerek iptal edildi işlem 
        if len(str_data) != 2:
            CyberBot.reply_to(msg, "❓Örnek Kullanım❓: /url https://google.com")
            return 
            
        # Eğer format uygunsa hedef target_url_is değişkenine atandı 
        target_url_is = str_data[1]


        
    # Programın tıkanmasını engellemek için threads'a fonksiyon hazırladık 
    def run_as_threads():

        # yanıt olarak mesaj atılacağı için sohbet tipine uygun olarak chat id alındı 
        if msg.chat.type == "private":
            chat_id_is = msg.from_user.id
        else:
            chat_id_is = msg.chat.id

        # alınan url nin geçerli olup olmadığı formata uygunluğu kontrol ediliyor 
        if not is_url(target_url_is):
            CyberBot.reply_to(msg, "❌ Geçersiz URL!")
            return ""

        # Analizin başladığı hakkında bir mesaj gönderildi ve daha sonrası için kaydedildi 
        main_msg = CyberBot.send_message(chat_id=chat_id_is   ,text=f"Bekleyiniz...⏳\nURL: `{str(target_url_is)}`"
            ,parse_mode="markdown"                         
                )
            
        # Sonraki düzenlemeler için mesajın benzersiz id si alındı  
        main_msg_id = main_msg.message_id

        # Hedef url VirusTotal api için yazdıgımız kutuphane fonksiyonuna verildi 
        scan_adım_1 = virustotal_url_scanner(target_url=target_url_is, vt_api_key=VIRUSTOTAL_API_KEY)

        # Gönerdiğimiz bilgilendirme mesajı silinmiş ise hata almamak için kontrol yaptı 
        if main_msg.text is not None:
                
            # Tarama sonucunda VirüsTotal isteği kabul etmişmi bakıyoruz   
            if scan_adım_1[0] == "true":

                # Apinin sonuçları takip etmemiz için verdiği id yi alıyoruz 
                izleme_id = scan_adım_1[1]

                # İSteğin kabul edildiği ve yaklasık 25sn sonra cevap geleceğini belirttik 
                CyberBot.edit_message_text(text="`VirüsTotal analizi bekleniyor..⏳`",
                    chat_id=chat_id_is, message_id=main_msg_id,
                    parse_mode="markdown"
                    )

                # Gereksiz kaynak yemesin diye ve bekleme sağlasın diye sleep kullanıyoruz
                time.sleep(25)

                # 2. adım olarak api den tarama sonuçlarını istiyoruz 
                scan_adım_2 = virustotal_url_response_handler(vt_api_key=VIRUSTOTAL_API_KEY, is_response_id=izleme_id)

                # eğer istek başarılı ise devam ediyoruz
                if scan_adım_2[0] == "true":
                    data = scan_adım_2[1]   
                        
                    # Yollanacak bilgileri markdown şeklinde eklemeler yaparak ayarlıyoruz 
                    output_data_is = f"""🛑Sonuçlar🛑:\n
🔗URL🔗: `{str(data[0])}`
🦠Tespit🦠: `{str(data[1])} / {str(data[2])}`
⏳Tarih⏳: `{str(data[3])}`
[🔗VirüsTotal Adresi🔗]({str(data[4])})
"""                 
                    # Ana mesajı düzenleyerek bu bilgileri ekliyoruz ve return ile işlemi bitiriyoruz
                    CyberBot.edit_message_text(chat_id=chat_id_is ,text=output_data_is ,message_id=main_msg_id,parse_mode="markdown")
                    return ""
                    
                else:
                    # 2.adımda hata alınırsa geri bildiim
                    CyberBot.edit_message_text(chat_id=chat_id_is,text=f"❌Hata❌: {scan_adım_2[1]}", message_id=main_msg_id)
            else:
                # 1.adımda hata alınırsa geri bildirim 
                CyberBot.edit_message_text(chat_id=chat_id_is, text=f"❌Hata❌: {scan_adım_1[1]}", message_id=main_msg_id)
                return ""


    # Threadsın tanımlanması ve başlatılması 
    vt_scanner_threads = threading.Thread(target=run_as_threads,daemon=True)
    vt_scanner_threads.start()   
    
    
    
known_faces = {}  # Bilinen yüzlerin saklandığı sözlük


# Yüzlerin set edilmesini sağlar 
@CyberBot.message_handler(commands=["yüz1", "yüz2"])
def get_face_comparsion(msg):

    # yanıt kontrol 
    if not msg.reply_to_message or not msg.reply_to_message.photo:
        CyberBot.reply_to(msg, "➡️ Bir adet yüz içeren resim yanıtlayın.")
        return

    # File size kontrol 
    if msg.reply_to_message.photo[-1].file_size > YUZ_TANIMA_MAX_IMAGE_SIZE:
        CyberBot.reply_to(msg, "➡️ Max resim boyutu 5.4mb olabilir!")
        return
    
    # Dosya bilgisini alma ve indirme 
    file_id = msg.reply_to_message.photo[-1].file_id
    file_info = CyberBot.get_file(file_id)
    downloaded_file = CyberBot.download_file(file_info.file_path)
    
    # metne göre filtreleme ve set etme işlemleri 
    if msg.text == '/yüz1':
        known_faces['yüz1'] = downloaded_file
        CyberBot.reply_to(msg, "➡️ Yüz-1 Kaydedildi.")
        return
    elif msg.text == '/yüz2':
        known_faces['yüz2'] = downloaded_file
        CyberBot.reply_to(msg, "➡️ Yüz-2 Kaydedildi.")
        return
    else:
        CyberBot.reply_to(msg, YUZ_KARSILASTIRMA_HELP_TEXT__FACE)


# Yüz karşılaştırma işlemini başlatan komut 
@CyberBot.message_handler(commands=["karsilastir"])
def compare_of_finaly(msg):
    
    # benzersiz kayıt isimleri belirleme 
    save_name1 = "save_face_1_"+str(random.randint(1,9999))+".png"
    save_name2 = "save_face_2_"+str(random.randint(1,9999))+".png"

    # dosya yollarının belirlenmesi
    face_1_path = TEMP_DIR+save_name1
    face_2_path = TEMP_DIR+save_name2

    # Resim 1 veya Resim 2 ayarlanmadı ise Geri bildirim vererek işlemin sonlandırılması 
    if "yüz1" not in known_faces.keys() or "yüz2" not in known_faces.keys():
        CyberBot.reply_to(msg,YUZ_KARSILASTIRMA_HELP_TEXT__COMPARE)
        return            

    # Resim 1 in dosya olarak kaydedilmesi 
    with open(face_1_path, "wb") as file1:
        file1.write(known_faces["yüz1"])

    # Resim 2 nin dosya olarak kaydedilmesi 
    with open(face_2_path, "wb") as file2:
        file2.write(known_faces["yüz2"])

    # Analizin başladığı hakkında bilgilendirme mesajı 
    main_msg = CyberBot.send_message(
        chat_id=msg.chat.id,text="`InsightFace çalışıyor...`",parse_mode="markdown")
    # Resimlerdeki yüzlerin karşılaştırılması 
    result_is = FaceAnalysisToolkit.compareFaces(sourceImage=face_1_path,targetImage=face_2_path)

    # işlem başarılımı kontrol ediliyor 
    if not result_is[0]:
        CyberBot.edit_message_text(
            chat_id=msg.chat.id,
            message_id=main_msg.message_id,
            text=f"`{result_is[1]}`",
            parse_mode="markdown")
        
        # Yüz dizisinin otomatik temizlenmesi 
        known_faces.clear()
        return    
            
    # verilerin değişkenlere atanması 
    benzerlik_is = result_is[1]
    save_name1 = result_is[2]
    save_name2 = result_is[3]

    # Gönderiecek resimlerin dizisi 
    group_of_landmarks = []
    # Bilgi metninin belirlenmesi
    FINALY_TEXT = f"""➡️ Sonuçlar:  
     
➡️ Bnezerlik (kosinüs): %{benzerlik_is}
"""
    # Resim 1 listeye ekleniyor 
    with open(save_name1,"rb") as send_d1:
        group_of_landmarks.append(
            types.InputMediaPhoto(media=send_d1.read(), caption=FINALY_TEXT))
    # Resim 2 listeye ekleniyor 
    with open(save_name2, "rb") as send_d2:
        group_of_landmarks.append(
            types.InputMediaPhoto(media=send_d2.read()))
        # İşlenen resimlerin gönderilmesi 
    CyberBot.send_media_group(chat_id=msg.chat.id,media=group_of_landmarks, )
    os.remove(save_name1)
    os.remove(save_name2)
    known_faces.clear()
    return




@CyberBot.message_handler(commands=["totext"])
def ses_den_metne(msg):
    # thread fonksiyonunun tanımlanması 
    def run_as_threads(): 
        # yanıtlanan mesaj bir sesli mesajmı diye kontrol ediliyor 
        if msg.reply_to_message:
            if not msg.reply_to_message.voice:
                CyberBot.reply_to(msg, "🎧 Lütfem bir sesli mesaj yanıtlayınız...")
                return
            
            # Dosya bilgilerinin alınması
            file_info = CyberBot.get_file(msg.reply_to_message.voice.file_id)
            target_ses_file = CyberBot.download_file(file_info.file_path)
            
            # Dosyaya benzersiz bir isim atanması ve TEMP path altına kaydedilmesi 
            rand_save_name = "voice2text_"+str(random.randint(1,999))+".ogg"
            with open(TEMP_DIR+rand_save_name, "wb") as ses_file:
                ses_file.write(target_ses_file)
                
            # Ses dosyasının google api sine yollanabilmesi için vaw formatına çevrilmesi 
            converted_sound_is = ConvertAnyAudio_to_wav(TEMP_DIR+rand_save_name,
                                                        temp_dir_path=TEMP_DIR)["path"]
            
            # Eski dosya çevrilerek yeni format verildi eski formattaki dosyanın kaldırılması 
            os.remove(TEMP_DIR+rand_save_name)
            
            # Kendi kütüphanemiz olan soundlib den sesden metne fonksiyonu ile çevirmeyi başltıyoruz 
            results_is = voice2text(converted_sound_is)
            
            # Google api sine istek atıldığı için dosyalara ihtiyacımız kalmadı kaldırabiliriz 
            os.remove(converted_sound_is)
            
            # Son olarak bilgilendirme metnini tanımlayalım 
            finaly_output_data_is = "🎧 Ses'den metne (Google):\n"
            
            # Bilgilendirme metninin sonuna api den gelen metni ekleyerek mesajı yanıtlayalım 
            CyberBot.reply_to(msg, finaly_output_data_is+results_is[1])
        
        # yanıtlanan mesaj bir ses dosyası değilse geri bildirim verilsin 
        else:
            CyberBot.reply_to(msg, "🎧 Lütfem bir sesli mesaj yanıtlayınız...")
            return

    # Threads'ın başlatılması 
    ses2metin_threadı = threading.Thread(target=run_as_threads)
    ses2metin_threadı.start()

    
    
    
    
# botun sürekli olarak döngüde olmasını sağlar 
p_info("Starting infinity polling for telegram bot ...")
CyberBot.infinity_polling()
