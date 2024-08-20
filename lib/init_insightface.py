from .output.consolePrint import p_info
from numba import jit
import insightface


__MODULE_LOG_NAME__ = "INIT_INSIGHTFACE"


def initilate_insightface(main_conf:list) -> insightface.app.FaceAnalysis:
    """
    config dosyasını referans alarak insightface objesini hazırlar ve döndürür.
    """
    p_info("Initilating insightface",locations=__MODULE_LOG_NAME__)
    insightfaceAnalyser = insightface.app.FaceAnalysis(**main_conf[1]["insightface"]["main"])


    p_info("Preaparing insightface app",locations=__MODULE_LOG_NAME__)
    insightfaceAnalyser.prepare(**main_conf[1]["insightface"]["prepare"])


    p_info("insightface successfuly started.",locations=__MODULE_LOG_NAME__)


    return insightfaceAnalyser
