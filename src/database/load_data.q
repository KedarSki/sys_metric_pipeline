// Function to load data safely
loadData:{[file; types]
  // Construct full path
  fullPath: hsym `$":/mnt/c/Git/sys_metric_pipeline/src/data/", file;
  
  // Check if file exists
  if[not .Q.fps[fullPath];
    -1 "File does not exist: ", string[file];
    :()];
  
  // Attempt to load data
  @[ {0: types x} ; fullPath; {err -1 "Error loading file: ", x; ()}]
 };

// Load each table with appropriate data types
cpu: loadData["CPU.csv", ("S"; "I"; "S"; "F"; "F")]; // Same as before
ram: loadData["RAM.csv", ("S"; "I"; "F")]; // Symbol, Integer, Float
disc: loadData["DISC.csv", ("S"; "S"; "F"; "F")]; // Symbol, Symbol, Float, Float
