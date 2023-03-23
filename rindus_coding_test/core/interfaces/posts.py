import abc


class PostInterface(abc.ABC):
    def __init__(self, raw_data) -> None:
        assert raw_data, '"raw_data" required'
        self.raw_data = raw_data

    @property
    @abc.abstractmethod
    def id(self):
        pass

    @property
    @abc.abstractmethod
    def user_id(self):
        pass

    @property
    @abc.abstractmethod
    def title(self):
        pass

    @property
    @abc.abstractmethod
    def body(self):
        pass

    def get_data_as_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "body": self.body,
        }
