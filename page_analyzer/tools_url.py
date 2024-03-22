from validators import url
from urllib.parse import urlparse


def validate_url(urls):
    errors = []
    domen = urlparse(urls).netloc
    if len(domen) > 250:
        errors.append("Домен должен быть не более 250 символов.")
    if urls:
        is_urls = url(urls)
    else:
        errors.append(("URL не обнаружен", "danger"))
    if not is_urls:
        errors.append(("URL некорректен", "danger"))
    return errors


def normalize_url(url):
    url = urlparse(url)
    return f"{url.scheme}://{url.netloc}"
