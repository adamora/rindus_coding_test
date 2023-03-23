from rindus_coding_test.core.interfaces.posts import PostInterface


class PostJsonAdapter(PostInterface):
    """Post representation bsed on Fake API Post object"""

    @property
    def id(self):
        return self.raw_data["id"]

    @property
    def user_id(self):
        return self.raw_data["userId"]

    @property
    def title(self):
        return self.raw_data["title"]

    @property
    def body(self):
        return self.raw_data["body"]
