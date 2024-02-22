from evaluation.evaluation import evaluation
from path2cpath import path2cpath

def BF(test_bugs, filePath):
    file_id = path2cpath(filePath)
    # print(file_id)
    for issue in test_bugs:
        files = {}
        for i in range(len(issue.artifacts)-1, -1, -1):
            files_set = set(f.new_filePath for f in issue.artifacts[i].files if f.new_filePath!="/dev/null" and f.new_filePath is not None)
            source_len = len(files_set)
            for f in files_set:
                if (f in files.keys()):
                    files[f] = files[f] + issue.artif_sim[i] * issue.artif_sim[i] / source_len
                else:
                    files[f] = issue.artif_sim[i] * issue.artif_sim[i] / source_len

        issue.simi_score = files
        # 对于files中的每一个文件（绝对路径），找到对应的id，将id相同的分数相加
        # files的key是绝对路径，value是分数
        for(file_abs_name, score) in files.items():
            # 对于这个文件的绝对路径，找到对应的表示：
            # 如/hotrod/TestInfinispanUpdateUsingAllTypes.java':
            # {'class_name': 'org.teiid.translator.infinispan.hotrod.TestInfinispanUpdateUsingAllTypes',
            # 'path_id': 170098,
            # 'path_count': 1}
            refactoring_files = file_id.get(file_abs_name, {})
            if refactoring_files != {}:
                blockID = refactoring_files.get('path_id', 0)
                for file_abs_name2 in files.keys():
                    if file_id.get(file_abs_name2, {}).get('path_id', 0) == blockID:
                        files[file_abs_name] += files[file_abs_name2]

        sorted_files = sorted(files.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        issue.predict_bf = [x[0] for x in sorted_files]
        # issue.predict_bf = [x[0] for x in sorted_files if x[0] in issue.source_files]

    # evaluation
    ground_truth = [set(f.new_filePath for f in issue.files if f.new_filePath!="/dev/null" and f.new_filePath is not None) for issue in test_bugs]
    predict_result = [issue.predict_bf for issue in test_bugs]

    # for i, (gt, pr) in enumerate(zip(ground_truth, predict_result)):
    #     print(f"Test Case {i + 1}:")
    #     print("  Ground Truth: ", gt if gt else "Empty Set")
    #     print("  Predicted Result: ", pr if pr else "Empty Set")
    #     print()

    evaluation(ground_truth, predict_result)