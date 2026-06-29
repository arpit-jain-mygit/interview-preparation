# System Design: Complete Interview Preparation Guide

A comprehensive guide covering foundational system design concepts and detailed case studies. This guide includes framework for approaching interviews, estimation techniques, scaling strategies, and real-world problem solving.

---

## Table of Contents

### **Part 1: Foundation & Framework**

#### [Chapter 1: Scale from Zero to Millions of Users](#chapter-1-scale-from-zero-to-millions-of-users)
   - Single server setup
   - Scaling web tier  
   - Database replication
   - Caching strategies
   - CDN for static content
   - Stateless architecture
   - Multi-datacenter setup

#### [Chapter 2: Back-of-the-Envelope Estimation](#chapter-2-back-of-the-envelope-estimation)
   - Power of two reference
   - Latency numbers
   - Availability and SLA
   - Estimation techniques
   - Real-world examples

#### [Chapter 3: A Framework for System Design Interviews](#chapter-3-a-framework-for-system-design-interviews)
   - The 4-step framework
   - What interviewers look for
   - Clarification questions
   - High-level design
   - Deep dive strategies
   - Time management
   - Dos and Don'ts

---

# Chapter 1: Scale from Zero to Millions of Users


## ⚠️ Important Notice

**This document is based on concepts from "System Design Interview" by Alex Xu.**

