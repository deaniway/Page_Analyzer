from bs4 import BeautifulSoup


class HTMLParser:

    def __init__(self, html):

        self.soup = BeautifulSoup(html, 'html.parser')

    def get_title(self):

        """Получает заголовок (title) веб-страницы."""

        title_tag = self.soup.title
        return title_tag.string if title_tag else None

    def get_h1(self):

        """Получает первый заголовок (h1) веб-страницы."""

        h1_tag = self.soup.h1
        return h1_tag.string if h1_tag else None

    def get_content(self):

        """Получает содержимое метатега 'description' веб-страницы."""
        for meta in self.soup.find_all('meta'):
            if meta.get('name') == 'description':
                content = meta.get('content')
                return content[:255]
        return None

    def get_page_data(self):

        """Общий результат."""
        result = {
            'title': self.get_title(),
            'h1': self.get_h1(),
            'content': self.get_content()
        }
        return result
