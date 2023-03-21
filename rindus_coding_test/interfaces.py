import abc


class InteractionsInterface(abc.ABC):

    @abc.abstractmethod
    def get_posts(self):
        pass

    @abc.abstractmethod
    def get_comments(self):
        pass


