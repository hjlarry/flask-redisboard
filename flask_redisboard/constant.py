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
wait_to_add = "wait to add"

SECURITY_CONFIG = OrderedDict({"requirepass": {"desc": wait_to_add, "can_edit": False}})

CLIENTS_CONFIG = OrderedDict(
    {"maxclients": {"desc": wait_to_add, "type": "number", "can_edit": True}}
)

MEMORY_CONFIG = OrderedDict(
    {
        "maxmemory": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "maxmemory-samples": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "maxmemory-policy": {"desc": wait_to_add, "type": "select", "can_edit": True},
    }
)

LAZY_FREEING_CONFIG = OrderedDict(
    {
        "lazyfree-lazy-eviction": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "lazyfree-lazy-expire": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "lazyfree-lazy-server-del": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "slave-lazy-flush": {"desc": wait_to_add, "type": "select", "can_edit": True},
    }
)

APPEND_ONLY_MODE_CONFIG = OrderedDict(
    {
        "auto-aof-rewrite-percentage": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "auto-aof-rewrite-min-size": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "no-appendfsync-on-rewrite": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "aof-load-truncated": {"desc": wait_to_add, "type": "select", "can_edit": True},
        "aof-use-rdb-preamble": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "appendfsync": {"desc": wait_to_add, "type": "select", "can_edit": True},
        "appendonly": {"desc": wait_to_add, "type": "select", "can_edit": True},
    }
)

LUA_SCRIPTING_CONFIG = OrderedDict(
    {"lua-time-limit": {"desc": wait_to_add, "type": "number", "can_edit": True}}
)

REDIS_CLUSTER_CONFIG = OrderedDict(
    {
        "cluster-node-timeout": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "cluster-migration-barrier": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "cluster-slave-validity-factor": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "cluster-require-full-coverage": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
    }
)

CLUSTER_DOCKER_NAT_CONFIG = OrderedDict(
    {
        "cluster-announce-ip": {"desc": wait_to_add, "type": "text", "can_edit": True},
        "cluster-announce-port": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "cluster-announce-bus-port ": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
    }
)

SLOWLOG_CONFIG = OrderedDict(
    {
        "slowlog-log-slower-than": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "slowlog-max-len": {"desc": wait_to_add, "type": "number", "can_edit": True},
    }
)

LATENCY_MONITOR_CONFIG = OrderedDict(
    {
        "latency-monitor-threshold": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        }
    }
)

EVENT_NOTIFICATION_CONFIG = OrderedDict(
    {
        "notify-keyspace-events": {
            "desc": wait_to_add,
            "type": "checklist",
            "can_edit": True,
        }
    }
)

DEFRAGMENTATION_CONFIG = OrderedDict(
    {
        "active-defrag-threshold-lower": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-threshold-upper": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-ignore-bytes": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-cycle-min": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "active-defrag-cycle-max": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "activedefrag": {"desc": wait_to_add, "type": "select", "can_edit": True},
    }
)

ADVANCED_CONFIG = OrderedDict(
    {
        "hash-max-ziplist-entries": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "hash-max-ziplist-value": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "list-max-ziplist-size": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "list-compress-depth": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "set-max-intset-entries": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "zset-max-ziplist-entries": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "zset-max-ziplist-value": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "hll-sparse-max-bytes": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "hz": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "activerehashing": {"desc": wait_to_add, "type": "select", "can_edit": True},
        "aof-rewrite-incremental-fsync": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "client-output-buffer-limit": {
            "desc": wait_to_add,
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
