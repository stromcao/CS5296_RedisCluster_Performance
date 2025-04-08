#!/bin/bash
# 预先存储 400000 个数据到 Redis 主节点
NUM=400000
MASTER_IP="34.228.155.62"  # 替换为你的主节点IP
for i in $(seq 1 $NUM); do
    redis-cli -h $MASTER_IP SET key$i "value$i"
done
echo "已存储 $NUM 个键值对。"
