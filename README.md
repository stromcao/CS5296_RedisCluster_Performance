# CS5296_RedisCluster_Performance

This project is used for the course replication of CS5296 Cloud Computing.This project aims to explore Redis cluster performance and is divided into three experiments. Before reproducing the experiments, some preparations are needed. Resources need to be requested on the AWS platform, using Amazon EC2 instances as the carrier.
The preparation workflow is as follows: 
1. Configure one Master node and three Slave nodes. t2.medium should be chosen for the Master node, and t2.micro, t2.medium, t2.large should be used for the three Slave nodes. 
2. After the creation of the four servers are completed, the following commands should be used for all four servers.
   
sudo apt update 
sudo apt install redis-server -y 
sudo apt install python3 python3-pip -y 

2.1 Configure the Master node by editing redis.conf, replica-announce, replica-conf, and replica-announce. conf, 

replica-announce-ip [ip_address of Master] 
 
sudo systemctl restart redis-server 
systemctl daemon-reload 

2.2 Configure Slave node, edit redis. conf, 

replicaof [ip_address of Master] 

sudo systemctl restart redis-server # reload Redis service

2.3 Master node to view cluster information 

redis-cli info replication 

3. After the success, enter the data To prepare for the replication, use the populate_redis.sh script on the Master node, which has been uploaded to github 

#Change permissions before use 
chmod +x populate_redis.sh 
#Execute the script 
. /populate_redis.sh

After completing the preparations, we can start our experiments.
For Experiment I, the Master node now needs to add the script write_sync.sh, and the rest of the Slave nodes need to add the script check_sync.sh. After the additions are complete, all Slave nodes will run the script check_sync.sh first, and then the Master node will run the script write_sync.sh. Note the following the order of execution. At this point, all Slave nodes will show the delay of this data synchronization.

Experiment II, the operation process is similar to Experiment I. You need to pay attention to the registered geographic location of the Amazon EC2 instance, and you need to modify the constituency first. the Master node and Slave1 node are arranged in us-east-1, and the Slave2 and Slave3 nodes are arranged in us-west-1, and then you execute the process of Experiment I, and you can get different results.

Experiment III, is divided into two parts, the first part prepares a three-node Redis cluster and the second part prepares a four-node Redis cluster. In addition to this a Client, a proxy layer is needed. So a total of 6 EC2 instances.
The proxy layer starts by executing the following commands, 
#Install Twemproxy 
sudo apt-get update 
sudo apt-get install nutcracker 

#Configure nutcracker files 
vim /etc/nutcracker.yml 
vim /etc/nutcracker/ nutcracker.yml 

#Enter the following in these two yml files 
redis_cluster: 
 listen: 0.0.0.0:22121 # IP and port the proxy listens on (for client connections) 
 hash: fnv1a_64 
 distribution: ketama 
 timeout: 400
  redis: true 
 auto_eject_hosts: true 
 server_retry_timeout. 30000 
 server_failure_limit: 3 
 servers.
    - Master_Node_IP:6379:1 
 - Slave1_Node_IP:6379:1 
 - Slave2_Node_IP:6379:1 
 - Slave3_Node_IP:6379:1 

#Restart Twemproxy proxy 
nutcracker -c /etc/ nutcracker.yml -d 
sudo ufw allow 22121/tcp 
sudo chown -R nutcracker:nutcracker /var/log/nutcracker 
sudo chmod 755 /var/log/nutcracker 

#Check if the proxy is on 
ps aux | grep nutcracker 

#At this point, the agent layer has been configured, and all Redis cluster nodes execute the following command 
apt install moreutils 
redis-cli MONITOR | ts '%Y-%m-%d %H:%M:%.S' > monitor.log 
redis-cli MONITOR | ts '%Y-%m-%d %H:%M:%.S' > monitor.log 
redis-cli MONITOR | ts '%Y-%m-%d %H:%M:%.S' > monitor.log 

#Execute each of the following commands on the new client 
#Client running concurrency tests 
redis- benchmark -h [Twemproxy_IP] -p 22121 -t get -n 10000 -c 50 
redis-benchmark -h [Twemproxy_IP] -p 22121 -t get -n 50000 -c 50 
redis-benchmark -h [Twemproxy_IP] -p 22121 -t get -n 50000 -c 50 redis-benchmark -h [Twemproxy_IP] -p 22121 -t get -n 50000 -c 50 IP] -p 22121 -t get -n 100000 -c 50 

#After execution is complete, stop the Redis nodes from writing commands and analyze them using the python script 
#Each node needs to be analyzed 
. /analyze.py monitor.log
