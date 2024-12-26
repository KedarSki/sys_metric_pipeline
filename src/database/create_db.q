// Define the database path for kdb+
sys_metric_pipeline: `:/mnt/c/git/sys_metric_pipeline/src/database/sys_metric_pipeline

// Convert to shell-compatible path by removing the leading colon
shellPath: string 1_ sys_metric_pipeline

// Attempt to create the database directory
show `$"Attempting to create directory: {shellPath}";
if[not "directory" in system "test -d ", shellPath;
    system "mkdir -p ", shellPath;  // Use system command for directory creation
    show `$"Directory successfully created: {shellPath}";
    ];

// Check the directory contents
dirContents: system "ls ", shellPath
show `$"Directory contents after creation: {dirContents}";

// Define and save the RAM table
ram:([] instance_id: `symbol$(); ram_usage: `int$(); date: `timestamp$())
sys_metric_pipeline,`ram set ram
show `$"RAM table saved to {string sys_metric_pipeline}/ram";

// Define and save the Disk table
disk:([] instance_id: `symbol$(); device: `symbol$(); disc_usage: `float$(); date: `timestamp$())
sys_metric_pipeline,`disk set disk
show `$"Disk table saved to {string sys_metric_pipeline}/disk";

// Define and save the CPU table
cpu:([] instance_id: `symbol$(); cpu: `int$(); mode: `symbol$(); time_of_usage: `float$(); date: `timestamp$())
sys_metric_pipeline,`cpu set cpu
show `$"CPU table saved to {string sys_metric_pipeline}/cpu";
