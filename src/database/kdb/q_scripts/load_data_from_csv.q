ram: ("SIF"; enlist csv) 0: `:/mnt/c/git/sys_metric_pipeline/src/data/ram.csv

`:/mnt/c/git/sys_metric_pipeline/src/database/kdb/q_tables/ram set ram

disk: ("SSFF"; enlist csv) 0: `:/mnt/c/git/sys_metric_pipeline/src/data/disk.csv

`:/mnt/c/git/sys_metric_pipeline/src/database/kdb/q_tables/disk set disk

cpu: ("SISFF"; enlist csv) 0: `:/mnt/c/git/sys_metric_pipeline/src/data/cpu.csv

`:/mnt/c/git/sys_metric_pipeline/src/database/kdb/q_tables/cpu set cpu

-1 "Data successfully loaded into tables and saved.";