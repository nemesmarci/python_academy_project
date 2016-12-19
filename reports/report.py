class Report(object):
    def __init__(self, user_count=0, document_count=0, user_count_by_roles=0, import_count=0, export_count=0):
        self.user_count = user_count
        self.document_count = document_count
        self.user_count_by_roles = user_count_by_roles
        self.import_count = import_count
        self.export_count = export_count
