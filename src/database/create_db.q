cpu:("SSSFF";enlist ",") 0: `:/mnt/c/Git/sys_metric_pipeline/src/data/CPU.csv
disc:("SSFFF";enlist ",") 0: `:/mnt/c/Git/sys_metric_pipeline/src/data/DISC.csv
ram:("SIF";enlist ",") 0: `:/mnt/c/Git/sys_metric_pipeline/src/data/RAM.csv

`:/mnt/c/Git/sys_metric_pipeline/src/data/CPU.csv set cpu
`:/mnt/c/Git/sys_metric_pipeline/src/data/DISC.csv set disc
`:/mnt/c/Git/sys_metric_pipeline/src/data/RAM.csv set ram

cpu: get ``:/mnt/c/Git/sys_metric_pipeline/src/database/cpu
disc: get `:/mnt/c/Git/sys_metric_pipeline/src/database/disk
ram: get ``:/mnt/c/Git/sys_metric_pipeline/src/database/ram