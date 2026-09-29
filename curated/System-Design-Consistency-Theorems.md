# System Design Consistency Theorems

Quick-reference notes — part of the System Design series. Converted from `System-Design-Notes.txt`.

## PARTITION IN CAP THEOREM

🚫 WHAT "PARTITION" MEANS:

PARTITION = Network COMMUNICATION BREAK between nodes
```
├─ Both servers are UP and running ✅
├─ Both have power ✅
├─ But they CAN'T TALK to each other ❌
└─ They are "partitioned" (separated/isolated from each other)

```

NOT about:
❌ Data partitioning (sharding) - that's splitting data across servers
❌ Hard drive partitions - that's disk storage
✅ NETWORK partition - cable cut, router down, firewall blocks traffic

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VISUAL EXAMPLE:

NORMAL STATE (No partition):
```
┌──────────────┐          ┌──────────────┐
│  Server A    │ ◀────► │  Server B    │
│              │  Network   │              │
│ Data: $100   │  Connected  │ Data: $100   │
└──────────────┘          └──────────────┘

```
Both can talk ✅

PARTITION (Network broken):
```
┌──────────────┐          ┌──────────────┐
│  Server A    │  X  X  X  │  Server B    │
│              │ BROKEN     │              │
│ Data: $100   │ CONNECTION │ Data: $100   │
└──────────────┘          └──────────────┘

```
Both up, can't talk ❌

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REAL-WORLD SCENARIOS (Partition):

1️⃣ NETWORK CABLE CUT
```
   ├─ Server A in NYC data center
   ├─ Server B in LA data center
   ├─ Network cable between them cut
   └─ Both running fine, just can't communicate

```

2️⃣ ROUTER FAILURE
```
   ├─ Server A connected to Router 1
   ├─ Server B connected to Router 2
   ├─ Routers can't reach each other
   └─ Servers isolated

```

3️⃣ FIREWALL BLOCKS TRAFFIC
```
   ├─ Server A trying to reach Server B
   ├─ Firewall rule added: BLOCK all traffic
   ├─ Servers alive but isolated
   └─ Partition created

```

4️⃣ DNS FAILURE
```
   ├─ Server A can't resolve Server B's address
   ├─ Can't reach it, even though it exists
   └─ Practical partition

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY INSIGHT:

A partition is NOT:
```
├─ Server crash (one node is down)
├─ Data loss (disk failure)
├─ Slow network (still communicating, just slow)
└─ Power loss (server actually dead)

```

A partition IS:
```
├─ Nodes are healthy ✅
├─ But isolated from each other ❌
├─ Can't exchange messages
└─ "Split brain" - each thinks other is dead

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BANK EXAMPLE (Partition):

SCENARIO: Network between Bank A (NYC) & Bank B (LA) breaks

NORMAL (No partition):
User deposits $100 at Bank A
```
└─ Bank A: "Verified by Bank B" → $100 added
└─ Both see $100 ✅

```

