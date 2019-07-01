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
        "logfile": {"desc": logfile_desc, "type": "text", "can_edit": True},
        "pidfile": {"desc": pidfile_desc, "type": "text", "can_edit": True},
        "databases": {"desc": databases_desc, "can_edit": False},
        "daemonize": {"desc": daemonize_desc, "can_edit": False},
        "loglevel": {"desc": loglevel_desc, "type": "select", "can_edit": True},
        "supervised": {"desc": supervised_desc, "can_edit": False},
        "syslog-facility": {"desc": syslog_fac_desc, "type": "text", "can_edit": True},
    }
)


unixsocket_desc = "Specify the path for the Unix socket that will be used to listen for incoming connections.There is no default, so Redis will not listen on a unix socket when not specified."
timeout_desc = (
    "Close the connection after a client is idle for N seconds (0 to disable)."
)
port_desc = "Accept connections on the specified port, default is 6379 (IANA #815344). If port 0 is specified Redis will not listen on a TCP socket."
tcp_backlog_desc = "In high requests-per-second environments you need an high backlog in order to avoid slow clients connections issues. Note that the Linux kernel will silently truncate it to the value of /proc/sys/net/core/somaxconn so make sure to raise both the value of somaxconn and tcp_max_syn_backlog in order to get the desired effect."
tcp_keepalive_desc = "In absence of communication redis sends ACKs to clients to check for dead peers.This config specifies the time period used to send ACKs. To close the connection double the specified time is needed.Default is set to 300."
protected_mode_desc = "Protected mode is a layer of security protection.By default protected mode is enabled.You should disable it only if you are sure you want clients from other hosts to connect to Redis even if no authentication is configured, nor a specific set of interfaces are explicitly listed using the bind directive."
unixsocketperm_desc = "Specify the path for the Unix socket that will be used to listen for incoming connections. There is no default, so Redis will not listen on a unix socket when not specified."
bind_desc = "By default, if no bind configuration directive is specified, Redis listens for connections from all the network interfaces available on the server.It is possible to listen to just one or multiple selected interfaces using the bind configuration directive, followed by one or more IP addresses."

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
stop_writes_on_bgsave_error_desc = "By default Redis will stop accepting writes if RDB snapshots are enabled and the latest background save failed. This will make you aware that data is not persisting on disk properly, otherwise chances are that no one will notice and some disaster will happen.If the background saving process will start working again Redis will automatically allow writes again.You can disable this so that Redis continue to work as usual even if there are problems with the disk."
rdbcompression_desc = "This Compresses string objects using LZF when dump .rdb databases.By default it is set to yes.If you want to save some CPU then set it to no."
rdbchecksum_desc = "Since version 5 of RDB a CRC64 checksum is placed at the end of the file. This makes the format more resistant to corruption but there is a performance hit to pay (around 10%) when saving and loading RDB files, so you can disable it for maximum performances.RDB files created with checksum disabled have a checksum of zero that will tell the loading code to skip the check."
dir_desc = "The working directory.The DB will be written inside this directory, with the filename specified above using the 'dbfilename' configuration directive.The Append Only File will also be created inside this directory."
save_desc = "Used for saving db on disk. The format is 'save <seconds><changes>'.Will save the DB if both the given number of seconds and the given number of write operations against the DB occurred."

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

wait_to_add = "wait to add"


REPLICATION_CONFIG = OrderedDict(
    {
        "masterauth": {"desc": wait_to_add, "can_edit": False},
        "slave-announce-ip ": {"desc": wait_to_add, "type": "text", "can_edit": True},
        "repl-ping-slave-period ": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "repl-timeout": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "repl-backlog-size": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "repl-backlog-ttl": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "slave-priority": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "slave-announce-port": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "min-slaves-to-write": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "min-slaves-max-lag": {"desc": wait_to_add, "type": "number", "can_edit": True},
        "repl-diskless-sync-delay": {
            "desc": wait_to_add,
            "type": "number",
            "can_edit": True,
        },
        "slave-serve-stale-data": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "slave-read-only": {"desc": wait_to_add, "type": "select", "can_edit": True},
        "repl-disable-tcp-nodelay": {
            "desc": wait_to_add,
            "type": "select",
            "can_edit": True,
        },
        "repl-diskless-sync": {"desc": wait_to_add, "type": "select", "can_edit": True},
        "slaveof": {"desc": wait_to_add, "can_edit": False},
    }
)

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
