import sys
sys.path.append("..") # 模块父目录下的model文件中

import sqlite3
import os

from data_processing.database import read_tracescore, insert_database_tracescore
from sklearn.metrics.pairwise import cosine_similarity

from BF import BF
# from tracescore.BF import BF


def calculate(issues, filePath):
    bugReport = [x for x in issues if x.issue_type == "Bug"]
    bugReport.sort(key=lambda x: x.created_date, reverse=False)
    print(len(bugReport), end=";")
    train_size = int(len(bugReport) * 0.5)
    test_bugs = bugReport[train_size:]

    for i in range(len(test_bugs)):
        issue = test_bugs[i]  # current issue
        index = issues.index(issue) #index of current issue
        # # artifact selection
        # within365 = [x for x in issues[:index] if (issue.created_date - x.fixed_date).days <= 365]

        within365 = [x for x in issues[:index] if  x.fixed_date is not None and issue.created_date is not None and (issue.created_date - x.fixed_date).days <= 365]
        # within365 = [x for x in issues[:index] if (issue.created_date - x.fixed_date).days <= 365 and issue.created_date>x.fixed_date]
        issue.artifacts = [x for x in within365 if (x.issue_type == "Bug" and len(set(f.new_filePath for f in x.files if f.new_filePath!="/dev/null" and f.new_filePath is not None)) <= 10) or (x.issue_type != "Bug" and len(set(f.new_filePath for f in x.files if f.new_filePath!="/dev/null" and f.new_filePath is not None)) <= 20)]
        issue.artif_sim = [cosine_similarity(issue.tfidf, x.tfidf) for x in issue.artifacts]
        issue.artif_sim = [float(x[0][0]) for x in issue.artif_sim]

    # read traceability information
    connection = sqlite3.connect(filePath)
    connection.text_factory = str
    cursor = connection.cursor()

    issue_mapping = {issue.issue_id:issue for issue in test_bugs}
    link_mapping = {} # issue_id, set()
    cursor.execute("select * from issue_link")
    result = cursor.fetchall()
    for tmp in result:
        if tmp[0] in link_mapping:
            link_mapping[tmp[0]].add(tmp[1])
        else:
            link_mapping[tmp[0]] = set()
            link_mapping[tmp[0]].add(tmp[1])
        if tmp[1] in link_mapping:
            link_mapping[tmp[1]].add(tmp[0])
        else:
            link_mapping[tmp[1]] = set()
            link_mapping[tmp[1]].add(tmp[0])
    for id, links in link_mapping.items():
        issue = issue_mapping.get(id)
        if issue is not None:
            for i in range(0, len(issue.artifacts)):
                if issue.artifacts[i].issue_id in links:
                    issue.artif_sim[i] = 1.0

    BF(test_bugs, filePath)#todo

    # insert_database_tracescore(filePath, test_bugs)


path = "../data/tracescore"
files = os.listdir(path)

files = ["teiid", "Weld", "infinispan", "Wildfly", "derby", "hornetq"]

print(";MAP;MRR;Top 1;Top 5;Top 10")
for file in files[:]:
    print(file, end=" ")
    filePath = path+"/"+file + ".sqlite3"
    issues = read_tracescore(filePath)
    calculate(issues, filePath)
