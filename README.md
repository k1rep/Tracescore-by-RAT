# tracescore-replication-package

This repository contains the source code that we used to perform the experiment in the paper titled "Is ABLoTS Replicable and Generalizable for Bug Localization? A Replication Study". And we replicate the work of using the results of RAT model(https://github.com/feifeiniu-se/RAT) into tracescore.

Please follow the steps below to reproduce the result.

## Dataset

The following projects are all open source and can be obtained from github as code repositories. In our work, we use `xxx1.sqlite3` to represent the output of the RAT model and `xxx2.sqlite3` to represent the issue and other relevant information obtained from Jira.

| Project                 | Abb. | Time Span             |
| ----------------------- | ---- | --------------------- |
| JBossTransactionManager | JT   | 2012-08-20~2023-01-09 |
| WildFlyCore             | WC   | 2012-03-24~2023-07-11 |
| Debezium                | DE   | 2016-03-02~2022-05-06 |
| Weld                    | WE   | 2011-11-09~2015-04-13 |
| Undertow                | UN   | 2013-04-09~2023-06-08 |
| Teiid                   | TE   | 2012-10-10~2018-03-20 |
| Wildfly                 | WI   | 2011-10-11~2023-05-31 |
| ModeShape               | MO   | 2009-08-04~2017-04-14 |
| Infinispan              | IN   | 2011-05-09~2020-10-03 |
| WildFlyElytron          | WL   | 2014-08-13~2023-06-06 |
| HAL                     | HA   | 2016-07-07~2022-02-22 |
| JGroups                 | JG   | 2011-03-20~2023-06-29 |
| RESTEasy                | RE   | 2012-05-11~2023-06-08 |

## Environment Requirements

Python  >= 3.7

## Experiment Result Replication Guide

```sh
python ./tracescore/stopword.py #remove the stopword in the issue table of xxx2.sqlite3
# then you can run the following py file to obtain tracescore result
python ./tracescore/tracescore.py
```

