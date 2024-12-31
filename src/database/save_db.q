savePath: ":/mnt/c/Git/sys_metric_pipeline/src/database/db/";

`:$(savePath, "cpu") set cpu;
`:$(savePath, "disc") set disc;
`:$(savePath, "ram") set ram;

// Verify the tables are saved
-1 "Tables saved at ", savePath;