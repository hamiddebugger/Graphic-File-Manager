class SearchManager:
    def search_by_name(self, files, query):
        return [file for file in files if query.lower() in file.lower()]

    def search_by_tag(self, tags, query):
        return [file for file, tag_list in tags.items() if query.lower() in tag_list]