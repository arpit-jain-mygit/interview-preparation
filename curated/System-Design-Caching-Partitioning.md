# System Design Caching Partitioning

Quick-reference notes — part of the System Design series. Converted from `System-Design-Notes.txt`.

## Caching

The cache is a high-speed storage layer that sits between the application and the original source of the data, such as a database, a file system, or a remote web service.
Types of Caching
1. In-memory caching
2. Disk caching
3. Database caching
4. Client-side caching
5. Server-side caching
6. CDN caching
7. DNS caching

Cache Strategies (WIRE - Write, Invalidation, Read, Eviction) - https://lnkd.in/p/dyJP_pCm
Read through - app - cache - DB (first check in DB, if not found store in cache)
Eviction - when its required - if expired (TTL) or Stale or space constraints

---


W - Write - TAB - Through, Arund, Back
I - Invalidation - PRBTS - Purge, Refresh, Ban, TTL, Stale-while-Revalidate
R - Read - AT - Aside, Through
E - Eviction - FIFO, LIFO, LRU, MRU, LFU, RR
```
╔═══════════════════════════╦══════════════════╦══════════════════════════════════════╦════════════════════════════════════════╦═════════════════════════════════════════╗
║ Strategy                  ║ Type             ║ What It Does                         ║ Memory Trick / Best For                ║ Decider                                 ║
╠═══════════════════════════╬══════════════════╬══════════════════════════════════════╬════════════════════════════════════════╬═════════════════════════════════════════╣
║ WRITE-THROUGH             ║ Write            ║ Write to cache AND DB simultaneously ║ 📋 Photocopy / Finance                 ║ Architect + Business Owner              ║
║ WRITE-AROUND              ║ Write            ║ Write to DB, skip cache              ║ ⏭️ Bypass / Streaming logs             ║ Architect                               ║
║ WRITE-BACK                ║ Write            ║ Write to cache only, DB later        ║ 📝 Sticky notes/ Social media          ║ Architect + Business Owner (risk)       ║
╠═══════════════════════════╬══════════════════╬══════════════════════════════════════╬════════════════════════════════════════╬═════════════════════════════════════════╣
║ PURGE                     ║ Invalidation     ║ Delete immediately (urgent)          ║ 🗑️ Trash NOW / Security breach         ║ Business Owner (when stale)             ║
║ REFRESH                   ║ Invalidation     ║ Fetch latest from server             ║ 🔄 Ctrl+R / Blog post update            ║ Architect + DevOps                      ║
║ BAN                       ║ Invalidation     ║ Delete by pattern/rules              ║ 🚫 Block by rules / User deleted        ║ Business Owner + Architect              ║
║ TTL                       ║ Invalidation     ║ Auto-delete after time expires       ║ ⏰ Expiration date / Weather            ║ Architect (time), Business (SLA)        ║
║ STALE-WHILE-REVALIDATE    ║ Invalidation     ║ Serve old + update silently          ║ 👻 Ghost + update / Netflix             ║ Architect (technical)                   ║
╠═══════════════════════════╬══════════════════╬══════════════════════════════════════╬════════════════════════════════════════╬═════════════════════════════════════════╣
║ READ-ASIDE                ║ Read             ║ App checks cache, handles mis~s       ║ 🤷 App responsible / E-commerce         ║ Architect (design flexibility)          ║
║ READ-THROUGH              ║ Read             ║ Cache auto-fetches on miss           ║ 🧠 Cache is boss / User sessions        ║ Architect (cache layer design)          ║
╠═══════════════════════════╬══════════════════╬══════════════════════════════════════╬════════════════════════════════════════╬═════════════════════════════════════════╣
║ FIFO                      ║ Eviction         ║ Remove oldest item                   ║ 🚪 Queue line / Oldest are stale        ║ Architect (data pattern analysis)       ║
║ LIFO                      ║ Eviction         ║ Remove newest item                   ║ 📚 Stack / Just-used won't be needed    ║ Architect (specific patterns)           ║
║ LRU                       ║ Eviction         ║ Remove least recently used item      ║ ⏱️ Dusty shelf / Haven't used = delete  ║ Architect (most common choice)          ║
║ MRU                       ║ Eviction         ║ Remove most recently used item       ║ 🔄 Opposite of LRU / Specific patterns  ║ Architect (niche use case)              ║
║ LFU                       ║ Eviction         ║ Remove least frequently used item    ║ 📊 Unpopular items / Popular stay       ║ Architect (hotspot data)                ║
║ RANDOM REPLACEMENT (RR)   ║ Eviction         ║ Remove random item                   ║ 🎲 Dice roll / Speed > logic            ║ Architect (performance tuning)          ║
╚═══════════════════════════╩══════════════════╩══════════════════════════════════════╩════════════════════════════════════════╩═════════════════════════════════════════╝

```

INVALIDATION vs EVICTION
```
╔═════════════════════════╦═════════════════════════════════════╦══════════════════════════════════════╗
║ Aspect                  ║ INVALIDATION                        ║ EVICTION                             ║
╠═════════════════════════╬═════════════════════════════════════╬══════════════════════════════════════╣
║ WHY remove?             ║ Data is STALE/WRONG                 ║ Cache is FULL (memory pressure)      ║
║ Trigger                 ║ Proactive (you decide)              ║ Reactive (system auto-triggers)      ║
║ Examples                ║ Purge, Refresh, Ban, TTL, SWR       ║ FIFO, LRU, LFU, MRU, LIFO, RR        ║
║ Who decides?            ║ Admin/Business logic/Timer          ║ Cache eviction policy                ║
║ What gets removed?      ║ Specific stale data                 ║ Any item (based on policy)           ║
║ Goal                    ║ Ensure DATA CORRECTNESS             ║ Manage MEMORY SPACE                  ║
║ Real-world analogy      ║ Expired milk → trash (stale)        ║ Full fridge → trash something (space)║
╚═════════════════════════╩═════════════════════════════════════╩══════════════════════════════════════╝

```


