from collections import OrderedDict

BADGE_STYLE = {
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
    "CPU",
    "Cluster",
]


logfile_desc = "You can specify the log file name.An empty string can be used to force Redis to log on the standard output."
pidfile_desc = "When redis is running as daemon it creates a pid file."
databases_desc = "Set the number of databases."
daemonize_desc = "Use 'yes' if you want Redis to run as a daemon. By default Redis does not run as a daemon. "
loglevel_desc = "This config specifies the verbosity level.Debug is useful for development and testing as a lot of information is given."
supervised_desc = "If you run Redis from upstart or systemd, Redis can interact with your supervision tree."
syslog_facility_desc = "Specifies the syslog facility."


GENERAL_CONFIG = OrderedDict(
    {
        "logfile": {"desc": logfile_desc, "type": "text", "can_edit": True},
        "pidfile": {"desc": pidfile_desc, "type": "text", "can_edit": True},
        "databases": {"desc": databases_desc, "can_edit": False},
        "daemonize": {"desc": daemonize_desc, "can_edit": False},
        "loglevel": {"desc": loglevel_desc, "type": "select", "can_edit": True},
        "supervised": {"desc": supervised_desc, "can_edit": False},
        "syslog-facility": {
            "desc": syslog_facility_desc,
            "type": "text",
            "can_edit": True,
        },
    }
)


unixsocket_desc = "Specify the path for the Unix socket that will be used to listen for incoming connections."
timeout_desc = "Close the connection after a client is idle for N seconds, 0 to disable.             "
port_desc = "Accept connections on the specified port, default is 6379 (IANA #815344). "
tcp_backlog_desc = "In high requests-per-second environments you need an high backlog in order to avoid slow clients connections issues."
tcp_keepalive_desc = "In absence of communication redis sends ACKs to clients to check for dead peers.   "
protected_mode_desc = "Protected mode is a layer of security protection.By default protected mode is enabled."
unixsocketperm_desc = "Specify the path for the Unix socket that will be used to listen for incoming connections. "
bind_desc = "By default, if no bind configuration directive is specified, Redis listens for connections from all the network interfaces available on the server."

NETWORK_CONFIG = OrderedDict(
    {
        "unixsocket": {"desc": unixsocket_desc, "can_edit": False},
        "timeout": {"desc": timeout_desc, "type": "number", "can_edit": True},
        "port": {"desc": port_desc, "can_edit": False},
        "tcp-backlog": {"desc": tcp_backlog_desc, "can_edit": False},
        "tcp-keepalive": {
            "desc": tcp_keepalive_desc,
            "type": "number",
            "can_edit": True,
        },
        "protected-mode": {
            "desc": protected_mode_desc,
            "type": "select",
            "can_edit": True,
        },
        "unixsocketperm ": {"desc": unixsocketperm_desc, "can_edit": False},
        "bind ": {"desc": bind_desc, "can_edit": False},
    }
)

dbfilename_desc = "The filename where to dump the database."
stop_writes_on_bgsave_error_desc = "By default Redis will stop accepting writes if RDB snapshots are enabled and the latest background save failed. "
rdbcompression_desc = "This Compresses string objects using LZF when dump .rdb databases.By default it is set to yes."
rdbchecksum_desc = "Since version 5 of RDB a CRC64 checksum is placed at the end of the file.          "
dir_desc = "The working directory.The DB will be written inside this directory, with the filename specified above using the 'dbfilename' configuration directive."
save_desc = "Used for saving db on disk. The format is 'save <seconds><changes>'."

SNAPSHOTTING_CONFIG = OrderedDict(
    {
        "dbfilename": {"desc": dbfilename_desc, "type": "text", "can_edit": True},
        "stop-writes-on-bgsave-error": {
            "desc": stop_writes_on_bgsave_error_desc,
            "type": "select",
            "can_edit": True,
        },
        "rdbcompression": {
            "desc": rdbcompression_desc,
            "type": "select",
            "can_edit": True,
        },
        "rdbchecksum": {"desc": rdbchecksum_desc, "can_edit": False},
        "dir": {"desc": dir_desc, "type": "text", "can_edit": True},
        "save": {"desc": save_desc, "type": "text", "can_edit": True},
    }
)


