import abc

from rindus_coding_test.core.interfaces.comments import CommentInterface
from rindus_coding_test.core.interfaces.posts import PostInterface


class InteractionsInterface(abc.ABC):
    """This interface allow us to adapt operations from different sources"""

    @abc.abstractmethod
    def get_posts(self) -> list[PostInterface]:
        pass

    @abc.abstractmethod
    def get_post(self, post_id: int) -> PostInterface:
        pass

    @abc.abstractmethod
    def create_post(self, post: PostInterface) -> PostInterface:
        pass

    @abc.abstractmethod
    def update_post(self, post: PostInterface, partial=False) -> PostInterface:
        pass

    @abc.abstractmethod
    def get_comments(self) -> list[CommentInterface]:
        pass

    @abc.abstractmethod
    def get_comment(self, comment_id: int) -> CommentInterface:
        pass

    @abc.abstractmethod
    def create_comment(self, comment: CommentInterface) -> CommentInterface:
        pass

    @abc.abstractmethod
    def update_comment(
        self, comment: CommentInterface, partial=False
    ) -> CommentInterface:
        pass
