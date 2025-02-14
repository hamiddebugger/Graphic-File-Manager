class TagsManager:
    def __init__(self):
        self.tags = {}

    def add_tag(self, file_path, tag):
        if file_path not in self.tags:
            self.tags[file_path] = []
        self.tags[file_path].append(tag)

    def get_tags(self, file_path):
        return self.tags.get(file_path, [])