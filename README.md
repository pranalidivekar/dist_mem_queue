# Installation

Run `./bin/install.sh` script to create the conda env with the requierements. It will create a conda env called `dist_mem_queue`.

# Run
Run the following commands:
```
conda activate dist_mem_queue
./bin/start_servers.sh
```
This will start 1 master server, 3 slave servers and 1 language model server

# Small test
`./bin/run_test_queries.sh` will run a simple test using a dummy set of queries and with 4 workers



