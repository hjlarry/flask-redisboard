REDISBOARD_DETAIL_TIMESTAMP_KEYS = ("last_save_time",)
REDISBOARD_DETAIL_SECONDS_KEYS = ("uptime_in_seconds",)
REDISBOARD_SLOWLOG_LEN = 10
REDISBOARD_SOCKET_TIMEOUT = None
REDISBOARD_SOCKET_CONNECT_TIMEOUT = None
REDISBOARD_SOCKET_KEEPALIVE = None
REDISBOARD_SOCKET_KEEPALIVE_OPTIONS = None
INFO_GROUPS = [
    "Server",
    "Clients",
    "Memory",
    "Persistence",
    "Stats",
    "Replication",
    "Cpu",
    "Cluster",
    "Keyspace",
    "Commandstats",
]
BADGE_CLASS = {
    "string": "badge-info",
    "list": "badge-success",
    "set": "badge-warning",
    "hash": "badge-dark",
    "zset": "badge-light",
}
