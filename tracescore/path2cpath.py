import sqlite3

def path2cpath(path):
    new_path = path[::-1].replace('2', '1', 1)[::-1]
    conn = sqlite3.connect(new_path)
    cur = conn.cursor()
    cur.execute(""" select * from Mapping; """)
    cpath_2_id = {it[0]: it[1] for it in cur.fetchall()}
    cur.close()
    conn.close()
    # cpath_2_id['org.teiid.translator.parquet']

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute(""" select file_path from code_change; """)
    abs_path = cur.fetchall()
    cur.close()
    conn.close()

    # 获取 path_2_id 的字典
    path_2_cpath = {}
    New_id = 10 ** 7  # 如果没有的话，给新的 id
    for single_file_name_tuple in sorted(list(set(abs_path))):
        single_file_name = single_file_name_tuple[0]
        for class_path in cpath_2_id.keys():
            if len(class_path) < 5:
                continue

            if single_file_name.replace('/', '.').replace('.java', '').endswith(class_path):
                if path_2_cpath.get(single_file_name) is not None:
                    path_2_cpath[single_file_name]['path_count'] += 1
                else:
                    path_2_cpath[single_file_name] = {
                        'class_name': class_path,
                        'path_id': cpath_2_id[class_path],
                        'path_count': 1,
                    }

        if path_2_cpath.get(single_file_name) is None:
            New_id += 1
            path_2_cpath[single_file_name] = {
                'class_name': 'None',
                'path_id': New_id,
                'path_count': 1,
            }

    return path_2_cpath
    # print(path_2_cpath)