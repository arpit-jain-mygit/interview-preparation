# Always Unknown Topics

Topics that frequently come up in interviews but are often unclear or misunderstood.

## Sharding vs Read Replicas

### Sharding

**Sharding** splits your data horizontally across multiple database instances based on a **shard key** (like user ID or region). Each shard holds a different subset of the data.

- **Example:** User IDs 1-1M on Shard A, 1M-2M on Shard B, etc.
- **Benefit:** Scales write capacity and storage — you can handle more data and writes
- **Cost:** Complex routing logic, harder to query across shards, rebalancing is painful

### Read Replicas

**Read Replicas** are exact copies of your entire database that sync from a primary instance. They're for reading only.

- **Example:** Primary DB in US, read replica in EU, another in Asia
- **Benefit:** Distributes read load geographically; low latency for readers in different regions
- **Cost:** Uses more storage (full copy per replica), doesn't help with write scaling

### Key Difference

| Aspect | Sharding | Read Replicas |
|--------|----------|---------------|
| **Data split** | Yes (partial) | No (full copy) |
| **Write scaling** | ✅ Yes | ❌ No (writes still go to primary) |
| **Read scaling** | ✅ Yes | ✅ Yes |
| **Complexity** | High | Low |
| **Query any data** | ❌ Hard (need shard key) | ✅ Easy |

**Real-world rule:** Use **read replicas** for read-heavy workloads across geographies. Use **sharding** when your data is too big to fit on one machine or writes are bottlenecking you.

## Read Replicas in NoSQL

Yes, **read replicas work with NoSQL databases** too. In fact, many NoSQL systems use replication as a core feature.

### How NoSQL Read Replicas Work

**NoSQL databases typically have built-in replication** (unlike traditional SQL where replicas are often a separate feature).

- **MongoDB:** Primary + Secondary replicas (replica sets)
- **Cassandra:** Every node is a replica; data replicates across the cluster
- **DynamoDB:** Automatically creates read replicas across availability zones
- **Redis:** Master → Slave replicas for read scaling

### Key Difference: NoSQL vs SQL Read Replicas

| Aspect | SQL Read Replicas | NoSQL Read Replicas |
|--------|-------------------|-------------------|
| **Setup** | Manual (add replicas) | Often built-in, automatic |
| **Consistency** | Usually eventual | Eventual (configurable) |
| **Failover** | Manual or semi-auto | Often automatic (Cassandra, MongoDB) |
| **Write conflicts** | Single primary | Can have multi-write (Cassandra) |

### Replication Styles in NoSQL

1. **Leader-Follower** (MongoDB)
   - One primary (writes), multiple secondaries (reads)
   - Same as SQL replicas

2. **Leaderless** (Cassandra, DynamoDB)
   - Every node accepts reads AND writes
   - Data spreads across all nodes
   - More resilient but eventual consistency

### When to Use NoSQL Read Replicas

- High read volume + low write volume
- Geographically distributed users (replicas in different regions)
- High availability needs

**Bottom line:** NoSQL databases are actually *better* at replication than SQL — it's baked into their DNA, not bolted on.