masterauth_desc = "If the master is password protected it is possible to tell the slave to authenticate before starting the replication synchronization process, otherwise the master will refuse the slave request."
slave_announce_ip_desc = "When port forwarding or Network Address Translation (NAT) is used, the slave may be actually reachable via different IP and port pairs. "
repl_ping_slave_period_desc = "Slaves send PINGs to server in a predefined interval. It's possible to change this interval with the repl-ping-slave-period option.The default value is 10 seconds."
repl_timeout_desc = "This config sets the replication timeout for 1.Bulk transfer I/O during SYNC from the point of view of slave,2.Master timeout from the point of view of slave and * Slave timeout from the point of view of masters."
repl_backlog_size_desc = "The backlog is a buffer that accumulates slave data when slaves are disconnected for some time."
repl_backlog_ttl_desc = "After a master has no longer connected slaves for some time, the backlog will be freed. "
slave_priority_desc = "The slave priority is an integer number published by Redis in the INFO output.            "
slave_announce_port_desc = "When port forwarding or Network Address Translation (NAT) is used, the slave may be actually reachable via different IP and port pairs."
min_slaves_to_write_desc = "It is possible for a master to stop accepting writes if there are less than N slaves connected. setting this value to 0 disables the fature."
min_slaves_max_lag_desc = "It is possible for a master to stop accepting writes if there are less than N slaves connected, having a lag less or equal than M seconds."
repl_diskless_sync_delay_desc = "When diskless replication is enabled, it is possible to configure the delay the server waits in order to spawn the child that transfers the RDB via socket to the slaves."
slave_serve_stale_data_desc = "This config is useful When a slave loses its connection with the master, or when the replication is still in progress. In this condition the slave can act in two different ways."
slave_read_only_desc = "You can configure a slave instance to accept writes or not. Writing against a slave instance may be useful to store some ephemeral data but may also cause problems if clients are writing to it because of a misconfiguration."
repl_disable_tcp_nodelay_desc = "If you select 'yes' Redis will use a smaller number of TCP packets and less bandwidth to send data to slaves. "
repl_diskless_sync_desc = "When diskless replication is used, the master waits a configurable amount of time before starting the transfer of data in the hope that multiple slaves will arrive and the transfer can be parallelized."
slaveof_desc = "Master-Slave replication. Use slaveof to make a Redis instance a copy of another Redis server.You need the master IP and master Port for this config."

REPLICATION_CONFIG = OrderedDict(
    {
        "masterauth": {"desc": masterauth_desc, "can_edit": False},
        "slave-announce-ip ": {
            "desc": slave_announce_ip_desc,
            "type": "text",
            "can_edit": True,
        },
        "repl-ping-slave-period ": {
            "desc": repl_ping_slave_period_desc,
            "type": "number",
            "can_edit": True,
        },
        "repl-timeout": {"desc": repl_timeout_desc, "type": "number", "can_edit": True},
        "repl-backlog-size": {
            "desc": repl_backlog_size_desc,
            "type": "number",
            "can_edit": True,
        },
        "repl-backlog-ttl": {
            "desc": repl_backlog_ttl_desc,
            "type": "number",
            "can_edit": True,
        },
        "slave-priority": {
            "desc": slave_priority_desc,
            "type": "number",
            "can_edit": True,
        },
        "slave-announce-port": {
            "desc": slave_announce_port_desc,
            "type": "number",
            "can_edit": True,
        },
        "min-slaves-to-write": {
            "desc": min_slaves_to_write_desc,
            "type": "number",
            "can_edit": True,
        },
        "min-slaves-max-lag": {
            "desc": min_slaves_max_lag_desc,
            "type": "number",
            "can_edit": True,
        },
        "repl-diskless-sync-delay": {
            "desc": repl_diskless_sync_delay_desc,
            "type": "number",
            "can_edit": True,
        },
        "slave-serve-stale-data": {
            "desc": slave_serve_stale_data_desc,
            "type": "select",
            "can_edit": True,
        },
        "slave-read-only": {
            "desc": slave_read_only_desc,
            "type": "select",
            "can_edit": True,
        },
        "repl-disable-tcp-nodelay": {
            "desc": repl_disable_tcp_nodelay_desc,
            "type": "select",
            "can_edit": True,
        },
        "repl-diskless-sync": {
            "desc": repl_diskless_sync_desc,
            "type": "select",
            "can_edit": True,
        },
        "slaveof": {"desc": slaveof_desc, "can_edit": False},
    }
)


