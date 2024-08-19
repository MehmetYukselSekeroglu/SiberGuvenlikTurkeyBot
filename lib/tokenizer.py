import numpy as np
def tokenize(tokenizer_is,yorumListesi:list, dimSize:int=50):
    y_yorumlar = []
    for yorum in yorumListesi:
        y_yorum= []  
        for kelime in yorum.split():
            if len(y_yorum) < dimSize and kelime in tokenizer_is:
                y_yorum.append(tokenizer_is[kelime])

        if len(y_yorum) < dimSize:
            add_zeros = list(np.zeros(dimSize- len(y_yorum), dtype=int))
            y_yorum =  add_zeros + y_yorum
        y_yorumlar.append(y_yorum)
        
            
    return np.array(y_yorumlar, dtype=np.dtype(np.int32))
