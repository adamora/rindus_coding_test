from rindus_coding_test.core.interfaces.comments import CommentInterface


class CommentInstanceAdapter(CommentInterface):
    """Comment representation bsed on Comment DB instances"""

    @property
    def id(self):
        return self.raw_data.id

    @property
    def post_id(self):
        return self.raw_data.post.id

    @property
    def name(self):
        return self.raw_data.name

    @property
    def email(self):
        return self.raw_data.email

    @property
    def body(self):
        return self.raw_data.body
