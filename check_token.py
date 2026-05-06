from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('HF_TOKEN')
print(f'Token loaded: {bool(token)}')
if token:
    print(f'First 20 chars: {token[:20]}')
    print('✅ Token is available')
else:
    print('❌ Token NOT loaded')