requirepass_desc = "Require clients to issue AUTH <PASSWORD> before processing any other commands. This might be useful in environments in which you do not trust others with access to the host running redis-server."

SECURITY_CONFIG = OrderedDict(
    {"requirepass": {"desc": requirepass_desc, "can_edit": False}}
)


maxclients_desc = "Set the max number of connected clients at the same time.By default this limit is set to 10000 clients."

CLIENTS_CONFIG = OrderedDict(
    {"maxclients": {"desc": maxclients_desc, "type": "number", "can_edit": True}}
)


maxmemory_desc = "Set a memory usage limit to the specified amount of bytes. When the memory limit is reached Redis will try to remove keys according to the eviction policy selected."
maxmemory_samples_desc = "LRU, LFU and minimal TTL algorithms are not precise algorithms but approximated algorithms (in order to save memory), so you can tune it for speed or accuracy."
maxmemory_policy_desc = "How Redis will select what to remove when maxmemory is reached. You can select among five behaviors."

MEMORY_CONFIG = OrderedDict(
    {
        "maxmemory": {"desc": maxmemory_desc, "type": "number", "can_edit": True},
        "maxmemory-samples": {
            "desc": maxmemory_samples_desc,
            "type": "number",
            "can_edit": True,
        },
        "maxmemory-policy": {
            "desc": maxmemory_policy_desc,
            "type": "select",
            "can_edit": True,
        },
    }
)


lazyfree_lazy_eviction_desc = "Redis deletes objects independently of a user call On eviction, because of the maxmemory and maxmemory policy configurations, in order to make room for new data, without going over the specified memory limit."
lazyfree_lazy_expire_desc = "Redis deletes objects independently of a user call because of expire. when a key with an associated time to live (see the EXPIRE command) must be deleted from memory."
lazyfree_lazy_server_del_desc = "Redis deletes objects independently of a user call Because of a side effect of a command that stores data on a key that may already exist."
slave_lazy_flush_desc = "Redis deletes objects independently of a user call During replication, when a slave performs a full resynchronization with its master, the content of the whole database is removed in order to load the RDB file just transfered."

LAZY_FREEING_CONFIG = OrderedDict(
    {
        "lazyfree-lazy-eviction": {
            "desc": lazyfree_lazy_eviction_desc,
            "type": "select",
            "can_edit": True,
        },
        "lazyfree-lazy-expire": {
            "desc": lazyfree_lazy_expire_desc,
            "type": "select",
            "can_edit": True,
        },
        "lazyfree-lazy-server-del": {
            "desc": lazyfree_lazy_server_del_desc,
            "type": "select",
            "can_edit": True,
        },
        "slave-lazy-flush": {
            "desc": slave_lazy_flush_desc,
            "type": "select",
            "can_edit": True,
        },
    }
)


auto_aof_rewrite_percentage_desc = "Automatic rewrite of the append only file. Redis is able to automatically rewrite the log file implicitly calling BGREWRITEAOF when the AOF log size grows by the specified percentage."
auto_aof_rewrite_min_size_desc = "You need to specify a minimal size for the AOF file to be rewritten, this is useful to avoid rewriting the AOF file even if the percentage increase is reached but it is still pretty small."
no_appendfsync_on_rewrite_desc = "In some Linux configurations Redis may block too long on the fsync() call.             "
aof_load_truncated_desc = "An AOF file may be found to be truncated at the end during the Redis startup process, when the AOF data gets loaded back into memory."
aof_use_rdb_preamble_desc = "When rewriting the AOF file, Redis is able to use an RDB preamble in the AOF file for faster rewrites and recoveries."
appendfsync_desc = "The fsync() call tells the Operating System to actually write data on disk instead of waiting for more data in the output buffer. "
appendonly_desc = "By default Redis asynchronously dumps the dataset on disk. This mode is good enough in many applications, but an issue with the Redis process or a power outage may result into a few minutes of writes lost."

