from Utils.Functions.url_utils import extract_place_name_from_url
from Infrastructure.Logging.logger import logger

raw_urls = [
    "https://www.google.com/maps/place/Domino's+Pizza/@38.8718568,-77.0768663,14z/data=!4m15!1m8!3m7!1s0x89b7b6ba2b02a023:0x15622e1516edc315!2sDomino's+Pizza!8m2!3d38.8627267!4d-77.0853943!10e2!16s%2Fg%2F1wbryp46!3m5!1s0x89b7b6ba2b02a023:0x15622e1516edc315!8m2!3d38.8627267!4d-77.0853943!16s%2Fg%2F1wbryp46?entry=ttu&g_ep=EgoyMDI1MDcyOS4wIKXMDSoASAFQAw%3D%3D",
    "https://www.google.com/maps/place/Papa+Johns+Pizza/@38.8606821,-77.130336,14z/data=!4m10!1m2!2m1!1spapa+johns+arlington!3m6!1s0x89b7b77f69c14da3:0xa3bad34a334f286f!8m2!3d38.8606821!4d-77.0922272!15sChRwYXBhIGpvaG5zIGFybGluZ3RvbiIDiAEBWhYiFHBhcGEgam9obnMgYXJsaW5ndG9ukgEQcGl6emFfcmVzdGF1cmFudKoBZwoNL2cvMTFjM3B0enB5aAoJL20vMDIwdHZtEAEqDiIKcGFwYSBqb2hucygAMh8QASIbL0F8561TCpgCrl_XvHRjzEodc_TqcxCD4TpEMhgQAiIUcGFwYSBqb2hucyBhcmxpbmd0b27gAQA!16s%2Fg%2F11t104lmtl?entry=ttu&g_ep=EgoyMDI1MDcwOS4wIKXMDSoASAFQAw%3D%3D",
    "https://www.google.com/maps/place/We,+The+Pizza/@38.8569522,-77.0876405,13.25z/data=!3m1!5s0x89b7b72f331803b7:0x7edf0a3adffa41c8!4m10!1m2!2m1!1sWe+the+Pizza+arlington!3m6!1s0x89b7b72f38e95a4b:0xc933eda7e98cbcb0!8m2!3d38.8551791!4d-77.049733!15sChZXZSB0aGUgUGl6emEgYXJsaW5ndG9uIgOIAQFaGCIWd2UgdGhlIHBpenphIGFybGluZ3RvbpIBEHBpenphX3Jlc3RhdXJhbnSqAX0KDS9nLzExYmM4Y2hqNGcKDS9nLzExaDhkNXdwNG4KDC9nLzFxNjJnNjZ2ZhABKhAiDHdlIHRoZSBwaXp6YSgAMh8QASIbh6sl9JvydA-N0Q_x_7Ny0gaLcmOvymT7j1KDMhoQAiIWd2UgdGhlIHBpenphIGFybGluZ3RvbuABAA!16s%2Fg%2F1q62g66vf?entry=ttu&g_ep=EgoyMDI1MDcwOS4wIKXMDSoASAFQAw%3D%3D",
    "https://www.google.com/maps/place/District+Pizza+Palace/@38.8527414,-77.0557157,17z/data=!3m1!4b1!4m6!3m5!1s0x89b7b77b2d1e64e3:0x70a3f6ac71ef0a9c!8m2!3d38.8527414!4d-77.0531408!16s%2Fg%2F11vc1fb80v?entry=ttu&g_ep=EgoyMDI1MDcyOS4wIKXMDSoASAFQAw%3D%3D",
    "https://www.google.com/maps/place/Extreme+Pizza/@38.8527341,-77.0943405,13z/data=!4m10!1m2!2m1!1sextreme+pizza!3m6!1s0x89b7b72778ab8871:0x3762c646ac6ddfe1!8m2!3d38.8602396!4d-77.0559854!15sCg1leHRyZW1lIHBpenphIgOIAQFaDyINZXh0cmVtZSBwaXp6YZIBEHBpenphX3Jlc3RhdXJhbnSqAWMKDS9nLzExYjdja3A1aHEKCi9tLzAyN3B5a18QASoRIg1leHRyZW1lIHBpenphKAAyHhABIhoOHwx7xhPORo2l7O-OL2JrFSNB4q5fdVwlWTIREAIiDWV4dHJlbWUgcGl6emHgAQA!16s%2Fg%2F12llsn19l?entry=ttu&g_ep=EgoyMDI1MDcwOS4wIKXMDSoASAFQAw%3D%3D",
    "https://www.google.com/maps/place/Pizza+Hut/@38.8430983,-77.1525032,13z/data=!4m10!1m2!2m1!1spizza+hut+arlington!3m6!1s0x89b7b11d7089bb7b:0x20fc75365f2ab2ab!8m2!3d38.8430983!4d-77.0762855!15sChNwaXp6YSBodXQgYXJsaW5ndG9uIgOIAQFaFSITcGl6emEgaHV0IGFybGluZ3RvbpIBFnBpenphX2RlbGl2ZXJ5X3NlcnZpY2WqAWMKDC9nLzExaDEwOWdjMQoIL20vMDljZnEQASoNIglwaXp6YSBodXQoADIfEAEiGw0LRaXc2G14SQlsm2Ulubdth41j4E1Y_2EqVDIXEAIiE3BpenphIGh1dCBhcmxpbmd0b27gAQA!16s%2Fg%2F1tfkrnnp?entry=ttu&g_ep=EgoyMDI1MDcwOS4wIKXMDSoASAFQAw%3D%3D"
]

if len(raw_urls) < 2:
    logger.error("📛 נראה שרק URL אחד נמצא ברשימה – ודא שהוספת פסיקים בין הקישורים ברשימה.")
    raise ValueError("📛 נראה שרק URL אחד נמצא ברשימה – ודא שהוספת פסיקים בין הקישורים ברשימה.")

LOCATIONS = [{"url": url, "name": extract_place_name_from_url(url)} for url in raw_urls]