---

## Data Partitioning

Split a huge database into smaller independent chunks across multiple servers so each server handles its own data faster and in parallel.
Problem									=>	Solution
Too many rows, can't fit in one server" =>	Horizontal
Too many columns, accessing only a few" =>	Vertical
Both problems exist"					 => Hybrid

```
╔═════════════════════════════╦═════════════════╦═══════════════════════════════════════╦═════════════════════════════════════════════════════════════════╗
║ Partitioning Method         ║ Splits          ║ Memory Trick                          ║ Best For / Example                                              ║
╠═════════════════════════════╬═════════════════╬═══════════════════════════════════════╬═════════════════════════════════════════════════════════════════╣
║ HORIZONTAL PARTITIONING     ║ ROWS (Shards)   ║ 📊 Shard by ID range / Location       ║ Scale users / Shard by geo: US on Server 1, EU on Server 2     ║
║ (Sharding)                  ║                 ║    Different rows per server          ║ Pros: Load balancing, parallel processing                       ║
║                             ║                 ║ 🎯 Key: ID, location, date range     ║ Cons: Hot shard problem (uneven distribution)                   ║
╠═════════════════════════════╬═════════════════╬═══════════════════════════════════════╬═════════════════════════════════════════════════════════════════╣
║ VERTICAL PARTITIONING       ║ COLUMNS         ║ 📑 Split by data type / attributes    ║ Separate hot/cold data / E-commerce:                            ║
║                             ║                 ║    Different columns per server       ║ Server 1: Name, Email (hot)                                     ║
║                             ║                 ║ 🎯 Key: Attribute type (hot vs cold) ║ Server 2: Order history, Address (cold)                         ║
║                             ║                 ║                                       ║ Pros: Optimized access patterns                                 ║
║                             ║                 ║                                       ║ Cons: Need joins across servers (slow)                          ║
╠═════════════════════════════╬═════════════════╬═══════════════════════════════════════╬═════════════════════════════════════════════════════════════════╣
║ HYBRID PARTITIONING         ║ ROWS + COLUMNS  ║ 🔀 Horizontal THEN Vertical           ║ Large-scale e-commerce / First shard by geo,                    ║
║                             ║                 ║    (or vice versa)                    ║ then within each shard split hot/cold data                      ║
║                             ║                 ║ 🎯 Keys: ID range + Attribute type   ║ Pros: Best of both worlds (scale + optimization)               ║
║                             ║                 ║                                       ║ Cons: Most complex to manage & query                            ║
╚═════════════════════════════╩═════════════════╩═══════════════════════════════════════╩═════════════════════════════════════════════════════════════════╝

```

Quick Comparison Table
```
┌──────────────────────┬─────────────────────┬──────────────────────┬──────────────────┐
│ Aspect               │ Horizontal          │ Vertical             │ Hybrid           │
├──────────────────────┼─────────────────────┼──────────────────────┼──────────────────┤
│ Splits               │ Rows                │ Columns              │ Both             │
│ Sharding Key         │ ID, location, date  │ Data type/attribute  │ Both             │
│ Example              │ US users vs EU      │ Profile vs History   │ Region + Profile │
│ Load Balance         │ Good (if key chosen)│ N/A (not for scale)  │ Very good        │
│ Query Complexity     │ Simple (single DB)  │ Hard (joins needed)  │ Complex          │
│ Best for             │ Scale data volume   │ Optimize columns     │ Both             │
│ Problem              │ Hot shard if uneven │ Cross-shard joins    │ Management overhead
└──────────────────────┴─────────────────────┴──────────────────────┴──────────────────┘

```

When to Use What
HORIZONTAL PARTITIONING
✓ Users growing rapidly (millions of users)
✓ Geographic distribution needed
✓ Load balancing critical
✗ Don't use if: Data access patterns differ wildly

VERTICAL PARTITIONING
✓ Some columns accessed way more than others
✓ Want to optimize cache/speed for hot data
✓ Storage optimization needed
✗ Don't use if: Need frequent joins across columns

HYBRID PARTITIONING
✓ Large-scale apps (Netflix, Uber, Amazon)
✓ Both scale AND optimization needed
✗ Don't use if: Team can't handle complexity

