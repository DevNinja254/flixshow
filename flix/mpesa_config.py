from datetime import datetime
import base64
from .access_token import generate_access_token

TIMESTAMP = datetime.now().strftime('%Y%m%d%H%M%S')
CONSUMER_KEY = "xrpPE7GeOlGz4A9jz5lmlevNkWfA6aUqGvbmqRMiiNKoLeOM"
CONSUMER_SECRET = "jUiqUHfMlGQGvWheUgQ5XNfD2dNvO5Rphe1K631HsG0IiypPIg64eJxphjVMmREm"
PASS_KEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
SHORT_CODE = "174379"
STK_PASSWORD = base64.b64encode((SHORT_CODE + PASS_KEY + TIMESTAMP).encode()).decode()
# TOKEN= generate_access_token(CONSUMER_KEY, CONSUMER_SECRET)
# HEADERS = {
#     'Authorization': 'Bearer ' + TOKEN,
#     'Content-Type': 'application/json'
# }