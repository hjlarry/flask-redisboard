from collections import OrderedDict


GENERAL_CONFIG_ITEM = OrderedDict(
    {
        "pidfile": {"des": "abbss", "can_edit": True},
        "logfile": {"des": "abbss", "can_edit": True},
        "loglevel": {"des": "abbss", "can_edit": True},
        "databases": {"des": "abbss", "can_edit": True},
        "daemonize": {"des": "abbss", "can_edit": True},
        "supervised": {"des": "abbss", "can_edit": True},
        "syslog-facility": {"des": "abbss", "can_edit": True},
    }
)

NETWORK_CONFIG_ITEM = OrderedDict(
    {
        "unixsocket": {"des": "abbss", "can_edit": True},
        "timeout": {"des": "abbss", "can_edit": True},
        "port": {"des": "abbss", "can_edit": True},
        "tcp-backlog": {"des": "abbss", "can_edit": True},
        "tcp-keepalive": {"des": "abbss", "can_edit": True},
        "protected-mode": {"des": "abbss", "can_edit": True},
        "unixsocketperm ": {"des": "abbss", "can_edit": True},
        "bind ": {"des": "abbss", "can_edit": True},
    }
)
"""

SNAPSHOTTING
dbfilename 
dump.rdb
stop-writes-on-bgsave-error 
yes
rdbcompression 
yes
rdbchecksum 
yes
dir 
/Users/hejl
save 
3600 1 300 100 60 10000
REPLICATION
masterauth 
-
slave-announce-ip 
-
repl-ping-slave-period 
10
repl-timeout 
60
repl-backlog-size 
1048576
repl-backlog-ttl 
3600
slave-priority 
100
slave-announce-port 
0
min-slaves-to-write 
0
min-slaves-max-lag 
10
repl-diskless-sync-delay 
5
slave-serve-stale-data 
yes
slave-read-only 
yes
repl-disable-tcp-nodelay 
no
repl-diskless-sync 
no
slaveof 
-
SECURITY
requirepass 
-
CLIENTS
maxclients 
10000
MEMORY MANAGEMENT
maxmemory 
0
maxmemory-samples 
5
maxmemory-policy 
noeviction
LAZY FREEING
lazyfree-lazy-eviction 
no
lazyfree-lazy-expire 
no
lazyfree-lazy-server-del 
no
slave-lazy-flush 
no
APPEND ONLY MODE
auto-aof-rewrite-percentage 
100
auto-aof-rewrite-min-size 
67108864
no-appendfsync-on-rewrite 
no
aof-load-truncated 
yes
aof-use-rdb-preamble 
no
appendfsync 
everysec
appendonly 
no
LUA SCRIPTING
lua-time-limit 
5000
REDIS CLUSTER
cluster-node-timeout 
15000
cluster-migration-barrier 
1
cluster-slave-validity-factor 
10
cluster-require-full-coverage 
yes
CLUSTER DOCKER/NAT
cluster-announce-ip 
-
cluster-announce-port 
0
cluster-announce-bus-port 
0
SLOWLOG
slowlog-log-slower-than 
10000
slowlog-max-len 
128
LATENCY MONITOR
latency-monitor-threshold 
0
EVENT NOTIFICATION
notify-keyspace-events 
-
DEFRAGMENTATION
active-defrag-threshold-lower 
10
active-defrag-threshold-upper 
100
active-defrag-ignore-bytes 
104857600
active-defrag-cycle-min 
25
active-defrag-cycle-max 
75
activedefrag 
no
ADVANCED CONFIG
hash-max-ziplist-entries 
512
hash-max-ziplist-value 
64
list-max-ziplist-size 
-2
list-compress-depth 
0
set-max-intset-entries 
512
zset-max-ziplist-entries 
128
zset-max-ziplist-value 
64
hll-sparse-max-bytes 
3000
hz 
10
activerehashing 
yes
aof-rewrite-incremental-fsync 
yes
client-output-buffer-limit
"""
