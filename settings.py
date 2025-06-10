from logger_util import get_logger

log = get_logger(__name__)

APP_NAME = "transcriptify"
SECRET_KEY = ""
FLASK_SERVER_PORT: int = 8000
UPLOAD_FOLDER = "/log"
# MONGO_URL = config['MONGO_URL']
# MONGO_DB_NAME = config['MONGO_DB_NAME']
# MONGO_PORT: int = 27017
DB_BASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/"
DB_NAME: str = "transcriptify"
ENV: str = "local"
VIDEO_MEDIA_TYPE: [str] = ["mp4"]
AUDIO_MEDIA_TYPE: [str] = ["mp3"]
DEEPGRAM_TOKEN: str = ""
# OPENAI_API_KEY: str = config['OPENAI_API_KEY']
# GEMINI_API_KEY: str = config['GEMINI_API_KEY']


log.info(f'{ENV} Setting loaded.')
