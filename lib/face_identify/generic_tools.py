import numpy as np
from numba import njit

def binaryData(file_path:str) -> bytes:
    with open(file_path, "rb") as target:
        return target.read()
    
    
@njit(nopython=True)    # numba ile hızlandırma makrosu
def cosineSimilarityCalculator(face_embedding_sourceFile, face_embedding_targetFile) -> int:

        # GErekli ön işlemler 
        dot_product_size = np.dot(face_embedding_sourceFile, face_embedding_targetFile)
        norm_sound1 = np.linalg.norm(face_embedding_sourceFile)
        norm_sound2 = np.linalg.norm(face_embedding_targetFile)
        # kosinus benzerliğini hesaplama 
        GetSimilarity = dot_product_size / (norm_sound1 * norm_sound2)
        GetSimilarity = GetSimilarity * 100
        GetSimilarity = int(GetSimilarity)

        if GetSimilarity < 0:
            GetSimilarity = 0
            
        return GetSimilarity