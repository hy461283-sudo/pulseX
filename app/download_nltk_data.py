import ssl
import nltk

# Bypass SSL certificate verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
print("NLTK data downloaded successfully!")
