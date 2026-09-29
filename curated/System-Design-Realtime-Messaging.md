# System Design Realtime Messaging

Quick-reference notes — part of the System Design series. Converted from `System-Design-Notes.txt`.

## Long-Polling vs WebSockets vs Server-Sent Events

⏰ LONG-POLLING:
Client polls server repeatedly: "Any new data?" → Server responds → Client waits → Repeat.
Each poll = HTTP request-response (connection closes). Simple but wasteful.

✅ PROS:
```
├─ Simple to implement (standard HTTP)
├─ Works with old browsers/proxies
├─ Stateless server (no persistent connections)
└─ Compatible with load balancers

```

❌ CONS:
```
├─ High latency (delay between polls)
├─ Wasteful (many empty responses)
├─ High server load (constant requests)
├─ Increased bandwidth
└─ Not real-time (polling delay)

```

💼 BUSINESS SCENARIO:
Occasional updates needed (weather app, stock prices every 5-10 sec). Email client checking new mail.
Tolerate 5-10 second delay.

🎯 MEMORY TRICK: "Knock-knock" — client keeps knocking asking "Got data yet?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 WEBSOCKETS:
Persistent TCP connection (bidirectional). Client & server can send messages anytime.
Upgrade from HTTP → WebSocket protocol. Low latency, always connected.

✅ PROS:
```
├─ True real-time (instant communication)
├─ Bidirectional (client ↔ server both ways)
├─ Low latency & overhead
├─ Persistent connection (efficient)
├─ High throughput
└─ Best for chat/gaming

```

❌ CONS:
```
├─ Complex to implement (stateful server)
├─ Hard to scale (sticky sessions needed)
├─ Firewall/proxy issues (some block WebSockets)
├─ More server memory per connection
├─ Requires server support (not all frameworks)
└─ Connection management complexity

```

💼 BUSINESS SCENARIO:
Real-time apps: Chat, multiplayer gaming, collaborative tools, live trading, live notifications.
CANNOT tolerate delay.

🎯 MEMORY TRICK: "Phone call" — both sides can talk anytime, 24/7 connection open.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📡 SERVER-SENT EVENTS (SSE):
Persistent HTTP connection (unidirectional). Server PUSHES data to client anytime.
Client opens connection, server sends updates. Client cannot send messages back.

✅ PROS:
```
├─ Simple to implement (standard HTTP)
├─ Real-time push (server initiates)
├─ Low latency
├─ Works with proxies/firewalls (HTTP)
├─ Automatic reconnection
├─ Less bandwidth than Long-Polling
├─ Stateless scaling easier than WebSockets
└─ Built-in event handling

```

❌ CONS:
```
├─ Unidirectional only (server → client)
├─ HTTP connection overhead
├─ Older browser support issues
├─ Max 6 connections per domain (browser limit)
├─ No binary data (text only)
└─ If client needs to send, need separate channel

```

💼 BUSINESS SCENARIO:
Server pushes updates: Live notifications, stock tickers, leaderboards, activity feeds, live comments.
ONE-way communication enough.

🎯 MEMORY TRICK: "News broadcast" — server broadcasts, clients listen (no feedback channel).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPARISON TABLE:

```
┌─────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ Aspect          │ Long-Polling     │ WebSockets       │ SSE              │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Latency         │ 🐌 High (5-10s)  │ ⚡ Low (<100ms)  │ ⚡ Low (<100ms)  │
│ Bi-directional  │ ✗ No (one-way)   │ ✓ Yes (both ways)│ ✗ No (push only) │
│ Complexity      │ 🟢 Simple        │ 🔴 Complex       │ 🟡 Medium        │
│ Bandwidth       │ 🔴 High (waste)  │ 🟢 Low           │ 🟢 Low           │
│ Scalability     │ 🟡 Medium        │ 🔴 Hard          │ 🟢 Easier        │
│ Firewall-safe   │ ✓ Yes            │ ✗ Sometimes      │ ✓ Yes            │
│ Server Load     │ 🔴 High          │ 🟡 Medium        │ 🟡 Medium        │
│ Real-time       │ ✗ No             │ ✓ Yes            │ ✓ Yes            │
│ Browser Support │ ✓ Old browsers   │ ✓ Modern only    │ ✓ Modern only    │
└─────────────────┴──────────────────┴──────────────────┴──────────────────┘

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION TREE:

Need real-time bidirectional?
```
├─ YES → WebSockets (chat, gaming, collaborative tools)
└─ NO → Server push enough?
   ├─ YES → SSE (notifications, feeds, leaderboards)
   └─ NO → Long-Polling (low traffic, simple, old browsers)

