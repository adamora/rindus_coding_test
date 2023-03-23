import abc


class CommentInterface(abc.ABC):
    def __init__(self, raw_data) -> None:
        assert raw_data, '"raw_data" required'
        self.raw_data = raw_data

    @property
    @abc.abstractmethod
    def id(self):
        pass

    @property
    @abc.abstractmethod
    def post_id(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @property
    @abc.abstractmethod
    def email(self):
        pass

    @property
    @abc.abstractmethod
    def body(self):
        pass

    def get_data_as_dict(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "name": self.name,
            "email": self.email,
            "body": self.body,
        }
