MAX_IP_STRING_LEN = 15

def is_validIp(target_ip:str) -> bool:
    try:
        target_ip = str(target_ip)        
        if len(target_ip) < 1:
            return False
        if len(target_ip) <= 15:
            if target_ip.count(".") == 3:
                check_numerics = target_ip.replace(".","")
                check_numerics = str(check_numerics)
                if check_numerics.isdigit():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    except Exception:
        return False
    
    