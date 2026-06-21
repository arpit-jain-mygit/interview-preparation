# Microservices Architect Interview Questions

## Table of Contents

### Core Patterns
1. [What is the distributed transaction problem in microservices?](#1-what-is-the-distributed-transaction-problem-in-microservices)
2. [What is the Saga pattern?](#2-what-is-the-saga-pattern)
3. [What is Saga choreography?](#3-what-is-saga-choreography)
4. [What is Saga orchestration?](#4-what-is-saga-orchestration)

### Tracing and Observability
4.5 [How to Enable Good Tracing in Choreography and Orchestration?](#45-how-to-enable-good-tracing-in-choreography-and-orchestration)
  - [In Choreography (Event-Driven)](#in-choreography-event-driven)
  - [In Orchestration (Centralized Control)](#in-orchestration-centralized-control)
  - [Comparison: Choreography vs Orchestration Tracing](#comparison-choreography-vs-orchestration-tracing)
  - [Should API Gateway Generate Trace ID Instead?](#should-api-gateway-generate-trace-id-instead)
    - [Approach 1: API Gateway Generates (REST only)](#approach-1-api-gateway-generates-rest-only)
    - [Approach 2: Service Generates (Event-driven)](#approach-2-service-generates-event-driven)
    - [Approach 3: Hybrid (BEST for Most Systems)](#approach-3-hybrid-best-for-most-systems)
  - [DCP Hybrid Approach: Complete Implementation](#dcp-hybrid-approach-complete-implementation)
    - [DCP Architecture with Tracing](#dcp-architecture-with-tracing)
    - [DCP Implementation: Hybrid Tracing Code](#dcp-implementation-hybrid-tracing-code)
    - [DCP Debugging: Following a Trace ID](#dcp-debugging-following-a-trace-id)

### Choreography vs Orchestration in Practice
  - [Choreography vs Orchestration: DCP and Pizza Store Comparison](#choreography-vs-orchestration-dcp-and-pizza-store-comparison)
    - [Pizza Store: Choreography-First (Simple)](#pizza-store-choreography-first-simple)
    - [DCP: Hybrid (Choreography + Orchestration)](#dcp-hybrid-choreography--orchestration)
    - [Comparison Table: When Each Pattern Shines](#comparison-table-when-each-pattern-shines)

### Messaging Patterns
5. [Are events used only in choreography?](#5-are-events-used-only-in-choreography)
6. [What is the difference between a command and an event?](#6-what-is-the-difference-between-a-command-and-an-event)
  - [Basic Difference](#basic-difference)
  - [When to Use Commands vs Events: Pizza Store](#when-to-use-commands-vs-events-pizza-store)
  - [When to Use Commands vs Events: DCP](#when-to-use-commands-vs-events-dcp)
  - [Decision Tree: Command vs Event](#decision-tree-command-vs-event)
  - [Pattern Summary](#pattern-summary)
  - [Interview-Ready Answer](#interview-ready-answer)

### Advanced Patterns
7. [What is a compensating transaction?](#7-what-is-a-compensating-transaction)
8. [What is event sourcing?](#8-what-is-event-sourcing)
9. [What is idempotency?](#9-what-is-idempotency)
10. [How do these patterns work together?](#10-how-do-these-patterns-work-together)

### Implementation and Applications
11. [Microservices design patterns and their DCP applicability](#11-microservices-design-patterns-and-their-dcp-applicability)
12. [Interview-ready answer](#interview-ready-answer-2)

---

## 1. What is the distributed transaction problem in microservices?

In a monolith, one database transaction can update multiple tables:

```text
BEGIN
  Approve document
  Publish document
  Record notification
COMMIT
```

If any operation fails, the database rolls back everything.

In microservices, each service normally owns its own database:

```text
Approval Service      → PostgreSQL
Dissemination Service → S3
Notification Service  → MongoDB
```

One ACID transaction cannot easily cover all these systems.

For example:

```text
Approve document ✅
Publish document ❌
Send notification ❌
```

The document is approved but not published. The system is temporarily inconsistent and needs a recovery strategy.

---

## 2. What is the Saga pattern?

A **Saga** treats one business transaction as a sequence of smaller local transactions.

```text
Approve document
       ↓
Publish document
       ↓
Send notification
```

Each service commits its own local transaction. If a later step fails, the Saga runs compensating transactions for the earlier completed steps.

```text
Approve document ✅
Publish document ❌
       ↓
Revoke approval or return document to PENDING_REVIEW
```

A compensating transaction is a new business operation. It is not a technical database rollback because the original transaction has already committed.

### Can Saga be used alone?

Saga is the overall distributed transaction pattern. We must also decide how its steps will be coordinated:

- **Choreography:** Services coordinate by reacting to events.
- **Orchestration:** A central orchestrator decides the next step.
- **Hybrid:** The main workflow is orchestrated while some downstream processing uses choreography.

Therefore:

> Saga defines the transaction and compensation strategy. Choreography and orchestration define how the Saga steps are coordinated.

---

## 3. What is Saga choreography?

In choreography, there is no central workflow controller. Each service reacts to events and publishes another event after completing its work.

```text
Approval Service
  └─ publishes DocumentApproved
                ↓
Dissemination Service
  └─ publishes DocumentPublished
                ↓
Notification Service
  └─ publishes NotificationSent
```

The services collectively create the workflow.

### Advantages

- Loose coupling between services
- Good scalability
- Easy to add another event consumer
- Suitable for simple, high-volume pipelines

### Disadvantages

- The complete workflow is not visible in one place
- Debugging requires tracing events across services
- Long event chains become difficult to understand
- Cyclic dependencies can develop
- Failure and timeout handling can become scattered

### Good use case

```text
Source document → Extract data → Check quality → Index result
```

---

## 4. What is Saga orchestration?

In orchestration, a central component owns the workflow and tells each service what to do.

```text
Saga Orchestrator
  ├─ Tell Approval Service to approve
  ├─ Tell Dissemination Service to publish
  ├─ Tell Notification Service to notify
  └─ Start compensation if a step fails
```

The orchestrator may be implemented using Camunda, Temporal, a state machine, or a custom workflow service.

### Advantages

- Complete workflow is visible in one place
- Easier monitoring and debugging
- Central handling of retries, timeouts and compensation
- Suitable for complex and human-driven workflows

### Disadvantages

- The orchestrator is coupled to the workflow participants
- It must be highly available
- It can become a bottleneck if designed poorly
- Too much business logic can turn it into a "god service"

### Good use case

```text
L1 review → L2 review → Approval → Publication → Notification
```

---

## 4.5 How to Enable Good Tracing in Choreography and Orchestration?

### The Problem: Distributed Tracing Across Services

When a single user action (e.g., "Approve document") spans multiple services and Kafka topics, how do you trace what happened?

```text
Approval Service approves doc-789
       ↓ (publishes DocumentApproved event)
Kafka topic
       ↓ (Dissemination Service consumes)
Dissemination Service publishes doc-789
       ↓ (publishes DocumentPublished event)
Kafka topic
       ↓ (Notification Service consumes)
Notification Service sends email
```

**Without tracing:** If something fails, which service caused it? How many events were created for this document? What's the exact sequence?

**With tracing:** One unique ID follows the entire flow, connecting all services and messages.

---

### The Solution: Trace ID (Correlation ID)

A **trace ID** (also called correlation ID) is a unique identifier that travels with every message through the entire workflow.

```text
trace_id = "550e8400-e29b-41d4-a716-446655440000"

This trace_id appears in:
  - Approval Service logs: "Approved doc-789 [trace_id]"
  - DocumentApproved event: {"doc_id": "doc-789", "trace_id": "550e..."}
  - Dissemination Service logs: "Publishing doc-789 [trace_id]"
  - DocumentPublished event: {"doc_id": "doc-789", "trace_id": "550e..."}
  - Notification Service logs: "Sending email [trace_id]"
```

---

### Who Generates Trace ID and When?

#### In Choreography (Event-Driven)

**Answer: The initial service generates the trace ID in step 1**

```text
Step 1: User action triggers Approval Service
        ├─ Generate trace_id = UUID()
        ├─ Approve document in database
        ├─ Log: "Approved doc-789 [trace_id]"
        └─ Publish DocumentApproved event with trace_id
        
Step 2: DocumentApproved event reaches Kafka
        ├─ Event contains: {"doc_id": "doc-789", "trace_id": "550e..."}
        └─ Dissemination Service consumes
        
Step 3: Dissemination Service processes
        ├─ Log: "Received approval for doc-789 [trace_id]"
        ├─ Publish document
        ├─ Log: "Published doc-789 [trace_id]"
        └─ Publish DocumentPublished event with SAME trace_id
        
Step 4: DocumentPublished event reaches Kafka
        ├─ Event contains: {"doc_id": "doc-789", "trace_id": "550e..."}
        └─ Notification Service consumes
        
Step 5: Notification Service processes
        ├─ Log: "Sending email for doc-789 [trace_id]"
        ├─ Send email
        └─ Log: "Email sent [trace_id]"
```

**Key point:** Trace ID is generated ONCE by the first service and PROPAGATED through all events and services.

---

#### In Orchestration (Centralized Control)

**Answer: The orchestrator generates the trace ID in step 1**

```text
Step 1: User action triggers Orchestrator
        ├─ Generate trace_id = UUID()
        ├─ Create saga instance: {trace_id, doc_id, status: "STARTED"}
        ├─ Log: "Starting saga for doc-789 [trace_id]"
        └─ Send command: {trace_id, "Approve doc-789"}
        
Step 2: Approval Service receives command
        ├─ Command contains: {trace_id, "Approve doc-789"}
        ├─ Log: "Received approval command [trace_id]"
        ├─ Approve document
        ├─ Log: "Approved doc-789 [trace_id]"
        └─ Return result with trace_id
        
Step 3: Orchestrator receives approval result
        ├─ Result contains: {trace_id, status: "approved"}
        ├─ Update saga: status = "APPROVED"
        ├─ Log: "Approval completed [trace_id]"
        └─ Send next command: {trace_id, "Publish doc-789"}
        
Step 4: Dissemination Service receives command
        ├─ Command contains: {trace_id, "Publish doc-789"}
        ├─ Log: "Received publish command [trace_id]"
        ├─ Publish document
        ├─ Log: "Published doc-789 [trace_id]"
        └─ Return result with trace_id
        
Step 5: Orchestrator receives publish result
        ├─ Result contains: {trace_id, status: "published"}
        ├─ Update saga: status = "PUBLISHED"
        ├─ Send final command: {trace_id, "Send notification"}
        └─ ...continues...
```

**Key point:** Orchestrator generates trace ID ONCE and includes it in EVERY command sent to services.

---

### Comparison: Choreography vs Orchestration Tracing

| Aspect | Choreography | Orchestration |
|--------|---|---|
| **Who generates trace ID** | Initial service (Approval) | Orchestrator |
| **When** | When user action triggers service | When orchestrator starts saga |
| **How it propagates** | Through event payload | Through command payload |
| **Services know about each other** | Implicitly (via events) | Explicitly (orchestrator coordinates) |
| **How to debug** | Search logs by trace_id across all services | Search logs by trace_id + check orchestrator state machine |
| **If step fails** | Need to trace back through events | Orchestrator shows exact failed step |

---

### Implementation: Adding Trace ID to Events (Choreography)

```python
# Approval Service (generates trace ID)
class ApprovalService:
    def approve_document(self, doc_id):
        trace_id = str(uuid.uuid4())  # Generate once
        
        logger.info(f"Approving {doc_id}", extra={"trace_id": trace_id})
        
        # Approve in database
        db.update("documents", doc_id, status="APPROVED")
        
        # Publish event WITH trace_id
        event = {
            "type": "DocumentApproved",
            "doc_id": doc_id,
            "trace_id": trace_id,  # Include in event
            "timestamp": now()
        }
        producer.send("document-events", value=event, key=doc_id)
        
        logger.info(f"Published DocumentApproved", extra={"trace_id": trace_id})

# Dissemination Service (receives and continues trace ID)
class DisseminationService:
    def on_document_approved(self, event):
        doc_id = event["doc_id"]
        trace_id = event["trace_id"]  # Extract from event
        
        logger.info(f"Received approval for {doc_id}", extra={"trace_id": trace_id})
        
        # Publish document
        s3.put_object(f"documents/{doc_id}.pdf", content)
        
        # Publish event with SAME trace_id
        next_event = {
            "type": "DocumentPublished",
            "doc_id": doc_id,
            "trace_id": trace_id,  # Same trace ID, continues the chain
            "timestamp": now()
        }
        producer.send("document-events", value=next_event, key=doc_id)
        
        logger.info(f"Published DocumentPublished", extra={"trace_id": trace_id})
```

**Query all logs for a document workflow:**
```bash
# Search across all services for this trace
logs.filter(trace_id="550e8400-e29b-41d4-a716-446655440000")

Results:
  [ApprovalService] Approving doc-789 [550e...]
  [ApprovalService] Published DocumentApproved [550e...]
  [DisseminationService] Received approval for doc-789 [550e...]
  [DisseminationService] Published DocumentPublished [550e...]
  [NotificationService] Sending email for doc-789 [550e...]
  [NotificationService] Email sent [550e...]
```

---

### Implementation: Adding Trace ID to Commands (Orchestration)

```python
# Orchestrator (generates trace ID)
class DocumentApprovalOrchestrator:
    def start_approval_workflow(self, doc_id):
        trace_id = str(uuid.uuid4())  # Generate once
        
        logger.info(f"Starting approval workflow for {doc_id}", 
                   extra={"trace_id": trace_id})
        
        # Create saga instance
        saga = {
            "saga_id": str(uuid.uuid4()),
            "trace_id": trace_id,
            "doc_id": doc_id,
            "status": "STARTED",
            "steps": []
        }
        db.insert("sagas", saga)
        
        # Step 1: Send approval command with trace_id
        command = {
            "type": "ApproveDocumentCommand",
            "doc_id": doc_id,
            "trace_id": trace_id,  # Include in command
            "saga_id": saga["saga_id"]
        }
        command_bus.send(command, routing_key="approval-service")
        
        logger.info(f"Sent ApproveDocumentCommand", 
                   extra={"trace_id": trace_id})

# Approval Service (receives command with trace ID)
class ApprovalService:
    def handle_approve_command(self, command):
        doc_id = command["doc_id"]
        trace_id = command["trace_id"]  # Extract from command
        saga_id = command["saga_id"]
        
        logger.info(f"Received approval command for {doc_id}", 
                   extra={"trace_id": trace_id})
        
        try:
            # Approve document
            db.update("documents", doc_id, status="APPROVED")
            
            logger.info(f"Approved {doc_id}", extra={"trace_id": trace_id})
            
            # Send result back to orchestrator with trace_id
            result = {
                "type": "DocumentApprovedResult",
                "doc_id": doc_id,
                "trace_id": trace_id,  # Same trace ID
                "saga_id": saga_id,
                "status": "success"
            }
            result_channel.send(result)
            
        except Exception as e:
            logger.error(f"Failed to approve {doc_id}: {e}", 
                        extra={"trace_id": trace_id})
            
            result = {
                "type": "DocumentApprovedResult",
                "doc_id": doc_id,
                "trace_id": trace_id,  # Same trace ID even on error
                "saga_id": saga_id,
                "status": "failure",
                "error": str(e)
            }
            result_channel.send(result)

# Orchestrator (receives result with trace ID)
class DocumentApprovalOrchestrator:
    def handle_approval_result(self, result):
        trace_id = result["trace_id"]  # Extract from result
        saga_id = result["saga_id"]
        
        logger.info(f"Approval completed with status: {result['status']}", 
                   extra={"trace_id": trace_id})
        
        if result["status"] == "success":
            # Step 2: Send next command with same trace_id
            command = {
                "type": "PublishDocumentCommand",
                "doc_id": result["doc_id"],
                "trace_id": trace_id,  # Continue same trace ID
                "saga_id": saga_id
            }
            command_bus.send(command, routing_key="dissemination-service")
            logger.info(f"Sent PublishDocumentCommand", 
                       extra={"trace_id": trace_id})
        else:
            # Handle failure and compensation
            logger.error(f"Approval failed, starting compensation", 
                        extra={"trace_id": trace_id})
            # ... compensation logic with same trace_id ...
```

**Query orchestrator logs for saga workflow:**
```bash
# Search for this trace
logs.filter(trace_id="550e8400-e29b-41d4-a716-446655440000")

Results:
  [Orchestrator] Starting approval workflow for doc-789 [550e...]
  [Orchestrator] Sent ApproveDocumentCommand [550e...]
  [ApprovalService] Received approval command for doc-789 [550e...]
  [ApprovalService] Approved doc-789 [550e...]
  [Orchestrator] Approval completed with status: success [550e...]
  [Orchestrator] Sent PublishDocumentCommand [550e...]
  [DisseminationService] Received publish command for doc-789 [550e...]
  [DisseminationService] Published doc-789 [550e...]
  [Orchestrator] Publish completed with status: success [550e...]
  [Orchestrator] Sent NotificationCommand [550e...]
  [NotificationService] Sending email for doc-789 [550e...]
  [Orchestrator] Notification completed with status: success [550e...]
```

---

### Best Practices for Tracing

**1. Generate trace ID early (first service or orchestrator)**
```python
# Good
trace_id = str(uuid.uuid4())
# Bad: Each service generates its own trace_id (breaks tracing)
```

**2. Include trace ID in every log**
```python
logger.info("Processing document", extra={"trace_id": trace_id})
```

**3. Pass trace ID in every message/event/command**
```python
event = {"doc_id": doc_id, "trace_id": trace_id}
command = {"doc_id": doc_id, "trace_id": trace_id}
```

**4. Never regenerate trace ID**
```python
# Good: Extract from event/command
trace_id = event["trace_id"]

# Bad: Generate new one
trace_id = str(uuid.uuid4())  # Wrong!
```

**5. Use consistent naming**
```python
# All services use same field name
event["trace_id"]
command["trace_id"]
logs["trace_id"]
```

**6. Log failed steps with trace ID**
```python
logger.error(f"Failed to publish: {error}", 
            extra={"trace_id": trace_id, "step": "publish"})
```

---

### Should API Gateway Generate Trace ID Instead?

**Short answer:** It depends on your architecture. API Gateway is better for REST/HTTP APIs, but insufficient for event-driven systems.

---

#### Approach 1: API Gateway Generates Trace ID (REST APIs)

**How it works:**

```text
Client
    ↓ (HTTP request)
API Gateway
    ├─ Generate trace_id = UUID() (if not provided)
    ├─ Add to request header: X-Trace-ID: 550e...
    └─ Route to backend service
    
Approval Service
    ├─ Extract trace_id from header
    ├─ Process request
    ├─ Include trace_id in logs
    ├─ Include trace_id in events published
    └─ Return response with trace_id header
```

**Implementation:**

```python
# API Gateway
from flask import Flask, request, Response
import uuid

app = Flask(__name__)

@app.before_request
def add_trace_id():
    # If client provided trace_id, use it (useful for debugging)
    trace_id = request.headers.get("X-Trace-ID")
    
    if not trace_id:
        # Generate new one if not provided
        trace_id = str(uuid.uuid4())
    
    # Store in Flask g object (request-local storage)
    g.trace_id = trace_id
    
    # Inject into forwarded request
    request.headers = dict(request.headers)
    request.headers["X-Trace-ID"] = trace_id

@app.route("/approve", methods=["POST"])
def proxy_approve():
    # Forward to backend
    response = requests.post(
        "http://approval-service/approve",
        json=request.json,
        headers={"X-Trace-ID": g.trace_id}  # Pass trace_id
    )
    
    # Include in response
    response.headers["X-Trace-ID"] = g.trace_id
    return response
```

**Backend service (Approval Service):**

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/approve", methods=["POST"])
def approve():
    trace_id = request.headers.get("X-Trace-ID")  # Extract from header
    doc_id = request.json["doc_id"]
    
    logger.info(f"Approving {doc_id}", extra={"trace_id": trace_id})
    
    # Approve document
    db.update("documents", doc_id, status="APPROVED")
    
    # Publish event with trace_id
    event = {
        "type": "DocumentApproved",
        "doc_id": doc_id,
        "trace_id": trace_id  # Continue trace
    }
    producer.send("document-events", value=event)
    
    logger.info(f"Published DocumentApproved", extra={"trace_id": trace_id})
    
    return {"status": "approved", "trace_id": trace_id}
```

**Advantages:**
- Single point of entry (API Gateway)
- Centralized trace ID management
- Client can provide their own trace ID for debugging
- Clean HTTP header propagation
- No need for services to know about trace ID generation

**Disadvantages:**
- Only works for REST/HTTP APIs
- Doesn't cover async event flows (Kafka events not initiated by HTTP)
- Doesn't help with internal service-to-service communication
- Doesn't trace webhooks, scheduled tasks, or other entry points

---

#### Approach 2: Each Service/Event Generates Its Own Trace ID (Event-Driven)

**How it works:**

```text
Kafka Event
    ↓
Approval Service consumes event
    ├─ No API Gateway involved
    ├─ Generate trace_id (if event doesn't have one)
    └─ Include trace_id in logs and published events
```

**Advantages:**
- Works for all event types (Kafka, internal, webhooks, etc.)
- Each entry point has its own trace ID
- No dependency on API Gateway
- Better for microservices without HTTP entry points

**Disadvantages:**
- Distributed trace ID generation (hard to coordinate)
- Multiple entry points mean multiple trace IDs for same business transaction
- Harder to trace across REST APIs and events

---

#### Approach 3: Hybrid (BEST for Most Systems)

**API Gateway generates for HTTP, Service continues through events**

```text
┌─ REST API Entry ─────────────────────────────┐
│ Client → API Gateway                          │
│          ├─ Generate trace_id = 550e...      │
│          └─ Forward to service                │
│                                               │
│ Service receives with trace_id in header      │
│ ├─ Extract from header                       │
│ ├─ Process request                           │
│ ├─ Publish event with trace_id               │
│ └─ Return response                           │
└───────────────────────────────────────────────┘

┌─ Event-Driven Entry ──────────────────────────┐
│ Kafka Event (no API Gateway)                  │
│ ├─ If event has trace_id: extract & continue │
│ ├─ If no trace_id: generate new one          │
│ ├─ Process event                             │
│ └─ Publish next event with same trace_id     │
└───────────────────────────────────────────────┘

┌─ Scheduled Task Entry ────────────────────────┐
│ Cron Job (no API Gateway)                     │
│ ├─ Generate trace_id = UUID()                │
│ ├─ Trigger service with trace_id             │
│ └─ Process task                              │
└───────────────────────────────────────────────┘
```

**Implementation:**

```python
# API Gateway (handles REST entry)
from flask import Flask, request
import uuid

app = Flask(__name__)

@app.before_request
def add_trace_id():
    # Client might provide trace_id for debugging
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
    g.trace_id = trace_id

@app.route("/api/approve", methods=["POST"])
def api_approve():
    response = requests.post(
        "http://approval-service/approve",
        json=request.json,
        headers={"X-Trace-ID": g.trace_id}
    )
    return response

# Backend Service (handles both HTTP and events)
from flask import Flask, request

app = Flask(__name__)
kafka_consumer = KafkaConsumer("document-events")

# HTTP endpoint
@app.route("/approve", methods=["POST"])
def approve_http():
    trace_id = request.headers.get("X-Trace-ID")  # From API Gateway
    doc_id = request.json["doc_id"]
    
    # Process with trace_id
    approve_internal(doc_id, trace_id)
    return {"status": "approved"}

# Kafka consumer (event entry point)
def handle_kafka_events():
    for message in kafka_consumer:
        event = json.loads(message.value)
        doc_id = event["doc_id"]
        
        # Extract trace_id if provided
        trace_id = event.get("trace_id") or str(uuid.uuid4())
        
        # Same processing logic
        approve_internal(doc_id, trace_id)

# Shared logic
def approve_internal(doc_id, trace_id):
    logger.info(f"Approving {doc_id}", extra={"trace_id": trace_id})
    
    db.update("documents", doc_id, status="APPROVED")
    
    event = {
        "type": "DocumentApproved",
        "doc_id": doc_id,
        "trace_id": trace_id  # Continue trace
    }
    producer.send("document-events", value=event)
    
    logger.info(f"Approved {doc_id}", extra={"trace_id": trace_id})
```

**Scheduled Task with Trace ID:**

```python
# Scheduled job (entry point with no API Gateway or Kafka)
import schedule
import uuid
from datetime import datetime

def daily_document_expiry_check():
    trace_id = str(uuid.uuid4())  # Generate for this task
    
    logger.info(f"Starting daily expiry check", extra={"trace_id": trace_id})
    
    # Find expired documents
    expired = db.query("SELECT * FROM documents WHERE expires_at < NOW()")
    
    for doc in expired:
        # Process each with same trace_id
        logger.info(f"Expiring {doc['id']}", extra={"trace_id": trace_id})
        
        # Publish event with trace_id
        event = {
            "type": "DocumentExpired",
            "doc_id": doc["id"],
            "trace_id": trace_id
        }
        producer.send("document-events", value=event)
    
    logger.info(f"Daily expiry check completed", extra={"trace_id": trace_id})

# Schedule it
schedule.every().day.at("03:00").do(daily_document_expiry_check)
```

---

#### Comparison: All Three Approaches

| Aspect | API Gateway Only | Service Only | Hybrid |
|--------|---|---|---|
| **REST API** | ✅ Works | ⚠️ Service generates | ✅ Gateway generates |
| **Kafka Events** | ❌ No trace | ✅ Works | ✅ Works |
| **Webhooks** | ❌ No trace | ✅ Service generates | ✅ Service generates |
| **Scheduled Tasks** | ❌ No trace | ✅ Service generates | ✅ Service generates |
| **Service-to-Service** | ⚠️ Only if via API Gateway | ✅ Direct events work | ✅ Works |
| **Complexity** | Low | Medium | Medium |
| **Centralization** | High (Gateway) | Low (Distributed) | Medium |
| **Debugging** | Easy for REST | Mixed | Easy for all |

---

#### Decision: Which Approach to Use?

**Use API Gateway only if:**
- Most traffic is REST APIs
- No event-driven workflows
- Simple synchronous system
- API Gateway is your only entry point

**Use Service generation if:**
- Mostly event-driven (Kafka, async)
- Multiple entry points (webhooks, scheduled tasks)
- No API Gateway in architecture
- Services are autonomous

**Use Hybrid (RECOMMENDED) if:**
- Mix of REST APIs and events
- Multiple entry points
- Complex distributed systems
- Want centralized tracing for REST + local for events

---

#### Real Example: DCP with Hybrid Tracing

```text
External Client
    ↓ (REST API)
API Gateway (generates trace_id)
    ├─ Send to Sourcing Service with X-Trace-ID header
    
Sourcing Service receives
    ├─ Extract trace_id from header
    ├─ Store document
    ├─ Publish DocumentSourced event with trace_id
    
Kafka: DocumentSourced event (has trace_id)
    ↓
Extraction Service consumes
    ├─ Extract trace_id from event
    ├─ Extract document fields
    ├─ Publish DocumentExtracted event with trace_id
    
Kafka: DocumentExtracted event (has trace_id)
    ↓
Quality Service consumes
    ├─ Extract trace_id from event
    ├─ Validate extracted data
    ├─ Publish QualityChecked event with trace_id
    
Scheduled Cleanup Task (entry point, no API Gateway)
    ├─ Generate NEW trace_id (different transaction)
    ├─ Clean old documents
    ├─ Publish DocumentCleaned event with NEW trace_id

Result: Two trace IDs in system
  trace_id_1: Original API request → all resulting events
  trace_id_2: Scheduled cleanup task → its events
```

**Why this is optimal:**
- API Gateway handles REST entry (centralized)
- Services continue trace through events
- Scheduled tasks get their own trace (different business transaction)
- Each "user action" has one trace ID
- Each "automated task" has its own trace ID

---

### DCP Hybrid Approach: Complete Implementation

The DCP is a perfect example of a hybrid system that needs sophisticated tracing:

```text
Multiple entry points:
  1. REST API (Sourcing Service)
  2. Kafka webhooks (resubmitted documents)
  3. Scheduled retry task (failed documents)
  4. Manual re-approval workflow
```

#### DCP Architecture with Tracing

```text
┌─────────────────────────────────────────────────────────────────┐
│ ENTRY POINT 1: REST API (External Source)                      │
│                                                                 │
│ External Client                                                 │
│   POST /api/upload {document: pdf}                             │
│         ↓                                                       │
│   API Gateway                                                  │
│   ├─ Generate trace_id = "550e8400-e29b-41d4-a716..."        │
│   ├─ Log: "Received document upload" [trace_id]               │
│   └─ Forward to Sourcing Service with X-Trace-ID header       │
│         ↓                                                       │
│   Sourcing Service                                             │
│   ├─ Extract trace_id from header                             │
│   ├─ Validate, scan, deduplicate document                     │
│   ├─ Publish DocumentSourced event with trace_id              │
│   └─ Log: "Document sourced" [trace_id]                       │
└─────────────────────────────────────────────────────────────────┘
         ↓ (Kafka event with trace_id)
┌─────────────────────────────────────────────────────────────────┐
│ EXTRACTION SERVICE                                              │
│                                                                 │
│ Kafka: DocumentSourced [550e...]                               │
│     ↓                                                           │
│ Extraction Service consumes                                    │
│ ├─ Extract trace_id from event                                │
│ ├─ Call ML providers (SparkAir, Cognaize)                     │
│ ├─ Store extracted data in MongoDB                            │
│ ├─ Publish DocumentExtracted event with SAME trace_id         │
│ └─ Log: "Document extracted" [trace_id]                       │
└─────────────────────────────────────────────────────────────────┘
         ↓ (Kafka event with trace_id)
┌─────────────────────────────────────────────────────────────────┐
│ QUALITY SERVICE                                                 │
│                                                                 │
│ Kafka: DocumentExtracted [550e...]                             │
│     ↓                                                           │
│ Quality Service consumes                                       │
│ ├─ Extract trace_id from event                                │
│ ├─ Validate fields, confidence scores                         │
│ ├─ Check business rules                                       │
│ ├─ Publish QualityChecked event with SAME trace_id            │
│ └─ Log: "Quality validation passed" [trace_id]                │
└─────────────────────────────────────────────────────────────────┘
         ↓ (Kafka event with trace_id)
┌─────────────────────────────────────────────────────────────────┐
│ APPROVAL SERVICE (L1/L2 Review)                                │
│                                                                 │
│ Kafka: QualityChecked [550e...]                               │
│     ↓                                                           │
│ Approval Service consumes                                      │
│ ├─ Extract trace_id from event                                │
│ ├─ Create task for L1 review                                  │
│ ├─ Wait for human approval                                    │
│ ├─ Publish DocumentApproved event with SAME trace_id          │
│ └─ Log: "Document approved by L2" [trace_id]                  │
└─────────────────────────────────────────────────────────────────┘
         ↓ (Kafka event with trace_id)
┌─────────────────────────────────────────────────────────────────┐
│ DISSEMINATION SERVICE                                          │
│                                                                 │
│ Kafka: DocumentApproved [550e...]                              │
│     ↓                                                           │
│ Dissemination Service consumes                                 │
│ ├─ Extract trace_id from event                                │
│ ├─ Publish to external APIs, S3, Email                        │
│ ├─ Publish DocumentPublished event with SAME trace_id         │
│ └─ Log: "Document disseminated" [trace_id]                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ENTRY POINT 2: Kafka Webhook (Resubmitted Document)            │
│                                                                 │
│ External System (SQS/SNS/Webhook)                              │
│   Sends: "Document resubmitted"                                │
│         ↓                                                       │
│ DCP Webhook Handler                                            │
│ ├─ Event has NO trace_id (external system)                    │
│ ├─ Generate NEW trace_id = UUID()                             │
│ ├─ Publish DocumentResubmitted event with NEW trace_id         │
│ └─ Log: "Resubmitted document" [NEW trace_id]                 │
└─────────────────────────────────────────────────────────────────┘
         ↓ (Continues with NEW trace_id)
         Extraction Service consumes with NEW trace_id...

┌─────────────────────────────────────────────────────────────────┐
│ ENTRY POINT 3: Scheduled Retry Task                            │
│                                                                 │
│ Scheduler (3 AM daily)                                         │
│ ├─ Find failed documents                                       │
│ ├─ Generate NEW trace_id for this batch = UUID()              │
│ ├─ Log: "Starting daily retry job" [NEW trace_id]             │
│ ├─ For each failed doc:                                        │
│ │  ├─ Publish DocumentRetry event with SAME trace_id          │
│ │  └─ Log: "Retrying doc-789" [trace_id]                      │
│ └─ Different trace_id than REST API uploads!                  │
└─────────────────────────────────────────────────────────────────┘
         ↓ (Continues with RETRY trace_id)
         Extraction Service consumes with RETRY trace_id...
```

---

#### DCP Implementation: Hybrid Tracing Code

**1. API Gateway (REST Entry Point)**

```python
# api_gateway.py - Handles REST API uploads

from flask import Flask, request, g
import uuid
import logging
import requests

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.before_request
def add_trace_id():
    """Add trace_id to every incoming request"""
    
    # Client might provide trace_id for debugging/tracking
    trace_id = request.headers.get("X-Trace-ID")
    
    if not trace_id:
        # Generate new trace_id for this user action
        trace_id = str(uuid.uuid4())
    
    # Store in Flask g object (request-local)
    g.trace_id = trace_id
    g.source = "REST_API"
    
    # Log at gateway level
    logger.info(
        f"Received request: {request.method} {request.path}",
        extra={
            "trace_id": trace_id,
            "source": "API_GATEWAY",
            "client_ip": request.remote_addr
        }
    )

@app.route("/api/documents/upload", methods=["POST"])
def upload_document():
    """REST endpoint for document upload"""
    
    trace_id = g.trace_id
    
    # Forward to Sourcing Service with trace_id header
    response = requests.post(
        "http://sourcing-service:8001/upload",
        json=request.json,
        headers={
            "X-Trace-ID": trace_id,  # Pass trace_id to backend
            "X-Source": "API_GATEWAY"
        }
    )
    
    # Return response with trace_id header
    response.headers["X-Trace-ID"] = trace_id
    
    logger.info(
        f"Forwarded to Sourcing Service",
        extra={"trace_id": trace_id}
    )
    
    return response

if __name__ == "__main__":
    app.run(port=8000)
```

**2. Sourcing Service (First Microservice)**

```python
# sourcing_service.py - Entry point for REST API

from flask import Flask, request
import json
import logging
from kafka import KafkaProducer

app = Flask(__name__)
logger = logging.getLogger(__name__)
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    enable_idempotence=True,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route("/upload", methods=["POST"])
def upload():
    """Handle document upload from API Gateway"""
    
    # Extract trace_id from API Gateway
    trace_id = request.headers.get("X-Trace-ID")
    
    doc_data = request.json
    doc_id = doc_data.get("doc_id")
    
    logger.info(
        f"Received document upload: {doc_id}",
        extra={
            "trace_id": trace_id,
            "service": "SOURCING"
        }
    )
    
    try:
        # Validate document
        validate_document(doc_data)
        
        # Store in database (with trace_id for audit)
        db.insert("sourced_documents", {
            "doc_id": doc_id,
            "content": doc_data["content"],
            "trace_id": trace_id,  # Store for audit trail
            "status": "SOURCED"
        })
        
        # Publish event with trace_id
        event = {
            "type": "DocumentSourced",
            "doc_id": doc_id,
            "trace_id": trace_id,  # Continue trace
            "content": doc_data["content"],
            "timestamp": datetime.now().isoformat()
        }
        
        producer.send("document-sourced", value=event, key=doc_id)
        
        logger.info(
            f"Published DocumentSourced event",
            extra={
                "trace_id": trace_id,
                "doc_id": doc_id,
                "service": "SOURCING"
            }
        )
        
        return {
            "status": "success",
            "doc_id": doc_id,
            "trace_id": trace_id
        }
        
    except Exception as e:
        logger.error(
            f"Failed to source document: {e}",
            extra={
                "trace_id": trace_id,
                "doc_id": doc_id,
                "service": "SOURCING",
                "error": str(e)
            }
        )
        return {"status": "error", "error": str(e)}, 500

if __name__ == "__main__":
    app.run(port=8001)
```

**3. Extraction Service (Kafka Consumer)**

```python
# extraction_service.py - Consumes DocumentSourced event

import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime

logger = logging.getLogger(__name__)
consumer = KafkaConsumer(
    "document-sourced",
    bootstrap_servers=['kafka:9092'],
    group_id="extraction-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    enable_idempotence=True,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def handle_kafka_events():
    """Consume DocumentSourced events"""
    
    for message in consumer:
        event = message.value
        doc_id = event["doc_id"]
        
        # Extract trace_id from event (CRITICAL)
        trace_id = event.get("trace_id")
        
        if not trace_id:
            # Fallback: generate new if not provided (shouldn't happen)
            import uuid
            trace_id = str(uuid.uuid4())
            logger.warning(
                f"No trace_id in event, generated new one",
                extra={"doc_id": doc_id, "trace_id": trace_id}
            )
        
        logger.info(
            f"Received DocumentSourced event",
            extra={
                "trace_id": trace_id,
                "doc_id": doc_id,
                "service": "EXTRACTION",
                "offset": message.offset
            }
        )
        
        try:
            # Extract fields using ML (with trace_id in logs)
            extracted = extract_with_ml(event["content"], trace_id)
            
            # Save to database (with trace_id for audit)
            db.insert("extracted_documents", {
                "doc_id": doc_id,
                "extracted_data": extracted,
                "trace_id": trace_id,  # Store for audit
                "status": "EXTRACTED"
            })
            
            logger.info(
                f"Successfully extracted fields",
                extra={
                    "trace_id": trace_id,
                    "doc_id": doc_id,
                    "service": "EXTRACTION"
                }
            )
            
            # Publish next event with SAME trace_id
            next_event = {
                "type": "DocumentExtracted",
                "doc_id": doc_id,
                "trace_id": trace_id,  # SAME trace_id
                "extracted_data": extracted,
                "timestamp": datetime.now().isoformat()
            }
            
            producer.send("document-extracted", value=next_event, key=doc_id)
            
            logger.info(
                f"Published DocumentExtracted event",
                extra={
                    "trace_id": trace_id,
                    "doc_id": doc_id,
                    "service": "EXTRACTION"
                }
            )
            
            # ACK to Kafka
            consumer.commit()
            
        except Exception as e:
            logger.error(
                f"Failed to extract document: {e}",
                extra={
                    "trace_id": trace_id,
                    "doc_id": doc_id,
                    "service": "EXTRACTION",
                    "error": str(e),
                    "offset": message.offset
                }
            )
            # Don't commit - will retry
            producer.send("dead-letter-queue", value={
                "type": "ExtractionFailed",
                "doc_id": doc_id,
                "trace_id": trace_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })

def extract_with_ml(content, trace_id):
    """Extract fields from document"""
    # ML extraction with trace_id in logs
    logger.info(
        f"Calling SparkAir ML service",
        extra={"trace_id": trace_id}
    )
    # ... extraction logic ...
    return extracted_data

if __name__ == "__main__":
    handle_kafka_events()
```

**4. Quality Service (Kafka Consumer)**

```python
# quality_service.py - Consumes DocumentExtracted event

import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime

logger = logging.getLogger(__name__)
consumer = KafkaConsumer(
    "document-extracted",
    bootstrap_servers=['kafka:9092'],
    group_id="quality-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    enable_idempotence=True,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def handle_kafka_events():
    """Consume DocumentExtracted events"""
    
    for message in consumer:
        event = message.value
        doc_id = event["doc_id"]
        trace_id = event.get("trace_id")  # Extract trace_id
        
        logger.info(
            f"Received DocumentExtracted event",
            extra={
                "trace_id": trace_id,
                "doc_id": doc_id,
                "service": "QUALITY"
            }
        )
        
        try:
            # Validate extracted data
            is_valid = validate_extraction(
                event["extracted_data"],
                trace_id
            )
            
            if is_valid:
                logger.info(
                    f"Quality validation passed",
                    extra={
                        "trace_id": trace_id,
                        "doc_id": doc_id,
                        "service": "QUALITY"
                    }
                )
                
                # Publish next event with SAME trace_id
                next_event = {
                    "type": "QualityChecked",
                    "doc_id": doc_id,
                    "trace_id": trace_id,  # SAME trace_id
                    "validated_data": event["extracted_data"],
                    "confidence": 0.95,
                    "timestamp": datetime.now().isoformat()
                }
                
                producer.send("quality-checked", value=next_event, key=doc_id)
            else:
                logger.warning(
                    f"Quality validation failed",
                    extra={
                        "trace_id": trace_id,
                        "doc_id": doc_id,
                        "service": "QUALITY"
                    }
                )
                
                # Publish rejection with SAME trace_id
                reject_event = {
                    "type": "QualityCheckFailed",
                    "doc_id": doc_id,
                    "trace_id": trace_id,  # SAME trace_id
                    "reason": "Validation failed",
                    "timestamp": datetime.now().isoformat()
                }
                
                producer.send("quality-failed", value=reject_event, key=doc_id)
            
            consumer.commit()
            
        except Exception as e:
            logger.error(
                f"Quality check error: {e}",
                extra={
                    "trace_id": trace_id,
                    "doc_id": doc_id,
                    "service": "QUALITY",
                    "error": str(e)
                }
            )

def validate_extraction(data, trace_id):
    """Validate extracted data"""
    logger.info(
        f"Validating extracted fields",
        extra={"trace_id": trace_id}
    )
    # ... validation logic ...
    return True

if __name__ == "__main__":
    handle_kafka_events()
```

**5. Scheduled Retry Task (Different Entry Point)**

```python
# scheduled_retry_task.py - Batch retry job

import schedule
import uuid
import json
import logging
from kafka import KafkaProducer
from datetime import datetime

logger = logging.getLogger(__name__)
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    enable_idempotence=True,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def daily_retry_failed_documents():
    """Scheduled job to retry failed documents"""
    
    # Generate NEW trace_id for this batch job
    # Different from REST API uploads!
    batch_trace_id = str(uuid.uuid4())
    
    logger.info(
        f"Starting daily retry job",
        extra={
            "trace_id": batch_trace_id,
            "service": "SCHEDULER",
            "job_type": "DAILY_RETRY"
        }
    )
    
    try:
        # Find failed documents
        failed_docs = db.query("""
            SELECT doc_id, extraction_error 
            FROM extracted_documents 
            WHERE status = 'FAILED' 
            AND last_retry < NOW() - INTERVAL '1 hour'
            LIMIT 100
        """)
        
        logger.info(
            f"Found {len(failed_docs)} documents to retry",
            extra={
                "trace_id": batch_trace_id,
                "count": len(failed_docs)
            }
        )
        
        for doc_record in failed_docs:
            doc_id = doc_record["doc_id"]
            
            logger.info(
                f"Retrying failed document",
                extra={
                    "trace_id": batch_trace_id,
                    "doc_id": doc_id,
                    "service": "SCHEDULER"
                }
            )
            
            # Publish retry event with BATCH trace_id
            retry_event = {
                "type": "DocumentRetry",
                "doc_id": doc_id,
                "trace_id": batch_trace_id,  # SAME batch trace
                "previous_error": doc_record["extraction_error"],
                "retry_attempt": 2,
                "timestamp": datetime.now().isoformat()
            }
            
            producer.send("document-retry", value=retry_event, key=doc_id)
            
            # Update database
            db.update("extracted_documents", doc_id, {
                "last_retry": datetime.now(),
                "retry_count": db.get(doc_id, "retry_count") + 1
            })
        
        logger.info(
            f"Daily retry job completed",
            extra={
                "trace_id": batch_trace_id,
                "documents_queued": len(failed_docs)
            }
        )
        
    except Exception as e:
        logger.error(
            f"Daily retry job failed: {e}",
            extra={
                "trace_id": batch_trace_id,
                "service": "SCHEDULER",
                "error": str(e)
            }
        )

# Schedule the job
schedule.every().day.at("03:00").do(daily_retry_failed_documents)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)
```

---

#### DCP Debugging: Following a Trace ID

**Scenario: User uploads document, something fails in Quality service**

```bash
# Search all logs for this trace_id across all services
$ logs.filter(trace_id="550e8400-e29b-41d4-a716-446655440000")

Results (in chronological order):

[2024-01-15 10:30:01] API_GATEWAY: Received request: POST /api/documents/upload
  trace_id: 550e8400...
  source: API_GATEWAY
  client_ip: 203.0.113.42

[2024-01-15 10:30:02] API_GATEWAY: Forwarded to Sourcing Service
  trace_id: 550e8400...

[2024-01-15 10:30:03] SOURCING: Received document upload: doc-789
  trace_id: 550e8400...
  service: SOURCING

[2024-01-15 10:30:04] SOURCING: Published DocumentSourced event
  trace_id: 550e8400...
  doc_id: doc-789

[2024-01-15 10:30:15] EXTRACTION: Received DocumentSourced event
  trace_id: 550e8400...
  doc_id: doc-789
  offset: 12345

[2024-01-15 10:30:20] EXTRACTION: Calling SparkAir ML service
  trace_id: 550e8400...

[2024-01-15 10:30:45] EXTRACTION: Successfully extracted fields
  trace_id: 550e8400...
  doc_id: doc-789

[2024-01-15 10:30:46] EXTRACTION: Published DocumentExtracted event
  trace_id: 550e8400...
  doc_id: doc-789

[2024-01-15 10:30:52] QUALITY: Received DocumentExtracted event
  trace_id: 550e8400...
  doc_id: doc-789

[2024-01-15 10:30:53] QUALITY: Validating extracted fields
  trace_id: 550e8400...

[2024-01-15 10:30:54] QUALITY: Quality validation failed ❌
  trace_id: 550e8400...
  doc_id: doc-789
  service: QUALITY
  reason: Confidence score too low (0.62 < 0.75)

[2024-01-15 10:30:55] QUALITY: Published QualityCheckFailed event
  trace_id: 550e8400...
  doc_id: doc-789

Complete flow captured! We can see:
  1. Request came from API Gateway at 10:30:01
  2. Sourcing processed and published at 10:30:04
  3. Extraction consumed at 10:30:15 (11 second lag)
  4. Extraction took 30 seconds (10:30:20 to 10:30:45)
  5. Quality consumed at 10:30:52 (6 second lag)
  6. Quality validation failed due to low confidence

NEXT STEP: Check why confidence is low
  - Was ML model updated?
  - Is document quality bad?
  - Are thresholds correct?
```

---

#### Summary: DCP Hybrid Tracing

| Entry Point | Generates Trace ID | Example Trace |
|---|---|---|
| **REST API Upload** | API Gateway | 550e8400-e29b-41d4-a716-... |
| **Kafka Webhook** | Webhook Handler | 660f9511-f30c-52e5-b827-... |
| **Scheduled Retry** | Scheduler | 770g0622-g41d-63f6-c938-... |
| **Manual Re-approval** | Approval Service | 880h1733-h52e-74g7-d049-... |

**Each entry point = unique trace ID = independent business transaction**

All downstream services continue with same trace ID, creating a complete audit trail.

---

## 5. Are events used only in choreography?

No. Events can be used in both choreography and orchestration.

The real difference is **who decides the next step**.

### Choreography

Events drive the workflow:

```text
DocumentApproved event
       ↓
Dissemination Service reacts
       ↓
DocumentPublished event
       ↓
Notification Service reacts
```

No central component controls the complete sequence.

### Orchestration using synchronous APIs

```text
Orchestrator → POST /approve
Orchestrator → POST /publish
Orchestrator → POST /notify
```

### Orchestration using asynchronous messages

```text
Orchestrator → PublishDocument command
Dissemination Service → DocumentPublished event
Orchestrator receives event → SendNotification command
```

This is still orchestration because the orchestrator receives the result and decides what should happen next.

| Question | Choreography | Orchestration |
|---|---|---|
| Who decides the next step? | Participating services | Central orchestrator |
| Are events used? | Yes, events drive the workflow | Optional; APIs, commands and events can be used |
| Is there a central workflow owner? | No | Yes |
| Best suited for | Simple event pipelines | Complex workflows and human tasks |

---

## 6. What is the difference between a command and an event?

### Basic Difference

A **command** asks a specific receiver to perform an action.

```text
PublishDocument
ReserveInventory
ChargePayment
```

Commands are written in imperative form (do this!). A command can **succeed or fail** — the receiver can reject it.

An **event** announces a fact that has already happened.

```text
DocumentPublished
InventoryReserved
PaymentCharged
```

Events are written in past tense. An event **should not be rejected** because it describes something that already occurred.

```text
Command: PublishDocument
Result:  DocumentPublished or DocumentPublicationFailed

Event: DocumentPublished
(No rejection possible — it already happened)
```

---

### When to Use Commands vs Events: Pizza Store

#### Scenario 1: Customer Places Order

**Using Event (Choreography):**

```python
# Customer places order via API
order = {"order_id": "order-123", "pizza": "Large Margherita"}

# Sourcing Service publishes EVENT (not command)
event = {
    "type": "OrderPlaced",  # Past tense
    "order_id": "order-123",
    "pizza": "Large Margherita",
    "timestamp": now()
}
producer.send("pizza-orders", event)

# Kitchen Service consumes event independently
def on_order_placed(event):
    print(f"Received OrderPlaced: {event['order_id']}")
    prepare_pizza(event)
    
# Delivery Service ALSO consumes same event
def on_order_placed(event):
    print(f"Received OrderPlaced: {event['order_id']}")
    schedule_delivery(event)

# Billing Service ALSO consumes same event
def on_order_placed(event):
    print(f"Received OrderPlaced: {event['order_id']}")
    reserve_payment(event)
```

**Why Event?**
- Multiple services need to react independently
- No central decision maker
- Services don't ask permission, they just react
- Fast and decoupled

---

#### Scenario 2: L1 Manager Reviews and Rejects Order

**Using Command (Orchestration):**

```python
# Manager says "Reject this order"
# Orchestrator sends COMMAND to Order Cancellation Service

command = {
    "type": "CancelOrder",  # Imperative
    "order_id": "order-123",
    "reason": "Wrong phone number",
    "sent_at": now()
}

# Send to specific service (not broadcast to many)
order_service.handle_command(command)

# Service receives command and decides
def handle_cancel_order_command(command):
    order_id = command["order_id"]
    
    try:
        # Attempt to cancel
        order = db.get(order_id)
        
        if order["status"] == "PREPARING":
            # Can cancel
            db.update(order_id, status="CANCELLED")
            # Publish event (result of command)
            producer.send("pizza-events", {
                "type": "OrderCancelled",
                "order_id": order_id,
                "reason": command["reason"]
            })
            return {"status": "success"}
        else:
            # Cannot cancel (already delivered)
            return {
                "status": "failed",
                "reason": "Order already delivered"
            }
    except Exception as e:
        return {"status": "failed", "error": str(e)}
```

**Why Command?**
- Specific service needs to decide
- Manager is asking permission (can fail)
- Only one receiver (Order Service)
- Result matters (success or failure)

---

#### Pizza Store Summary

| Situation | Use Command | Use Event | Why |
|-----------|---|---|---|
| Customer places order | ❌ | ✅ | Multiple services react, no decision |
| Kitchen confirms pizza ready | ❌ | ✅ | Delivery & Billing both react |
| Manager cancels order | ✅ | ❌ | Specific request to Order Service, needs decision |
| Manager re-assigns delivery driver | ✅ | ❌ | Specific request to Delivery Service |
| Payment failed → notify customer | ❌ | ✅ | Notification Service reacts to event |

---

### When to Use Commands vs Events: DCP

**Important:** DCP uses BOTH commands AND events in BOTH choreography AND orchestration zones. The key is WHO DECIDES and WHO SENDS, not which pattern.

---

#### Zone A: Automatic Pipeline (Mostly Events, Rarely Commands)

**Scenario 1: Document Sourced (EVENT - Choreography)**

```python
# Sourcing Service publishes EVENT
event = {
    "type": "DocumentSourced",  # Past tense: it happened
    "doc_id": "doc-789",
    "content": pdf_content,
    "timestamp": now()
}
producer.send("document-sourced", event)

# Multiple services react independently
def on_document_sourced(event):
    # Extraction Service
    extracted = extract_with_ml(event["content"])
    producer.send("document-extracted", {
        "type": "DocumentExtracted",
        "doc_id": event["doc_id"],
        "extracted_data": extracted
    })

def on_document_sourced(event):
    # Audit Service also consumes
    audit.log(f"Document {event['doc_id']} sourced")
    
def on_document_sourced(event):
    # Quality Service also interested
    check_file_format(event["doc_id"])
```

**Why Event?**
- Announcement: "This document was sourced"
- Multiple services react (Extraction, Audit, Quality)
- No permission needed
- Automatic processing

---

**Scenario 1b: Extraction Fails (COMMAND - Error Handling in Choreography)**

```python
# In rare cases, services send commands to handle errors
def on_document_sourced(event):
    try:
        extracted = extract_with_ml(event["content"])
        producer.send("document-extracted", {...})
    except PermanentExtractionError as e:
        # Emergency: send COMMAND to stop processing
        orchestrator.handle_command({
            "type": "QuarantineDocument",  # COMMAND
            "doc_id": event["doc_id"],
            "reason": f"Cannot extract: {e}",
            "alert_level": "critical"
        })
```

**Why Command here?**
- Error handling (not normal flow)
- Needs specific decision from Orchestrator
- Extraction Service needs response (did quarantine succeed?)

---

#### Zone B: Human Workflow (Mostly Commands, Publishes Events)

**Scenario 2: Quality Check Passes → Create L1 Task (COMMAND - Orchestration)**

```python
# Quality Service publishes EVENT
def on_document_extracted(event):
    is_valid = validate(event)
    if is_valid:
        producer.send("document-events", {
            "type": "DocumentQualityChecked",  # EVENT
            "doc_id": event["doc_id"]
        })

# Orchestrator listens to event
def on_document_quality_checked(event):
    # Orchestrator sends COMMAND to Task Service
    command = {
        "type": "CreateL1ReviewTask",  # COMMAND
        "doc_id": event["doc_id"],
        "assigned_to": "l1-team",
        "due_date": tomorrow()
    }
    task_service.handle_command(command)
    
    # Orchestrator REMEMBERS state
    saga = {
        "doc_id": event["doc_id"],
        "status": "AWAITING_L1_REVIEW",
        "l1_assigned_at": now()
    }
    db.insert("sagas", saga)
```

**Why Event → Command?**
- Quality publishes EVENT (fact: passed validation)
- Orchestrator reacts by sending COMMAND (asking Task Service to create task)
- Task Service makes decision (can it create task?)

---

**Scenario 3: L1 Rejects → Rework (COMMAND - Orchestration)**

```python
# L1 human says "Reject and rework"
def on_l1_rejection(decision):
    # Orchestrator sends COMMAND to Extraction Service
    command = {
        "type": "ReworkDocumentExtraction",  # COMMAND
        "doc_id": decision["doc_id"],
        "feedback": decision["feedback"],
        "reason": decision["reason"]
    }
    result = extraction_service.handle_command(command)
    
    if result["status"] == "success":
        # Orchestrator publishes EVENT (result of command)
        producer.send("document-events", {
            "type": "DocumentReworked",  # EVENT
            "doc_id": decision["doc_id"],
            "feedback": decision["feedback"]
        })
        
        # Orchestrator updates saga
        db.update("sagas", decision["doc_id"], 
                 {"status": "REWORK_IN_PROGRESS"})
    else:
        # Handle failure
        producer.send("document-events", {
            "type": "ReworkFailed",  # EVENT
            "doc_id": decision["doc_id"],
            "reason": result["error"]
        })
```

**Why Command → Event?**
- Orchestrator sends COMMAND: "Rework this" (needs decision)
- Extraction Service accepts/rejects
- If accepted, Orchestrator publishes EVENT: "DocumentReworked" (fact)
- Other services can react to DocumentReworked event

---

#### Zone C: Publication (Mostly Events)

**Scenario 4: Document Approved → Disseminate (EVENT - Choreography)**

```python
# Orchestrator publishes EVENT after L2 approval
def on_l2_approval(decision):
    # Publish EVENT (fact: approved)
    producer.send("document-events", {
        "type": "DocumentApproved",  # EVENT
        "doc_id": decision["doc_id"],
        "approved_by": decision["l2_reviewer"]
    })

# Multiple services react
def on_document_approved(event):
    # Dissemination Service consumes independently
    publish_to_s3(event["doc_id"])
    publish_to_customer_api(event["doc_id"])
    producer.send("document-events", {
        "type": "DocumentPublished",  # EVENT
        "doc_id": event["doc_id"]
    })

def on_document_approved(event):
    # Audit Service consumes independently
    audit.log(f"Document {event['doc_id']} approved")
```

**Why Event?**
- Approval is a fact (already happened)
- Multiple services react (Dissemination, Audit)
- No rejections possible

---

#### Complete DCP Flow: Commands AND Events Throughout

```
┌─ AUTOMATIC PIPELINE ────────────────────────────┐
│ DocumentSourced EVENT                           │
│     ↓ (multiple services react)                │
│ Extraction Service extracts                    │
│     ↓                                           │
│ DocumentExtracted EVENT                        │
│     ↓                                           │
│ Quality Service validates                      │
│     ↓                                           │
│ DocumentQualityChecked EVENT                   │
└──────────────────────────────────────────────────┘
         ↓
┌─ ORCHESTRATION ZONE ────────────────────────────┐
│ Orchestrator receives DocumentQualityChecked   │
│ Sends COMMAND: CreateL1ReviewTask              │
│     ↓                                           │
│ Task Service executes (can it create?)         │
│     ↓                                           │
│ L1 reviews (human decision)                    │
│     ↓                                           │
│ L1 response: "Reject"                          │
│     ↓                                           │
│ Orchestrator sends COMMAND: ReworkExtraction   │
│     ↓                                           │
│ Extraction Service executes                    │
│     ↓                                           │
│ Orchestrator publishes DocumentReworked EVENT  │
│     ↓ (back to automatic pipeline)             │
│ Quality Service validates again                │
└──────────────────────────────────────────────────┘
         ↓
┌─ PUBLICATION ZONE ──────────────────────────────┐
│ DocumentApproved EVENT                         │
│     ↓ (multiple services react)                │
│ Dissemination Service publishes                │
│ Audit Service records                          │
│     ↓                                           │
│ DocumentPublished EVENT                        │
└──────────────────────────────────────────────────┘
```

---

#### DCP: Command vs Event Decision Table

| Situation | Use | Why |
|-----------|---|---|
| Document sourced | **EVENT** | Multiple services react, automatic |
| Extraction fails in pipeline | **COMMAND** | Error handling, needs orchestrator decision |
| Quality passed | **EVENT** | Fact happened, orchestrator reacts |
| Create L1 task | **COMMAND** | Orchestrator requests, Task Service decides |
| L1 rejects document | **COMMAND** | Specific request to Extraction, needs decision |
| Extraction rework completes | **EVENT** | Fact happened, other services can react |
| L2 approves | **COMMAND** (sent by L2 UI) | Or EVENT if system auto-approves |
| Document approved (fact) | **EVENT** | Multiple services react (Dissemination, Audit) |
| Document published | **EVENT** | Fact happened, Audit Service reacts |

---

#### Key Insight: DCP's True Pattern

DCP is **NOT choreography OR orchestration**. It's **BOTH + proper use of commands vs events**:

| Phase | Pattern | Primary Mechanism |
|-------|---------|---|
| **Auto Pipeline** | Choreography | EVENTS (services react) |
| **Error Handling** | Choreography | COMMANDS (when auto-pipeline breaks) |
| **Human Workflow** | Orchestration | COMMANDS (orchestrator directs) |
| **Publishing Results** | Orchestration | EVENTS (orchestrator announces) |
| **Publication** | Choreography | EVENTS (multiple services react) |

Commands and events are **NOT synonymous with choreography and orchestration**. Both patterns use both message types!

---

### Decision Tree: Command vs Event

```text
Question: Who needs to DECIDE if this can happen?

├─ Multiple independent services
│  └─ Use EVENT
│     (DocumentSourced → Kitchen reacts AND Delivery reacts)
│
├─ One specific service
│  └─ Who sent this?
│     ├─ Orchestrator / Manager (asking to do something)
│     │  └─ Use COMMAND
│     │     (L1 says "Reject", Extraction Service decides)
│     │
│     └─ Another service (announcing a fact)
│        └─ Use EVENT
│           (DocumentExtracted → Quality consumes)
│
└─ Can this fail?
   ├─ YES → Probably COMMAND
   │        (Manager's request might be rejected)
   │
   └─ NO → Probably EVENT
          (DocumentApproved is a fact, can't fail)
```

---

### Pattern Summary

| Aspect | Command | Event |
|--------|---------|-------|
| **Form** | Imperative ("Do this") | Past tense ("Did this") |
| **Sender** | Orchestrator, Manager, Client | Any service (result of work) |
| **Receiver** | Specific service (one) | Any interested service (many) |
| **Can Fail?** | Yes (receiver decides) | No (already happened) |
| **Response** | Success or failure | No response needed |
| **Use in Choreography** | Rare | Common |
| **Use in Orchestration** | Common | Common (as side effects) |
| **Example: Pizza** | CancelOrder | OrderPlaced, PizzaPrepared |
| **Example: DCP** | ReworkDocumentExtraction | DocumentSourced, DocumentApproved |

---

### Interview-Ready Answer

> **Command** is a request to do something sent to a specific service. It asks the receiver to decide if it can be done, and the receiver can accept or reject it.
>
> **Event** is an announcement that something already happened. Multiple services can react to it independently, but they cannot reject it because it's a fact.
>
> **In choreography (Pizza Store):** Use events because services react independently without central control.
>
> **In orchestration (DCP human workflow):** Use commands when the orchestrator directs specific services, and events when announcing completed facts that other services should react to.
>
> **DCP pattern:** Automatic processing uses events (DocumentSourced → Extract → Quality), human decisions use commands (L1 says "Rework"), and results publish events (DocumentReworked).

---

## 7. What is a compensating transaction?

A compensating transaction reverses or neutralizes the business effect of an earlier completed transaction.

Example:

```text
Reserve payment   ✅
Reserve inventory ✅
Arrange shipping  ❌
```

Compensation:

```text
Release inventory
Release or refund payment
```

Common examples:

| Forward action | Compensation |
|---|---|
| Reserve inventory | Release inventory |
| Charge payment | Refund payment |
| Approve document | Revoke approval |
| Create booking | Cancel booking |

Compensation is not always a perfect undo. An email cannot be unsent, so the compensation may be to send a correction email.

Irreversible operations should generally be placed near the end of the Saga.

---

## 8. What is event sourcing?

Normally, a system stores only the current state:

```text
Order status = DELIVERED
```

This tells us where the order is now, but it does not show how the order reached that state.

With event sourcing, the system stores every change as an event:

```text
1. OrderCreated
2. PaymentCompleted
3. OrderShipped
4. OrderDelivered
```

The event history becomes the source of truth. The current state is calculated by replaying the events in order:

```text
Start with an empty order
→ Apply OrderCreated
→ Apply PaymentCompleted
→ Apply OrderShipped
→ Apply OrderDelivered

Current status = DELIVERED
```

### Simple analogy: A bank account

A bank does not only store the current balance:

```text
Balance = ₹10,000
```

It also stores every transaction:

```text
+ ₹15,000 salary
- ₹3,000 rent
- ₹2,000 shopping
```

The bank can calculate the current balance from this transaction history. Event sourcing works in a similar way: store everything that happened, then derive the current state from that history.

### Why use event sourcing?

- It provides a complete history of what happened.
- We can see who changed something and when.
- We can reconstruct the state at an earlier point in time.
- We can rebuild the current state if a read database is lost or corrupted.
- We can replay events after fixing a bug in processing logic.
- It is useful for auditing and regulatory requirements.

### What are the downsides?

- It is more complex than storing only the latest state.
- Old event formats must continue to work as the application evolves.
- Replaying a large number of events can be slow.
- Read models may update later, causing eventual consistency.
- Event replay must not accidentally repeat external actions such as charging a payment or sending an email.

### Does event sourcing solve distributed transactions?

No.

- **Event sourcing** records what happened.
- **Saga** coordinates work across services and handles failures.

They solve different problems, although they can be used together.

Also, Kafka does not have to be the authoritative event store. A durable append-only database can be the event store while Kafka distributes events to consumers.

### Interview-ready answer

> Event sourcing stores every state change as an immutable event instead of storing only the latest state. The current state is reconstructed by replaying those events. It provides a complete audit history and replay capability, but it adds complexity and does not by itself solve distributed transactions.

---

## 9. What is idempotency?

An operation is idempotent when repeating it produces the same final result as executing it once.

For example, the same money-transfer message may be delivered twice:

```text
Transfer ₹100 from Account A to Account B
Transfer ID = TX-123
```

Without idempotency, Account A could be debited twice or Account B could be credited twice. With idempotency, each service processes `TX-123` only once.

### Simple debit and credit architecture

```text
transfer-request topic
        ↓
JVM 1: Debit Service
        ↓
debit-completed topic
        ↓
JVM 2: Credit Service
        ↓
transfer-completed topic
```

JVM 1 and JVM 2 run independently. Each service has its own Kafka consumer and producer.

### Kafka delivery modes

#### At-most-once

The consumer commits the offset before processing:

```text
Commit offset → Process message
```

If the consumer crashes after committing the offset but before processing, the message is lost.

```text
Message loss: Possible
Duplicate processing: No
```

#### At-least-once

The consumer processes the message before committing the offset:

```text
Process message → Commit offset
```

If the consumer crashes after processing but before committing the offset, Kafka delivers the message again.

```text
Message loss: Normally avoided
Duplicate processing: Possible
```

This is the most common mode, so consumers should be idempotent.

#### Exactly-once

Exactly-once does not mean the processing code executes only once. The code may run again after a crash.

It means that, for Kafka-to-Kafka processing, only one successful result becomes visible.

### Exactly-once in JVM 1: Debit Service

JVM 1 receives `TransferRequested(TX-123)` and performs one Kafka transaction:

```text
BEGIN KAFKA TRANSACTION

1. Read TransferRequested(TX-123)
2. Produce DebitCompleted(TX-123)
3. Commit the transfer-request offset

COMMIT KAFKA TRANSACTION
```

Kafka commits the output event and consumed offset together.

If JVM 1 crashes before committing:

```text
DebitCompleted visible? No
Input offset committed? No
Input message retried?  Yes
```

If the transaction succeeds:

```text
DebitCompleted visible? Yes
Input offset committed? Yes
```

### Exactly-once in JVM 2: Credit Service

JVM 2 starts a separate Kafka transaction:

```text
BEGIN KAFKA TRANSACTION

1. Read DebitCompleted(TX-123)
2. Produce TransferCompleted(TX-123)
3. Commit the debit-completed offset

COMMIT KAFKA TRANSACTION
```

If JVM 2 crashes before committing, neither its output event nor its consumed offset is committed. Kafka delivers `DebitCompleted(TX-123)` again.

Consumers reading transactional output should use `isolation.level=read_committed` so they do not see aborted records.

### Important limitation: Kafka cannot protect database updates

Suppose JVM 1 stores Account A in PostgreSQL:

```text
1. Debit ₹100 from Account A in PostgreSQL ✅
2. JVM 1 crashes before committing the Kafka offset ❌
3. Kafka delivers TX-123 again
4. Account A could be debited again ❌
```

Kafka cannot atomically roll back or commit a normal database transaction together with its own transaction.

Therefore, the Debit Service must use `TX-123` as an idempotency key:

```sql
BEGIN;

INSERT INTO processed_transfers (transfer_id)
VALUES ('TX-123'); -- UNIQUE constraint

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 'A';

COMMIT;
```

The idempotency record and debit must be saved in the same database transaction.

When Kafka redelivers `TX-123`, the unique constraint shows that the transfer was already processed. JVM 1 skips the second debit.

JVM 2 follows the same approach when crediting Account B:

```text
TX-123 not processed → Credit B and record TX-123
TX-123 already exists → Skip duplicate credit
```

Avoid implementing these as unrelated steps:

```text
Check transfer ID → Update balance → Save transfer ID
```

Two consumer instances could check at the same time and both update the balance.

### Complete practical solution

```text
JVM 1: Debit Service
  1. Receive TX-123
  2. Record TX-123 and debit A in one database transaction
  3. Publish DebitCompleted(TX-123)

JVM 2: Credit Service
  1. Receive DebitCompleted(TX-123)
  2. Record TX-123 and credit B in one database transaction
  3. Publish TransferCompleted(TX-123)
```

Use:

- **Kafka transactions** to atomically commit Kafka output records and consumed offsets.
- **Idempotency keys** to prevent duplicate database debit and credit operations.
- **Saga compensation** to refund Account A if crediting Account B permanently fails.

### Interview-ready answer

> JVM 1 and JVM 2 perform separate Kafka transactions. Kafka exactly-once atomically commits each JVM's output records and consumed offsets, so only one successful Kafka result becomes visible. It does not create one transaction across both JVMs or their databases. Database debit and credit operations still require a stable transfer ID, such as `TX-123`, stored with the balance update in one local transaction. If credit permanently fails, a Saga compensates by refunding the debit.

---

## 10. How do these patterns work together?

They solve different parts of the distributed transaction problem:

```text
Saga
└─ Defines the complete business transaction

Orchestration or choreography
└─ Coordinates the Saga steps

Compensating transactions
└─ Recover from partially completed work

Idempotency
└─ Makes retries and duplicate messages safe

Event sourcing
└─ Stores history and allows state reconstruction
```

A practical architecture may use:

```text
Fast processing pipeline
→ Choreography + idempotent consumers

Complex human approval workflow
→ Orchestration + compensating transactions

Audit-sensitive state
→ Event sourcing
```

### Why use choreography for a fast processing pipeline?

Consider a simple automatic pipeline:

```text
Document uploaded
        ↓
Extract text
        ↓
Check quality
        ↓
Create search index
```

Each service can react to the event produced by the previous service:

```text
DocumentUploaded → TextExtracted → QualityChecked → DocumentIndexed
```

Choreography is a good fit because:

- The flow is simple and predictable.
- Services can process many documents in parallel.
- Each service can scale independently.
- A new consumer, such as Analytics Service, can listen without changing the existing services.

The consumers must be idempotent because Kafka may deliver the same event again after a crash or timeout.

```text
First delivery  → Process and record event ID
Second delivery → Event ID already exists, so skip
```

Therefore, choreography gives loose coupling and scalability, while idempotency makes retries safe.

### Does every human workflow require orchestration?

No. A simple human decision can use choreography:

```text
Document submitted
        ↓
Human clicks Approve or Reject
        ↓
DocumentApproved or DocumentRejected event
        ↓
Other services react
```

The presence of a human does not automatically require an orchestrator.

### When does orchestration become useful?

Consider a more complex approval process:

```text
1. Assign Reviewer 1.
2. Wait up to two days.
3. Send a reminder after one day.
4. Escalate to a manager after two days.
5. If approved, assign Reviewer 2.
6. Reviewer 2 may approve, reject or request rework.
7. Rework returns to Reviewer 1.
8. The requester may cancel the process.
9. Operations must see where the document is waiting.
```

This creates several paths:

```text
Reviewer 1
  ├─ No response → Reminder → Escalation
  ├─ Reject      → Finish
  └─ Approve     → Reviewer 2
                      ├─ Approve → Publish
                      ├─ Reject  → Finish
                      └─ Rework  → Reviewer 1
```

Choreography can implement this, but the workflow state becomes scattered across several services:

```text
Review Service     → approvals and rework
Timer Service      → reminders and deadlines
Escalation Service → manager escalation
Document Service   → cancellation
```

For example, when a deadline event arrives, a service must answer:

```text
Was the document already approved?
Was it cancelled?
Is it currently in rework?
Is this an old timer from an earlier review attempt?
Is Reviewer 1 or Reviewer 2 currently responsible?
```

With orchestration, one workflow engine remembers the complete current state:

```text
Workflow ID: DOC-123
Current step: WAITING_FOR_REVIEWER_2
Review attempt: 2
Deadline: 20 June, 5:00 PM
Status: ACTIVE
```

If an old Reviewer 1 timer arrives while the workflow is waiting for Reviewer 2, the orchestrator can see that the timer is stale and ignore it.

An orchestrator is helpful for:

- **Long-running workflows:** The process remains active for hours, days or weeks.
- **Multiple stages:** Steps must happen in a controlled order.
- **Timers:** Reminders or deadline actions must run at the correct time.
- **Escalation:** Work moves to a manager when someone does not respond.
- **Branching:** Approval, rejection and rework have different paths.
- **Rework:** The workflow returns to and repeats an earlier step.
- **Central visibility:** Operations can see where a workflow is currently waiting.

Compensating transactions handle steps that have already completed when a later step permanently fails. For example, if publishing fails after approval, the workflow may revoke the approval, return the document for review, or mark it as `APPROVED_NOT_PUBLISHED`.

### Simple decision rule

```text
One human decision followed by simple reactions
→ Choreography can work well

A managed process that must remember where it is,
handle timers and decide the next valid action
→ Orchestration is usually easier
```

The reason for choosing orchestration is not simply that a human is involved. The reason is the amount of workflow state and decision logic that must be managed.

---

## 11. Microservices design patterns and their DCP applicability

The Data Collection Platform (DCP) receives financial documents from sources such as S3, email and APIs. It extracts data using external AI providers, validates the result, sends uncertain documents for human review and publishes approved data to downstream systems.

Each pattern below solves a specific business or technical problem in that flow.

### Circuit breaker: How does it help the business user?

Suppose the Extraction Service calls the external SparkAir AI API.

```text
DCP Extraction Service → SparkAir
```

If SparkAir becomes unavailable and there is no circuit breaker, every extraction worker continues calling it:

```text
Document 1 → wait 30 seconds → fail
Document 2 → wait 30 seconds → fail
Document 3 → wait 30 seconds → fail
```

Workers remain occupied waiting for a service that is already known to be unhealthy. The Kafka backlog grows and users see documents stuck in `EXTRACTION_IN_PROGRESS`.

A circuit breaker watches the recent calls:

```text
SparkAir calls are healthy
→ Circuit CLOSED
→ Calls are allowed

Failure rate crosses the configured limit
→ Circuit OPEN
→ Stop calling SparkAir temporarily

After a waiting period
→ Circuit HALF-OPEN
→ Allow a small test call

Test succeeds
→ Close circuit and resume normal traffic
```

When the circuit opens, DCP can immediately take another business path:

```text
SparkAir unavailable
        ↓
Try Cognize fallback
        ↓
If Cognize also fails
        ↓
Queue document for manual extraction
        ↓
Notify the L1 user
```

#### Business benefit

The circuit breaker does not repair SparkAir. It prevents one failing dependency from making the whole DCP slow or unavailable.

For the business user, this means:

- The upload request can return quickly instead of hanging.
- The user sees an honest status such as `QUEUED_FOR_RETRY` or `MANUAL_EXTRACTION_REQUIRED`.
- Documents continue through the fallback or manual path.
- Healthy parts of DCP, such as review and dissemination, remain responsive.
- Recovery is faster because the system does not create a huge pile of timed-out calls.

#### Why not just use retries?

Retries help with a short, temporary error:

```text
One network call fails → Retry after a short delay → Success
```

They make a long outage worse:

```text
2,000 documents × 3 retries = 6,000 calls to an unhealthy provider
```

Use retries for small transient failures. Open the circuit when failures continue.

### Pattern applicability in DCP

#### Service and data boundaries

| Pattern | Simple meaning | DCP business use case | Why it fits |
|---|---|---|---|
| Decompose by business capability | Create services around business responsibilities | Sourcing, Extraction, Rules/Quality, Workflow, Approval and Dissemination services | Each area has different rules, scaling needs and ownership |
| Database per service | A service owns its data and other services use its API or events | Approval owns review decisions; Extraction owns extracted document data; Workflow owns task state | Prevents one service from changing another service's data behind its back |
| Polyglot persistence | Use the database that best fits each type of data | PostgreSQL for structured metadata, MongoDB for flexible extracted documents, Elasticsearch for entity search, Redis for short-lived cache | DCP handles structured and highly variable document data |

#### Communication and API patterns

| Pattern | Simple meaning | DCP business use case | Why it fits |
|---|---|---|---|
| Synchronous API | Call another service and wait for an immediate answer | Approval UI loads the current document details; template validation returns immediately | The user needs an immediate response |
| Asynchronous messaging | Publish work and process it later | Sourcing publishes `DocumentSourced`; extraction workers consume documents from Kafka | Upload does not need to wait for slow AI extraction |
| API Gateway | One controlled entry point for clients | Routes L1/L2 UI requests and applies authentication, RBAC and rate limits | Keeps internal services private and applies common security rules |
| Backend for Frontend | API designed for a specific client | A Review UI BFF returns document image, extracted fields, confidence scores and validation errors in one response | Reviewers should not make many service calls from the browser |
| API composition / Aggregator | Fetch live information from several services when a request arrives | Operations screen requests live extraction status, workflow assignment and dissemination status | Useful when the screen needs fresh data from only a few healthy services |

#### Workflow and transaction patterns

| Pattern | Simple meaning | DCP business use case | Why it fits |
|---|---|---|---|
| Saga | Break one business transaction into local transactions | Approve document → publish data → notify downstream users | No single database transaction can cover Approval, S3 and Notification |
| Choreography | Services react to events without a central controller | `DocumentSourced` → `DocumentExtracted` → `QualityChecked` | The automatic pipeline is simple, high-volume and easy to parallelize |
| Orchestration | A central workflow component decides the next step | L1 assignment → L2 review → reminder → escalation → rework → final approval | The process must remember stages, deadlines, branches and reviewer state |
| Compensating transaction | Perform a business-level undo after partial failure | Publication fails after approval, so mark `APPROVED_NOT_PUBLISHED`, retry publication or revoke approval based on policy | The completed approval cannot be technically rolled back across services |

---

### Choreography vs Orchestration: DCP and Pizza Store Comparison

**Which pattern does each system use? The answer is NOT simple: both systems use BOTH patterns, but for different parts of their workflows.**

#### Pizza Store: Choreography-First (Simple)

```text
WORKFLOW:
  Customer places order
       ↓
  OrderPlaced event
       ↓ (Kafka)
  Kitchen Service consumes
       ├─ Prepares pizza
       └─ Publishes PizzaPrepared event
       ↓ (Kafka)
  Delivery Service consumes
       ├─ Assigns delivery partner
       └─ Publishes DeliveryStarted event
       ↓ (Kafka)
  Billing Service consumes
       ├─ Charges customer
       └─ Publishes PaymentProcessed event
```

**Why Choreography?**
- Simple linear flow: Order → Prepare → Deliver → Bill
- No central decision maker
- Each service reacts to events independently
- High throughput (can process 1000s of orders/sec)
- Easy to parallelize (multiple kitchen pods)
- No complex state management

**Orchestration?** Not needed for Pizza Store because:
- No human workflows
- No conditional branching
- No long-running waits
- No state that needs to be remembered across steps
- Each order follows same path

**Conclusion:** Pizza Store is **99% choreography**

---

#### DCP: Hybrid (Choreography + Orchestration)

DCP uses **both patterns for different parts** of the workflow:

##### Part 1: Automatic Pipeline (CHOREOGRAPHY)

```text
WORKFLOW:
  Document uploaded (REST API)
       ↓
  Sourcing Service publishes DocumentSourced
       ↓ (Kafka)
  Extraction Service consumes
       ├─ Calls ML (SparkAir, Cognize)
       └─ Publishes DocumentExtracted
       ↓ (Kafka)
  Quality Service consumes
       ├─ Validates rules
       └─ Publishes QualityChecked (or QualityFailed)
```

**Why Choreography for this part?**
- Fast, automatic processing
- Simple event sequence
- No human decision making
- Can be parallelized across many workers
- High throughput

**No orchestrator needed here because:**
- No branching decisions
- No long waits (humans not involved)
- Service B simply reacts to Service A's event
- Error handling via Kafka DLQ (not compensation)

##### Part 2: Human Workflow (ORCHESTRATION)

```text
WORKFLOW:
  Document passes quality checks
       ↓
  Workflow Orchestrator receives QualityChecked event
       ├─ Creates task for L1 reviewer
       └─ Waits for L1 decision
       ↓
  L1 reviews (human)
       ├─ Approves OR rejects OR requests rework
       └─ Sends decision to Orchestrator
       ↓
  Orchestrator decides next step based on L1 decision
       ├─ If approved: create L2 task
       ├─ If rejected: send notification
       ├─ If rework: notify Extraction service
       └─ Waits for L2 decision
       ↓
  L2 reviews (human)
       ├─ Final approval decision
       └─ Sends to Orchestrator
       ↓
  Orchestrator publishes DocumentApproved
       ↓ (Kafka event triggers Dissemination)
  Dissemination Service consumes & publishes data
```

**Why Orchestration for this part?**
- Decisions made by humans (unpredictable timing)
- Process remembers state (L1 reviewed, waiting for L2)
- Conditional branching (approve/reject/rework)
- Deadlines and reminders ("5 days waiting for L2, send reminder")
- Escalation logic ("No response in 10 days, escalate")
- Compensation needed (revoke approval if publication fails)

**Why NOT choreography?**
- Can't publish event for "waiting for human"
- Must remember: "We're in L1 review stage for doc-123"
- Event-driven doesn't handle long-running waits well
- No way to enforce deadlines or escalations

---

#### Comparison Table: When Each Pattern Shines

| Aspect | Pizza Store (Choreography) | DCP (Both) |
|--------|---|---|
| **Automatic Processing** | ✅ Choreography | ✅ Choreography (Sourcing→Extraction→Quality) |
| **Human Workflows** | ❌ N/A | ✅ Orchestration (L1→L2 review) |
| **Decision Logic** | Simple (just events) | Complex (conditions, timeouts, escalation) |
| **State Needed** | Minimal | High (which stage? who's reviewing? deadline?) |
| **Branching** | None (all orders same path) | Multiple (approve/reject/rework) |
| **Long Waits** | No (pizza cooks in minutes) | Yes (humans take hours/days) |
| **Compensation** | Not needed (idempotent retries) | Needed (revoke approval) |
| **Total Pattern Usage** | 95% Choreography, 5% Orchestration | 40% Choreography, 60% Orchestration |

---

#### Visual: Where Each Pattern is Used

**Pizza Store:**
```
┌─────────────────────────────────────────────┐
│ Order → Prepare → Deliver → Bill            │
│ All CHOREOGRAPHY (events trigger events)    │
│ No orchestrator needed                      │
└─────────────────────────────────────────────┘
```

**DCP:**
```
┌─────────────────────────────────────────────┐
│ CHOREOGRAPHY ZONE (Automatic)               │
│                                             │
│ Upload → Source → Extract → Quality         │
│ (Events → Events → Events)                  │
│                                             │
├─────────────────────────────────────────────┤
│ ORCHESTRATION ZONE (Human)                  │
│                                             │
│ Orchestrator                                │
│  ├─ Create L1 task                         │
│  ├─ Wait for L1 response                   │
│  ├─ Create L2 task                         │
│  ├─ Wait for L2 response                   │
│  ├─ On timeout: send reminder              │
│  ├─ On rework: send back to Extraction     │
│  └─ On approval: publish document          │
│                                             │
├─────────────────────────────────────────────┤
│ CHOREOGRAPHY ZONE (Publication)             │
│                                             │
│ Document → Disseminated                     │
│ (Events trigger events)                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

#### Code Pattern: DCP's Hybrid Approach

**Choreography Part (Extraction):**
```python
# Extraction Service consumes event
def handle_document_sourced(event):
    trace_id = event["trace_id"]
    doc_id = event["doc_id"]
    
    # Do work (no central orchestrator)
    extracted = extract_with_ml(event)
    
    # Publish event (choreography)
    producer.send("document-extracted", {
        "doc_id": doc_id,
        "trace_id": trace_id,
        "extracted_data": extracted
    })
```

**Orchestration Part (Human Workflow):**
```python
# Workflow Orchestrator handles human decisions
class DocumentApprovalOrchestrator:
    def handle_quality_checked(self, event):
        doc_id = event["doc_id"]
        
        # Create saga instance (remembers state)
        saga = {
            "doc_id": doc_id,
            "status": "AWAITING_L1",
            "l1_assigned_at": now()
        }
        db.insert("sagas", saga)
        
        # Create task for L1 reviewer
        task = {"doc_id": doc_id, "reviewer_level": 1}
        task_service.create_task(task)
        
        # Wait for L1 response (orchestrator remembers state)
        # No event published yet (unlike choreography)
    
    def handle_l1_approval(self, decision):
        saga_id = decision["saga_id"]
        
        # Orchestrator makes decision
        saga = db.get("sagas", saga_id)
        
        if decision["approved"]:
            # Move to L2
            saga.status = "AWAITING_L2"
            task = {"doc_id": saga["doc_id"], "reviewer_level": 2}
            task_service.create_task(task)
        else:
            # Reject and publish event
            producer.send("approval-rejected", {
                "doc_id": saga["doc_id"]
            })
        
        db.update("sagas", saga_id, saga)
    
    def handle_l2_approval(self, decision):
        saga_id = decision["saga_id"]
        
        if decision["approved"]:
            # Final approval - publish event to choreography zone
            producer.send("document-approved", {
                "doc_id": saga["doc_id"]
            })
            saga.status = "APPROVED"
        else:
            saga.status = "REJECTED"
        
        db.update("sagas", saga_id, saga)
```

---

#### Key Insight: Why DCP Needs Both

| Zone | Pattern | Reason |
|---|---|---|
| **Sourcing→Extraction→Quality** | Choreography | Fast, high-volume, auto-processing, no decisions |
| **Quality→Review→Approval** | Orchestration | Humans involved, complex state, timeouts, escalations |
| **Approval→Dissemination** | Choreography | Fast, event-driven, once approved just publish |

**DCP uses orchestration as a "decision gate"** in the middle of an otherwise choreography-driven system.

---

#### Pizza Store: Why NOT Orchestration?

If Pizza Store tried to use an orchestrator for every order:

```python
# BAD: Orchestrator for every order
orchestrator.create_order_saga(order_id)
orchestrator.send_command("Cook pizza", order_id)
    ↓ Wait for response
orchestrator.send_command("Deliver pizza", order_id)
    ↓ Wait for response
orchestrator.send_command("Bill customer", order_id)
```

**Problems:**
- Orchestrator becomes bottleneck (1000s of orders/sec)
- Orchestrator memory grows (storing every order's state)
- Latency increases (waiting for each step response)
- Higher complexity for no benefit
- Harder to scale

**Instead, simple choreography works:**
```python
# GOOD: Event-driven (choreography)
producer.send("orders", event=order)
    ↓ No wait
Kitchen consumes and publishes PizzaPrepared
    ↓ (no orchestrator)
Delivery consumes and publishes DeliveryStarted
    ↓ (no orchestrator)
Billing consumes and publishes PaymentProcessed
```

**Benefits:**
- Decoupled services
- No bottleneck
- Massive parallelism
- Simple to understand
- Scales linearly

---

## Final Answer

| System | Pattern | Use Case |
|--------|---------|----------|
| **Pizza Store** | Choreography (95%) + minimal Orchestration | Fast food orders don't need central workflow logic |
| **DCP** | Both: Choreography (40%) + Orchestration (60%) | Auto-processing is choreography, human-review workflow needs orchestration |

The difference: Pizza Store's entire workflow is "just process events", while DCP has a human decision gate in the middle that requires orchestration.

---



#### Reliable messaging and data patterns

| Pattern | Simple meaning | DCP business use case | Why it fits |
|---|---|---|---|
| Transactional outbox | Save business data and an event in one database transaction | Sourcing saves document metadata and an outbox `DocumentSourced` record together | Prevents a saved document from being lost to the pipeline because Kafka publication failed |
| Idempotent consumer | Safely ignore a duplicate message | Extraction uses `documentId + version/hash`; Dissemination uses a publication ID | Kafka redelivery must not extract or publish the same document twice |
| Dead-letter queue | Move repeatedly failing messages aside | Corrupt PDFs, unsupported formats or permanently invalid extraction events go to a DLQ | One bad document should not block the complete topic; operations can inspect and replay it |
| Event sourcing | Store every important state change as an immutable event | Record `SOURCED`, `EXTRACTED`, `QUALITY_CHECKED`, `APPROVED` and `PUBLISHED` | Financial data requires lineage, auditing and historical reconstruction |
| CQRS | Use a write model for changes and a read model optimized for queries | Events update a `DocumentSummary` view used by reviewer and operations dashboards | Users get a fast single view without calling every service |
| API composition | Combine live responses during the user request | Display a low-volume administrative detail screen using live service calls | Simpler than CQRS when traffic and fan-out are small and freshness is more important |

#### Resilience patterns

| Pattern | Simple meaning | DCP business use case | Business benefit |
|---|---|---|---|
| Timeout | Stop waiting after a safe limit | Stop waiting when SparkAir, Soniq or a destination API does not respond | The user request and worker do not hang forever |
| Retry with backoff and jitter | Retry temporary failures with increasing delays | Retry an S3 timeout or temporary destination API error | Handles short failures without creating an immediate traffic storm |
| Circuit breaker | Temporarily stop calls to a repeatedly failing dependency | Open the SparkAir circuit, use Cognize, then route to manual extraction if required | Users receive a quick alternative path instead of seeing every document stuck |
| Fallback | Use an alternative result or provider | SparkAir → Cognize → manual extraction | DCP continues delivering business value during provider outages |
| Bulkhead | Isolate resources used by different dependencies or workloads | Separate worker pools for AI extraction, Soniq entity mapping and dissemination | Slow entity mapping cannot consume all workers and stop document review |
| Rate limiting | Restrict how much work one caller can submit | Limit bulk upload or partner API traffic per tenant | One source cannot overload DCP and delay every other business user |
| Cache-aside | Read from cache first and load on a miss | Cache templates, extraction rules and Soniq entity mappings | Review and extraction become faster while expensive external calls decrease |

#### Scaling, discovery and operational patterns

| Pattern | Simple meaning | DCP business use case | Why it fits |
|---|---|---|---|
| Competing consumers | Multiple workers consume from the same topic | Scale extraction workers from 5 to 20 pods based on Kafka lag | Documents are processed in parallel while each partition is owned by one consumer |
| Service discovery | Find healthy service instances dynamically | Kubernetes Service DNS locates Extraction, Workflow and Approval pods | Pod addresses change during scaling and deployment |
| Sidecar | Run a supporting component beside the application | A telemetry or proxy sidecar exports logs, metrics and traces | Adds common operational behavior without duplicating it in every service |
| Service mesh | Apply common service-to-service network policies | Mutual TLS, traffic policies and observability across many DCP services | Useful when the number of services and security policies justifies the operational cost |

#### Migration patterns

| Pattern | Simple meaning | DCP business use case | Why it fits |
|---|---|---|---|
| Strangler Fig | Replace a legacy system one capability at a time | Route new document types to DCP while older types continue through the legacy collection platform | Reduces the risk of a full rewrite and allows gradual business migration |
| Anti-corruption layer | Translate between the new and legacy models | Convert legacy status codes and document schemas into DCP's canonical events | Prevents legacy concepts from spreading into new services |

### Detailed DCP business examples

The tables above are useful for quick revision. The following examples explain how each pattern affects the actual DCP workflow and its business users.

#### 1. Decompose by business capability

Split DCP according to business responsibilities:

```text
Sourcing Service
Extraction Service
Quality/Rules Service
Workflow Service
Approval Service
Dissemination Service
```

This fits DCP because each capability behaves differently:

- Extraction needs high compute and independent scaling.
- Approval contains human-review and authorization rules.
- Workflow manages assignments, deadlines and escalation.
- Dissemination supports different external destinations and formats.

Each capability can be owned, changed, deployed and scaled independently.

#### 2. Database per service

Each service owns its data:

```text
Extraction Service → extracted document data
Approval Service   → decisions and comments
Workflow Service   → assignments and deadlines
```

For example, Approval Service should not directly update Workflow Service tables. It should send a command or publish an event.

This protects service boundaries and prevents one team's database change from silently breaking another service.

#### 3. Synchronous API

Use synchronous communication when the user needs an immediate answer.

DCP examples:

```text
Reviewer opens a document
→ Fetch document details immediately

Administrator validates an extraction template
→ Return validation errors immediately
```

Do not make the complete extraction pipeline synchronous. AI extraction may take seconds or minutes, and the upload request should not remain open for the entire process.

#### 4. Asynchronous messaging

Use Kafka for slow or background processing:

```text
DocumentUploaded
      ↓
DocumentSourced
      ↓
DocumentExtracted
      ↓
QualityChecked
```

The user receives an upload acknowledgement without waiting for extraction to finish.

This helps DCP:

- Absorb large upload spikes.
- Process documents in parallel.
- Scale extraction workers independently.
- Continue accepting documents while a downstream stage is temporarily slow.

#### 5. API Gateway

The review applications use one controlled entry point:

```text
L1/L2 Review UI
       ↓
API Gateway
  ├── Document Service
  ├── Workflow Service
  └── Approval Service
```

The gateway handles:

- Authentication
- L1/L2 role permissions
- Rate limiting
- Routing
- Request logging

The business receives consistent security, while internal services remain private.

Core approval or extraction rules should remain inside their business services rather than being placed in the gateway.

#### 6. Backend for Frontend

A Review BFF returns everything needed by one reviewer screen:

```text
Document image
Extracted fields
Confidence scores
Validation errors
Reviewer assignment
Comments
```

Without a BFF, the browser may need to call many services and combine the results itself.

The BFF gives reviewers a faster and simpler user experience while hiding internal service boundaries from the UI.

#### 7. API composition

For a low-volume operations screen, an aggregator can fetch live data:

```text
Operations UI
      ↓
Aggregator
  ├── Extraction status
  ├── Workflow status
  └── Dissemination status
```

Use API composition when:

- Only a few services are involved.
- Live data is more important than consistently low latency.
- The query volume is moderate.

The trade-off is that the response becomes slow or incomplete when a participating service is slow or unavailable.

#### 8. CQRS

DCP events can maintain a pre-built document summary:

```text
DocumentSourced
DocumentExtracted
QualityChecked
DocumentApproved
DocumentPublished
        ↓
DocumentSummary read model
```

The dashboard performs one fast query:

```text
GET /documents/DOC-123
```

It does not call Sourcing, Extraction, Quality, Approval and Dissemination every time a reviewer opens the page.

Use CQRS when:

- The dashboard is requested frequently.
- Fast and predictable responses matter.
- The read view combines data owned by several services.
- A small delay before the view reflects the latest event is acceptable.

CQRS gives fast reads but introduces eventual consistency and requires monitoring of the projection consumers.

#### 9. Saga

A complete DCP business transaction may be:

```text
Approve document
→ Publish approved data
→ Notify downstream users
```

Each step belongs to a different service or external system. A single database transaction cannot cover all of them.

If publishing fails, the Saga applies the business recovery policy:

```text
Retry publication
or
Mark APPROVED_NOT_PUBLISHED
or
Revoke approval and return for review
```

Saga provides coordination and business-level recovery instead of a cross-service database rollback.

#### 10. Choreography

Use choreography for DCP's simple automatic pipeline:

```text
DocumentSourced
→ DocumentExtracted
→ QualityChecked
```

Each service reacts to the previous event and publishes its result.

This fits because the pipeline is:

- High volume
- Mostly sequential
- Easy to parallelize
- Suitable for independent service scaling

If the pipeline develops many branches, timers, rework loops or central visibility requirements, orchestration may become easier to manage.

#### 11. Orchestration

Use orchestration for a complex review workflow:

```text
Assign L1 reviewer
→ Wait for review
→ Send reminder
→ Escalate if overdue
→ Assign L2 reviewer
→ Handle approval, rejection or rework
```

The orchestrator remembers:

```text
Current reviewer
Current stage
Deadline
Review attempt
Previous decisions
```

The presence of a human is not itself the reason for orchestration. The reason is the amount of workflow state, timing and decision logic that must be managed.

#### 12. Transactional outbox

Consider this failure:

```text
Save document metadata ✅
Publish DocumentSourced ❌
```

The document exists in DCP but never enters extraction.

With an outbox, the service saves both records in one database transaction:

```text
BEGIN

Save document metadata
Save DocumentSourced in outbox

COMMIT
```

A background publisher later sends the outbox event to Kafka.

The business benefit is that an accepted document is not silently lost from the processing pipeline.

#### 13. Idempotent consumer

Kafka may deliver `DocumentSourced` more than once.

DCP can use a stable identifier:

```text
documentId + documentVersion or contentHash
```

The consumer records that identifier in the same local transaction as its business update:

```text
First delivery  → Extract and record the identifier
Second delivery → Identifier already exists, so skip
```

This prevents duplicate extraction, publication and notification.

#### 14. Dead-letter queue

A corrupt PDF may repeatedly fail extraction:

```text
Document event
→ Retry
→ Retry
→ Still fails
→ Dead-letter topic
```

The remaining documents continue processing.

Operations can inspect the failed message, correct its data or configuration and replay it.

A DLQ must have alerts, ownership and a recovery process. Otherwise, it becomes a place where failed business documents are forgotten.

#### 15. Event sourcing

Store the document's complete history:

```text
DocumentSourced
DocumentExtracted
QualityChecked
AssignedForReview
DocumentApproved
DocumentPublished
```

This is useful in DCP because financial-data systems need:

- Complete audit history
- Data lineage
- Historical state reconstruction
- Evidence of who approved a document and when

Event sourcing is valuable where these requirements justify the additional storage, schema-versioning and replay complexity.

#### 16. Timeout

DCP should not wait indefinitely for SparkAir, Soniq or a destination API:

```text
Call SparkAir
→ Stop waiting after the configured timeout
```

The document can then move to retry, fallback or manual handling instead of remaining stuck forever.

A timeout is the foundation for retries and circuit breakers. Without it, a call may consume a worker indefinitely.

#### 17. Retry with backoff

For a temporary S3 or network failure:

```text
Attempt 1 → fail
Wait 1 second
Attempt 2 → fail
Wait 2 seconds
Attempt 3 → success
```

Backoff and jitter prevent all workers from retrying at exactly the same time.

Use retries only for temporary failures and safe or idempotent operations. Validation failures, corrupt files and permission errors usually require correction rather than retry.

#### 18. Fallback

DCP can define a sequence of alternative extraction paths:

```text
SparkAir
→ Cognize
→ Manual extraction
```

The fallback may provide less automation, but it allows the business process to continue instead of stopping completely.

The user should see which path is being used and whether manual action is required.

#### 19. Bulkhead

Use separate worker pools or concurrency limits:

```text
AI extraction workers
Soniq entity-mapping workers
Dissemination workers
```

If Soniq becomes slow, it consumes only the resources assigned to entity mapping.

Reviewers can continue approving existing documents, and dissemination can continue publishing completed work.

The pattern is named after ship compartments: flooding one compartment should not sink the entire ship.

#### 20. Rate limiting

Suppose one partner uploads 50,000 documents at once.

Without rate limiting, that partner may use all available capacity and delay every other source.

With rate limiting:

```text
Partner A → controlled submission rate
Partner B → retains fair access to DCP
```

Rate limits can be applied per tenant, partner, API key or expensive operation.

The business benefit is predictable and fair service for all users.

#### 21. Cache-aside

Cache frequently reused data:

```text
Extraction templates
Validation rules
Soniq entity mappings
```

The service checks the cache first:

```text
Check cache
├─ Found   → Return quickly
└─ Missing → Load source data and cache it
```

This reduces database and external API calls while making extraction and review faster.

The cache needs an expiry or invalidation strategy so users do not continue seeing obsolete templates or rules.

#### 22. Competing consumers

Several Extraction Service pods consume from the same Kafka consumer group:

```text
Extraction topic
  ├── Worker 1
  ├── Worker 2
  ├── Worker 3
  └── Worker 20
```

Kafka assigns partitions among the active consumers.

When the backlog grows, Kubernetes can add workers. When it falls, workers can scale down.

The number of active consumers that can process simultaneously is limited by the number of topic partitions.

#### 23. Strangler Fig

During gradual migration:

```text
New document types → DCP
Old document types → Legacy platform
```

Capabilities move to DCP one at a time instead of replacing the complete legacy platform in one risky release.

The business benefit is lower migration risk and the ability to learn from each migrated capability before moving the next one.

#### 24. Anti-corruption layer

The legacy platform may use unclear models:

```text
Status = 17
Document type = FIN_USPF_V2
```

An anti-corruption layer translates them into DCP concepts:

```text
Status = APPROVED
Document type = AuditedFinancialStatement
```

The anti-corruption layer prevents legacy terminology and data structures from contaminating the new DCP domain model.

### Quick DCP decision guide

| DCP situation | Prefer |
|---|---|
| Upload should return before extraction finishes | Kafka asynchronous messaging |
| SparkAir fails briefly | Timeout and retry with backoff |
| SparkAir keeps failing | Circuit breaker and Cognize fallback |
| Both AI providers fail | Manual extraction queue and user notification |
| One malformed document repeatedly fails | Dead-letter queue |
| The same Kafka event is delivered again | Idempotent consumer |
| Save document metadata and reliably publish an event | Transactional outbox |
| Simple automated sourcing-to-quality pipeline | Choreography |
| L1/L2 review with timers, escalation and rework | Orchestration |
| Publication fails after approval | Saga compensation and controlled retry |
| Reviewer dashboard needs a fast combined document view | CQRS read model |
| Low-volume screen requires the freshest live status | API composition |
| Regulators need the complete document history | Event sourcing |
| Soniq becomes slow but extraction must continue | Bulkhead plus cache |
| One partner sends a very large traffic spike | Rate limiting |

### Architect interview summary

> For DCP, I use choreography and competing consumers for the high-volume automatic pipeline, and orchestration for the stateful L1/L2 workflow. Outbox and idempotency prevent lost and duplicate processing. CQRS gives reviewers a fast document summary, while event sourcing provides regulatory lineage. External providers are protected with timeout, controlled retry, circuit breaker, fallback and bulkhead. Each pattern is selected for a specific business failure or scaling concern, not simply because it is popular.

---

## Interview-ready answer

> In microservices, I would avoid a distributed ACID transaction across service databases. I would model the business transaction as a Saga made of local transactions. For a simple event pipeline, I would use choreography. For a complex workflow involving timeouts, branching or human approval, I would use orchestration. Each completed step would have a compensating action, and every message consumer would be idempotent because duplicate delivery is possible. I would use event sourcing only where complete history, auditing or replay provides enough business value to justify its complexity.
