# System Design Interview - Chapter 4: Design a Rate Limiter

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [Benefits of Rate Limiting](#benefits-of-rate-limiting)
3. [Requirements](#requirements)
4. [Different Solutions/Algorithms](#different-solutionsalgorithms)
5. [Architecture Considerations](#architecture-considerations)
6. [Challenges in Distributed Systems](#challenges-in-distributed-systems)
7. [Additional Considerations](#additional-considerations)

---

## Problem Statement

A **rate limiter** is used to control the rate of traffic sent by a client or service. In the HTTP world, it limits the number of client requests allowed to be sent over a specified period. If the API request count exceeds the threshold defined by the rate limiter, all excess calls are blocked.

### Real-World Examples:
- A user can write no more than 2 posts per second
- You can create a maximum of 10 accounts per day from the same IP address
- You can claim rewards no more than 5 times per week from the same device

### Real-World Rate Limits:
- **Twitter**: 300 tweets per 3 hours
- **Google Docs APIs**: 300 per user per 60 seconds for read requests

---

## Benefits of Rate Limiting

### 1. **Prevent DoS Attacks**
- Almost all APIs published by large tech companies enforce some form of rate limiting
- Prevents both intentional and unintentional Denial of Service attacks
- Protects resources from being starved by malicious users

### 2. **Reduce Costs**
- Limiting excess requests means fewer servers and resources allocated
- Extremely important for companies using paid third-party APIs
- External APIs (check credit, make payment, retrieve health records, etc.) are charged on a per-call basis

### 3. **Prevent Server Overload**
- Filters out excess requests caused by bots or users' misbehavior
- Reduces server load during traffic spikes
- Ensures stable performance for legitimate users

---

## Requirements

### Functional Requirements:
- **Accurately limit excessive requests** - Must prevent requests exceeding the threshold
- **Flexible throttling** - Support different throttle rules (IP, user ID, or other properties)
- **Distributed** - Work across multiple servers/processes
- **Clear feedback** - Inform users when they are throttled (HTTP 429 status code)

### Non-Functional Requirements:
- **Low latency** - Rate limiter should not slow down HTTP response time
- **Memory efficient** - Use minimal memory
- **High fault tolerance** - If a component fails, it doesn't affect the entire system
- **Large scale** - Support high number of requests in a distributed environment

---

## Different Solutions/Algorithms

### 1. Token Bucket Algorithm ⭐ (Most Popular)

**How It Works:**
- A token bucket has pre-defined capacity
- Tokens are added to the bucket at preset rates periodically
- Each request consumes one token
- If there are enough tokens, request goes through; otherwise, it's dropped

**Example:**
```
Bucket Capacity: 4 tokens
Refill Rate: 2 tokens per second

Request arrives:
- Check if tokens available
- If yes: consume 1 token, allow request
- If no: drop request
```

**Parameters:**
- **Bucket size**: Maximum number of tokens allowed in the bucket
- **Refill rate**: Number of tokens added per second

**How Many Buckets?**
- Different bucket per API endpoint (e.g., 1 post/sec, 150 friends/day, 5 likes/sec → 3 buckets per user)
- Different bucket per IP address
- Global bucket for entire system

**Pros:**
- ✅ Easy to implement
- ✅ Memory efficient
- ✅ Allows burst traffic for short periods
- ✅ Used by Amazon and Stripe

**Cons:**
- ❌ Challenging to tune bucket size and refill rate properly
- ❌ Two parameters to optimize

---

### 2. Leaking Bucket Algorithm

**How It Works:**
- Processes requests at a fixed rate (FIFO queue)
- New requests added to queue if not full
- Otherwise, request is dropped
- Queue is drained at regular intervals

**Parameters:**
- **Bucket size**: Queue size holding requests
- **Outflow rate**: How many requests processed per second

**Real-World Usage:**
- Shopify uses this for rate-limiting

**Pros:**
- ✅ Memory efficient with limited queue size
- ✅ Requests processed at stable rate
- ✅ Suitable for stable outflow requirements

**Cons:**
- ❌ Burst of traffic fills queue with old requests
- ❌ Recent requests get rate limited
- ❌ Difficult to tune two parameters

---

### 3. Fixed Window Counter Algorithm

**How It Works:**
- Timeline divided into fixed-sized windows
- Each window has a counter
- Request increments counter
- Once counter reaches threshold, new requests dropped until new window starts

**Example:**
```
Window size: 1 second
Limit: 3 requests per second

Window [1:00-1:01): Counter reaches 3 → excess requests dropped
Window [1:01-1:02): Counter resets to 0
```

**Pros:**
- ✅ Memory efficient
- ✅ Easy to understand
- ✅ Quota resets at end of time window

**Cons:**
- ❌ **Major Issue**: Burst traffic at window edges allows more requests than quota
- ❌ Example: With 5 requests/minute limit:
  - 5 requests between 2:00:00-2:01:00
  - 5 requests between 2:01:00-2:02:00
  - Between 2:00:30-2:01:30 window: 10 requests go through! (2x allowed)

---

### 4. Sliding Window Log Algorithm

**How It Works:**
- Keeps track of request timestamps (usually in Redis sorted sets)
- When new request arrives, removes outdated timestamps (older than current window start)
- Adds new request timestamp to log
- If log size ≤ allowed count, request accepted; otherwise rejected

**Example:**
```
Rate limit: 2 requests per minute

1:00:01 - Request arrives, log empty → ACCEPT (log size = 1)
1:00:30 - Request arrives → ACCEPT (log size = 2)
1:00:50 - Request arrives → REJECT (log size = 3, exceeds limit of 2)
1:01:40 - Request arrives
  - Remove outdated timestamps before 1:00:40 (1:00:01, 1:00:30)
  - Add new timestamp → ACCEPT (log size = 2)
```

**Pros:**
- ✅ Very accurate in any rolling window
- ✅ Requests never exceed rate limit

**Cons:**
- ❌ **High memory consumption** - Stores every rejected request timestamp
- ❌ Not scalable for high-traffic systems

---

### 5. Sliding Window Counter Algorithm (Hybrid Approach)

**How It Works:**
- Combines fixed window counter and sliding window log
- Uses formula to estimate requests in rolling window:
  ```
  Requests in current window + 
  (Requests in previous window × overlap percentage of rolling window)
  ```

**Example:**
```
Rate limit: 7 requests per minute
Previous minute requests: 5
Current minute requests: 3
New request arrives at 30% position in current minute:

Calculation: 3 + (5 × 0.7) = 3 + 3.5 = 6.5 → round down to 6
Since 6 < 7 limit: REQUEST ACCEPTED
```

**Pros:**
- ✅ Smooths out traffic spikes
- ✅ Based on average rate of previous window
- ✅ Memory efficient

**Cons:**
- ❌ Only works for not-so-strict lookback windows
- ❌ Approximation (assumes even distribution)
- ❌ Cloudflare found only 0.003% error rate among 400M requests (acceptable)

---

## Algorithm Comparison Table

| Algorithm | Memory | Accuracy | Complexity | Use Case |
|-----------|--------|----------|-----------|----------|
| Token Bucket | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Easy | Most common, burst traffic |
| Leaking Bucket | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Medium | Stable outflow needed |
| Fixed Window | ⭐⭐⭐⭐⭐ | ⭐⭐ | Easy | Simple, but edge issues |
| Sliding Window Log | ⭐⭐ | ⭐⭐⭐⭐⭐ | Complex | High accuracy needed |
| Sliding Window Counter | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Medium | Good balance |

---

## Architecture Considerations

### Where to Place the Rate Limiter?

#### 1. **Client-Side Implementation** ❌
- **Not recommended** - Clients are unreliable
- Client requests can be forged by malicious actors
- No control over client implementation

#### 2. **Server-Side Implementation** ✅
- Rate limiter placed directly on server
- Added latency to requests
- Coupled with application code

#### 3. **API Gateway/Middleware** ✅ (Recommended)
- Rate limiter as separate middleware
- Decoupled from application
- Supports multiple algorithms
- Popular in microservices architecture

### Storage for Counters

**Why Not Database?**
- ❌ Too slow - disk access latency
- ❌ Not suitable for real-time counters

**Why Redis?** ✅
- ✅ In-memory - fast access
- ✅ Supports time-based expiration
- ✅ Two key commands:
  - `INCR`: Increment counter by 1
  - `EXPIRE`: Set timeout for counter (auto-delete)

### High-Level Architecture Flow

```
1. Client sends request to rate limiter middleware
2. Rate limiter fetches counter from Redis
3. Check if limit reached
   - If YES: Return HTTP 429 (Too Many Requests)
   - If NO: Forward to API servers, increment counter, save to Redis
4. Return response with rate limit headers to client
```

---

## Challenges in Distributed Systems

### 1. Race Condition Problem

**Scenario:**
```
Redis counter value: 3
Two concurrent requests read counter simultaneously

Thread 1: Read 3 → Check (3+1 ≤ limit) → Write 4
Thread 2: Read 3 → Check (3+1 ≤ limit) → Write 4

Result: Counter is 4 (WRONG! Should be 5)
```

**Solutions:**
- **Lua Script** - Atomic operation in Redis
- **Sorted Sets** - Redis data structure for atomic operations
- Avoid using simple locks (too slow)

### 2. Synchronization Issue in Multi-Server Setup

**Problem:**
```
Client 1 → Rate Limiter Server 1 (has client 1's counter)
Client 2 → Rate Limiter Server 2 (has client 2's counter)

Due to stateless design, clients might switch servers:
Client 1 → Rate Limiter Server 2 (doesn't have client 1's data!)
Rate limiter doesn't work properly
```

**Solution:**
- Use **centralized data store** (Redis)
- All rate limiter servers fetch/update counters from same Redis
- ❌ Avoid sticky sessions (not scalable, not flexible)

---

## Additional Considerations

### 1. Rate Limiter Response Headers

Inform clients about their rate limit status:

```
X-Ratelimit-Limit: The max requests allowed per time window
X-Ratelimit-Remaining: Remaining requests in current window
X-Ratelimit-Retry-After: When to retry after being rate limited
```

### 2. Handling Rate-Limited Requests

**Option A: Drop Request**
- Return HTTP 429 immediately
- Client must retry

**Option B: Queue for Later**
- Example: Keep orders in queue to process later
- Prevents loss during overload

### 3. Performance Optimization

#### Multi-Data Center Setup
- Deploy rate limiters in geographically distributed edge servers
- Route traffic to closest edge server
- Reduces latency for global users
- Example: Cloudflare has 194+ edge servers worldwide

#### Eventual Consistency
- Synchronize data across data centers with eventual consistency model
- Trade absolute consistency for performance
- Acceptable for rate limiting use cases

### 4. Monitoring & Analytics

**Track:**
- Is the rate limiting algorithm effective?
- Are the rate limiting rules effective?

**Scenarios:**
- Rules too strict → Many valid requests dropped → Relax rules
- Algorithm ineffective during flash sales → Use Token Bucket for burst traffic

### 5. Hard vs Soft Rate Limiting

- **Hard**: Request count cannot exceed threshold (strict)
- **Soft**: Requests can exceed threshold for short period (flexible)

### 6. Rate Limiting at Different OSI Layers

Not just application level (HTTP):
- **Layer 7 (Application)**: HTTP rate limiting (this chapter)
- **Layer 3 (Network)**: IP address rate limiting using Iptables

### 7. Client Best Practices to Avoid Rate Limiting

- Use client-side cache to avoid frequent API calls
- Understand the limit and don't send too many requests in short time
- Implement exception handling for graceful recovery
- Add sufficient backoff time to retry logic

---

## Summary

| Aspect | Key Takeaway |
|--------|--------------|
| **Best Algorithm** | Token Bucket (most flexible, widely used) |
| **Best Placement** | API Gateway/Middleware (decoupled, flexible) |
| **Best Storage** | Redis (fast, TTL support) |
| **Distributed Challenge** | Use Redis for centralized counters + Lua scripts for atomicity |
| **Optimization** | Multi-data center setup + eventual consistency |

---

## References
- Rate-limiting strategies: https://cloud.google.com/solutions/rate-limiting-strategies-techniques
- Twitter rate limits: https://developer.twitter.com/en/docs/basics/rate-limits
- Google docs API limits: https://developers.google.com/docs/api/limits
- AWS API Gateway throttling: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
- Stripe rate limiters: https://stripe.com/blog/rate-limiters
- Shopify rate limits: https://help.shopify.com/en/api/reference/rest-admin-api-rate-limits
- Better Rate Limiting with Redis: https://engineering.classdojo.com/blog/2015/02/06/rolling-rate-limiter/
- Lyft rate limiting: https://github.com/lyft/ratelimit