APPEND_ONLY_MODE_CONFIG = OrderedDict(
    {
        "auto-aof-rewrite-percentage": {
            "desc": auto_aof_rewrite_percentage_desc,
            "type": "number",
            "can_edit": True,
        },
        "auto-aof-rewrite-min-size": {
            "desc": auto_aof_rewrite_min_size_desc,
            "type": "number",
            "can_edit": True,
        },
        "no-appendfsync-on-rewrite": {
            "desc": no_appendfsync_on_rewrite_desc,
            "type": "select",
            "can_edit": True,
        },
        "aof-load-truncated": {
            "desc": aof_load_truncated_desc,
            "type": "select",
            "can_edit": True,
        },
        "aof-use-rdb-preamble": {
            "desc": aof_use_rdb_preamble_desc,
            "type": "select",
            "can_edit": True,
        },
        "appendfsync": {"desc": appendfsync_desc, "type": "select", "can_edit": True},
        "appendonly": {"desc": appendonly_desc, "type": "select", "can_edit": True},
    }
)


lua_time_limit_desc = "Max execution time of a Lua script in milliseconds."

LUA_SCRIPTING_CONFIG = OrderedDict(
    {
        "lua-time-limit": {
            "desc": lua_time_limit_desc,
            "type": "number",
            "can_edit": True,
        }
    }
)


cluster_node_timeout_desc = "Cluster node timeout is the amount of milliseconds a node must be unreachable for it to be considered in failure state."
cluster_migration_barrier_desc = "Slaves migrate to orphaned masters only if there are still at least a given number of other working slaves for their old master. This number is the migration barrier."
cluster_slave_validity_factor_desc = "A large slave-validity-factor may allow slaves with too old data to failover a master, while a too small value may prevent the cluster from being able to elect a slave at all."
cluster_require_full_coverage_desc = "By default Redis Cluster nodes stop accepting queries if they detect there is at least an hash slot uncovered (no available node is serving it)."

REDIS_CLUSTER_CONFIG = OrderedDict(
    {
        "cluster-node-timeout": {
            "desc": cluster_node_timeout_desc,
            "type": "number",
            "can_edit": True,
        },
        "cluster-migration-barrier": {
            "desc": cluster_migration_barrier_desc,
            "type": "number",
            "can_edit": True,
        },
        "cluster-slave-validity-factor": {
            "desc": cluster_slave_validity_factor_desc,
            "type": "number",
            "can_edit": True,
        },
        "cluster-require-full-coverage": {
            "desc": cluster_require_full_coverage_desc,
            "type": "select",
            "can_edit": True,
        },
    }
)


cluster_docker_nat_desc = "In certain deployments, Redis Cluster nodes address discovery fails, because addresses are NAT-ted or because ports are forwarded."

CLUSTER_DOCKER_NAT_CONFIG = OrderedDict(
    {
        "cluster-announce-ip": {
            "desc": cluster_docker_nat_desc,
            "type": "text",
            "can_edit": True,
        },
        "cluster-announce-port": {
            "desc": cluster_docker_nat_desc,
            "type": "number",
            "can_edit": True,
        },
        "cluster-announce-bus-port ": {
            "desc": cluster_docker_nat_desc,
            "type": "number",
            "can_edit": True,
        },
    }
)


slowlog_log_slower_than_desc = "This tells Redis what is the execution time, in microseconds, to exceed in order for the command to get logged."
slowlog_max_len_desc = "This is the length of the slow log.There is no limit to this length. Just be aware that it will consume memory."

SLOWLOG_CONFIG = OrderedDict(
    {
        "slowlog-log-slower-than": {
            "desc": slowlog_log_slower_than_desc,
            "type": "number",
            "can_edit": True,
        },
        "slowlog-max-len": {
            "desc": slowlog_max_len_desc,
            "type": "number",
            "can_edit": True,
        },
    }
)


