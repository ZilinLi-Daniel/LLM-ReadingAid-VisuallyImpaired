class News:
    def __init__(self, id=None, title=None, time=None, url=None, abstract=None, kind=None, content=None):
        self.id = id
        self.title = title
        self.time = time
        self.url = url
        self.abstract = abstract
        self.kind = kind
        self.content = content

    def __str__(self):
        return f"News(id={self.id}, title='{self.title}', time='{self.time}', url='{self.url}', description='{self.abstract}', kind='{self.kind}', content='{self.content}')"
