# Distributed Memory Priority Queue for Query Processing in Large Language Models

# Description
Designed a distributed memory system to enhance query response times for LLMs, reducing reliance on slow disk operations.
System architecture comprises of 3 slaves maintaining independent query queues, and 1 master distributing incoming queries.
Used a linear regression model to predict query execution times, enabling the master server to select and send the top queries to the GPT-2 server for processing and response generation.

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



