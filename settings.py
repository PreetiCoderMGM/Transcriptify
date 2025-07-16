from logger_util import get_logger

log = get_logger(__name__)

APP_NAME = "transcriptify"
SECRET_KEY = "88726fd2b17ab8f0cb2dbghb1901bfaefe63800518a9d069"
FLASK_SERVER_PORT: int = 8000
UPLOAD_FOLDER = "/log"
DB_BASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/"
DB_NAME: str = "transcriptify"
ENV: str = "local"
VIDEO_MEDIA_TYPE: [str] = ["mp4"]
AUDIO_MEDIA_TYPE: [str] = ["mp3"]
DEEPGRAM_TOKEN: str = ""
MEDIA_CACHE_SEC: int = 3600
SYS_SECRET_KEY = b'Stfbwg52_XCI7C1YyTr--7JdQ5LY49Q92yQCo2fK5kg='
SUPPORTED_MEDIA_TYPE = VIDEO_MEDIA_TYPE + AUDIO_MEDIA_TYPE
# OPENAI_API_KEY: str = config['OPENAI_API_KEY']
# GEMINI_API_KEY: str = config['GEMINI_API_KEY']
# MONGO_URL = config['MONGO_URL']
# MONGO_DB_NAME = config['MONGO_DB_NAME']
# MONGO_PORT: int = 27017

log.info(f'{ENV} Setting loaded.')
