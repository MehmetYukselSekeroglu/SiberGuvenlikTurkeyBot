import requests
import json


def GetIpQuery(ip_addrs): 
    try:
        MainUrl = f"https://ipinfo.io/{ip_addrs}"
        IpQuery = requests.get(url=MainUrl,timeout=10)
        
        if IpQuery.ok:
            IpQuery = json.loads(IpQuery.text)
            return ["true", IpQuery]
        else:
            return ["false", f"❌ İstek Geçersiz Durum Kodu Döndürdü. "]
    except Exception as err:
        return [ "false", "❌ İşlem hatalar ile sonuçlandı." ]
    