```

Need to scale to 100k+ concurrent users?
```
├─ Long-Polling → Hard (too many requests)
├─ WebSockets → Very hard (stateful, sticky sessions)
└─ SSE → Easier (stateless, simpler scaling)

```

Have firewall/proxy restrictions?
```
├─ YES → Long-Polling or SSE (HTTP safe)
└─ NO → WebSockets (more efficient)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REAL-WORLD EXAMPLES:

Long-Polling:
```
├─ Gmail (checks new mail every few seconds)
├─ Old messaging apps
└─ Polling-based systems

```

WebSockets:
```
├─ Discord chat (instant messages)
├─ Online multiplayer games (Fortnite, Call of Duty)
├─ Collaborative tools (Google Docs)
├─ Live trading platforms
└─ Video conferencing (signaling)

```

SSE:
```
├─ Twitter/Facebook notifications (likes, comments)
├─ Live score updates (sports apps)
├─ Stock tickers
├─ YouTube live chat (one-way)
├─ Activity feeds
└─ Weather alerts

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTERVIEW SCENARIOS:

Q: "Design notification system for 1M users"
A: "Use SSE. Server pushes notifications (one-way enough). Easier to scale than WebSockets.
    Simple HTTP, works with load balancers. If users need to ACK, add separate small channel."

Q: "Design chat application"
A: "Use WebSockets. Need real-time bidirectional (messages both ways). Use sticky sessions
    for scaling. Or hybrid: WebSockets for chat, SSE for notifications."

Q: "Design stock ticker"
A: "Use SSE. Server pushes price updates (one-way). Low bandwidth, simple, scales well.
    Client just listens to price stream."

Q: "Design system for old IE6 browsers"
A: "Use Long-Polling. WebSockets not supported. Accept higher latency/load for compatibility."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK SUMMARY:

🟢 Long-Polling  = Client knocks repeatedly. Simple, old browsers, high latency/load.
🔵 WebSockets    = Always-open call. Real-time both ways, complex, hard to scale.
🟡 SSE           = Server broadcasts. Real-time one-way, simple, scalable.

Pick based on:
```
├─ Need instant two-way? → WebSockets
├─ Need instant one-way? → SSE
└─ Can wait 5-10 sec? → Long-Polling

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCALABILITY RANKING (Best → Worst):
1. SSE (easiest to scale, HTTP, stateless)
2. Long-Polling (harder, lots of requests)
3. WebSockets (hardest, stateful, sticky sessions)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BANDWIDTH RANKING (Best → Worst):
1. WebSockets (persistent, minimal overhead)
2. SSE (HTTP overhead but persistent)
3. Long-Polling (many requests, lots of overhead)


---

## How SSE is stateless ?

GREAT CLARIFICATION QUESTION!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Actually, SSE is NOT perfectly stateless. I should clarify what I meant earlier.

When I said "SSE is stateless," I was comparing it to WebSockets.
More accurate: "SSE is SIMPLER STATE than WebSockets"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WEBSOCKETS (Stateful):

Server must maintain:
```
├─ Connection object for each client
├─ Client ID → Socket mapping
├─ Bidirectional message queue
├─ Connection state (open, closed, etc.)
├─ Message history per client
└─ All in server memory

```

Example:
  Server memory:
```
  ├─ Client1 → Socket1 (open, connected)
  ├─ Client2 → Socket2 (open, connected)
  └─ Client3 → Socket3 (open, connected)

```

If server crashes:
```
  └─ ALL connections lost! ❌

```

Scaling problem:
```
  ├─ Load balancer routes Client1 to Server A
  ├─ Client1 reconnects → goes to Server B (sticky session problem!)
  └─ Server B doesn't know Client1's state from Server A

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SSE (Simpler State):

Server maintains:
```
├─ Open HTTP connections (just streams, not complex objects)
├─ List of connected clients (simpler)
├─ Just need to push data periodically
└─ No bidirectional messaging complexity

