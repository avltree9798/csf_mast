import os

PLATFORM_EXTENSION = {
    'ipa': 'ios',
    'apk': 'android'
}
JADX_PATH = os.environ.get('JADX_PATH', '/opt/jadx/bin/jadx')
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = int(os.environ.get('DB_PORT', '1491'))
DB_PASS = os.environ.get('DB_PASS', 'SecretPassword')
DB_MAX_CONNECTION = int(os.environ.get('DB_MAX_CONNECTION', '100'))
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_WORKER = int(os.environ.get('MAX_WORKER', 200))
