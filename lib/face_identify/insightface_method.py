import cv2
import insightface
import numpy as np
from ..ImageTools.opencv_tools import *
import os
detectModelDefaultResulation = (640,640)

class FaceAnlyser():
    def __init__(self, insightFaceAnalyserUI:insightface.app.FaceAnalysis) -> None:
        
        
        self.faceAnalyserUI = insightFaceAnalyserUI
        
        
        
    def compareFaces(self, sourceImage:str,targetImage:str) -> list:
        try:

            # verilerin okunması
            soruce_cv2_data = cv2.imread(sourceImage)
            target_cv2_data = cv2.imread(targetImage)
            
            # analiz edilmesi 
            analysSource = self.faceAnalyserUI.get(soruce_cv2_data)
            analysTarget = self.faceAnalyserUI.get(target_cv2_data)
            
            # sorunların tespit edilmesi
            if len(analysSource) > 1 or len(analysTarget) > 1:
                return [ False, "❌ Her resimde sadece 1 adet yüz kabul edilebilir." ]
            
            if len(analysSource) == 0:
                return [ False, "❌ Kaynak resimde yüz bulunamadı."]
            
            if len(analysTarget) == 0:
                return [False, "❌ Hedef resimde yüz bulunamadı."]
            
            
            # Gömme noktaları
            face_embedding_sourceFile = analysSource[0]["embedding"]
            face_embedding_targetFile = analysTarget[0]["embedding"]
            
            
            # Kosinüs benzerliği 
            dot_product_size = np.dot(face_embedding_sourceFile, face_embedding_targetFile)
            norm_sound1 = np.linalg.norm(face_embedding_sourceFile)
            norm_sound2 = np.linalg.norm(face_embedding_targetFile)
            GetSimilarity = dot_product_size / (norm_sound1 * norm_sound2)
            GetSimilarity = GetSimilarity * 100
            GetSimilarity = round(GetSimilarity,2)
            
            
            # Renkli noktalar
            soruce_cv2_data = landmarks_rectangle(soruce_cv2_data,data_list=analysSource[0]["bbox"])
            soruce_cv2_data = landmarks_rectangle_2d(soruce_cv2_data, data_list=analysSource[0]["landmark_2d_106"])
            
            
            target_cv2_data = landmarks_rectangle(target_cv2_data,data_list=analysTarget[0]["bbox"])
            target_cv2_data = landmarks_rectangle_2d(target_cv2_data, data_list=analysTarget[0]["landmark_2d_106"])



            # olası hatalara karşı önlem 
            if GetSimilarity < float(0):
                GetSimilarity = float(0)
        

            cv2.imwrite(sourceImage,soruce_cv2_data)
            cv2.imwrite(targetImage, target_cv2_data)
            
            return [
                True,
                str(GetSimilarity),
                str(sourceImage),
                str(targetImage)
                
            ]
        
        
        except Exception as err:
            print(f"[ FACE COMPARSION ERROR ]: {err}")
            try:
                print(f"[ otomatik silme ]: {sourceImage}, {targetImage}")
                os.remove(sourceImage)
                os.remove(targetImage)
                print("[ otomatik silme ]: tamamlandır ")
            except Exception as err:
                print(f"[ otomatik silme hatası ]: {err}")
            
            return [False, "❌ Sistem kaynaklı bir hata gerçekleşti."]