```

Example:
  Server memory:
```
  ├─ Client1 → Stream (open)
  ├─ Client2 → Stream (open)
  └─ Client3 → Stream (open)

```

If server crashes:
```
  └─ Clients reconnect automatically (SSE has built-in reconnect!) ✓

```

Scaling:
```
  ├─ Client1 connects to Server A (gets stream)
  ├─ Server A crashes
  ├─ Load balancer routes Client1 to Server B
  ├─ Client1 automatically reconnects (SSE protocol)
  ├─ Server B: "New client, start sending data"
  └─ Client doesn't care which server! ✓

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY SSE IS "MORE STATELESS" THAN WEBSOCKETS:

WebSockets:
```
├─ Server: "I need to remember who Client1 is"
├─ Server: "I need to know Client1's message history"
├─ Server: "Client1 ONLY talks to me"
├─ Stateful relationship
└─ Hard to scale

```

SSE:
```
├─ Server: "I just push data to anyone listening"
├─ Server: "If they disconnect, they reconnect themselves"
├─ Server: "Client can reconnect to ANY server"
├─ Less stateful relationship
└─ Easy to scale (stateless servers)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRACTICAL EXAMPLE: STOCK TICKER

WebSockets (Stateful):

Server A keeps track:
```
├─ Client1 connected to Server A
├─ If Client1 disconnects → data about them is gone
├─ Server A must remember "Client1 was here"
└─ Must use sticky sessions (always route to A)

```

Load balancing problem:
```
  Client1 ──────→ Server A (connected)

```
             ↓ (crash)
         Route to Server B?
             ↓
         Server B: "Who is Client1?" ❌

SSE (Stateless-like):

Server A and B both broadcast:
```
├─ Server A: "Stock price is $100"
├─ Server B: "Stock price is $100"
├─ Any client listening gets the data
├─ Client doesn't care which server!

```

Client switching:
```
  Client1 ──→ Server A (gets stream)

```
         ↓ (A crashes)
```
  Client1 ──→ Server B (automatically reconnects, gets stream)

```
         ↓ (no state lost, just continues receiving data)

Server doesn't need to know:
```
  ├─ "Which Client1 are you?"
  ├─ "What history do you need?"
  ├─ "Are you the real Client1?"
  └─ Just: "You want stock prices? Here they are:"

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPARISON TABLE:

```
┌──────────────────┬──────────────────────┬──────────────────────┐
│ Aspect           │ WebSockets (Stateful)│ SSE (Stateless-like) │
├──────────────────┼──────────────────────┼──────────────────────┤
│ Server tracks    │ Connection state     │ Just streams         │
│ Client identity? │ YES (must remember)  │ NO (just push data)  │
│ Crash recovery   │ Connections lost ❌  │ Auto-reconnect ✓     │
│ Sticky sessions? │ YES (needed)         │ NO (not needed)      │
│ Load balancing   │ Hard (affinity)      │ Easy (any server)    │
│ State per client?│ High (complex)       │ Low (simple)         │
│ Scalability      │ Limited              │ Better               │
└──────────────────┴──────────────────────┴──────────────────────┘

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BUT SSE ISN'T TRULY STATELESS:

SSE still has STATE:
```
├─ Server must track: "Who is connected?"
├─ Server must know: "Which clients need which data?"
├─ Server must manage: "Open connections"
└─ It's simpler state, but still state!

```

Better term: "SSE is LOOSELY COUPLED" or "EASIER TO SCALE"

Not truly stateless like HTTP (where each request is independent):
```
├─ HTTP stateless: Each request is independent
│  └─ Server doesn't remember previous requests
├─ SSE: Maintains connection stream
│  └─ But doesn't need to remember client details
└─ Somewhere in between

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY SSE SCALES BETTER (The Real Advantage):

Server can be FUNCTIONALLY STATELESS:

SSE pattern:
```
├─ Server A: Broadcasts "Stock price = $100"
├─ Server B: Broadcasts "Stock price = $100"
├─ Load balancer: Routes clients randomly
├─ Client1 → Server A → Reconnects → Server B (same data!)
├─ Result: No sticky sessions needed!

```

This means:
```
├─ Servers can be identical (no special state tracking)
├─ Can add/remove servers dynamically
├─ Load balancer can route freely
├─ Easier horizontal scaling

```

