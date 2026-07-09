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

## Caching Strategies

Caching strategies determine *how* and *when* to update cached data when the underlying data changes.

### Cache Update Strategies

#### 1. Cache-Aside (Lazy Loading)

Application checks cache first. If miss → fetch from DB and update cache.

```
Request → Check Cache → Hit? Return
                      → Miss? Fetch DB → Update Cache → Return
```

**Pros:** Simple, only caches what's used  
**Cons:** First request is slow (cache miss)  
**Use:** General purpose, web apps

#### 2. Write-Through

Write to cache AND database simultaneously before returning.

```
Write → Update Cache + Update DB (together) → Return
```

**Pros:** Cache always consistent with DB  
**Cons:** Slower writes, extra latency  
**Use:** Critical data (financial, medical)

#### 3. Write-Behind (Write-Back)

Write to cache first, then asynchronously write to DB.

```
Write → Update Cache → Return (immediately)
          → Async update DB (later)
```

**Pros:** Fast writes, high throughput  
**Cons:** Data loss risk if cache crashes before DB sync  
**Use:** Non-critical data, high-volume writes

#### 4. Refresh-Ahead

Proactively refresh cache before it expires.

```
Cache TTL expiring soon → Fetch fresh data → Update Cache
```

**Pros:** Avoids cache misses, always fresh data  
**Cons:** Wastes resources refreshing unused data  
**Use:** Predictable access patterns (leaderboards, recommendations)

### Update Strategies Comparison

| Strategy | Consistency | Write Speed | Read Speed | Best For |
|----------|-------------|-------------|-----------|----------|
| **Cache-Aside** | Eventually | Fast | Slow (miss) | Web apps |
| **Write-Through** | Strong | Slow | Fast | Critical data |
| **Write-Behind** | Very Fast | Very Fast | Fast | High throughput |
| **Refresh-Ahead** | Strong | Fast | Very Fast | Predictable reads |

---

## Cache Eviction Strategies

Eviction strategies determine *which* items to remove when cache is full.

### 1. LRU (Least Recently Used)

Remove the item that hasn't been used for the longest time.

```
Access order: A → B → C → A → B
Cache full, need to evict → Remove C (least recently used)
```

**Pros:** Simple, works well for most cases  
**Cons:** Doesn't consider how *frequently* items are used  
**Use:** Most common choice (Redis default, browser cache)

### 2. LFU (Least Frequently Used)

Remove the item that's been accessed the fewest times.

```
Access counts: A(10 times) → B(5 times) → C(2 times)
Cache full → Remove C (least frequent)
```

**Pros:** Favors "hot" data  
**Cons:** Overhead to track access counts  
**Use:** When you care about frequency over recency

### 3. FIFO (First In, First Out)

Remove the oldest item added to cache, regardless of access.

```
Order added: A → B → C → D
Cache full → Remove A (first added)
```

**Pros:** Very simple  
**Cons:** Ignores usage patterns completely  
**Use:** Simple queues, rarely used now

### 4. LRU-K

Remove based on the K-th most recent access (hybrid of LRU + frequency).

```
Example (K=2): Track last 2 accesses per item
Item A: [5 min ago, 10 min ago]
Item B: [2 min ago, 50 min ago]
Remove item with oldest K-th access
```

**Pros:** Better than LRU, adapts to patterns  
**Cons:** More complex  
**Use:** Database buffer pools (MySQL)

### 5. TTL (Time To Live)

Items expire after a fixed time, regardless of usage.

```
Item A added at 10:00 → TTL=5min → Expires at 10:05 (auto-remove)
```

**Pros:** Simple, predictable expiration  
**Cons:** Doesn't adapt to actual usage  
**Use:** Session data, short-lived data

### Eviction Strategies Comparison

| Strategy | Best For | Overhead | Popular |
|----------|----------|----------|---------|
| **LRU** | General purpose | Low | ⭐⭐⭐ |
| **LFU** | Hot/cold data separation | Medium | ⭐⭐ |
| **FIFO** | Simple cases | Very Low | ⭐ |
| **LRU-K** | Database caching | Medium-High | ⭐⭐ |
| **TTL** | Time-sensitive data | Low | ⭐⭐⭐ |

### Real-World Examples

- **Redis:** LRU (default), can switch to LFU or random
- **Browser cache:** LRU + TTL
- **MySQL buffer pool:** LRU-K
- **CDN caches:** TTL + LRU hybrid
- **Memcached:** LRU

**Golden rule:** **LRU is the safest default.** Use LFU if you have clearly "hot" data, TTL for time-sensitive data.

## 301 vs 302 Redirects for Data Analytics

### The Key Difference

**301 (Permanent):** Tells search engines "this URL moved forever" → they update records and point directly to new URL

**302 (Temporary):** Tells search engines "this URL moved temporarily" → they keep original URL in their records

### Why 302 is Better for Analytics

#### 1. Preserve Analytics History

With **301:**
```
Old URL: /products → gets removed from analytics
         → All traffic now shows under new URL
         → Lost visibility into old URL's performance
```

With **302:**
```
Old URL: /products → stays in analytics
         → Shows: "This redirected to /products-v2"
         → You see complete redirect path + traffic flow
```

#### 2. Track User Journey

**302 lets you see:**
- How much traffic uses the old URL (gives insight into user bookmarks, links)
- Conversion paths through the redirect
- Which traffic sources link to old URL
- User behavior across redirect

**301 hides this** because search engines stop indexing the old URL.

#### 3. Easy A/B Testing & Rollback

```
302 Redirect: Test new URL while keeping original
             → If new URL performs worse, switch back
             → Original URL's analytics intact

301 Redirect: Hard to rollback
             → Search engines already updated
             → Analytics data scattered
```

#### 4. Keep SEO Credit Separate

With **301:**
```
Old URL (100K backlinks) → All credit flows to new URL
                         → Hard to measure which URL performs better
```

With **302:**
```
Old URL (100K backlinks) → Keeps separate in search results
                         → Can compare performance of both URLs
                         → More data = better insights
```

### When to Use What

| Situation | Use | Why |
|-----------|-----|-----|
| **Temporary campaign/test** | 302 | Track separately, easy rollback |
| **URL migration (keep testing)** | 302 | See redirect funnel |
| **Permanent domain change** | 301 | SEO consolidation |
| **Site restructure (final)** | 301 | Clean slate, new URL is permanent |

### Real-World Example

```
Scenario: Moving /old-landing → /new-landing

With 302:
Analytics show:
├── /old-landing: 5K visitors → redirected
└── /new-landing: 5K visitors (via redirect)
You see the complete funnel!

With 301:
Analytics show:
└── /new-landing: 5K visitors
(Where did they come from? Lost!)
```

**Golden rule:** Use 302 by default for anything that's not permanent. You get better analytics + flexibility. Switch to 301 only when you're 100% sure the old URL is gone forever.