```
╔════════════════════════════════╦═════════════════════════════════════════╦═════════════════════════════════╦═══════════════════════════════════════════════════════════════════════════╗
║ Data Partitioning              ║ How It Works                            ║ Relates to Method               ║ Trick / Pro / Con / Workaround                                            ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ ─── PARTITIONING METHODS ───   ║                                         ║                                 ║                                                                           ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ HORIZONTAL (Sharding)           ║ Split ROWS across servers               ║ –                               ║ 📊 Scale users / Pro: Load balance / Con: Hot shard risk                  ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ VERTICAL                        ║ Split COLUMNS across servers            ║ –                               ║ 📑 Hot vs cold data / Pro: Optimize columns / Con: Joins slow              ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ HYBRID                          ║ Split ROWS then COLUMNS                 ║ –                               ║ 🔀 Best of both / Pro: Scale + optimize / Con: Most complex               ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ ─── PARTITIONING CRITERIA ───   ║                                         ║                                 ║                                                                           ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ KEY/HASH-BASED                  ║ ID % 100 = server number                ║ –                               ║ 🔢 Uniform distribution / Con: Can't scale (use Consistent Hashing)      ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ LIST                            ║ Assign by value list (countries, regions)║ –                               ║ 📋 Geographic data / Con: Manual maintenance                             ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ ROUND-ROBIN                     ║ Row i → partition (i mod n)             ║ –                               ║ 🔄 Simple & uniform / Con: Ignores data semantics                        ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ COMPOSITE                       ║ Combine multiple criteria (hash+list)    ║ –                               ║ 🎯 Flexible / Con: Complex / Workaround: Directory lookup                ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ ─── COMMON PROBLEMS ───         ║                                         ║                                 ║                                                                           ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ JOINS & DENORMALIZATION         ║ Can't join across partitions            ║ VERTICAL + HORIZONTAL           ║ 🐌 High severity / Workaround: Denormalize DB (redundant data)            ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ REFERENTIAL INTEGRITY           ║ Foreign keys don't work cross-shard     ║ HORIZONTAL + VERTICAL          ║ 🚨 High severity / Workaround: App-level enforcement + cleanup jobs       ║
╠════════════════════════════════╬═════════════════════════════════════════╬═════════════════════════════════╬═══════════════════════════════════════════════════════════════════════════╣
║ REBALANCING (Hot Shard)         ║ Uneven data distribution / need rehash  ║ HORIZONTAL (primary)            ║ ⚠️  Medium severity / Workaround: Directory-based + zero-downtime migrate ║
╚════════════════════════════════╩═════════════════════════════════════════╩═════════════════════════════════╩═══════════════════════════════════════════════════════════════════════════╝

```

- Use Hash for numeric IDs (uniform) | Use List for categories (geographic)
- Horizontal scales users | Vertical optimizes columns | Hybrid does both
- Denormalize to fix joins | App-level to fix foreign keys | Directory to fix rebalancing

Indexes
📚 WHAT: Data structure (sorted table of contents) that points to actual data rows. Example: Library catalog sorted by title or author for fast lookups.
✅ BENEFIT: Dramatically speeds up READ queries. Essential for large datasets (terabytes) with small payloads by providing quick access without scanning all data.
⚠️  TRADE-OFF: Slows down WRITE operations (insert/update/delete) because index must be updated too. Avoid unnecessary indexes if dataset is write-heavy. Memory trick: Fast reads ↔ Slow writes.


---

## Consistent Hashing