WebSockets pattern:
```
├─ Server A: Maintains specific client connections
├─ Server B: Maintains different client connections
├─ Load balancer: Must route Client1 → always Server A
├─ If A crashes → Client1 must explicitly reconnect to same data
├─ Result: Needs sticky sessions (complex)

```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORRECT TERMINOLOGY:

NOT stateless, but:
```
├─ ✓ "Easier to scale" (simpler state management)
├─ ✓ "Loosely coupled" (client doesn't depend on specific server)
├─ ✓ "Horizontally scalable" (can add servers)
├─ ✓ "Load-balancer friendly" (no sticky sessions needed)
└─ ✓ "Functionally stateless" (servers behave like stateless)

```

True stateless = HTTP (each request independent, no connection)
Not stateless = SSE (maintains connection stream)
But closer to stateless than WebSockets!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:

"SSE is stateless" was an oversimplification.

Better: "SSE has simpler state than WebSockets, making it easier to scale
horizontally and implement as load-balanced servers without sticky sessions."

It's not that SSE has NO state, it's that:
```
├─ State is simpler (just: "who's listening?")
├─ State is interchangeable (any server can handle client)
├─ State doesn't need to persist (auto-reconnect handles it)
└─ Servers can be disposed and recreated easily

```

That's what makes it "stateless-like" and scalable! 🎯


---

## Explain serverless concept rgarding functions, containers and databases. I used to think, only functions can be serverless.

SERVERLESS ≠ ONLY FUNCTIONS
```
═══════════════════════════════════════════════════════════════

```

What "Serverless" ACTUALLY means:
```
└─ You don't manage servers
└─ You don't provision capacity
└─ You pay per usage (not per hour)
└─ Auto-scaling built-in
└─ No ops overhead

```

It applies to ANYTHING:


```
┌────────────────┬──────────────────────┬──────────────────────────┐
│ Component      │ Traditional          │ Serverless               │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Functions      │ Your own servers     │ Lambda, Cloud Functions  │
│                │ (provision 10 VMs)   │ (pay per invoke)         │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Containers     │ Kubernetes, EC2      │ Fargate, Cloud Run       │
│                │ (manage cluster)     │ (Docker, no ops)         │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Databases      │ RDS, self-managed DB │ DynamoDB, Firestore      │
│                │ (provision capacity) │ (pay per read/write)     │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Storage        │ S3 managed           │ S3 (already serverless)  │
├────────────────┼──────────────────────┼──────────────────────────┤
│ Queues         │ RabbitMQ, Kafka      │ SQS, Pub/Sub             │
└────────────────┴──────────────────────┴──────────────────────────┘

```


SERVERLESS FUNCTIONS
```
═══════════════════════════════════════════════════════════════

```

Traditional:
```
├─ Rent server (24/7)
├─ Deploy code
├─ Pay $100/month (always running)
├─ Handle 10 requests/day or 10k/day (same cost)
└─ You manage scaling

```

Serverless (Lambda):
```
├─ Upload function
├─ Triggered on demand
├─ Pay $0.20/million invocations
├─ Auto-scales to 1000s concurrent
└─ Zero management

```


SERVERLESS CONTAINERS
```
═══════════════════════════════════════════════════════════════

```

Traditional (Kubernetes):
```
├─ Manage cluster of VMs
├─ Deploy containers
├─ Pay for all VMs (24/7)
├─ Manual scaling

```

Serverless (Fargate):
```
├─ Upload Docker image
├─ Fargate runs it
├─ Pay per container-second
├─ Auto-scales to 100s of containers

```


SERVERLESS DATABASES
```
═══════════════════════════════════════════════════════════════

```

Traditional (RDS):
```
├─ Provision DB instance (db.t3.medium)
├─ Pay for instance size ($50-100/month)
├─ Handle 100 or 100k requests (same cost)
├─ You scale: upgrade to larger instance
└─ You manage: backups, patches

```

Serverless (DynamoDB):
```
├─ Create table
├─ Pay per read/write: $0.0000125 per read
├─ Auto-scales to millions of requests
├─ AWS manages everything
└─ Cost scales with usage

```


