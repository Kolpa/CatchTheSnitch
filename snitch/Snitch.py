import os
from random import randrange
from praw import Reddit


class Snitch:
    def __init__(self, username, passwd, url, subreddit):
        self.rh = Reddit('Release the Snitch v 0.1 by Kolpa')
        self.rh.login(username, passwd)

        self.css = self.__load_css()
        self.desc = self.__load_desc()

        self.url = url
        self.subreddit = subreddit

    def __load_css(self):
        with open('raw.css', 'r') as f:
            return f.read()

    def __load_desc(self):
        with open('descripiton.txt', 'r') as f:
            return f.read()

    def __get_last_id(self):
        with open('current', 'r') as f:
            return f.read()

    def __set_new_id(self):
        id = randrange(0, 999999)
        with open('current', 'w') as f:
            f.write(str(id))
        return id

    def _get_random_pos(self):
        return randrange(0, 100, 10), randrange(0, 100, 10)

    def __update_desc(self, desc):
        self.rh.update_settings(self.rh.get_subreddit(self.subreddit), description=desc)

    def can_move(self, id):
        if not os.path.exists('current'):
            return True
        return id == self.__get_last_id()

    def move(self, id):
        try:
            if self.can_move(id):
                new_id = self.__set_new_id()
                desc = self.desc.format(new_id)

                x, y = self._get_random_pos()
                css = self.css.format(x, y, self.url)

                self.rh.set_stylesheet(self.subreddit, css)
                self.__update_desc(desc)
                return True
        except Exception:
            return False