ram: ("SIF"; enlist csv) 0: `:/mnt/c/git/sys_metric_pipeline/src/data/ram.csv

`:data/ram set ram

disk: ("SSFF"; enlist csv) 0: `:/mnt/c/git/sys_metric_pipeline/src/data/disk.csv

`:data/disk set disk

cpu: ("SISFF"; enlist csv) 0: `:/mnt/c/git/sys_metric_pipeline/src/data/cpu.csv

`:data/cpu set cpu

-1 "Data successfully loaded into tables and saved.";