REAL COMPARISON TABLE
```
═══════════════════════════════════════════════════════════════

┌──────────────┬──────────────────┬──────────────────┬──────────────────┐
│ Aspect       │ Traditional      │ Serverless       │ Trade-off        │
├──────────────┼──────────────────┼──────────────────┼──────────────────┤
│ Payment      │ Fixed (capacity) │ Variable (usage) │ Cost varies      │
│ Scaling      │ Manual           │ Automatic        │ Instant but slow │
│ Cold start   │ None             │ 100-1000ms       │ First call slow  │
│ Limits       │ None (big box)   │ Limits per func  │ Can't do all jobs│
│ Management   │ High ops burden  │ Zero ops         │ Vendor lock-in   │
│ Concurrency  │ Limited          │ Unlimited        │ Scaling cost     │
└──────────────┴──────────────────┴──────────────────┴──────────────────┘

```


SERVERLESS ARCHITECTURE EXAMPLE
```
═══════════════════════════════════════════════════════════════

```

Traditional full-stack:
```
├─ EC2 server ($100/month)
├─ RDS database ($50/month)
├─ S3 storage ($5/month)
└─ Total: $155/month (even if idle)

```

Serverless full-stack:
```
├─ Lambda functions ($0.20 per million invokes)
├─ DynamoDB ($1 per million reads)
├─ S3 storage ($0.023 per GB)
└─ Total: $10-50/month (if low traffic), $1000/month (if high traffic)

```


WHEN SERVERLESS WORKS
```
═══════════════════════════════════════════════════════════════

```

✓ Functions: Event-driven (webhooks, triggers)
✓ Containers: Batch jobs, APIs without 24/7 traffic
✓ Databases: Read/write heavy, variable traffic

Example architecture:
```
└─ API Gateway → Lambda function → DynamoDB
   └─ Webhook comes in → Lambda triggers → Writes to DynamoDB
   └─ Zero servers to manage, auto-scales to 1000s

```


WHEN NOT SERVERLESS
```
═══════════════════════════════════════════════════════════════

```

✗ Functions: Long-running tasks (>15 min)
✗ Containers: Constant 24/7 baseline load
✗ Databases: Predictable high load (cheaper with RDS)

Example:
```
└─ Website gets 10M requests/day steadily
└─ RDS ($100/month) cheaper than DynamoDB ($10k/month)
└─ Lambda would cold-start every request
└─ Traditional servers better choice

```


THE KEY INSIGHT
```
═══════════════════════════════════════════════════════════════

```

"Serverless" = "You don't manage servers"

NOT = "Only functions"
NOT = "Always cheaper"
NOT = "No limits"

It's a OPERATIONAL MODEL:
```
├─ Functions are serverless
├─ Containers (Fargate) are serverless
├─ Databases (DynamoDB) are serverless
├─ Storage (S3) is serverless
└─ Queues (SQS) are serverless

```

All share:
```
├─ No server provisioning
├─ Auto-scaling
├─ Pay per usage
└─ AWS manages ops

```

YES - Serverless databases are PERSISTENT
```
═══════════════════════════════════════════════════════════════

```

Key point: "Serverless" ≠ "Temporary"

Serverless DB will STAY FOREVER (unless you delete):
```
├─ DynamoDB table created → stays running
├─ Data written → persists indefinitely
├─ Even if unused for years → stays there
├─ You pay for storage every month
└─ Only deleted when YOU delete it

```


CONFUSION POINT
```
═══════════════════════════════════════════════════════════════

```

Serverless FUNCTIONS (stateless, temporary):
```
├─ Created when triggered
├─ Runs for milliseconds
├─ Dies when done
├─ Spawned again on next trigger
└─ "Serverless" = no servers to manage

```

Serverless DATABASES (stateful, persistent):
```
├─ Created once
├─ Stays running forever
├─ Grows with data
├─ Survives function calls
└─ "Serverless" = no servers to manage, but DATA PERSISTS ✓

```


COMPARISON
```
═══════════════════════════════════════════════════════════════

┌──────────────┬──────────────────────┬──────────────────────┐
│ Component    │ Lifetime             │ Data Persistence     │
├──────────────┼──────────────────────┼──────────────────────┤
│ Lambda func  │ Milliseconds (call)  │ Stateless            │
│ DynamoDB     │ Until you delete     │ Persistent ✓         │
│ Firestore    │ Until you delete     │ Persistent ✓         │
│ S3           │ Until you delete     │ Persistent ✓         │
└──────────────┴──────────────────────┴──────────────────────┘

```


