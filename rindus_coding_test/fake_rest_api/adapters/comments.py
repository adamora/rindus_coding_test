from rindus_coding_test.core.interfaces.comments import CommentInterface


class CommentJsonAdapter(CommentInterface):
    """Comment representation bsed on Fake API Comment object"""

    @property
    def id(self):
        return self.raw_data["id"]

    @property
    def post_id(self):
        return self.raw_data["postId"]

    @property
    def name(self):
        return self.raw_data["name"]

    @property
    def email(self):
        return self.raw_data["email"]

    @property
    def body(self):
        return self.raw_data["body"]
