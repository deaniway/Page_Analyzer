from urllib.parse import urlparse
from validators import url as validate


def normalize_url(url):
    """
    Нормализация URL.
    """
    parse_url = urlparse(url)
    return f'{parse_url.scheme}://{parse_url.netloc}'


def validate_url(input_url):
    if not input_url:
        return 'URL обязателен для заполнения'
    if not validate(input_url):
        return 'Некорректный URL'
    if len(input_url) > 255:
        return 'Введенный URL превышает длину в 255 символов'
