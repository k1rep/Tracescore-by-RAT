import os
import re
import sqlite3
import string

# preprocess summary and description
#  remove stopwords, lower case, remove punctuations, camel case splitting and stemming

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stopwords = stopwords.words('english')
def text_preprocessing(texts):
    result = []
    for text in texts:
        if text is None:
            result.append(None)
            continue
        text = text.replace("/", " ").replace("-", " ").replace(".", " ")
        remove = str.maketrans('', '', string.punctuation)
        text = text.translate(remove)  # remove punctuation
        splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', text)).split()
        text = [w.lower() for w in splitted]

        text = [w for w in text if not w in stopwords]  # remove stopwords
        s = nltk.stem.SnowballStemmer('english')
        text_list = [s.stem(ws) for ws in text]
        # print(text)
        text = " ".join(text_list)
        result.append(text)
    return result


path = "../data/tracescore"
# 1是RAT的结果，2是爬取的结果
#files = ["teiid2", "Weld2", "WildFlyCore2", "WildFlyElytron2", "WildFly2","Undertow2", "RestEasy2", "ModeShape2", "JGroups2", "JBossTransactionManager2", "infinispan2", "HAL2", "Debezium2"]
files = ["Wildfly2"]
for file in files[:]:
    print(file, end=" ")
    filePath = path+"/"+file + ".sqlite3"
    connection = sqlite3.connect(filePath)
    connection.text_factory = str
    cursor = connection.cursor()
    cursor.execute("select issue_id, summary_stemmed, description_stemmed from issue")
    result = cursor.fetchall()
    ids = [tmp[0] for tmp in result]
    summary = [tmp[1] for tmp in result]
    description = [tmp[2] for tmp in result]
    summary_stem = text_preprocessing(summary)
    description_stem = text_preprocessing(description)


    data = []
    for i in range(len(ids)):
        x = [summary_stem[i], description_stem[i], ids[i]]
        data.append(x)

    cursor = connection.cursor()
    # cursor.execute("alter table issue add column summary_stem text")
    # cursor.execute("alter table issue add column description_stem text")
    cursor.executemany("update issue set summary_stemmed = ?, description_stemmed = ? where issue_id = ?", data)
    connection.commit()
    cursor.close()
    connection.close()
    print()