❌ NAIVE HASHING PROBLEM:
hash(key) % total_servers → server number. When you add/remove server, ALL mappings break!
Example: hash("California") % 5 = 1 → Server 1. Add 1 server (6 total) → hash % 6 = different server. 
Massive data movement! 🔴
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ CONSISTENT HASHING SOLUTION:
Arrange servers in a RING (circular hash space). Each server owns a RANGE (token to next token - 1).
When server added/removed, only adjacent server's data moves. Minimal disruption! ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RING STRUCTURE:
Hash range 1-100, 4 servers. Server 1: 1-25, Server 2: 26-50, Server 3: 51-75, Server 4: 76-100.
Data placed by: hash(key) → find which range → which server owns that range.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOKENS & RANGES:
Token = Start of a range. Range = Token to (Next Token - 1). Example: Server 1 has token 1, range 1-25.
Hash function (MD5) on key determines which range → which server.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROBLEM: NON-UNIFORM DISTRIBUTION:
Fixed 1 token per server → uneven data distribution → HOTSPOTS (some servers overloaded).
Solution: Virtual Nodes (Vnodes) 🎯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIRTUAL NODES (VNODES):
Instead of 1 token per server, assign MULTIPLE smaller tokens (subranges) to each physical node.
Example: Server 1 owns ranges [1-6, 26-31, 51-56...] instead of just [1-25]. 
Result: More balanced distribution, easier rebalancing when nodes join/leave.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADVANTAGES OF VNODES:
1. Faster rebalancing (many nodes participate, not just 1 replica)
2. Heterogeneous clusters (powerful servers get more Vnodes, weak servers fewer)
3. Less hotspot risk (smaller ranges per server, more evenly distributed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA REPLICATION:
Replication Factor (RF) = how many nodes store the data. RF=3 means 3 copies on 3 different nodes.
Coordinator node stores data locally, then replicates to N-1 clockwise successor nodes on ring.
Example: Key K → Server 1 (primary), Server 2, Server 3 (replicas). All 3 have the data.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY CONSISTENT HASHING SCALES:
Add/Remove server? Only 1 adjacent server is affected (their token ranges shift). 
Naive hashing? ALL mappings recalculated, all data moved. Consistent hashing: Minimal data movement! 🎯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHEN ADDING A NEW SERVER:
Naive: All keys remapped to new server count → chaos.
Consistent: New server gets some Vnodes from existing servers (rebalance) → minimal disruption.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USE CASES:
✓ Distributed caching (add/remove cache servers dynamically)
✓ Database sharding (partition data across DB servers)
✓ Load balancing (distribute requests across servers)
✓ Any system needing data replication & high availability

Real examples: Amazon Dynamo, Apache Cassandra, Redis Cluster
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERVIEW ANSWER:
"Use Consistent Hashing because:
```
 ├─ Server added? Only 1 adjacent server affected (O(n/k) data movement, not O(n))
 ├─ Replication built-in (clockwise replicas on ring)
 ├─ Vnodes balance load (no hotspots)
 └─ Handles scale gracefully (dynamic add/remove)"

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEMORY TRICK:
Consistent = CON-SISTENT-ENT
```
├─ "Consistent" = same behavior (add/remove servers, still same mapping for unaffected keys)
├─ "Ring" = circular arrangement (wraps around)
├─ "Vnodes" = many small slices (balanced like pizza)
└─ "Replication" = copies on clockwise neighbors (high availability)

```


---

## Bloom Filters

BLOOM FILTERS — PROBLEM FIRST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 THE PROBLEM (Business/Technical):

SCENARIO 1: GOOGLE SAFE BROWSING
Google has 1 BILLION malicious URLs. User clicks a link, browser needs to check:
"Is this URL safe or malicious?"

Problem:
```
├─ Query Google server every time? → Slow (network latency)
├─ Store all 1B URLs locally? → Impossible (100GB+ data)
├─ Use hash set? → Still 10-20GB memory per browser
├─ Check database? → Too slow (millions of queries/sec)
└─ Current solution = broken or expensive

```

😫 USER PAIN:
```
├─ Browser freezes checking if URL is safe
├─ Network calls for every link = slow browsing
├─ Server gets hammered with 100M requests/sec = expensive

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCENARIO 2: DATABASE OPTIMIZATION
Database has 1 BILLION user records. Application needs to check:
"Does this user ID exist?"

Problem:
```
├─ Query database? → 1-10ms latency per query (SLOW)
├─ Store all IDs in memory? → 10-20GB RAM needed (EXPENSIVE)
├─ Hash set in memory? → Still huge memory overhead
└─ Current = Pick: Speed OR Memory, can't have both

```

😫 BUSINESS IMPACT:
```
├─ Slow lookups = slow app = users leave
├─ More memory = bigger servers = higher AWS bills ($10k/month)
├─ Database overloaded = downtime = lost revenue

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCENARIO 3: DUPLICATE USERNAME CHECK
User types username → Check "Is it taken?" (millions of users)

Problem:
```
├─ Query database? → "Wait 1 second..." (too slow for real-time UX)
├─ Store all usernames in memory? → 5-10GB for millions of users
├─ Every keystroke triggers database query? → Server on fire 🔥
└─ Current = Users get frustrated waiting

```

😫 USER EXPERIENCE:
```
├─ "Type name... wait... wait... finally get answer" (bad UX)
├─ Server can't handle all the queries
├─ Application is slow and expensive

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE DILEMMA:

```
┌──────────────────────────────┬──────────────────┬──────────────────┐
│ Approach                     │ Speed            │ Memory           │
├──────────────────────────────┼──────────────────┼──────────────────┤
│ Query database every time    │ 🐌 SLOW (1ms)    │ 🟢 Tiny (DB only)│
│ Store all in memory (HashMap)│ ⚡ FAST (1μs)    │ 🔴 HUGE (20GB)   │
│ No storage, query DB         │ 🐌 SLOW          │ 🟢 Tiny          │
└──────────────────────────────┴──────────────────┴──────────────────┘

```

You must choose: Speed OR Memory. You can't have BOTH.

This is the actual problem Bloom Filters solve! 🎯

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ BLOOM FILTER SOLUTION:

Bloom Filter = "Quick gatekeeper that sometimes lies about YES but NEVER lies about NO"

```
┌──────────────────────────────────────────────────────────────┐
│                    BLOOM FILTER                              │
├──────────────────────────────────────────────────────────────┤
│ ✓ Super FAST lookup (microseconds)                           │
│ ✓ Tiny MEMORY (1MB for billion items!)                       │
│ ✓ Trade-off: Occasional false positives (~1-2%)              │
└──────────────────────────────────────────────────────────────┘

```

Example: Check if URL is malicious

BEFORE Bloom Filter:
User clicks URL → Query Google server → Wait 100ms → Check if safe
Problem: 100M users × 100 clicks/day = 100 billion queries/day = EXPENSIVE

AFTER Bloom Filter:
User clicks URL → Check Bloom Filter (1μs) → "Definitely safe" or "Maybe risky"
```
├─ If "Definitely safe" → User browses immediately (save server query)
├─ If "Maybe risky" → Query server for verification (rare)

```
Result: Save 99% of server queries, instant response to user

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOW SMALL IS BLOOM FILTER?

📊 Store 1 BILLION usernames in memory:

Hash Set (HashMap):
```
├─ 1 string = ~30 bytes average
├─ 1B strings = 30GB RAM
└─ Cost: $300/month for memory alone

```

Bloom Filter:
```
├─ 1 bit per possible item
├─ 1B items = 1 billion bits = ~125MB
├─ With 2% false positive = ~1MB!
└─ Cost: negligible memory

```

THAT'S 30,000x SMALLER! 🚀

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REAL-WORLD COMPARISON:

SCENARIO: Check username availability (1M usernames)

❌ BAD APPROACH (Query DB):
  User types "john123" → Query database → Wait 5ms → "Taken"
  User types "john124" → Query database → Wait 5ms → "Available"
  Result: Each keystroke = 5ms delay (BAD UX)

❌ WORSE APPROACH (Store all in memory):
  Store 1M usernames in HashMap = 30MB RAM per server
  10 servers = 300MB (scales as users grow)
  Result: RAM costs balloon with each new user

✅ BEST APPROACH (Bloom Filter):
  Store 1M usernames in Bloom Filter = 1MB!
  User types "john123" → Check Bloom Filter (1μs) → "Maybe taken"
  → Query DB for exact answer (acceptable delay)
  User types "john124" → Check Bloom Filter (1μs) → "Definitely NOT taken"
  → Instantly say "Available!" (skip DB query)
  Result: Instant UX + tiny memory + reduced DB load

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE TRADE-OFF (The KEY):

Bloom Filter accepts FALSE POSITIVES to get:
```
├─ Super fast lookups
├─ Tiny memory usage
└─ Better scalability

```

What does this mean?

Sometimes Bloom Filter says "Maybe exists" when it DOESN'T actually exist.
This is ACCEPTABLE in most business cases because:

Example: Malicious URL check
```
├─ False positive: "URL is maybe malicious" (it's actually safe)
├─ Cost: 1 extra server query (acceptable)
├─ Benefit: Save 99% of server queries

```

Example: Username availability
```
├─ False positive: "Username maybe taken" (it's actually available)
├─ Cost: User sees "checking..." and gets actual answer in 5ms (acceptable)
├─ Benefit: Skip DB query 99% of time

```

Example: Duplicate email check
```
├─ False positive: "Email maybe exists" (it doesn't)
├─ Cost: User sees verification step (annoying but acceptable)
├─ Benefit: Avoid 99% of expensive database lookups

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHEN FALSE POSITIVES ARE NOT ACCEPTABLE:

❌ Financial transactions: "Do you have $100?" — Cannot be wrong!
❌ Medical diagnosis: "Do you have disease?" — Cannot be wrong!
❌ Legal: "Is this contract valid?" — Cannot be wrong!

These need 100% accuracy, so Bloom Filter NOT suitable.

✅ When false positives ARE acceptable:

✓ "Is this URL safe?" — Extra verification OK
✓ "Is username taken?" — Checking DB is fine
✓ "Did user see this video?" — Showing repeat is OK
✓ "Is this IP blocked?" — Extra check is fine

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BUSINESS VALUE:

💰 Cost savings:
```
├─ Reduce database queries by 80-99%
├─ Save ~$100k/month in server costs
├─ Reduce cloud infrastructure by 10-20x

```

⚡ Performance:
```
├─ Instant response (microseconds vs milliseconds)
├─ Better user experience
├─ Improved app responsiveness

```

📈 Scalability:
```
├─ Handle 100x more users with same infrastructure
├─ Grow without adding servers
├─ Predictable costs

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NOW LET'S LOOK AT HOW IT WORKS:

🎯 WHAT IS A BLOOM FILTER?
A probabilistic data structure that answers: "Is this item in the set?" SUPER FAST with minimal memory.
Answer: "Definitely NO" or "MAYBE YES" (never false negatives, but has false positives).

Memory trick: "Quick bouncer" — bouncer checks guest list instantly, sometimes lets fakes through.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW BLOOM FILTERS WORK — DETAILED EXPLANATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: CREATE BIT ARRAY (Empty)

What is a bit array?
```
├─ Array of 0s and 1s (not storing data, just yes/no positions)
├─ Each position = 1 bit (tiny!)
├─ Example: 16-bit array

```

    Index:  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    Bits:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
Why so small?
```
├─ 1 bit per position (not 30 bytes like a string)
├─ 1 million items = 1 million bits = ~125 KB
├─ Hash set would be = 30 MB
├─ Bloom Filter is 240x SMALLER!

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: CHOOSE HASH FUNCTIONS

What are hash functions?
```
├─ Functions that convert input → random number
├─ Example: hash1("alice") = 5, hash2("alice") = 12
├─ Same input always gives same output (deterministic)

```

Why multiple hash functions?
```
├─ 1 hash function = high collision probability
├─ Multiple functions = spread items across array
├─ Usually 2-4 hash functions (we'll use 2)

```

Example hash functions:
    hash1(x) = (x * 31) % 16
    hash2(x) = (x * 37) % 16

Try it:
    hash1("alice") = (97*31) % 16 = 3007 % 16 = 15
    hash2("alice") = (97*37) % 16 = 3589 % 16 = 5

So "alice" will set bits at positions 15 and 5.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: ADD ITEM TO BLOOM FILTER

Adding "alice":

Step 1: Calculate hash values
    hash1("alice") = 15
    hash2("alice") = 5

Step 2: Set those bit positions to 1
    BEFORE: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    Set bit[5] = 1:
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
           ↑ position 5
    
    Set bit[15] = 1:
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                                                   ↑ position 15
    
    AFTER: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

That's it! "alice" is now in the Bloom Filter.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: ADD ANOTHER ITEM

Adding "bob":

Step 1: Calculate hash values
    hash1("bob") = (98*31) % 16 = 3038 % 16 = 14
    hash2("bob") = (98*37) % 16 = 3626 % 16 = 10

Step 2: Set bit[14] and bit[10] to 1
    BEFORE: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    
    Set bit[10] = 1:
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
                                  ↑ position 10
    
    Set bit[14] = 1:
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
                                              ↑ position 14

Now both "alice" and "bob" are in the filter.

Current state:
    Positions with 1s: [5, 10, 14, 15]
    "alice" uses: [5, 15]
    "bob" uses: [10, 14]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: QUERY - IS "ALICE" IN FILTER?

Question: Is "alice" in the Bloom Filter?

Step 1: Calculate hash values for "alice"
    hash1("alice") = 15
    hash2("alice") = 5

Step 2: Check if BOTH positions are 1
    Current array: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
                     0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    
    Check bit[5]?  → 1 ✓
    Check bit[15]? → 1 ✓
    
    RESULT: "MAYBE IN FILTER"

Why "MAYBE"?
```
├─ Both bits are 1, which is good
├─ But other items could have set those same bits
├─ So we can't be 100% sure (but "alice" WAS added, so high probability)

```

Key insight:
    If ANY bit is 0 → Item DEFINITELY NOT in filter
    If ALL bits are 1 → Item MAYBE in filter

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 6: QUERY - IS "CHARLIE" IN FILTER?

Question: Is "charlie" in the Bloom Filter?

Step 1: Calculate hash values for "charlie"
    hash1("charlie") = (99*31) % 16 = 3069 % 16 = 13
    hash2("charlie") = (99*37) % 16 = 3663 % 16 = 15

Step 2: Check if BOTH positions are 1
    Current array: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
                     0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    
    Check bit[13]? → 0 ✗ (NOT 1!)
    Check bit[15]? → 1 ✓
    
    RESULT: "DEFINITELY NOT IN FILTER"

Why so certain?
```
├─ At least ONE bit is 0
├─ If "charlie" was in the filter, BOTH bits would be 1
├─ Since one is 0, "charlie" was NEVER added
├─ 100% certain it's not there! ✓

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 7: FALSE POSITIVE EXAMPLE

Question: Is "david" in the Bloom Filter?

Step 1: Calculate hash values for "david"
    hash1("david") = (100*31) % 16 = 3100 % 16 = 12
    hash2("david") = (100*37) % 16 = 3700 % 16 = 4

Wait, let me recalculate to get a false positive...
Actually, let me use different hash functions:
    hash1("david") = 14
    hash2("david") = 10

Step 2: Check if BOTH positions are 1
    Current array: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1]
                     0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    
    Check bit[14]? → 1 ✓ (Set by "bob")
    Check bit[10]? → 1 ✓ (Set by "bob")
    
    RESULT: "MAYBE IN FILTER"

But here's the thing:
```
├─ "david" was NEVER added
├─ Yet both its hash positions (14, 10) are 1
├─ Because "bob" happened to set those same bits!
├─ This is a FALSE POSITIVE ❌

```

What happened?
    "david" uses positions: [14, 10]
    "bob" uses positions: [14, 10]
    
    By coincidence, they use the SAME positions!
    So Bloom Filter thinks "david" is in the set (but it's not)

This is why we get false positives → multiple items can map to same bits

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 8: WHY NO FALSE NEGATIVES?

False Negative = Bloom Filter says NO, but item WAS added

Can this happen?

Remember the rule:
    If ANY bit is 0 → Item DEFINITELY NOT in filter
    If ALL bits are 1 → Item MAYBE in filter

If we added "alice" (set bits 5 and 15 to 1), then:
    When we query "alice": Check bits 5 and 15
    Both are still 1 (we never change them back to 0)
    So Bloom Filter will say "MAYBE IN FILTER"

False negative can ONLY happen if:
```
    ├─ We added item (set bits to 1)
    └─ But then those bits turned back to 0

```

But bits NEVER turn back to 0 in Bloom Filter!
```
    ├─ We can only SET bits to 1
    ├─ We never UNSET bits back to 0
    └─ Therefore FALSE NEGATIVES = IMPOSSIBLE ✓

```

This is why Bloom Filters are reliable for "NO" answers.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY TABLE:

```
┌─────────────────────┬─────────────────────┬──────────────────────┐
│ Query Result        │ Accuracy            │ Action               │
├─────────────────────┼─────────────────────┼──────────────────────┤
│ "DEFINITELY NOT"    │ 100% certain ✓      │ Skip expensive check │
│ (Any bit is 0)      │ ZERO false negatives│ (No database query)  │
├─────────────────────┼─────────────────────┼──────────────────────┤
│ "MAYBE IN FILTER"   │ ~98-99% certain     │ Do verification      │
│ (All bits are 1)    │ Could be false pos  │ (Query database)     │
└─────────────────────┴─────────────────────┴──────────────────────┘

```

EXAMPLE WORKFLOW:

1. User tries username "alice"
```
   ├─ Check Bloom Filter: bits [5, 15] → both 1
   └─ Result: "MAYBE taken"
   └─ Action: Query database (confirm if taken)

```

2. User tries username "charlie"
```
   ├─ Check Bloom Filter: bits [13, 15] → 13 is 0
   └─ Result: "DEFINITELY NOT taken"
   └─ Action: Skip database query, instantly tell user "Available!" ✓

```

BENEFIT:
```
├─ For "charlie" → Saved database query (instant response)
├─ For "alice" → Same as before (acceptable delay for verification)
└─ 50% of queries saved in this example (more with more items)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY DOES THIS WORK? (The Magic)

Regular Hash Set:
    Store actual strings in memory
    {"alice", "bob"} = 60 bytes
    1 million users = 30 MB

Bloom Filter:
    Store only "fingerprints" (bit positions)
    Instead of "alice" → just mark bits [5, 15]
    1 million users = ~125 KB (240x smaller!)

The Trade-off:
```
    ├─ Loss: Can't be 100% sure about "MAYBE" answers
    ├─ Gain: Tiny memory, instant lookup
    └─ Result: Acceptable for most use cases

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REAL CODE LOGIC:

ADD ITEM:
    for each hash_function in [hash1, hash2]:
        index = hash_function(item) % array_size
        bits[index] = 1
    # Done! Item stored with just 2 bit flips

QUERY ITEM:
    for each hash_function in [hash1, hash2]:
        index = hash_function(item) % array_size
        if bits[index] == 0:
            return "DEFINITELY NOT in set"
    return "MAYBE in set"

VISUAL:

Adding "alice":     Query "alice":        Query "charlie":
[0000000000000000]  [0000010000010001] → [0000010000010001]
     ↓              Check bit 5: 1 ✓  Check bit 13: 0 ✗
Set bit 5           Check bit 15: 1 ✓  → "DEFINITELY NOT"
Set bit 15          → "MAYBE YES"
[0000010000010001]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY TAKEAWAYS:

1. Uses BIT ARRAY (not actual data)
```
   ├─ Each item = 2-4 bit positions set to 1
   └─ Rest stays 0

```

2. Uses MULTIPLE HASH FUNCTIONS
```
   ├─ hash1(item) → position 1
   ├─ hash2(item) → position 2
   └─ Spread items across array

```

3. QUERIES ARE INSTANT
```
   ├─ Check a few bits (microseconds)
   └─ vs Database query (milliseconds)

```

4. ANSWERS ARE PROBABILISTIC
```
   ├─ "NO" = 100% accurate (never wrong)
   ├─ "MAYBE" = ~99% accurate (rare false positives)
   └─ This is the acceptable trade-off

```

5. MEMORY USAGE TINY
```
   ├─ Bits vs objects
   ├─ 240x smaller than hash set
   └─ Can store billions in few MB

```


KEY INSIGHT:

✓ If ANY bit is 0 → Item DEFINITELY not in set (100% accurate NO)
✓ If ALL bits are 1 → Item MAYBE in set (might be false positive)

FALSE POSITIVE: System says "YES" but item not actually added.
FALSE NEGATIVE: Never happens (if all bits are 1, probability high item was added).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:

PROBLEM: Need to check membership in HUGE set (fast + memory efficient)
SOLUTION: Bloom Filter (accept rare false positives for speed + memory)
RESULT: 1000x smaller memory, instant lookup, 80-99% fewer database queries

WHEN TO USE:
✓ Pre-filter before expensive operations (DB query, network call)
✓ When false positives acceptable
✓ When memory constrained
✓ When speed critical

REAL EXAMPLES:
✓ Google Safe Browsing (malicious URLs)
✓ Database index optimization
✓ Cache miss prevention
✓ Duplicate detection (emails, usernames)
✓ Spam filtering


---

## Diff b/w CDN and Cache

```
┌─────────────────┬──────────────────────┬──────────────────────┐
│ Aspect          │ Cache                │ CDN                  │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Problem         │ Slow computation/DB  │ Slow geography       │
│ Solution        │ Store in memory      │ Serve from edge      │
│ Speed gain      │ 100x (100ms→1ms)     │ 20x (200ms→10ms)     │
│ Technology      │ Redis, Memcached     │ Cloudflare, AWS CF   │
│ Location        │ Same datacenter      │ Worldwide edges      │
│ Best for        │ Dynamic data         │ Static files         │
│ Cost            │ RAM                  │ Per bandwidth        │
└─────────────────┴──────────────────────┴──────────────────────┘

```

Example:
- Cache: DB query (100ms) → cached (1ms)
- CDN: Image from Germany (200ms) → served from Tokyo edge (10ms)


---

## When CDN serves static content, how is it faster when user needs dynamic content as well, so dynamic content srving becomes weakest link?

```
┌─────────────────┬──────────────────────┬──────────────────────┐
│ Aspect          │ Cache                │ CDN                  │
├─────────────────┼──────────────────────┼──────────────────────┤
│ Problem         │ Slow computation/DB  │ Slow geography       │
│ Solution        │ Store in memory      │ Serve from edge      │
│ Speed gain      │ 100x (100ms→1ms)     │ 20x (200ms→10ms)     │
│ Technology      │ Redis, Memcached     │ Cloudflare, AWS CF   │
│ Location        │ Same datacenter      │ Worldwide edges      │
│ Best for        │ Dynamic data         │ Static files         │
│ Cost            │ RAM                  │ Per bandwidth        │
│ Latency cut     │ DB query → Memory    │ Far server → Near    │
│ Invalidation    │ TTL, manual purge    │ Auto + manual purge  │
│ Data type       │ Computed results     │ Images, videos, CSS  │
│ Example         │ User profile lookup  │ Image from CDN edge  │
└─────────────────┴──────────────────────┴──────────────────────┘

```

TL;DR:
Cache = Fix slow operations (DB, compute)
CDN   = Fix slow geography (far servers)
Both  = Complete optimization

ARCHITECTURE: CDN + CACHE

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS (Global)                          │
│                    (USA, Europe, Asia)                          │
└────────────┬──────────────────────────┬──────────────────────────┘
             │                          │

```
             ▼                          ▼
```
    ┌─────────────────┐       ┌─────────────────┐
    │ CDN Edge USA    │       │ CDN Edge Asia   │
    │ (Static files)  │       │ (Static files)  │
    │ - images        │       │ - images        │
    │ - CSS, JS       │       │ - CSS, JS       │
    │ ⚡ 10ms         │       │ ⚡ 10ms         │
    └────────┬────────┘       └────────┬────────┘
             │                         │
             └──────────────┬──────────┘
                            │

```
                    (network latency ~100-200ms)
```
                            │

```
                            ▼
```
            ┌───────────────────────────────┐
            │    ORIGIN SERVER (Germany)    │
            │                               │
            │  ┌───────────────────────┐   │
            │  │  CACHE LAYER (Redis)  │   │
            │  │                       │   │
            │  │ • User profiles       │   │
            │  │ • Feed results        │   │
            │  │ • API responses       │   │
            │  │ ⚡ 1ms               │   │
            │  └───────────┬───────────┘   │
            │              │               │
            │              ▼               │
            │  ┌───────────────────────┐   │
            │  │      DATABASE         │   │
            │  │ (PostgreSQL, MySQL)   │   │
            │  │ ⏱️ 50-100ms           │   │
            │  └───────────────────────┘   │
            └───────────────────────────────┘

```


REQUEST FLOW EXAMPLE: User in USA loads webpage
```
═══════════════════════════════════════════════════════════════

```

1. Browser requests HTML
```
   └─→ USA CDN Edge → 10ms → Gets from origin → 100ms delay
   └─→ Returns HTML (110ms)

```

2. Browser requests image1.jpg (parallel)
```
   └─→ USA CDN Edge → 10ms → Already cached! ✓
   └─→ Returns image (10ms)

```

3. Browser requests /api/feed (parallel)
```
   └─→ Origin server
   └─→ Check Redis cache → HIT! ✓
   └─→ Returns cached feed (1ms)

```

4. Browser requests style.css (parallel)
```
   └─→ USA CDN Edge → 10ms → Already cached! ✓
   └─→ Returns CSS (10ms)

```

Total time (all parallel): ~110ms
Without CDN+Cache: ~400ms+


REQUEST FLOW: Cold cache (first user)
```
═══════════════════════════════════════════════════════════════

```

1. /api/feed requested
2. Origin checks Redis → MISS ❌
3. Query database → 100ms
4. Store in Redis
5. Return to user (100ms)

Next request (same data):
1. /api/feed requested
2. Origin checks Redis → HIT ✓
3. Return cached (1ms)

Benefit: 100x faster for repeat users!


TRAFFIC FLOW DIAGRAM
```
═══════════════════════════════════════════════════════════════

```

WITHOUT CDN+CACHE:
```
User1 ────┐
User2 ────┼──→ Origin (100% load) ⚠️ Bottleneck
User3 ────┘

```

WITH CDN+CACHE:
```
User1 ──→ CDN (static) ──┐
User2 ──→ CDN (static) ──┼──→ Origin (20% load) ✓
User3 ──→ Cache (API) ───┤   No bottleneck
User4 ──→ CDN (static) ──┘

```


EXAMPLE: Netflix architecture
```
═══════════════════════════════════════════════════════════════

```

Static Layer (CDN):
```
├─ Video file (1GB) → Serve from nearest edge → 10ms
├─ Poster image → Serve from nearest edge → 10ms
├─ CSS/JS bundles → Serve from nearest edge → 10ms
└─ Result: Same speed for USA/Europe/Asia users ✓

```

Dynamic Layer (Cache):
```
├─ User profile → Redis (1ms)
├─ Recommendation list → Redis (1ms)
├─ Watch history → Redis (1ms)
└─ Result: No database queries, instant responses ✓

```

Database Layer:
```
├─ Write operations only
├─ Reads serve from cache
└─ Result: Database handles 100x more users ✓

```


CAPACITY COMPARISON
```
═══════════════════════════════════════════════════════════════

```

Without CDN/Cache:
```
└─ 1 origin server, 1M users → Can handle ~100 concurrent
└─ Need 10,000 servers or expensive origin

```

With CDN only:
```
└─ CDN handles 90% static traffic
└─ 1 origin server → Can handle ~1,000 concurrent
└─ Need 1,000 servers (10x better)

```

With CDN + Cache:
```
└─ CDN handles 90% static
└─ Cache handles 50% dynamic
└─ 1 origin server → Can handle ~10,000 concurrent
└─ Need 100 servers (100x better) ✓✓

```

COST BREAKDOWN
```
═══════════════════════════════════════════════════════════════

```

Server costs (handling 1M users):
```
├─ No CDN/Cache: 10,000 servers × $100 = $1M/month
├─ CDN only: 1,000 servers × $100 = $100k/month
├─ CDN + Cache: 100 servers × $100 = $10k/month ✓
└─ CDN bandwidth: ~$50k/month
└─ TOTAL with CDN+Cache: ~$60k/month (vs $1M)

```

Key insight: CDN + Cache work on different layers, so together they handle both static AND dynamic bottlenecks. Neither alone is enough for scale.


---

## How a something can be cahced at client side, who decides what to be cached?

CLIENT-SIDE CACHING
```
═══════════════════════════════════════════════════════════════

```

Who decides: SERVER (via HTTP headers)

Browser receives response:
```
├─ Server header: "Cache-Control: max-age=3600"
├─ Browser reads header
├─ Stores response locally
├─ Next request for same URL → serve from cache
└─ No server call needed ✓

```


HTTP CACHE HEADERS
```
═══════════════════════════════════════════════════════════════

```

Server sends:
Cache-Control: max-age=3600
```
├─ Cache for 3600 seconds
├─ After 3600s, fetch fresh

```

Cache-Control: no-cache
```
├─ Cache, but validate with server first
├─ Server: "Still fresh? Use cache"
└─ Server: "Stale? Fetch new"

```

Cache-Control: no-store
```
├─ Don't cache at all
└─ Fetch every time

```

ETag: "abc123"
```
├─ Unique identifier for resource
├─ Browser: "Do you have abc123?"
├─ Server: "Yes, use cache" (304 Not Modified)
└─ No body transferred, bandwidth saved ✓

```


FLOW
```
═══════════════════════════════════════════════════════════════

```

First request:
```
├─ Client: GET /image.jpg
├─ Server: [image data] + Cache-Control: max-age=3600
├─ Browser: Stores in disk cache

```

Second request (within 3600s):
```
├─ Browser: Checks cache first
├─ Found! Return from disk
├─ Zero server call ✓

```

Third request (after 3600s):
```
├─ Cache expired
├─ Fetch fresh from server

```


---

