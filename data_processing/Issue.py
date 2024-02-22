import datetime


def parse_date(date_str):
    if date_str and date_str.lower() != 'null':
        return datetime.datetime.strptime(date_str.replace("T", " ").replace("Z", "")[:19], "%Y-%m-%d %H:%M:%S")
    else:
        return None

class Issue:
    def __init__(self, info):
        self.issue_id = info[0]
        self.issue_type = info[1]
        self.fixed_date = parse_date(info[2])
        self.created_date = parse_date(info[5])
        self.first_commit_date = '2022-12-31 11:59:59'
        self.first_commit_hash = set()
        self.summary_stem = info[3]
        if info[4] is not None:
            self.description_stem = info[4]
        else:
            self.description_stem = ""
        self.tfidf = []
        self.files = [] # ground truth of file level
        self.artifacts = []
        self.artif_sim = []
        self.source_files = set() # file path of all source code at current version

        self.summary = ""
        self.description = ""

        self.cache_score = {}
        self.bluir_score = {}
        self.simi_score = {}
        self.amalgam = []
        self.amalgam_score = {}
        self.ablots = []
        self.ablots_score = {}

        self.predict_bf = []