latency_monitor_threshold_desc = "The Redis latency monitoring subsystem samples different operations at runtime in order to collect data related to possible sources of latency of a Redis instance."

LATENCY_MONITOR_CONFIG = OrderedDict(
    {
        "latency-monitor-threshold": {
            "desc": latency_monitor_threshold_desc,
            "type": "number",
            "can_edit": True,
        }
    }
)


notify_keyspace_events_desc = "The 'notify-keyspace-events' takes as argument a string that is composed of zero or multiple characters."

EVENT_NOTIFICATION_CONFIG = OrderedDict(
    {
        "notify-keyspace-events": {
            "desc": notify_keyspace_events_desc,
            "type": "checklist",
            "can_edit": True,
        }
    }
)


active_defrag_threshold_lower_desc = "Minimum percentage of fragmentation to start active defrag.                              "
active_defrag_threshold_upper_desc = "Maximum percentage of fragmentation at which we use maximum effort.                      "
active_defrag_ignore_bytes_desc = "Minimum amount of fragmentation waste to start active defrag.                               "
active_defrag_cycle_min_desc = "Minimal effort for defrag in CPU percentage."
active_defrag_cycle_max_desc = "Maximal effort for defrag in CPU percentage"
activedefrag_desc = "Active defragmentation allows a Redis server to compact the spaces left between small allocations and deallocations of data in memory, thus allowing to reclaim back memory."

DEFRAGMENTATION_CONFIG = OrderedDict(
    {
        "active-defrag-threshold-lower": {
            "desc": active_defrag_threshold_lower_desc,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-threshold-upper": {
            "desc": active_defrag_threshold_upper_desc,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-ignore-bytes": {
            "desc": active_defrag_ignore_bytes_desc,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-cycle-min": {
            "desc": active_defrag_cycle_min_desc,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-cycle-max": {
            "desc": active_defrag_cycle_max_desc,
            "type": "number",
            "can_edit": True,
        },
        "activedefrag": {"desc": activedefrag_desc, "type": "select", "can_edit": True},
    }
)


client_query_buffer_limit_desc = "Client query buffers accumulate new commands."
lfu_log_factor_desc = "The LFU counter is just 8 bits per key, it's maximum value is 255, so Redis uses a probabilistic increment with logarithmic behavior."
lfu_decay_time_desc = "The counter decay time is the time, in minutes, that must elapse in order for the key counter to be divided by two (or decremented if it has a value less <= 10)."
hash_max_ziplist_entries_desc = "Hashes are encoded using a memory efficient data structure when they have a small number of entries, and the biggest entry does not exceed a given threshold.These thresholds can be configured using the above directive."
hash_max_ziplist_value_desc = "Hashes are encoded using a memory efficient data structure when they have a small number of entries, and the biggest entry does not exceed a given threshold.These thresholds can be configured using the above directive."
list_max_ziplist_size_desc = "Lists are also encoded in a special way to save a lot of space. The number of entries allowed per internal list node can be specified as a fixed maximum size or a maximum number of elements."
list_compress_depth_desc = "Lists may also be compressed. Compress depth is the number of quicklist ziplist nodes from each side of the list to exclude from compression. The head and tail of the list are always uncompressed for fast push/pop operations."
set_max_intset_entries_desc = "Sets have a special encoding in just one case: when a set is composed of just strings that happen to be integers in radix 10 in the range of 64 bit signed integers."
zset_max_ziplist_entries_desc = "Sorted sets are also specially encoded in order to save a lot of space. This encoding is only used when the length and elements of a sorted set are below the specified limits."
zset_max_ziplist_value_desc = "Sorted sets are also specially encoded in order to save a lot of space. This encoding is only used when the length and elements of a sorted set are below the specified limits."
hll_sparse_max_bytes_desc = "HyperLogLog sparse representation bytes limit. The limit includes the 16 bytes header."
hz_desc = "Redis calls an internal function to perform many background tasks, like closing connections of clients in timeout, purging expired keys that are never requested, and so forth. "
activerehashing_desc = "Active rehashing uses 1 millisecond every 100 milliseconds of CPU time in order to help rehashing the main Redis hash table."
aof_rewrite_incremental_fsync_desc = "When a child rewrites the AOF file, if the following option is enable the file will be fsync_ed every 32 MB of data generated. This is useful in order to commit the file to the disk more incrementally and avoid big latency spikes."
client_output_buffer_limit_desc = "The client output buffer limits can be used to force disconnection of clients that are not reading data from the server fast enough for some reason.The limit can be set differently for the three different classes of clients: normal,slave or pubsub."