This is **original content**: summaries, explanations, and real-world examples created to help understand system design concepts. It does not reproduce copyrighted material from the book. All content is restructured and rewritten for clarity and educational purposes.

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Single Server Setup](#single-server-setup)
3. [Scaling Web Tier](#scaling-web-tier)
4. [Scaling Database Tier](#scaling-database-tier)
5. [Adding Cache Layer](#adding-cache-layer)
6. [Content Delivery Network (CDN)](#content-delivery-network-cdn)
7. [Stateless vs Stateful Architecture](#stateless-vs-stateful-architecture)
8. [Multiple Data Centers](#multiple-data-centers)
9. [Message Queue](#message-queue)
10. [Complete Architecture](#complete-architecture)

---

## Executive Summary

Scaling a system from supporting one user to millions requires a journey of continuous refinement. This chapter builds a system step-by-step, showing you the common techniques and patterns used in production systems.

**Key Principle:** Scale horizontally (add more servers) rather than vertically (upgrade one server).

---

## Single Server Setup

### The Journey Begins

Start with everything on one server - web app, database, cache, everything.

**Architecture:**
```
User → DNS → IP Address (15.125.23.214)
           ↓
       Web Server (Web App + Database)
           ↓
       HTML/JSON Response
```

### Request Flow

```
1. User visits: api.mysite.com
   ↓
2. DNS service returns IP: 15.125.23.214
   ↓
3. HTTP request sent to web server
   ↓
4. Web server processes request
   ↓
5. Returns HTML or JSON response
```

### Traffic Sources

**Web Application:**
- Server-side languages (Java, Python)
- Client-side languages (HTML, JavaScript)

**Mobile Application:**
- HTTP protocol for communication
- JSON format for API responses

**Example API Response:**
```json
GET /users/12
Response: { "id": 12, "name": "Alice", "email": "alice@example.com" }
```

### Problem with Single Server

```
✗ No failover: Server goes down = website offline
✗ No scalability: Growth requires upgrading one server (limited)
✗ No redundancy: All data on one machine = disaster if it fails
```

**Next Step:** Separate web and database tiers

---

## Scaling Web Tier

### Vertical vs Horizontal Scaling

**Vertical Scaling (Scale Up):**
```
Add more CPU/RAM to existing server

Pros:
  ✓ Simple

Cons:
  ✗ Hard limit (can't add unlimited CPU/RAM)
  ✗ No failover (one server = single point of failure)
  ✗ High cost ($$$)
```

**Horizontal Scaling (Scale Out):**
```
Add more servers

Pros:
  ✓ No hard limit
  ✓ Failover capability
  ✓ Better cost-effectiveness at scale

Cons:
  ✓ More complexity (distributed system)
```

### Load Balancer

**Problem:**
```
Multiple web servers, but how do requests get distributed?
How do we handle server failures?
```

**Solution: Load Balancer**
```
User → Load Balancer (Public IP)
                ↓
        ┌───────┼───────┐
        ↓       ↓       ↓
    Server1  Server2  Server3
   (Private) (Private) (Private)
```

**How It Works:**
```
1. User connects to public IP of load balancer
2. Load balancer distributes traffic to one of the servers
3. If Server1 fails, load balancer routes to Server2 or Server3
4. Adding new servers automatically spreads load
```

### Benefits

```
✓ Failover: One server down ≠ website down
✓ Horizontal scaling: Add servers as needed
✓ High availability: Users can always access service
```

---

## Scaling Database Tier

### Problem with Single Database

```
✗ No failover: Database down = service down
✗ No read scalability: Single DB handle all read requests
✗ Data loss risk: Single point of failure
```

### Database Replication

**Master-Slave Architecture:**
```
Master Database (Write Operations)
        ↑
        │ Replication
        ↓
Slave1  Slave2  Slave3 (Read Operations)
```

**How It Works:**
```
Write requests (INSERT, UPDATE, DELETE)
        ↓
  Master Database
        ↓
Replicated to Slaves

Read requests (SELECT)
        ↓
Distributed across Slaves
```

### Real-World Example

**Twitter writes:** 3,500 tweets per second
**Twitter reads:** 35,000 requests per second (10:1 ratio)

```
Solution:
  Master: Handles 3,500 writes/sec
  Slaves: Each handles 11,667 reads/sec
  (Multiple slaves share the read load)
```

### Advantages of Replication

```
✓ Better Performance: Reads distributed, writes handled by master
✓ Reliability: Data replicated = survives disasters
✓ High Availability: Service works if one slave fails
```

### Failover Strategy

**If Slave Fails:**
```
Read operations → Master (temporarily)
     ↓
New healthy slave replaces old one
```

**If Master Fails:**
```
One slave promoted to new Master
All operations → New Master
New slave added to replace old master
```

---

## Adding Cache Layer

### Problem

```
Every request hits database
↓
Repetitive database calls for same data
↓
Slow response times, high database load
```

### Solution: Cache Tier

```
Request arrives
        ↓
Check Cache (Redis/Memcached)
        ├─ Cache Hit: Return data immediately (1µs)
        ├─ Cache Miss: Query Database (100µs)
        └─ Store in Cache for next time
```

### Caching Strategy: Read-Through Cache

```
Step 1: Web server checks cache
        ├─ Cache has data? Return it
        └─ Cache miss? Continue to Step 2

Step 2: Query database
        ├─ Get data
        └─ Store in cache

Step 3: Return to client
```

### Real Numbers

**With cache:**
```
Scenario: Popular blog post gets 10,000 reads per hour
  First read: 100µs (from database)
  Remaining 9,999 reads: 1µs each (from cache)
  Total time: 100µs + (9,999 × 1µs) ≈ 10ms
  
Without cache:
  Total time: 10,000 × 100µs = 1000ms = 1 second
  
Speedup: 100X faster!
```

### Cache Considerations

**When to Use Cache:**
```
✓ Data read frequently
✓ Data modified infrequently
✗ Don't use for critical data (RAM = volatile)
```

**Expiration Policy:**
```
Set TTL (Time-to-Live) for cached data

Too short:  System reloads from DB too often (overhead)
Too long:   Data becomes stale (incorrect)
Sweet spot: Balance freshness and performance
```

**Single Point of Failure:**
```
✗ One cache server down = requests to database spike
✓ Solution: Multiple cache servers across regions
```

**Eviction Policy:**
```
Cache is full, new data arrives, which gets removed?

LRU (Least Recently Used): Remove least recently accessed
LFU (Least Frequently Used): Remove least frequently accessed
FIFO (First In First Out): Remove oldest data
```

---

## Content Delivery Network (CDN)

### Problem

```
Static content (images, CSS, JS) served from origin server
↓
Users far from server = slow load
↓
Bandwidth wasted, users frustrated
```

### Solution: CDN (Content Delivery Network)

```
CDN = Network of servers geographically dispersed

User in Los Angeles    User in Europe     User in Tokyo
        ↓                   ↓                  ↓
   CDN in LA          CDN in London      CDN in Tokyo
        └─────────────────┼────────────────┘
                        Origin
                       (S3, etc.)
```

### How CDN Works

```
1. User requests: image.png
   URL: https://mysite.cloudfront.net/logo.jpg

2. CDN server closest to user?
   ├─ Has image in cache? → Return immediately
   └─ Not in cache? → Fetch from origin

3. Origin sends image + TTL (how long to cache)

4. CDN caches image, returns to user

5. Next user in same region gets from cache
```

### Real-World Impact

```
Without CDN:
  User in London requests image from US server
  Distance: ~5000 miles
  Latency: ~150ms per request

With CDN:
  User in London requests from CDN in London
  Distance: ~10 miles
  Latency: ~10ms per request
  
Speedup: 15X faster!
```

### CDN Considerations

**Cost:**
```
Pay for data transferred out of CDN
Infrequently used assets should not be on CDN (waste)
```

**Expiration:**
```
Too short: Reload from origin frequently (high cost)
Too long: Stale content (incorrect)
```

**Fallback:**
```
If CDN fails, request to origin server
Prevents complete blackout
```

---

## Stateless vs Stateful Architecture

### Problem: Server Affinity

```
Stateful (Bad):
  User A connects to Server 1
  User A's session data on Server 1
  User A MUST always go to Server 1
  ↓
  Load balancer must use "sticky sessions"
  ↓
  Hard to scale, fail-over difficult

Example:
  Server 1: User A
  Server 2: User B
  Server 3: User C
  ↓
  If Server 1 down, User A's data lost!
```

### Solution: Stateless Architecture

```
Move session data OUT of web servers
Store in shared persistent storage (database, Redis, etc.)

User A connects to Server 1
        ↓
Server 1 fetches session from shared storage
        ↓
If Server 1 fails, User A can go to Server 2
        ↓
Server 2 fetches same session from shared storage
        ↓
No disruption to user!
```

### Architecture Comparison

**Stateful (Problematic):**
```
Load Balancer
        ↓
    ┌───┼───┬───┐
    ↓   ↓   ↓   ↓
Server1 Server2 Server3 Server4
│ User │ │ User │ │ User │ │ User │
│  A   │ │  B   │ │  C   │ │  D   │
└───────┘ └───────┘ └───────┘ └───────┘

Problem: Each user tied to specific server
```

**Stateless (Solution):**
```
Load Balancer
        ↓
    ┌───┼───┬───┐
    ↓   ↓   ↓   ↓
Server1 Server2 Server3 Server4
(Interchangeable)
        ↓
    Session Store
    (Redis/DB)
        ↓
    User A, B, C, D sessions

Benefit: Any server can handle any user
```

### Benefits

```
✓ Auto-scaling: Add/remove servers without state concerns
✓ Failover: No sticky sessions needed
✓ Horizontal scaling: All servers identical
✓ Easy deployment: New servers immediately useful
```

---

## Multiple Data Centers

### Problem

```
Single data center:
  ✗ Single point of failure
  ✗ Users far away = high latency
  ✗ Natural disasters (earthquake, typhoon)
```

### Solution: Geo-routed Multi-DC Setup

```
User in US    → Route to US Data Center
User in EU    → Route to EU Data Center
User in APAC  → Route to APAC Data Center
```

### How It Works

**Normal Operation:**
```
geoDNS: Resolves domain to nearest data center IP

User location          DNS lookup           Data Center
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│ Los Angeles  │ ─→ │ geoDNS finds │ ─→ │ US-West DC   │
│              │     │ nearest DC   │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

**Failover:**
```
DC1 Offline
        ↓
geoDNS detects outage
        ↓
All traffic redirected to DC2
        ↓
100% traffic to healthy DC
        ↓
service continues
```

### Technical Challenges

**Traffic Redirection:**
```
geoDNS routes based on user location
Detects failures, redirects automatically
```

**Data Synchronization:**
```
Challenge: Data in DC1 might not be in DC2

Solution: Replicate data across DCs
  Synchronous: Wait for all DCs (slow, guaranteed)
  Asynchronous: Send and continue (fast, eventual consistency)

Netflix approach: Asynchronous replication
```

**Testing & Deployment:**
```
Must test across all data centers
Automated deployment tools keep services consistent
```

---

## Message Queue

### Problem: Tight Coupling

```
Direct dependencies between services:
  Web Server → Database (write)
  Web Server → Image Processing (upload)
  Web Server → Email Service (notification)
  
If any service is slow/down, everything stalls
```

### Solution: Message Queue

```
Decouple services with asynchronous messaging

Web Server ─→ Message Queue ─→ Image Processing
                       ↓
                    Email Service
                       ↓
                   Notification Service

Web server doesn't wait for processing!
```

### How It Works

```
1. User uploads image to web server
2. Web server puts message in queue
3. Web server returns response immediately
4. Image processor reads from queue
5. Processes image asynchronously

User gets response in 100ms
Image processing happens in background
```

### Benefits

```
✓ Decoupling: Services independent
✓ Asynchronous: Requests don't wait
✓ Scalability: Add workers independently
✓ Fault tolerance: Service down ≠ message lost
```

---

## Complete Architecture

### Final System Design

```
                        ┌─── CDN ───┐
                        │ (Static)  │
                        └────────┬──┘
                                 │
    Users ─→ geoDNS ─→ Load Balancer
                            │
                ┌───────────┼───────────┐
                ↓           ↓           ↓
            Server1     Server2     Server3
            (Stateless) (Stateless) (Stateless)
                │           │           │
                └───────────┼───────────┘
                            │
            ┌───────────────┼───────────────┐
            ↓               ↓               ↓
        Cache Layer    Session Store    Message Queue
        (Redis)       (Redis/Database)      │
            │               │               ↓
            │               │       ┌───────┼───────┐
            └───────────────┼───────┘       ↓       ↓
                            ↓        Image Service  Email Service
                    Master Database
                            ↓
                    ┌───────┼───────┐
                    ↓       ↓       ↓
                Slave1   Slave2   Slave3
                (Read)   (Read)   (Read)
```

### Data Flow Example

**Write Request (Create Post):**
```
1. User submits post via web form
2. Load balancer routes to available server
3. Server authenticates user (session from session store)
4. Server writes to master database
5. Post replicated to slave databases
6. Put message in queue for image processing
7. Return response to user immediately
8. Image service processes asynchronously
9. Notification service sends updates
```

**Read Request (Load Feed):**
```
1. User requests feed
2. Server checks cache
3. Cache hit? Return from cache (1µs)
4. Cache miss? Query read replica
5. Store result in cache
6. Return to user
```

---

## Key Takeaways

```
✓ Start simple, scale incrementally
✓ Add components based on bottlenecks
✓ Separate concerns (web, cache, database)
✓ Use multiple servers (horizontal scaling)
✓ Replicate data for reliability
✓ Distribute geographically for latency
✓ Decouple services with message queues
✓ Keep state external for stateless servers
✓ Monitor and measure everything
```

---

## References

- System Design Interview by Alex Xu, Chapter 1
- Database Replication Patterns
- Content Delivery Network (CDN) Concepts
- Asynchronous Messaging Patterns

---

# Chapter 2: Back-of-the-Envelope Estimation


## ⚠️ Important Notice

**This document is based on concepts from "System Design Interview" by Alex Xu.**

This is **original content**: summaries, explanations, and real-world examples created to help understand system design concepts. It does not reproduce copyrighted material from the book. All content is restructured and rewritten for clarity and educational purposes.

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Power of Two](#power-of-two)
3. [Latency Numbers](#latency-numbers-every-programmer-should-know)
4. [Availability Numbers](#availability-numbers)
5. [Estimation Techniques](#estimation-techniques)
6. [Real-World Example: Twitter](#real-world-example-twitter)
7. [Tips for Estimation](#tips-for-estimation)

---

## Executive Summary

**Back-of-the-Envelope Estimation** = Rough calculations to understand system requirements using common performance numbers and basic math.

**Why It Matters:**
- Estimate if design meets requirements
- Identify bottlenecks early
- Make architectural decisions based on data, not guessing
- Impress interviewer with structured thinking

**Key Principle:** Process matters more than perfect accuracy. Interviewers want to see your problem-solving approach.

---

## Power of Two

### Why Power of Two?

Data grows exponentially in distributed systems. Understanding powers of 2 helps you quickly estimate:
- Storage capacity
- Memory needed
- Request handling

### Quick Reference Table

```
2^10 = 1 Thousand          (1K)
2^20 = 1 Million           (1M)
2^30 = 1 Billion           (1B)
2^40 = 1 Trillion          (1T)

Byte Units:
1 Byte = 8 bits
1 KB = 1,024 bytes         ≈ 1K
1 MB = 1,024 KB            ≈ 1M
1 GB = 1,024 MB            ≈ 1G
1 TB = 1,024 GB            ≈ 1T
1 PB = 1,024 TB            ≈ 1P
```

### Examples

**ASCII Character:**
```
1 character = 1 byte

"Hello" = 5 bytes

Tweet (280 characters) = 280 bytes
```

**Storage Calculation:**
```
1M users × 1M data per user = 1T storage
1M users × 1G data per user = 1P storage
```

**Memory Needed:**
```
Cache 1M entries × 1KB each = 1GB RAM
Cache 100M entries × 1KB each = 100GB RAM
```

---

## Latency Numbers Every Programmer Should Know

### What Are These Numbers?

Latency = How long an operation takes (in nanoseconds, microseconds, milliseconds)

### Reference Table (As of 2020)

```
Operation                           Time
─────────────────────────────────────────
L1 cache reference                  0.5 ns
Branch mispredict                   5 ns
L2 cache reference                  7 ns
Mutex lock/unlock                   25 ns
Main memory reference               100 ns
Compress 1K with Snappy             2,000 ns
Send 1K bytes over 1 Gbps network   10,000 ns
Read 1 MB from memory               250,000 ns
Round trip within same data center  500,000 ns
Disk seek                           10,000,000 ns
Read 1 MB from disk                 20,000,000 ns
Send packet US East to US West      150,000,000 ns
Send packet US East to Europe       150,000,000 ns
Send packet US East to Asia         150,000,000 ns
```

### Time Units Conversion

```
1 ns (nanosecond)   = 10^-9 seconds
1 µs (microsecond)  = 10^-6 seconds = 1,000 ns
1 ms (millisecond)  = 10^-3 seconds = 1,000 µs
1 s (second)        = 1,000 ms
```

### Key Insights

```
Memory is FAST:
  L1 cache:      0.5 ns
  L2 cache:      7 ns
  Main memory:   100 ns
  
Disk is SLOW:
  Disk seek:     10,000,000 ns
  Disk read:     20,000,000 ns
  
Network is SLOW:
  Same DC:       500,000 ns (0.5 ms)
  Different DC:  150,000,000 ns (150 ms)
```

### Practical Implications

**1. Avoid Disk Seeks**
```
One disk seek = 10 million ns
One memory read = 100 ns

Disk seek is 100,000X slower than memory!
```

**2. Compress Data Before Sending**
```
Compress 1K:      2,000 ns
Send 1K (1Gbps):  10,000 ns
Total:            12,000 ns

Uncompressed 1K:  10,000 ns
Send 1K (1Gbps):  10,000 ns
Total:            20,000 ns

Compression saves 40%! Worth the CPU cost.
```

**3. Network Distance Matters**
```
Same data center: 0.5 ms
Different region: 150 ms (300X slower!)

Solution: Replicate data geographically
```

### Real-World Example: Google Search

```
User types query
        ↓
Query goes to nearest data center: 50ms
        ↓
Search index lookup: 1-5 ms
        ↓
Result aggregation: 10-20 ms
        ↓
Formatting and compression: 5 ms
        ↓
Send back to user: 50 ms
        ↓
Total: ~200 ms
(Feels instant to user!)
```

---

## Availability Numbers

### Definition

**Availability** = Ability of system to stay operational for extended periods.

Measured in **uptime percentage**. Higher = better.

### SLA (Service Level Agreement)

Promise to customers about uptime:

```
99% SLA       = "System will be up 99% of the time"
99.9% SLA     = "System will be up 99.9% of the time" ✓ Industry standard
99.99% SLA    = "System will be up 99.99% of the time"
99.999% SLA   = "System will be up 99.999% of the time" ✓ Only for critical
```

### Uptime vs Downtime

```
99% uptime:
  Downtime per year: 365 × 24 × 60 × 0.01 = 52 minutes
  
99.9% uptime (3 nines):
  Downtime per year: 365 × 24 × 60 × 0.001 = 5.26 minutes
  
99.99% uptime (4 nines):
  Downtime per year: 365 × 24 × 60 × 0.0001 = 31.5 seconds
  
99.999% uptime (5 nines):
  Downtime per year: 365 × 24 × 60 × 0.00001 = 3.15 seconds
```

### Real-World SLAs

```
Amazon AWS:   99.99% (4 nines)
Google Cloud: 99.99% (4 nines)
Microsoft Azure: 99.99% (4 nines)

Netflix relies on multiple services:
  Each at 99.99% → Combined availability lower
  Solution: Circuit breakers, fallbacks, redundancy
```

### How to Achieve High Availability

```
99.9% (3 nines) - Achievable:
  ✓ Database replication (master-slave)
  ✓ Load balancing
  ✓ Basic failover

99.99% (4 nines) - Requires:
  ✓ Multi-region deployment
  ✓ Automated failover
  ✓ Health monitoring
  ✓ Regular backup and recovery testing

99.999% (5 nines) - Extreme:
  ✓ Planetary-scale redundancy
  ✓ Sophisticated monitoring
  ✓ Zero-downtime updates
  ✗ Very expensive ($$$)
```

---

## Estimation Techniques

### Step-by-Step Process

**1. Break Down the Problem**
```
Don't estimate whole system at once
Break into components:
  - Write operations per second
  - Read operations per second
  - Storage needs
  - Cache needs
  - Network bandwidth
```

**2. Make Assumptions Clear**
```
Write them down!
  "Assuming 100 million DAU"
  "Assuming 10:1 read-to-write ratio"
  "Assuming 5 years data retention"
```

**3. Start with Known Numbers**
```
1 billion seconds ≈ 31 years
1 year = 365 days
1 day = 24 hours × 60 minutes × 60 seconds = 86,400 seconds
```

**4. Use Approximation**
```
Don't try to be precise!
99,987 / 9.1 = ?
Approximate as: 100,000 / 10 = 10,000

Close enough for estimation!
```

---

## Real-World Example: Twitter

### Problem Statement

Estimate Twitter's capacity needs:

```
Assumptions:
  - 300 million monthly active users
  - 50% use Twitter daily (DAU)
  - Users post 2 tweets per day on average
  - 10% of tweets contain media (images/videos)
  - Media is stored for 5 years

Questions to answer:
  1. What is tweet posting rate (QPS)?
  2. What is tweet reading rate (QPS)?
  3. How much storage needed?
```

### Estimation: Write Operations

```
Daily Active Users (DAU):
  300M monthly × 50% daily rate = 150M DAU

Tweets per second:
  150M DAU × 2 tweets/day ÷ 24 hours ÷ 3600 seconds
  = 300M ÷ 86,400
  ≈ 3,500 tweets/second

Peak QPS (usually 2× average):
  3,500 × 2 = 7,000 tweets/second
```

### Estimation: Read Operations

```
Assuming 10:1 read-to-write ratio (common for social media)

Read QPS:
  3,500 writes/sec × 10 = 35,000 reads/second

This means:
  Read load is 10× greater than write load
  Need read replicas and caching!
```

### Estimation: Storage

```
Tweets with media per day:
  150M DAU × 2 tweets × 10% with media
  = 30M tweets with media per day

Average media size:
  Image: ~1-2 MB
  Video: ~5-100 MB
  Average: ~1 MB

Storage per day:
  30M tweets × 1 MB = 30 TB per day

Storage for 5 years:
  30 TB/day × 365 days/year × 5 years
  = 30 × 365 × 5
  = 54,750 TB
  ≈ 55 PB (Petabytes)
```

### Real Numbers Analysis

```
55 PB over 5 years
  Cost (assuming $0.20 per GB per month):
  55 × 10^6 GB × $0.20/GB/month × 12 months × 5 years
  ≈ $660 billion
  
This shows why video storage is expensive!
Solution: Use CDN, compress, tiered storage
```

---

## Tips for Estimation

### 1. Rounding and Approximation

```
Don't do exact math. Estimate!

Exact:   99,987 / 9.1 = 10,987.09...
Approx:  100,000 / 10 = 10,000

Error: 1.3% (Acceptable!)
```

### 2. Label Your Units

```
Bad: "System needs 5"
     5 what? KB? MB? GB? TB?

Good: "System needs 5 TB"
      Clear units prevent confusion
```

### 3. Document Assumptions

```
Write down explicitly:
  ✓ Number of users
  ✓ Growth rate
  ✓ Data retention period
  ✓ Ratios (read:write)
  ✓ Geographic distribution
```

### 4. Practice Common Calculations

Memorize these:
```
1 year = 365 days
1 day = 86,400 seconds (≈ 100,000 seconds)
1 hour = 3,600 seconds
1 minute = 60 seconds

QPS for N days of data:
  N × 86,400 seconds per day
  
Example:
  1 billion records in 1 year
  = 1 billion ÷ (365 × 86,400)
  ≈ 31 records per second
```

### 5. Common Bottlenecks to Estimate

When analyzing a system, estimate:
```
✓ QPS (Queries Per Second)
  Peak QPS usually 2X average

✓ Storage
  Per user, per day, multiply by retention period

✓ Cache hit rate
  Affects database load significantly

✓ Network bandwidth
  Required to send data between components

✓ Number of servers needed
  QPS ÷ capacity per server

✓ Memory required
  For cache, sessions, etc.
```

### 6. Sanity Check Your Numbers

```
Does 55 PB for 5 years seem reasonable?
  ✓ 150M DAU × 30MB per user per year = reasonable
  ✓ Price estimate matches industry standards
  ✓ Similar to Netflix, YouTube scale
  
If number seems way off:
  ✓ Re-check calculations
  ✓ Re-examine assumptions
  ✓ Ask interviewer for feedback
```

---

## Quick Reference Estimation Checklist

```
□ Break problem into components
□ Write down assumptions clearly
□ Know power of 2 (2^10, 2^20, 2^30)
□ Know latency numbers (memory vs disk vs network)
□ Calculate QPS for peak traffic (2X average)
□ Estimate storage for retention period
□ Consider read-to-write ratio
□ Use approximation, not exact math
□ Label all units (KB, MB, GB, TB, PB)
□ Sanity check final numbers
□ Identify potential bottlenecks
□ Propose scaling solutions
```

---

## Key Takeaways

```
✓ Estimation is about process, not precision
✓ Know power of 2 and latency numbers by heart
✓ Break problems into manageable pieces
✓ Make assumptions explicit
✓ Use approximation fearlessly
✓ Sanity check your numbers
✓ Think about bottlenecks early
✓ Understand availability implications
✓ Practice, practice, practice
```

---

## References

- System Design Interview by Alex Xu, Chapter 2
- Latency Numbers Every Programmer Should Know: colin-scott.github.io
- Google Pro Tip: Back-of-the-Envelope Calculations
- Cloud Provider SLA Documentation (AWS, Google Cloud, Azure)

---

# Chapter 3: A Framework for System Design Interviews


## ⚠️ Important Notice

**This document is based on concepts from "System Design Interview" by Alex Xu.**

This is **original content**: summaries, explanations, and real-world examples created to help understand system design concepts. It does not reproduce copyrighted material from the book. All content is restructured and rewritten for clarity and educational purposes.

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Understanding the Interview](#understanding-the-interview)
3. [What Interviewers Look For](#what-interviewers-look-for)
4. [The 4-Step Framework](#the-4-step-framework)
5. [Step 1: Understand the Problem](#step-1-understand-the-problem-and-establish-design-scope)
6. [Step 2: High-Level Design](#step-2-propose-high-level-design-and-get-buy-in)
7. [Step 3: Design Deep Dive](#step-3-design-deep-dive)
8. [Step 4: Wrap-up](#step-4-wrap-up)
9. [Time Management](#time-management)
10. [Dos and Don'ts](#dos-and-donts)

---

## Executive Summary

System design interviews simulate **real-world collaboration** where two engineers solve an ambiguous problem together.

**Key Insight:** The final design is LESS important than demonstrating:
- Clear thinking and communication
- Problem-solving approach
- Ability to handle feedback
- Architectural understanding

**The Goal:** Show you can navigate ambiguity, ask good questions, and make sound decisions.

---

## Understanding the Interview

### What It's NOT

```
✗ Not a trivia contest with right/wrong answers
✗ Not about knowing everything
✗ Not about designing Netflix from scratch in 45 minutes
✗ Not about perfect code or detailed implementation
```

### What It IS

```
✓ Collaboration between two engineers
✓ Solving an ambiguous, open-ended problem
✓ Demonstrating design skills and trade-off analysis
✓ Showing communication and problem-solving ability
✓ Proving you can ask the RIGHT questions
```

### Real vs Interview Design

```
Real System (Netflix):
  - Built by 1000+ engineers
  - 10+ years of iteration
  - Billions in infrastructure
  - Unimaginably complex

Interview Design (45 minutes):
  - Focus on core concepts
  - Demonstrate architectural thinking
  - Show scalability patterns
  - Explain trade-offs clearly

You're NOT expected to design the real Netflix!
```

---

## What Interviewers Look For

### 1. Collaboration Skills

```
✓ Works with interviewer as a teammate
✓ Asks for feedback actively
✓ Adjusts based on input
✓ Explains reasoning clearly

✗ Works silently without talking
✗ Defensive about ideas
✗ Ignores feedback
```

### 2. Handling Pressure & Ambiguity

```
✓ Stays calm when requirements unclear
✓ Makes reasonable assumptions
✓ Asks clarifying questions
✓ Adapts to changing requirements

✗ Panics when stuck
✗ Gives up easily
✗ Assumes silently without confirming
```

### 3. Communication Ability

```
✓ Explains concepts clearly
✓ Walks interviewer through thinking
✓ Draws diagrams on whiteboard
✓ Labels components clearly
✓ Uses consistent terminology

✗ Stays silent for long periods
✗ Mumbles or unclear speech
✗ Jumps between ideas randomly
```

### 4. Question-Asking Ability

```
✓ Asks to clarify requirements
✓ Questions assumptions
✓ Probes for constraints
✓ Tests understanding

✗ Assumes you know everything
✗ Jumps to implementation
✗ Never asks for clarification
```

### 5. Technical Depth

```
✓ Understands distributed systems concepts
✓ Discusses trade-offs knowledgeably
✓ Considers scalability from start
✓ Identifies bottlenecks

✗ Only knows one approach
✗ Can't explain why choices made
✗ Overengineers unnecessarily
```

### Red Flags to Avoid

```
🚩 Over-engineering: Perfect design that's overkill
   Example: Designing Netflix-scale system for startup

🚩 Narrow-mindedness: Only considers one solution
   Example: "NoSQL is always better" (context dependent!)

🚩 Not listening: Ignores interviewer feedback
   Example: Interviewer says "focus on scalability"
           You spend 30 mins on UI/UX

🚩 No trade-off analysis: Pretends every choice is free
   Example: "We'll use both Kafka and RabbitMQ"
           Without discussing why or trade-offs

🚩 Vague design: Handwavy architecture
   Example: "We'll use the cloud" (which service? how?)
```

---

## The 4-Step Framework

### Overview

```
45-minute interview breakdown:

Step 1: Understand Problem          3-10 minutes
        ↓
Step 2: High-Level Design          10-15 minutes
        ↓
Step 3: Design Deep Dive           10-25 minutes
        ↓
Step 4: Wrap-up                    3-5 minutes
```

**Time is flexible based on problem scope and interviewer feedback!**

---

## Step 1: Understand the Problem and Establish Design Scope

### The Mistake to Avoid

```
❌ Bad: Candidate jumps straight to solution
        "We need load balancer, database replicas, cache..."
        (Without knowing actual requirements!)

✅ Good: Candidate asks clarifying questions first
         "What features are most important?"
         "How many users?"
         "What's the growth timeline?"
```

### Questions to Ask

```
Functional Requirements:
  Q: What specific features must we build?
  Q: Who are the users?
  Q: How do users interact with the system?

Scale and Traffic:
  Q: How many users do we expect?
  Q: What's the traffic volume? (QPS, DAU, etc.)
  Q: What's the expected growth? (3 months, 6 months, 1 year?)

Constraints:
  Q: Any compliance requirements? (GDPR, HIPAA, etc.)
  Q: What's our latency requirement? (< 100ms?)
  Q: What's our availability target? (99.9%?)

Technology Stack:
  Q: What existing services can we leverage?
  Q: Any preferred technologies?
  Q: Cloud or on-premise?
```

### Real Interview Example: Design a News Feed System

```
Candidate: "Is this mobile, web, or both?"
Interviewer: "Both"

Candidate: "What are the key features?"
Interviewer: "Make a post and see friends' posts"

Candidate: "How many friends can a user have?"
Interviewer: "5000"

Candidate: "What's the traffic?"
Interviewer: "10 million DAU"

Candidate: "Can posts have media?"
Interviewer: "Yes, images and videos"

Candidate: "How should the feed be sorted?"
Interviewer: "Reverse chronological order (newest first)"
```

### Document Your Assumptions

```
Write on whiteboard:
  • 10 million daily active users
  • 50% read-to-write ratio
  • Users can have up to 5,000 friends
  • Average session: 30 minutes
  • Spike traffic: 2X average

Why?
  Prevents misunderstandings later
  Gives you reference point during interview
  Shows structured thinking
```

---

## Step 2: Propose High-Level Design and Get Buy-In

### The Goal

```
Create a simple blueprint showing:
  ✓ Major components
  ✓ How they interact
  ✓ Data flow between them
  ✓ Basic architecture
```

### What to Include

**Box Diagram with:**
```
Clients (mobile/web)
    ↓
Load Balancer
    ↓
Web Servers
    ↓
Cache Layer
    ↓
Database
    ↓
Other services
```

### Example: News Feed System High-Level Design

```
Users
  ↓
Load Balancer
  ├─→ Web Server (Timeline API)
  ├─→ Web Server (Feed API)
  └─→ Web Server (Auth API)
  ↓
Database
  └─→ Write to master
  └─→ Read from replicas
  ↓
Cache (Redis)
  └─→ Store frequently accessed feeds
  ↓
Message Queue
  └─→ Async feed updates
```

### Back-of-Envelope Estimation

```
At this step, do rough calculations:

10M DAU × 1 hour average session = 10M requests per hour
= 10M ÷ 3600 = ~2,777 requests per second

Peak: 2,777 × 2 = ~5,500 QPS

How many servers?
Each server handles ~500 QPS
5,500 ÷ 500 = 11 servers (round up to 12)

✓ Store these numbers, reference later
```

### Key Principle: Collaborate

```
✓ "I'm thinking about this architecture. What do you think?"
✓ Draw on whiteboard, explain as you draw
✓ Ask for feedback: "Does this approach work?"
✓ Be open to suggestions: "That's a good point, let me adjust"

✗ "Here's what we're doing" (no discussion)
✗ Draw everything then explain (audience lost)
✗ Defend ideas regardless of feedback
```

### Be Flexible on Detail Level

```
Sometimes interviewer will say:
  "This looks good, but let's focus on X"

Adjust your depth accordingly!
  • Asked about caching? → Deep dive on cache
  • Asked about database? → Deep dive on sharding
  • Asked about scalability? → Deep dive on load handling

Don't waste time on what they don't care about
```

---

## Step 3: Design Deep Dive

### The Goal

```
Take most critical/interesting components and detail them

NOT: Detail every single component equally
YES: Deep dive into interviewer's areas of interest
```

### Time Management

```
You have 10-25 minutes for deep dive
Can't detail everything!

Prioritize based on:
  1. What interviewer explicitly asked about
  2. What shows your strengths
  3. What impacts scalability most
  4. Most interesting technical challenges
```

### Example Deep Dives

**News Feed System Deep Dives:**
```
❌ Don't try to detail:
   - How load balancer works
   - How cache eviction works
   - How database indexing works
   (Unless interviewer asks)

✅ Instead, deep dive into:
   - How to generate feed efficiently
   - How to handle 10M DAU
   - How to reduce latency
   - How to handle hot users
   (Most interesting technical challenges)
```

**URL Shortener Deep Dives:**
```
Option 1: Hash function design
  - Hash + collision resolution
  - Base 62 conversion
  - Trade-offs between approaches

Option 2: Distributed ID generation
  - Snowflake IDs
  - Scalability concerns
  - Failure handling

Option 3: Database optimization
  - Sharding strategy
  - Indexing
  - Query patterns
```

### Structure of Deep Dive

```
For each component:

1. Identify current bottleneck
   "With 1M QPS, single cache server can't keep up"

2. Propose solution
   "Use Redis cluster with sharding"

3. Explain trade-off
   "Faster but adds complexity"

4. Discuss alternatives
   "Could use Memcached, but Redis offers more"

5. Estimate impact
   "Reduces latency from 100ms to 5ms"
```

### Red Flags During Deep Dive

```
🚩 Going too deep on unimportant details
   "Let me explain this obscure configuration..."
   → Focus on what matters for system design

🚩 Not explaining reasoning
   "We use PostgreSQL"
   → Why? Trade-offs vs MySQL? When to choose?

🚩 Oversimplifying
   "We just use AWS, it handles everything"
   → Which AWS services? How? Trade-offs?

🚩 Running out of time
   Plan ahead, don't spend 20 mins on step 2
```

---

## Step 4: Wrap-up

### The Goal

```
Finish strong by showing:
  ✓ System bottlenecks
  ✓ Potential improvements
  ✓ How to handle next scale curve
  ✓ Additional considerations
```

### Topics to Cover

**Identify Bottlenecks:**
```
Q: Where might this system break?
A: "At 100M users:
    - Database reads would slow down
    - Cache hit ratio might drop
    - Network between DCs might saturate"
```

**Discuss Improvements:**
```
Never say "My design is perfect"
Always have ideas for next steps:
  - "If we need 10X capacity, we'd shard the database"
  - "We could move hot data to separate cache"
  - "We could add CDN for static content"
```

**Handle Next Scale Curve:**
```
"If traffic grows 10X:
  - Add read replicas for database
  - Expand cache cluster
  - Implement database sharding
  - Add more data centers"
```

**Error Cases & Resilience:**
```
What if...?
  "Database is down?"
  "Cache server fails?"
  "Network partition between regions?"
  "Sudden traffic spike?"
  
For each: Explain mitigation strategy
```

**Monitoring & Operations:**
```
How would you know if this works?
  - Key metrics to monitor
  - Alerting thresholds
  - Logging strategy
  - Deployment approach
```

### Great Closing Statement

```
"The key trade-off we made is between consistency
and availability. We chose eventual consistency
for better scalability, which is acceptable for
a social media feed. For mission-critical data,
we'd make different choices."

Shows:
  ✓ Thoughtful decision-making
  ✓ Understanding of constraints
  ✓ Maturity in design
  ✓ No false confidence
```

---

## Time Management

### 45-Minute Breakdown (Guide Only)

```
Ideal Case:

Step 1 (5 min):  Understand problem
                 - Ask 3-5 clarifying questions
                 - Document assumptions
                 - Confirm understanding

Step 2 (12 min): High-level design
                 - Draw simple architecture
                 - Do back-of-envelope estimation
                 - Get interviewer buy-in
                 - Identify areas for deep dive

Step 3 (20 min): Design deep dive
                 - Interviewer leads (based on interest)
                 - Detail most important component
                 - Discuss trade-offs
                 - Explain reasoning

Step 4 (4 min):  Wrap-up
                 - Summarize design
                 - Discuss bottlenecks
                 - Mention improvements if time left
                 - Thank interviewer
```

### Adjust Based on Feedback

```
If interviewer says "Focus on scalability":
  Spend more time on Step 3 (deep dive)
  Less time on Step 1 (clarification done)

If interviewer keeps asking questions:
  They want more details
  Go deeper than initially planned

If interviewer looks bored:
  Move faster, less detail
  Jump to next topic
```

### Watch the Clock

```
0:00 - 0:05   Step 1 (understand problem)
0:05 - 0:20   Step 2 (high-level design)
0:20 - 0:40   Step 3 (deep dive)
0:40 - 0:45   Step 4 (wrap-up)

If you're at 0:30 still in Step 1:
  ⚠️ Speed up! You're behind schedule
  Ask fewer questions, propose design
```

---

## Dos and Don'ts

### DOs ✓

```
✓ Always ask for clarification
  "Can you explain what you mean by real-time?"

✓ Make assumptions explicit
  "I'm assuming 1M DAU. Is that correct?"

✓ Communicate constantly
  "I'm thinking about load balancing here..."

✓ Draw diagrams
  Visual communication > words only

✓ Suggest multiple approaches
  "We could use X, Y, or Z. Here's the trade-off..."

✓ Think out loud
  "Let me think... first we need to..."

✓ Listen to interviewer feedback
  "You made a good point about latency..."

✓ Start high-level, then drill down
  "First, broad architecture, then we'll detail..."

✓ Bounce ideas off interviewer
  "What do you think about this approach?"

✓ Never give up
  If stuck: "Let me think about that... any hints?"
```

### DON'Ts ✗

```
✗ Jump to solution without clarifying
  "We need Kafka, Redis, and PostgreSQL"
  (Without understanding what you're building!)

✗ Go deep too early
  "The cache eviction policy should be LRU because..."
  (First, does caching help? How much?)

✗ Pretend to know everything
  "I know exactly how to build this"
  (Red flag! Everyone asks questions)

✗ Be defensive about ideas
  Interviewer: "What about caching?"
  You: "It won't help for this use case"
  (Listen to their idea!)

✗ Ignore time pressure
  "Let me explain one more thing..."
  (Time's up!)

✗ Make up numbers
  Interviewer: "How much storage?"
  You: "Like... 500 TB?"
  (Show your math!)

✗ Assume you understand requirements
  Confirm everything explicitly!

✗ Code or get into implementation details
  "Let me write the algorithm..."
  (System design is architecture, not coding!)

✗ Overcomplicate early
  "We need distributed transactions with Paxos..."
  (Do you really? Justify it!)

✗ Think in silence
  Interviewer gets lost
  "What are you thinking?"
  (Talk out loud!)
```

---

## Example: System Design in Action

### Problem: Design Instagram

**Step 1: Clarify (3 min)**
```
Candidate: "Is this just the mobile app or web too?"
Interviewer: "Both"

Candidate: "What features are most important?"
Interviewer: "Upload photo, see feed, like, comment"

Candidate: "How many users?"
Interviewer: "100M DAU"

Assumptions documented:
  • 100M daily active users
  • Peak traffic: 2X average
  • Photos stored for 10 years
  • Simple feed (reverse chronological)
```

**Step 2: High-Level Design (12 min)**
```
Candidate draws:

                      CDN
                       ↓
                  Load Balancer
                       ↓
    ┌──────────────┬──────────────┬──────────────┐
    ↓              ↓              ↓              ↓
Upload Service  Feed Service  Search Service  Auth Service
    │              │              │              │
    └──────────────┴──────────────┴──────────────┘
                       ↓
                  Cache (Redis)
                       ↓
               Master Database
                       ↓
          Slave1  Slave2  Slave3
                       ↓
               Object Storage (S3)

Candidate: "Back-of-envelope: 100M DAU doing ~1 action/min
           = ~1.6M actions/second peak
           = ~20 servers at 100K QPS each
           = ~50TB storage for 1 day of photos"
```

**Step 3: Deep Dive (20 min)**
```
Interviewer: "Let's focus on photo upload scalability"

Candidate dives into:
  1. Upload flow
     Client → Upload Service → Validation → S3
  2. Thumbnail generation
     Async job after upload
  3. Feed generation
     How to show photos from followed accounts
  4. Scaling at 100M users
     Horizontal scaling strategy
  5. Trade-offs
     Synchronous vs async thumbnail gen
```

**Step 4: Wrap-up (5 min)**
```
Candidate: "Current bottlenecks:
           - Feed generation could be slow
           - Photo storage grows quickly
           
If we scale to 500M users:
  - Database sharding
  - Photo CDN worldwide
  - More async processing
  
Questions?"

Interviewer: "Good job!"
```

---

## Key Takeaways

```
✓ Process matters more than perfect design
✓ Ask questions before jumping to solution
✓ Communicate constantly with interviewer
✓ Use diagrams effectively
✓ Back-of-the-envelope early
✓ Focus deep dive on interesting parts
✓ Discuss trade-offs thoughtfully
✓ Never claim design is perfect
✓ Manage time carefully
✓ Show you can handle feedback
✓ Stay calm under pressure
```

---

## References

- System Design Interview by Alex Xu, Chapter 3
- "Mastering the System Design Interview" talks
- Real interviews from top tech companies (Facebook, Google, Amazon, etc.)

---

## Navigation

**Table of Contents:** [Back to Top](#table-of-contents)