EXAMPLE: User profile data
```
═══════════════════════════════════════════════════════════════

```

User creates account → Data written to DynamoDB
```
├─ 2024: User active, accessing profile
├─ 2025: User inactive, no requests
├─ 2026: User returns
└─ Profile still there! ✓

```

Cost implication:
```
├─ 2024: Pay for reads/writes
├─ 2025: Pay for STORAGE ONLY ($0.25 per GB/month)
├─ 2026: Pay for reads/writes again
└─ Data survived 1 year of inactivity ✓

```


TRADITIONAL vs SERVERLESS DB
```
═══════════════════════════════════════════════════════════════

```

Traditional RDS:
```
├─ Create instance (db.t3.medium)
├─ Pay hourly even if idle
├─ Can stop instance (pause billing)
├─ Data survives pause ✓
└─ Resume anytime

```

Serverless DynamoDB:
```
├─ Create table
├─ Automatic scaling, no pause
├─ Pay only for usage + storage
├─ Data survives indefinitely ✓
└─ Can't "stop" like RDS

```


SO WHAT'S "SERVERLESS" ABOUT IT?
```
═══════════════════════════════════════════════════════════════

```

NOT: "Database disappears"
NOT: "Data is temporary"
NOT: "Infrastructure is temporary"

YES: "AWS manages servers, you don't"

Traditional RDS:
```
├─ You provision instance size
├─ You manage backups
├─ You manage scaling
├─ You manage patches
└─ You worry about capacity

```

Serverless DynamoDB:
```
├─ AWS provisions resources
├─ AWS manages backups (automatic)
├─ AWS manages scaling (automatic)
├─ AWS manages patches (automatic)
└─ You just access your data ✓

```


PERSISTENCE GUARANTEE
```
═══════════════════════════════════════════════════════════════

```

DynamoDB durability:
```
├─ Data replicated across 3 availability zones
├─ Survives server failures
├─ Survives datacenter failures
├─ Survives regional outages (with multi-region)
└─ Your data is SAFER than traditional DB ✓

```

Deletion:
```
├─ Only happens if YOU delete
├─ AWS won't delete (unless billing fails)
└─ Even then, 30-day grace period

```


BILLING EXAMPLE
```
═══════════════════════════════════════════════════════════════

```

Create DynamoDB table with 1MB data:

Month 1: $0.25 (storage)
Month 2: $0.25 (storage) - zero API calls
Month 3: $0.25 (storage) - zero API calls
Year 1: $3 (storage only)

Then you use it:
Month 13: $0.25 + $100 (queries) = $100.25

Data survived 1 year of zero usage!

Bottom line: Serverless databases are 100% persistent. Your data stays forever (costs money for storage) until you explicitly delete it. The "serverless" part means AWS manages the infrastructure, not that your data is temporary.


---

## How to solve "cold start" problem for serverless functions

COLD START SOLUTIONS
```
═══════════════════════════════════════════════════════════════

┌─────────────────────────┬────────┬──────────┬─────────┐
│ Solution                │ Cost   │ Reduction│ Effort  │
├─────────────────────────┼────────┼──────────┼─────────┤
│ Provisioned Concurrency │ $$$$   │ 100%     │ Low     │
│ Warmup trigger (5min)   │ $      │ 80%      │ Low     │
│ Use Go/Node (not Java)  │ Free   │ 50%      │ Medium  │
│ Optimize package size   │ Free   │ 30%      │ Low     │
│ Reserved concurrency    │ $$     │ 0%*      │ Minimal │
└─────────────────────────┴────────┴──────────┴─────────┘

```
*Prevents throttling, doesn't prevent cold start

QUICKEST FIX:
```
├─ CloudWatch rule → invoke Lambda every 5min
├─ Cost: ~$2/month
└─ Reduces cold starts 80%

```

BEST FOR TRAFFIC API:
```
├─ Provisioned Concurrency: 10-20 containers
├─ Cost: $3-7/day
└─ Zero cold starts

```


---

## How would a kafka broker ever push messages to consumer, I thought, its always pull?

KAFKA IS ALWAYS PULL
```
═══════════════════════════════════════════════════════════════

```

You're correct. Kafka never pushes to consumers.

