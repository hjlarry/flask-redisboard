from collections import OrderedDict

BADGE_CLASS = {
    "string": "badge-info",
    "list": "badge-success",
    "set": "badge-warning",
    "hash": "badge-dark",
    "zset": "badge-light",
}

INFO_GROUPS = [
    "Server",
    "Clients",
    "Memory",
    "Persistence",
    "Stats",
    "Replication",
    "Cpu",
    "Cluster",
]

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

logfile_desc = "You can specify the log file name.An empty string can be used to force Redis to log on the standard output. Note that if you use standard output for logging but daemonize, logs will be sent to /dev/null."
pidfile_desc = "When redis is running as daemon it creates a pid file. Redis writes it where specified at startup and removes it at exit. You can set the path for pid file."
databases_desc = "Set the number of databases.The default database is DB 0, you can select a different one on a per-connection basis using SELECT <dbid> where dbid is a number between 0 and 'databases'-1."
daemonize_desc = "Use 'yes' if you want Redis to run as a daemon. By default Redis does not run as a daemon. Redis will write a pid file in /var/run/redis.pid when daemonized."
loglevel_desc = "This config specifies the verbosity level.Debug is useful for development and testing as a lot of information is given.Verbose is selected to logs many rarely used info.Notice is used in production because it is moderately verbose.Warning as the name specifies logs only the very important messages"
supervised_desc = "If you run Redis from upstart or systemd, Redis can interact with your supervision tree.If 'no' is selected then there will be no supervision interaction.If upstart is selected - signal upstart by putting Redis into SIGSTOP mode.If systemd is selected -signal systemd by writing READY=1 to $NOTIFY_SOCKET and If it is set to auto-detect upstart or systemd method based on UPSTART_JOB or NOTIFY_SOCKET environment variables."
syslog_fac_desc = (
    "Specifies the syslog facility. Must be USER or between LOCAL0-LOCAL7."
)


GENERAL_CONFIG = OrderedDict(
    {
        "pidfile": {"des": pidfile_desc, "type": "text", "can_edit": True},
        "logfile": {"des": logfile_desc, "type": "text", "can_edit": True},
        "loglevel": {"des": loglevel_desc, "type": "select", "can_edit": True},
        "databases": {"des": databases_desc, "type": "number", "can_edit": True},
        "daemonize": {"des": daemonize_desc, "type": "text", "can_edit": False},
        "supervised": {"des": supervised_desc, "type": "text", "can_edit": False},
        "syslog-facility": {"des": syslog_fac_desc, "type": "text", "can_edit": True},
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