PARTITION (Network breaks):
User deposits $100 at Bank A
```
├─ Bank A can't reach Bank B
├─ Bank A: "What do I do?"
│  Option 1 (CP): Reject deposit (wait for connection)
│  Option 2 (AP): Accept anyway (sync later, might conflict)
└─ Bank A & B now disagree on balance ❌

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"PARTITION TOLERANCE" MEANS:

System continues operating DESPITE a partition existing.
```
├─ CP: "Operate, but reject requests" (consistent but unavailable)
├─ AP: "Operate, accept requests" (available but inconsistent)
└─ Both are "partition tolerant" (system doesn't crash)

```

NOT partition tolerant would be: "Network breaks → ENTIRE system crashes" ❌

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEMORY TRICK:

"Partition" = "Split" = Two parts of system separated
Not communicating ≠ Not working

Think of restaurant split by wall:
```
├─ Kitchen 1 & Kitchen 2 same restaurant
├─ Wall blocks them (partition)
├─ Both kitchens work fine
└─ But can't sync menu/prices (separated)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK SUMMARY:

Partition = Network communication break between healthy nodes
```
├─ Both nodes UP ✅
├─ Both alive ✅
├─ But isolated ❌
└─ Can't sync data ❌

```

CAP says: "When partition happens, choose Consistency OR Availability"


---

## CAP Theorem

🎯 CORE CONCEPT (Pick 2 out of 3):
You CANNOT have all 3. Network partitions WILL happen. So you choose: CP or AP.

```
                    ┌─────────────────────────────────────────┐
                    │ CONSISTENCY (C)                         │
                    │ All nodes see SAME data at SAME time    │
                    └─────────────────────────────────────────┘

```
                                      OR
```
                    ┌─────────────────────────────────────────┐
                    │ AVAILABILITY (A)                        │
                    │ System ALWAYS responds (even if broken)  │
                    └─────────────────────────────────────────┘
                    
                    ┌─────────────────────────────────────────┐
                    │ PARTITION TOLERANCE (P)                 │
                    │ Network failures don't crash system      │
                    └─────────────────────────────────────────┘

```
                    (You MUST have this in distributed systems)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3 PROPERTIES EXPLAINED:

✅ CONSISTENCY (C) = All users see same data everywhere
   Example: Bank transfer = both sides updated together. No half-updates.
   
✅ AVAILABILITY (A) = System always responds (never says "I'm down")
   Example: Facebook stays up even if servers crash. Returns something (maybe old data).
   
✅ PARTITION TOLERANCE (P) = Network breaks but system keeps working
   Example: Network cable cut between Server 1 & Server 2. Both keep serving requests.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE CHOICE (In case of network partition):

🔴 CP (Consistency + Partition Tolerance)
```
   ├─ Sacrifice: Availability
   ├─ If network breaks: Stop serving requests (stay consistent)
   ├─ Example: Banks, payment systems, financial data
   ├─ Real DB: MongoDB, HBase, BigTable (strong consistency)
   └─ User sees: "Service temporarily unavailable" (but data is 100% correct)

```

🟢 AP (Availability + Partition Tolerance)
```
   ├─ Sacrifice: Consistency
   ├─ If network breaks: Keep serving (even if data is stale)
   ├─ Example: Social media, Netflix, DynamoDB
   ├─ Real DB: Cassandra, DynamoDB, CouchDB (eventual consistency)
   └─ User sees: Old data (but system is always up)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REAL-WORLD ANALOGY (Restaurant):

SCENARIO: Network breaks between Kitchen 1 & Kitchen 2 (2 kitchens can't talk)

CP CHOICE (Consistency):
```
├─ Decision: "Close both kitchens until network fixed"
├─ Why: Can't guarantee same menu/prices on both kitchens
├─ User sees: "Restaurant closed temporarily" (but guaranteed correctness)
└─ Example: Bank (can't process if unsure of balance)

```

AP CHOICE (Availability):
```
├─ Decision: "Keep both kitchens open, serve independently"
├─ Why: Kitchen 1 has old menu, Kitchen 2 has new menu (inconsistent)
├─ User sees: Different prices depending which kitchen (but can always order)
└─ Example: Facebook (different regions might show old likes count)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE: BANK TRANSFER ($100, Server A → Server B, Network breaks)

CP SYSTEM (Consistency preferred):
```
  ┌────────────────────────────────────────┐
  │ Network breaks before both confirm      │
  ├────────────────────────────────────────┤
  │ Decision: ABORT both, no transfer      │
  │ Why: Can't guarantee both see same $   │
  │ User sees: "Transfer failed" ❌         │
  │ But: Money is safe, data is correct ✅ │
  └────────────────────────────────────────┘

```

AP SYSTEM (Availability preferred):
```
  ┌────────────────────────────────────────┐
  │ Network breaks before sync              │
  ├────────────────────────────────────────┤
  │ Decision: Transfer goes through anyway  │
  │ Why: Keep system up, sync later         │
  │ User sees: "Transfer successful" ✅     │
  │ But: Servers might disagree (stale) ❌ │
  └────────────────────────────────────────┘

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION TABLE:

```
┌──────────────────────────────┬──────────────────┬──────────────────────────┐
│ System Type                  │ Prioritizes      │ Real-World Examples      │
├──────────────────────────────┼──────────────────┼──────────────────────────┤
│ CP (Consistency)             │ Correctness      │ Banks, payments, ledgers │
│ Data > Uptime                │ ✅ 100% correct  │ MongoDB, HBase, BigTable │
│                              │ ❌ May go down   │                          │
├──────────────────────────────┼──────────────────┼──────────────────────────┤
│ AP (Availability)            │ Uptime           │ Facebook, Twitter, Netflix
│ Uptime > Correctness         │ ✅ Always up     │ DynamoDB, Cassandra      │
│                              │ ❌ Stale data ok │                          │
└──────────────────────────────┴──────────────────┴──────────────────────────┘

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY YOU CAN'T HAVE ALL 3:

Imagine network breaks → Server A & B can't talk.
User writes to Server A → Updates A's data.
Now: What does user reading from B see?

CONSISTENCY route: "Stop serving from B" (violates Availability)
AVAILABILITY route: "Serve from B anyway" (B has old data - violates Consistency)

You must choose ONE.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEMORY TRICK:

CAP = Choose 2:
```
├─ CP = "Stop the system" (Banks)
├─ AP = "Keep the system running" (Social media)
└─ CA = "Doesn't exist in real world" (no partition tolerance = not distributed)

```

When network breaks → You MUST have P (partition tolerance).
So real choice = CP or AP.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IN INTERVIEWS:

User: "Should I use MongoDB or Cassandra?"
Answer: "What's critical - correctness or uptime?
```
         ├─ Need 100% correct data? → MongoDB (CP)
         └─ Need always-on system? → Cassandra (AP)"

```

User: "What about during network partition?"
Answer: "CAP theorem says we can't have both. We pick:
```
         ├─ CP: Refuse requests until healed (safe but down)
         └─ AP: Serve stale data (up but inconsistent)"

```


---

## PACELC Theorem

🎯 CORE CONCEPT:

PACELC extends CAP theorem by answering: "What if there's NO partition?"

CAP says: "When partition → choose C or A"
PACELC adds: "When NO partition → choose L or C"

PAC = CAP theorem (during partition)
ELC = New rule (Else, when no partition: choose Latency OR Consistency)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2 SCENARIOS:

SCENARIO 1: PARTITION EXISTS (Network breaks)
```
├─ Use CAP logic: Choose A (Availability) or C (Consistency)
├─ Example: "Network down, accept stale data or refuse requests?"
└─ PA/EC (Cassandra) or PC/EC (HBase)

```

SCENARIO 2: NO PARTITION (Network working fine)
```
├─ Use PACELC logic: Choose L (Low Latency) or C (Consistency)
├─ Example: "Everything works, serve fast or serve guaranteed correct?"
└─ Trade-off: Fast response vs guaranteed correctness

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LATENCY vs CONSISTENCY (The new trade-off):

🚀 LATENCY = How fast you respond
```
   ├─ Low latency: Return immediately (don't wait for replicas)
   ├─ Fast response to user
   └─ But might not be 100% up-to-date

```

✅ CONSISTENCY = How correct the data is
```
   ├─ Wait for all replicas to confirm
   ├─ Guaranteed correct data
   └─ But slower response to user

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REAL-WORLD EXAMPLE (Social Media Feed):

SCENARIO 1: Network is WORKING (No partition)

Option L (Low Latency):
```
├─ User asks: "Show me my feed"
├─ System: "Return immediately from nearest server" ⚡ (fast)
├─ Problem: Might show old likes/comments
└─ Choose: LATENCY over CONSISTENCY

```

Option C (Consistency):
```
├─ User asks: "Show me my feed"
├─ System: "Wait for all servers to sync" ⏳
├─ Benefit: 100% correct likes/comments
└─ Choose: CONSISTENCY over LATENCY

```

SCENARIO 2: Network is DOWN (Partition exists)

Option A (Availability):
```
├─ System: "Server 1 can't reach Server 2"
├─ But accept requests anyway
├─ Return from local data
└─ Choose: AVAILABILITY over CONSISTENCY

```

Option C (Consistency):
```
├─ System: "Server 1 can't reach Server 2"
├─ Refuse requests until fixed
├─ Guarantee correctness
└─ Choose: CONSISTENCY over AVAILABILITY

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXAMPLE SYSTEMS:

📱 CASSANDRA (PA/EL):
```
├─ During partition: Choose A (Availability) over C
├─ During normal: Choose L (Low Latency) over C
├─ Strategy: "Always fast, eventually consistent"
├─ Use: High-scale systems (Facebook, Twitter)
└─ Accept old data for speed/uptime

```

🗄️ HBASE / BIGTABLE (PC/EC):
```
├─ During partition: Choose C (Consistency) over A
├─ During normal: Choose C (Consistency) over L
├─ Strategy: "Always correct, might be slow"
├─ Use: Financial, banking systems
└─ Always wait for confirmation

```

📊 MONGODB (PA/EC default):
```
├─ During partition: Choose A (Availability) over C
├─ During normal: Choose C (Consistency) over L
├─ Strategy: "Always correct when healthy, available during failures"
├─ Use: General purpose
└─ Fast & consistent normally, but accepts stale data during partition

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION TREE:

Network down (Partition)?
```
│
├─ YES → Use CAP logic
│  ├─ PA: Serve stale (Cassandra)
│  └─ PC: Refuse requests (HBase)
│
└─ NO → Use PACELC logic
   ├─ EL: Fast response (even if not guaranteed fresh)
   └─ EC: Slow response (but guaranteed correct)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPARISON TABLE:

```
┌──────────────┬──────────────────────────────┬──────────────────────────────┐
│ System       │ During Partition (PAC)       │ Normal (ELC)                 │
├──────────────┼──────────────────────────────┼──────────────────────────────┤
│ Cassandra    │ PA (Choose Availability)     │ EL (Choose Low Latency)      │
│ (PA/EL)      │ Serve old data               │ Fast responses               │
├──────────────┼──────────────────────────────┼──────────────────────────────┤
│ HBase        │ PC (Choose Consistency)      │ EC (Choose Consistency)      │
│ (PC/EC)      │ Refuse if can't check        │ Wait for all replicas        │
├──────────────┼──────────────────────────────┼──────────────────────────────┤
│ MongoDB      │ PA (Choose Availability)     │ EC (Choose Consistency)      │
│ (PA/EC)      │ Accept during failure        │ Consistent when healthy      │
└──────────────┴──────────────────────────────┴──────────────────────────────┘

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY PACELC MATTERS:

CAP only covers "What if partition?" (1 scenario)
PACELC covers both scenarios:
```
├─ "What if partition?" → CAP logic
└─ "What if NO partition?" → New ELC logic (E = Else)

```

Real systems spend most time without partition.
So the ELC choice matters more in practice!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRACTICAL EXAMPLE (E-commerce):

CASSANDRA (PA/EL):
During normal: 
```
  └─ User buys item, item shows out of stock instantly ⚡
  └─ But inventory might not be synced across all servers yet
  └─ Risk: Oversell if multiple people buy

```

During partition:
```
  └─ Servers isolated, keeps selling ✅ (Availability)
  └─ But data inconsistent ❌

```

HBASE (PC/EC):
During normal:
```
  └─ User buys item, waits ⏳
  └─ System confirms ALL servers updated before responding
  └─ Guaranteed correct ✅

```

During partition:
```
  └─ System stops accepting orders
  └─ Refuses requests until healed ❌

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEMORY TRICK:

CAP = "What if things break?"
PACELC = "What if things work? AND what if things break?"

P = Partition exists → A or C
E = Else (no partition) → L or C

Think: "We always have to pick between two things"
```
├─ Bad times (partition): C vs A
└─ Good times (no partition): C vs L

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IN INTERVIEWS:

User: "Should I use Cassandra or HBase?"

Answer: "Depends on what matters:
  
  Cassandra (PA/EL):
```
  ├─ If partition: Serve stale data (Availability)
  └─ If healthy: Fast responses (Low Latency)
  └─ Best for: Social media, high-scale, speed matters

```
  
  HBase (PC/EC):
```
  ├─ If partition: Refuse requests (Consistency)
  └─ If healthy: Wait for confirmation (Consistency)
  └─ Best for: Finance, banking, correctness matters"

```


---

## Any system which is equally READ and WRITE heavy both? and how to decide architecture?

EQUAL READ + WRITE HEAVY SYSTEMS
```
═══════════════════════════════════════════════════════════════

```

Real examples:
```
├─ Twitter: Read feed (100M/sec) + Write tweets (1M/sec)
├─ Real-time chat: Read messages + Write messages equally
├─ Trading platforms: Read prices + Write orders equally
└─ Gaming leaderboards: Read scores + Write scores equally

```


PROBLEM WITH PRIMARY-REPLICA
```
═══════════════════════════════════════════════════════════════

```

Primary-replica scales READS, not WRITES:
```
├─ Add replicas for reads ✓
├─ Writes still bottleneck (primary only) ❌
└─ Not suitable for write-heavy

```


ARCHITECTURE OPTIONS
```
═══════════════════════════════════════════════════════════════

```

1. SHARDING (Partition writes)
```
├─ Split data by user_id, region, time
├─ Each shard handles its writes
├─ Writes: Distributed ✓
├─ Reads: Query relevant shards
├─ Cost: Complex routing, resharding pain
└─ Example: Twitter uses sharding

```

2. CQRS (Command Query Responsibility Segregation)
```
├─ Writes go to write-optimized DB (normalized)
├─ Reads go to read-optimized cache (denormalized)
├─ Write: Fast insert to primary
├─ Read: Fast lookup from cache
├─ Consistency: Eventually consistent
└─ Example: E-commerce product catalog

```

3. NOSQL PEER-TO-PEER
```
├─ Any node accepts reads AND writes
├─ Both scale horizontally ✓
├─ Writes replicate async
├─ Reads: Local node (fast) or latest replica
├─ Cost: Conflict resolution
└─ Example: Cassandra, DynamoDB

```


DECISION MATRIX
```
═══════════════════════════════════════════════════════════════

┌────────────┬──────────┬──────────┬────────────┐
│ Approach   │ Write    │ Read     │ Complexity │
├────────────┼──────────┼──────────┼────────────┤
│ Sharding   │ Scales ✓ │ Scales ✓ │ High       │
│ CQRS       │ Scales ✓ │ Scales ✓ │ High       │
│ NoSQL P2P  │ Scales ✓ │ Scales ✓ │ Medium     │
└────────────┴──────────┴──────────┴────────────┘

```


TWITTER EXAMPLE (High R/W)
```
═══════════════════════════════════════════════════════════════

```

Architecture:
```
├─ Write path: Write-optimized database (sharded)
│  └─ Tweets go to shard 1-N by user_id
├─ Read path: Cache layer (Redis)
│  └─ Feed cache pre-computed, served instantly
├─ Fanout: When user tweets
│  └─ Update followers' feed caches
└─ Result: Both R and W scale ✓

```


SIMPLER APPROACH: Cache Everything
```
═══════════════════════════════════════════════════════════════

```

If R/W equally heavy:
```
├─ Primary DB: Write-optimized (normalized)
├─ Cache layer: Read-optimized (denormalized)
├─ Write: DB + invalidate cache
├─ Read: Cache first, then DB
├─ Scales both R and W ✓
├─ Cost: Cache overhead
└─ Simplest for moderate scale

```


RECOMMENDATION
```
═══════════════════════════════════════════════════════════════

```

Start simple:
```
├─ Primary-replica + Redis cache
├─ Scale reads: Add replicas
├─ Scale writes: Add cache layer
└─ If still bottleneck → then shard

```

Only shard when:
```
├─ 100k+ writes/sec needed
├─ Cost justifies engineering complexity
└─ Sharding becomes necessary

```


---