Consumer behavior:
```
├─ Consumer: "Give me messages from offset 100"
├─ Broker: "Here's messages 100-105"
├─ Consumer: (waits configured time)
├─ Consumer: "Give me messages from offset 106"
├─ Repeat continuously
└─ Result: PULL model ✓

```

Why it FEELS like push:
```
├─ Consumer polls every 300ms (configurable)
├─ New message arrives almost immediately
├─ Consumer app receives via callback
└─ Developer doesn't write poll loop (SDK does)
└─ Looks like "message arrived" but it's still pull

```


PUSH vs PULL
```
═══════════════════════════════════════════════════════════════

```

Push (RabbitMQ, SQS):
```
├─ Broker sends message to consumer
├─ Broker holds connection
├─ Consumer can get overwhelmed

```

Pull (Kafka):
```
├─ Consumer requests "give me next batch"
├─ Consumer controls rate (backpressure)
├─ Consumer can pause/resume easily

```


KAFKA CONSUMER CODE
```
═══════════════════════════════════════════════════════════════

```

while True:
    records = consumer.poll(timeout_ms=300)  ← Explicit pull
    for record in records:
        process(record)


HOW PUSH BROKERS WORK
```
═══════════════════════════════════════════════════════════════

```

RabbitMQ (Push):
```
├─ Consumer connects → establishes channel
├─ Broker sends messages down channel automatically
├─ Broker controls rate (prefetch limit)
├─ Consumer: "I'm ready, send me messages"
└─ Broker: Pushes continuously

```

Google Pub/Sub (Push):
```
├─ Broker makes HTTP POST to consumer's endpoint
├─ "Here's a message: {...}"
├─ Consumer receives unsolicited
└─ Consumer can't control pace (must handle backpressure)

```

SQS (Pull, but looks like push):
```
├─ Actually pull model (consumer polls)
├─ But AWS SDK hides polling
├─ App receives via callback/handler
└─ Feels like push

```


MECHANISM: RabbitMQ example
```
═══════════════════════════════════════════════════════════════

```

Consumer connects:
1. channel.basic_consume(queue_name, callback)
2. Connection stays open
3. Broker sees consumer ready
4. Message arrives in queue
5. Broker sends down connection immediately
6. callback(message) fires
7. Broker waits for ACK
8. Repeat

Vs Kafka:
1. Consumer polls: "any new messages?"
2. Broker replies: "Here's 5 messages"
3. Consumer processes
4. Consumer polls again (loop)


BACKPRESSURE HANDLING
```
═══════════════════════════════════════════════════════════════

```

Push (RabbitMQ):
```
├─ Broker sends fast
├─ Consumer can't keep up
├─ Queue grows on broker
├─ Broker can drop messages if full
└─ Risk: Message loss

```

Pull (Kafka):
```
├─ Consumer asks for batch size (e.g., 100)
├─ Consumer controls pace
├─ No queue buildup on broker
└─ Safe: No message loss        

```


---

## Backpressure?

BACKPRESSURE = Producer faster than Consumer
```
═══════════════════════════════════════════════════════════════

```

Example:
```
├─ Producer: Creates 1000 messages/sec
├─ Consumer: Processes 100 messages/sec
├─ Gap: 900 messages pile up
└─ Problem: Memory fills, system crashes

```


PUSH MODEL (RabbitMQ)
```
═══════════════════════════════════════════════════════════════

```

Broker sends fast:
```
┌──────────┐         ┌──────────┐
│  Broker  │ ─────→  │ Consumer │
│ 1000/sec │         │ 100/sec  │
└──────────┘         └──────────┘

```
            ↓
        Queue builds on broker
        Memory fills
        Risk: Messages dropped


PULL MODEL (Kafka)
```
═══════════════════════════════════════════════════════════════

```

Consumer controls pace:
```
┌──────────┐         ┌──────────┐
│  Broker  │ ←─────  │ Consumer │
│ 1000/sec │ "Give   │ 100/sec  │
│ (waits)  │  me 100"│ (safe)   │
└──────────┘         └──────────┘

```
            ↓
        Consumer pulls only what it can handle
        No queue buildup
        Safe: No message loss


TL;DR:
Push = Broker controls → can overwhelm consumer
Pull = Consumer controls → natural backpressure


---