ADVANCED_CONFIG = OrderedDict(
    {
        "client-query-buffer-limit": {
            "desc": client_query_buffer_limit_desc,
            "type": "number",
            "can_edit": True,
        },
        "lfu-log-factor": {
            "desc": lfu_log_factor_desc,
            "type": "number",
            "can_edit": True,
        },
        "lfu-decay-time": {
            "desc": lfu_decay_time_desc,
            "type": "number",
            "can_edit": True,
        },
        "hash-max-ziplist-entries": {
            "desc": hash_max_ziplist_entries_desc,
            "type": "number",
            "can_edit": True,
        },
        "hash-max-ziplist-value": {
            "desc": hash_max_ziplist_value_desc,
            "type": "number",
            "can_edit": True,
        },
        "list-max-ziplist-size": {
            "desc": list_max_ziplist_size_desc,
            "type": "number",
            "can_edit": True,
        },
        "list-compress-depth": {
            "desc": list_compress_depth_desc,
            "type": "number",
            "can_edit": True,
        },
        "set-max-intset-entries": {
            "desc": set_max_intset_entries_desc,
            "type": "number",
            "can_edit": True,
        },
        "zset-max-ziplist-entries": {
            "desc": zset_max_ziplist_entries_desc,
            "type": "number",
            "can_edit": True,
        },
        "zset-max-ziplist-value": {
            "desc": zset_max_ziplist_value_desc,
            "type": "number",
            "can_edit": True,
        },
        "hll-sparse-max-bytes": {
            "desc": hll_sparse_max_bytes_desc,
            "type": "number",
            "can_edit": True,
        },
        "hz": {"desc": hz_desc, "type": "number", "can_edit": True},
        "activerehashing": {
            "desc": activerehashing_desc,
            "type": "select",
            "can_edit": True,
        },
        "aof-rewrite-incremental-fsync": {
            "desc": aof_rewrite_incremental_fsync_desc,
            "type": "select",
            "can_edit": True,
        },
        "client-output-buffer-limit": {
            "desc": client_output_buffer_limit_desc,
            "type": "text",
            "can_edit": True,
        },
    }
)


CONFIG = (
    (NETWORK_CONFIG, "NETWORK"),
    (GENERAL_CONFIG, "GENERAL"),
    (SNAPSHOTTING_CONFIG, "SNAPSHOTTING"),
    (REPLICATION_CONFIG, "REPLICATION"),
    (SECURITY_CONFIG, "SECURITY"),
    (CLIENTS_CONFIG, "CLIENTS"),
    (MEMORY_CONFIG, "MEMORY MANAGEMENT"),
    (LAZY_FREEING_CONFIG, "LAZY FREEING"),
    (APPEND_ONLY_MODE_CONFIG, "APPEND ONLY MODE"),
    (LUA_SCRIPTING_CONFIG, "LUA SCRIPTING"),
    (REDIS_CLUSTER_CONFIG, "REDIS CLUSTER"),
    (CLUSTER_DOCKER_NAT_CONFIG, "CLUSTER DOCKER/NAT"),
    (SLOWLOG_CONFIG, "SLOWLOG"),
    (LATENCY_MONITOR_CONFIG, "LATENCY MONITOR"),
    (EVENT_NOTIFICATION_CONFIG, "EVENT NOTIFICATION"),
    (DEFRAGMENTATION_CONFIG, "DEFRAGMENTATION"),
    (ADVANCED_CONFIG, "ADVANCED CONFIG"),
)
