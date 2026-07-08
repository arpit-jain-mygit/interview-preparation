# URL Shortener System Design

**Author:** Arpit Jain  
**Target:** MAANG System Design Interview  
**Status:** Revision 1 - Initial Design with Feedback  
**Last Updated:** 2026-07-08

---

## Table of Contents

1. [Revision 1: Initial Design](#revision-1-initial-design)
   - [Functional Requirements](#functional-requirements)
   - [Non-Functional Requirements](#non-functional-requirements)
   - [Design Decisions](#design-decisions)
   - [Your Diagrams](#your-diagrams)
   - [Feedback on Revision 1](#feedback-on-revision-1)

---

# Revision 1: Initial Design

## Functional Requirements

1. **Generated short URLs should be collision free**
   - Every long URL gets a unique short code
   - No two different URLs can map to the same short code

2. **User should be able to provide a long URL and get short URL**
   - Simple API to convert long URL → short URL
   - Simple API to redirect short URL → long URL

3. **Read:Write ratio is 9:1**
   - Most traffic is redirects (clicks), not new shortenings
   - Design must optimize for read performance

---

## Non-Functional Requirements

1. **System should support 100M URL creation per day**
   - 100M URLs/day ÷ 86,400 seconds = **1,160 writes/sec**
   - With 9:1 ratio: 1,160 × 10 = **11,600 reads/sec**
   - Peak traffic could be 2-3x higher

2. **System should respond within 2 seconds**
   - **Write latency:** <2 sec for shortening requests
   - **Read latency:** <200ms for redirect requests (critical!)
   - **Target:** <100ms for reads (normal case)

3. **High availability**
   - System must be operational 24/7
   - Single component failure shouldn't bring down the system

---

## Design Decisions

### 1. Database Choice: Key-Value Store (Cassandra/DynamoDB)

**Your Choice:** Cassandra or DynamoDB

**Rationale:**
- Key-value lookup is ideal for this workload
- Simple mapping: `short_url → long_url`
- Scales horizontally for high throughput
- Handles high read ratio efficiently

**Table Schema:**
```
Table: url_mapping

Columns:
  short_url      (Primary Key) - VARCHAR(20)  ← 20 bytes
  long_url       (Clustering Key) - VARCHAR(2048) ← 70 bytes (avg)
  created_on     (Timestamp) - 10 bytes
  [optional] user_id - 8 bytes
  [optional] expires_at - 10 bytes

Total per row: ~100 bytes (average)
```

---

### 2. Storage Requirements Calculation

**Your Calculation:**
```
Daily write requests:     100M URLs/day
Storage per request:      ~100 bytes
Daily storage:            10 GB

Per year:                 3,650 GB (~3.65 TB)
For 5 years:              18 TB
With 3x redundancy:       54 TB
```

**This is correct!** ✅

**Additional considerations:**
- Network bandwidth: 100M × 100 bytes = 10 GB/day = ~1 MB/sec
- Read bandwidth (9:1 ratio): ~9 MB/sec
- Both easily manageable

---

### 3. API Design

**API 1: Create Short URL**
```
POST /api/v1/data/shorten

Request:
{
  "longUrl": "https://en.wikipedia.org/wiki/Systems_design",
  [optional] "customAlias": "system-design",
  [optional] "ttl": 86400,
  [optional] "userId": "user-123"
}

Response (Success - 201):
{
  "shortUrl": "https://tinyurl.com/y7keocwj",
  "longUrl": "https://en.wikipedia.org/wiki/Systems_design",
  "createdAt": "2026-07-08T10:30:00Z",
  "expiresAt": "2026-07-09T10:30:00Z"
}

Response (Error):
  400: Invalid URL format
  409: Custom alias already exists
  429: Rate limit exceeded
  500: Server error
```

**API 2: Redirect Short URL**
```
GET /api/v1/shortUrl/{shortCode}

Response (Success - 302):
  Status: 302 Temporary Redirect
  Location: https://en.wikipedia.org/wiki/Systems_design
  [Cache-Control headers]

Response (Error):
  404: Short URL not found
  410: Short URL expired
  500: Server error
```

---

### 4. Algorithm: Batch Pre-Generation with Randomization

**Your Approach:**

#### Phase 1: Generate Codes

```
Code format:        6 characters (alphanumeric)
Character set:      62 symbols (0-9, a-z, A-Z)
Total combinations: 62^6 = 56.8 BILLION codes

Generation:
  Sequential: 000000 → 000001 → ... → zzzzzz
  Time: ~1 hour (one-time job)
  Output: sequential-ref-code.txt (400 GB)
  Storage: AWS S3 (360 GB for 56B codes @ 6 bytes each)
```

**Storage breakdown:**
- 56 billion codes × 6 bytes = 336 GB
- With compression (gzip): ~100-150 GB
- Spread across multiple 1GB files in S3

#### Phase 2: Randomize Codes

```
Command: $ sort -R sequential-codes.txt > randomized-codes.txt

Why shuffle?
  WITHOUT: 000000, 000001, 000002 (sequential, predictable!)
  WITH:    xYz9aB, 2kLmOp, Q7rWvX (random, unpredictable!)

Benefits:
  - Prevents code guessing
  - Better security
  - Looks more professional
```

#### Phase 3: Load into Kafka

```
Kafka Topic: url-shortener-codes
Partitions:  10-100 (based on throughput needs)

Distribution:
  ├─ Partition 0: [xYz9aB, 2kLmOp, Q7rWvX, ...]
  ├─ Partition 1: [abc123, def456, ghi789, ...]
  ├─ Partition 2: [jkl012, mno345, pqr678, ...]
  └─ ...

Each partition holds: ~5.6 billion codes (56B ÷ 10)
Load rate: ~1M codes/sec
Total load time: ~15-20 hours
```

---

## Your Diagrams

### Diagram 1: Batch Design - Short URLs Generation, Randomization, and Ready to be Mapped

```
┌─────────────────────────────────────────────────────────────────────┐
│                      BATCH DESIGN FLOW                              │
│                                                                     │
│  ┌─────────────────────┐                                           │
│  │ Python program to   │                                           │
│  │ generate 56B ID in  │                                           │
│  │ Files (1 GB each)   │                                           │
│  │ Total 360 files     │                                           │
│  └──────────┬──────────┘                                           │
│             │                                                       │
│             ▼                                                       │
│  ┌─────────────────────┐                                           │
│  │ Store these files   │                                           │
│  │ in S3               │                                           │
│  └──────────┬──────────┘                                           │
│             │                                                       │
│             ▼                                                       │
│  ┌─────────────────────────────────────┐                           │
│  │ Write a Spark program to load these  │                          │
│  │ files and for each, call Unix sort   │                          │
│  │ command to shuffle                  │                          │
│  └──────────┬──────────────────────────┘                           │
│             │                                                       │
│             ▼                                                       │
│  ┌──────────────────────┐                                          │
│  │ Reload shuffled files│                                          │
│  │ in S3                │                                          │
│  └──────────┬───────────┘                                          │
│             │                                                       │
│             ▼                                                       │
│  ┌──────────────────────────────┐                                  │
│  │ Load shuffled files using    │                                  │
│  │ Spark                        │                                  │
│  └──────────┬───────────────────┘                                  │
│             │                                                       │
│             ▼                                                       │
│  ┌──────────────────────────────────────────┐                      │
│  │ Spark loads these entries from each file │                      │
│  │ into Kafka partitions                    │                      │
│  └──────────┬───────────────────────────────┘                       │
│             │                                                       │
│             ▼                                                       │
│  ┌──────────────────────────────────────────┐                      │
│  │ Short URLs are ready to be mapped to     │                      │
│  │ long URLs on request                     │                      │
│  └──────────────────────────────────────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Your design captures:** ✅
- Sequential generation (1 GB files, 360 files total)
- Randomization via Unix sort
- S3 storage
- Spark parallel loading
- Kafka partitioning

---

### Diagram 2: User Request Flow - Write (Long to Short URL) / Read (Redirect Short to Long URL)

```
┌──────────────────────────────────────────────────────────────────────┐
│         USER REQUEST FLOW - WRITE & READ                             │
│                                                                      │
│                    User                                              │
│                      │                                               │
│                      ▼                                               │
│            ┌─────────────────┐                                       │
│            │   API Gateway   │                                       │
│            └────────┬────────┘                                       │
│                     │                                                │
│                     ▼                                                │
│            ┌─────────────────────┐                                   │
│            │   Load Balancer     │                                   │
│            └────────┬────────────┘                                   │
│                     │                                                │
│        ┌────────────┼────────────┐                                   │
│        │                         │                                   │
│  Long→Short                 Short→Long                               │
│  (Write)                    (Read)                                   │
│        │                         │                                   │
│        ▼                         ▼                                   │
│   ┌────────────────┐      ┌──────────────────┐                      │
│   │ Create Short   │      │ Redirect Short   │                      │
│   │ URLs App       │      │ URL to Long URL  │                      │
│   │ Server serving │      │ App Server       │                      │
│   │ Microservices  │      │ serving          │                      │
│   │ PODs using     │      │ Microservices    │                      │
│   │ Kubernetes     │      │ PODs using       │                      │
│   │                │      │ Kubernetes       │                      │
│   └────┬───────────┘      └────┬─────────────┘                      │
│        │                       │                                    │
│        ▼                       ▼                                    │
│   ┌──────────┐            ┌──────────┐                             │
│   │ NoSQL    │            │ Cache    │                             │
│   │ Database │            │ Cluster  │                             │
│   │ Cassandra│            │ (Redis)  │                             │
│   │/DynamoDB │            └──┬───────┘                             │
│   │          │               │                                     │
│   │ Long URL │         If not found                                │
│   │ Short URL│         in cache ↓                                  │
│   │ Created_ │        ┌────────────────┐                           │
│   │ on       │        │ Kafka          │                           │
│   └──────────┘        │ (If not found  │                           │
│                       │ in cache)      │                           │
│                       └────────────────┘                           │
│                                                                    │
└──────────────────────────────────────────────────────────────────────┘
```

**Your design captures:** ✅
- API Gateway
- Load Balancer
- Microservices on Kubernetes
- Database (Cassandra/DynamoDB)
- Cache (Redis)
- Kafka (for fallback)
- Separation of Write and Read paths

---

## Feedback on Revision 1

### ✅ Strengths (Good Decisions)

1. **Batch Pre-Generation Approach** - Excellent!
   - Avoids collision checks at runtime
   - Eliminates database bottleneck for code generation
   - Pre-shuffling ensures unpredictability

2. **Capacity Planning** - Correct Math
   - 100 bytes per entry
   - 54 TB with 3x redundancy (accurate)
   - Proper baseline for storage

3. **NoSQL Choice** - Good for this workload
   - Cassandra/DynamoDB suitable for key-value
   - Handles high write/read throughput
   - Scales horizontally

4. **Microservices Architecture** - Scalable design
   - Kubernetes for orchestration
   - Separate write/read paths
   - Stateless services (easy to scale)

5. **High-Level Components** - All present
   - API Gateway ✓
   - Load Balancer ✓
   - Database ✓
   - Cache ✓

---

### ❌ Critical Gaps (Missing for MAANG)

#### 1. Code Length Decision Not Justified

**Current:** 62^6 = 56.8 billion codes
**Problem:** Only covers ~1.8 years at 100M/day

```
Your calculation:
  56B codes ÷ 100M/day = 560 days ≈ 1.8 years

MAANG interviewer will ask:
  "What happens after 1.8 years? System crashes?"

Missing:
  - Why 6 chars? (should explain capacity planning)
  - Alternative: 62^7 = 3.5 trillion (covers 96 years)
  - Regeneration strategy (when to move from 62^6 to 62^7)
```

**Add to next revision:**
```
Code length strategy:
  Phase 1: 62^6 (covers 1.8 years)
  At 80% exhaustion: Trigger regeneration
  Phase 2: 62^7 (covers 96 years)
  Transition: Gradual switchover (no service interruption)
```

---

#### 2. Missing Cache Strategy (Critical for 9:1 Read Ratio!)

**Current Design:** Shows Redis but doesn't explain strategy

**Missing Details:**
```
❌ No TTL mentioned
❌ No cache hit rate target
❌ No LRU/eviction policy
❌ No multi-layer caching strategy
❌ No cache invalidation logic
```

**Add to next revision:**
```
Caching Strategy:
  - Cache type: Redis with LRU eviction
  - TTL: 1 hour (normal URLs), 24 hours (popular URLs)
  - Cache size: 1-10 million entries
  - Hit rate target: 99%
  - Multi-layer:
      L1: Browser cache (via 301 redirect for some URLs)
      L2: CDN cache (geo-distributed)
      L3: Redis (in-memory)
      L4: Database (last resort)
```

---

#### 3. No Rate Limiting / API Gateway Protection

**Current:** Shows "API Gateway" but no details

**Missing:**
```
❌ Rate limiting rules not specified
❌ Protection against abuse not mentioned
❌ Error codes (429) not defined
❌ Request validation not detailed
```

**Add to next revision:**
```
API Gateway Features:
  - Rate limiting: 100 URLs/hour per IP address
  - Return 429 Too Many Requests if exceeded
  - Authentication/authorization checks
  - Request validation (URL format, length)
  - Logging and monitoring
```

---

#### 4. No Deduplication Strategy

**Current:** No mention of checking existing URLs

**Problem:**
```
User 1: Shortens https://google.com → gets "abc123"
User 2: Shortens https://google.com → gets "def456"?

Should be: User 2 gets "abc123" (same URL = same code)
```

**Add to next revision:**
```
Deduplication Logic:
  1. Before assigning new code:
     SELECT short_url FROM url_mapping WHERE long_url = ?
  
  2. If exists: Return cached short_url
  
  3. If new: 
     - Get code from Kafka queue
     - Save to database
     - Return new short_url
  
  Benefits:
    - Conserves codes (extends 56B runway)
    - Prevents duplicate work
    - Users get same URL on repeat requests
```

---

#### 5. Missing 301 vs 302 Trade-off Discussion

**Current:** No mention in your design

**Critical Interview Question:**
```
Interviewer: "Should you use 301 or 302 redirect?"

301 (Permanent):
  ✓ Browser caches → reduces load
  ✗ Can't track clicks for analytics
  ✗ Can't change destination URL
  
302 (Temporary):
  ✓ Every click hits your server (analytics possible)
  ✗ Higher server load
  ✗ Browser doesn't cache
```

**Add to next revision:**
```
Redirect Strategy: 302 (Temporary Redirect)

Reasoning:
  - Analytics tracking is important for business
  - Cache layer (Redis) handles load anyway
  - Every click captured in logs
  - Flexibility to change destination if needed

Performance consideration:
  - Browser doesn't cache (on surface)
  - But our Redis cache handles it (5ms response)
  - So latency is still low despite 302
```

---

#### 6. No Failure Handling / Recovery

**Current:** No mention of failures

**Missing:**
```
❌ What if Kafka broker fails?
❌ What if Cassandra goes down?
❌ What if Spark shuffle job crashes?
❌ What if cache layer fails?
```

**Add to next revision:**
```
Failure Handling:
  
  Kafka Consumer Failure:
    - Multiple consumers in group
    - Checkpointing (resume from offset)
    - Replication factor 3 for fault tolerance
    - Alert if queue depth drops
  
  Batch Job Failure:
    - Idempotent generation (restart from checkpoint)
    - Alert and retry with exponential backoff
    - Fallback: on-demand ID generation
  
  Database Failure:
    - Read replicas (3-5 copies)
    - Automatic failover to replica
    - Backup + restore SLA
  
  Cache Failure:
    - Graceful fallback to database
    - Database latency increases (but OK)
    - System keeps working (degraded)
```

---

#### 7. No Sharding/Partitioning Strategy

**Current:** Database is shown but no mention of scaling

**Missing:**
```
❌ How data is distributed across nodes
❌ Partition key strategy not mentioned
❌ No discussion of scaling beyond single cluster
```

**Add to next revision:**
```
Sharding Strategy:
  
  Partition Key: short_url (first character)
  
  Shard 0: short_url starts with [0-9]  → Cassandra Node 1
  Shard 1: short_url starts with [a-m]  → Cassandra Node 2
  Shard 2: short_url starts with [n-z]  → Cassandra Node 3
  
  Benefits:
    - Even distribution (each shard ~1/3 of data)
    - Query: Get first char → route to correct shard
    - Scales horizontally (add more nodes)
    - Supports read replicas per shard
```

---

#### 8. No Monitoring / Alerting

**Current:** No mention of monitoring

**Missing:**
```
❌ No KPIs defined
❌ No alert thresholds
❌ No monitoring dashboard mentions
❌ No exhaustion monitoring
```

**Add to next revision:**
```
Monitoring & Alerting:

  Key Metrics:
    - Kafka queue depth (alert if <50% capacity)
    - Cache hit rate (target 99%, alert if <95%)
    - Database CPU (alert if >80%)
    - API latency (p50, p99)
    - Error rate (alert if >0.1%)
  
  Exhaustion Monitoring:
    - Track: remaining codes in Kafka queue
    - Calculate: % of 56B used
    - Alert at 80%: Trigger regeneration
    - Start Phase 2 (62^7) before Phase 1 exhausts
  
  Dashboard:
    - Real-time metrics
    - Historical trends
    - Alert status
```

---

#### 9. Missing Batch Job Details

**Current:** Shows batch flow but lacks specifics

**Missing:**
```
❌ Performance metrics (speed of generation, shuffle, load)
❌ Storage efficiency (compression ratio)
❌ Failure recovery steps
❌ Scheduled vs on-demand
❌ Monitoring during batch execution
```

**Add to next revision:**
```
Batch Job Specifications:

  Generation Phase:
    - Time: ~1-3 hours
    - Input: Sequentially generate 0 to 62^6-1
    - Output: 360 × 1GB files in S3
    - Compression: gzip (reduces to ~100GB)
  
  Shuffle Phase:
    - Time: ~1-2 hours per 1GB file
    - Method: Unix sort -R (randomize)
    - Parallelization: Spark (100+ executors)
    - Output: Shuffled files back to S3
  
  Load Phase:
    - Time: ~2-4 hours
    - Method: Spark → Kafka producer
    - Partition count: 10-100
    - Rate: ~1M codes/sec
  
  Total Batch Time: ~6-10 hours
  Frequency: Once per 1.8 years (when 80% exhausted)
  SLA: Must complete before codes run out
```

---

#### 10. API Specifications Incomplete

**Current:** Mentions /createURL and /getLongURL

**Missing:**
```
❌ No request/response format
❌ No error codes
❌ No optional parameters
❌ No authentication mentioned
❌ No headers (cache control, etc)
```

**Add to next revision:**
```
Complete API Specification:

  POST /api/v1/data/shorten
    Input: { longUrl, [customAlias], [ttl], [userId] }
    Success: 201 { shortUrl, createdAt, expiresAt }
    Errors: 400, 409, 429, 500
    Rate limit: 100/hour/IP
  
  GET /api/v1/shortUrl/{shortCode}
    Response: 302 redirect (Location: {longUrl})
    Cache-Control: no-cache (force revalidation)
    Errors: 404, 410, 500
    Latency SLA: <100ms
```

---

## Summary: Revision 1 Grade

| Aspect | Grade | Comment |
|--------|-------|---------|
| Problem understanding | A | Clear on requirements |
| Batch pre-generation | A | Excellent approach |
| Architecture diagram | A | Good component layout |
| Capacity planning | A | Math is correct |
| Database choice | A | Appropriate for workload |
| **Cache strategy** | D | Only mentioned, not detailed |
| **Rate limiting** | D | Not explained |
| **Code length decision** | D | No justification |
| **Deduplication** | D | Missing entirely |
| **301 vs 302** | F | Not mentioned |
| **Failure handling** | F | Not addressed |
| **Monitoring** | F | No alerting strategy |
| **API specs** | C | Mentioned but incomplete |
| **Sharding** | D | Not detailed |

**Overall Score:** 65-70% for MAANG  
**With fixes:** 85-90% ✅

---

## Next Steps for Revision 2

To improve this design for MAANG interviews:

1. ✅ Add code length justification (62^6 vs 62^7)
2. ✅ Detail cache strategy (TTL, hit rate, layers)
3. ✅ Add rate limiting rules (100/hour/IP)
4. ✅ Include deduplication logic (check before assign)
5. ✅ Discuss 301 vs 302 (pick 302, explain why)
6. ✅ Add failure recovery (Kafka, Batch, DB, Cache)
7. ✅ Define monitoring/alerting (KPIs, thresholds)
8. ✅ Explain sharding strategy (by first char)
9. ✅ Detail batch job SLAs (time, frequency, recovery)
10. ✅ Complete API specifications (all endpoints, errors)

---

**Ready for Revision 2?** Let me know what to add or modify! 🚀
