# Interview Prep: Last-Minute Revision (Condensed)

**How to use this:** read it the night before and the morning of the interview. Each section gives the core idea in plain words, what to say in an interview, and a link to the full answer in [0-interview-prep.md](0-interview-prep.md) for depth.

**The four ideas that cover most questions**

1. **Split fast from slow.** Users get fast answers. Slow work (AI, batch, approvals) runs in the background behind a queue.
2. **Make everything safe to retry.** Duplicates happen. Idempotency and the outbox prevent double-processing and lost events.
3. **Variation belongs in data, not code.** Templates, rules and tenants are configuration.
4. **Measure what you promise.** SLOs, p95, golden-set evals and error budgets. Claim only numbers you can explain.

---

## 1. Role snapshot and fit
- 22 years of Java and architecture. Strong in distributed systems, cloud, and AI.
- Gaps to own: OCI, Flink, gRPC and SOAP in production, Oracle depth. Say what you'd do to ramp up. ([§1](0-interview-prep.md#1-role-snapshot--fit), [§28](0-interview-prep.md#28-wfs-senior-solution-architect-adp-qa))

## 2. Core Java and frameworks
- **Why Spring Boot:** mature Kafka and PostgreSQL drivers, and AOP for cross-cutting concerns.
- **Safe Kafka retries:** outbox for publishing, idempotent consumers for receiving. ([§2](0-interview-prep.md#2-core-java--framework-depth))


**Level 2: more detail**
- **Design patterns in DCP:** Factory picks the extraction engine (SparkAir, Cognize, Deepmine). Adapter normalizes PDF, Excel and CSV parsers. Strategy switches manual or AI extraction. State tracks document lifecycle (sourced, extracted, approved, published). Chain of Responsibility runs validation.
- **Why Spring Boot:** mature Kafka and PostgreSQL drivers, and AOP to add logging, caching and retry in one place across six services.

## 3. Distributed systems
- **Why Kafka:** decoupling, buffering, replay, fan-out, per-key ordering.
- **Real incident:** a consumer saved its result, crashed before committing the offset, and processed the document again. Fix: check for the message ID inside the same transaction as the write.
- **Partition sizing:** size for 2x growth. Consumers beyond the partition count sit idle.
- **Autoscale on lag, not CPU.** Consumers wait on external calls, so CPU stays low. ([§3](0-interview-prep.md#3-distributed-systems--large-scale-compute-design))


**Level 2: more detail**
- **Sizing example:** peak 100 docs/s, one consumer does 5 docs/s, so 20 consumers. At 2x growth, 40 consumers, so 48 partitions give headroom.
- **Entity mapping (biggest bottleneck):** 50K entities/day against a 1,000 requests/min API. Fix: Redis cache (85% hit rate), batches of 10, circuit breaker with fuzzy-match fallback, and an async retry every 5 minutes. Result: 92% mapping success, 40% more throughput.
- **Consistency without distributed locks:** event sourcing plus CQRS. Each state change is an immutable event, ordered per documentId. Approval conflicts fell by 99%.
- **Fan-out to many machines:** publish once to a partitioned topic, and let competing consumers pull their share.

## 4. Cloud and infrastructure
- **Kubernetes and deployment:** canary (10 → 50 → 100%), with automatic rollback.
- **Cost:** job clusters that end when the job ends, plus spot for re-runnable work. Never spot for the driver or SLA-critical paths. ([§4](0-interview-prep.md#4-cloud--infrastructure-at-scale))
- **Multi-AZ vs multi-region:** multi-AZ by default. Multi-region only when a whole-region outage is the risk. ([§15](0-interview-prep.md#15-additional-details))


**Level 2: more detail**
- **Scaling:** HPA on CPU, memory and Kafka lag. Extraction pods scale 5 to 50. Canary steps 10% then 50% then 100% over about 30 minutes, with instant rollback.
- **Incident defense-in-depth:** pre-flight checklist (tests, coverage, rollback plan), canary, runbooks, blameless postmortems. Incidents 4 to 1 per month on critical, about 60% overall.
- **Databricks cost:** job clusters instead of all-purpose clusters, and spot only for workers, never the driver. ⚠ Verify the specifics.
- **Multi-cloud:** adds data-transfer cost, duplicate infrastructure and ops headcount. Only worth it when it prevents outages that cost more.

## 5. Data and storage
- **Polyglot persistence:** Postgres for ACID metadata, Mongo for flexible documents and the event log, Redis for cache, Elasticsearch for search.
- **Durability:** idempotent processing, outbox, replica sets, and PostgreSQL HA. ([§5](0-interview-prep.md#5-data--storage))


**Level 2: more detail**
- **Durability:** idempotent processing, outbox, MongoDB 3-node replica set, PostgreSQL HA with under 30-second failover, 4-hour RTO and 1-hour RPO from S3 backup.
- **Lakehouse:** Bronze (raw), Silver (clean, deduplicated), Gold (aggregates), with Spark. Dedup at about 1 billion document scale.
- **Relational vs NoSQL:** relational for ACID and stable schemas (metadata, approval rules). NoSQL when the schema varies per record and the store doubles as an event log.

## 6. Leadership and agile
- **Contested decisions:** turn opinions into requirements, score each option, and ask the skeptic which requirement justifies their option.
- **Adoption:** pilot with 2 people, then use the data to convert skeptics. ([§6](0-interview-prep.md#6-engineering-leadership--agile-execution))


**Level 2: more detail**
- **Team conflict (legacy vs microservices):** the root cause was no coordination channel, not personality. Fix: a cache-invalidation plan submitted a week ahead, and two-week cross-shadowing. Result: zero cache-invalidation incidents.
- **Tech-debt balance:** split a 100-engineer org 50/50 between modernization and features, with monthly dashboards. Result: a 2M-line monolith shrank 40%.
- **CI/CD adoption:** a 2-developer pilot shipped 2x features per month with zero incidents. That data converted the skeptics.

## 7. Mentoring and people
- **Skeptic:** give them the hardest part of the problem to solve.
- **Mistake:** separate the person from the failure, then hand the fix back to them.
- **Hard decision:** be honest up front, then give each person a real choice. ([§7](0-interview-prep.md#7-mentoring--people-development))


**Level 2: more detail**
- **Skeptic:** a senior engineer distrusted event-driven design. Give him the reliability design (idempotency, retries, dead-letter queues). He became its loudest defender.
- **Morale after an outage:** 1:1s with everyone who fought the fire, extra vacation days, and a lighter next sprint. Velocity recovered by week three.
- **Fragmented teams:** a decision log, and async-first meetings. Trust score rose from 3 to 8 out of 10. Singapore attrition fell from 30% to 5%.

## 8. Strategy and vision
- **Modernize without a big bang:** strangler pattern, one business line at a time.
- **Advocacy:** quantify the cost of not investing, and show progress on a regular cadence. ([§8](0-interview-prep.md#8-strategictechnical-vision))


**Level 2: more detail**
- **Staged capacity:** validate 2x capacity on the existing design before any rewrite.
- **Honest regret:** would add stronger eventual-consistency messaging to users from day one. The event-sourcing trade-off was still right.

## 9. Motivation and fit
- Frame the move as a deliberate trade of breadth for depth. Be ready to say why this company, specifically. ([§9](0-interview-prep.md#9-motivation--fit))

## 10. GenAI
- **LLM extraction:** the model alone was about 85% accurate. The system, with routing, validation and audits, delivered about 95% straight through and about 99% after review.
- **Agents:** agents act only through governed tools, with human approval for risky actions. ([§10](0-interview-prep.md#10-genai-wildcard))


**Level 2: more detail**
- **Confidence routing:** above 0.9 auto-approve, 0.7 to 0.9 L2 review, below 0.7 manual. Plus rule validation and hourly sampling audits (100 documents, alert if below 99%).
- **Personal project (VoxAlchemy):** the user stays the orchestrator. The transaction flow doesn't need agentic complexity.
- **Cost:** route by task. Cheap model for classification, big model only where reasoning pays off. Cache and set per-tenant budgets.

## 11. Questions to ask
- Ask about the current bottleneck, the 12-month priority, and how success is measured. ([§11](0-interview-prep.md#11-questions-to-ask-them))

## 12. Numbers to memorize
- **DCP:** 10K+ documents/day, p95 1.5s, 99%+ availability, 95% accuracy.
- **Cost:** about $180K/year saved, EC2 down 70%, Databricks down 97.5%.
- **Incidents:** 60 → 24 a month, MTTR 2 hours → 20 minutes. ([§12](0-interview-prep.md#12-key-numbers-cheat-sheet))


**Level 2: more detail**
- **Latency and load:** p95 1.5s, approval about 800ms, cached lookup about 50ms, 500+ concurrent users.
- **Scale:** 12K/day validated, 20K/day designed, Kafka 1,000 events/s.
- **Error budget:** 99.9% is about 44 minutes a month. 99.95% is about 22 minutes.

## 13. Gaps to own
- Quarkus, quant-domain depth, and the director-to-hands-on framing. Say them before the interviewer does. ([§13](0-interview-prep.md#13-gaps--own-these-honestly))

## 14. XiP / XiNG (Citi)
- **Compute at scale:** Amdahl's law: a 10x speedup needs the serial part shrunk, not only more machines.
- **Stragglers:** speculative execution and hierarchical aggregation.
- **Reproducibility:** fixed reduce order, because floating-point sums change with order. ([§14](0-interview-prep.md#14-xip-specific-technical-questions))

## 15. Additional details
- **Transactional outbox:** save state and the event in one transaction, then publish the event.
- **Blue-green and canary:** switch traffic in steps, keeping the old version ready for rollback.
- **Entity mapping:** cache, batch, circuit breaker and fallback, then an async retry queue. ([§15](0-interview-prep.md#15-additional-details))

## 16. Microservices
- **Saga:** a sequence of local transactions, each with a compensating action.
- **Choreography:** services react to events. Good for simple pipelines.
- **Orchestration:** one coordinator tracks steps and timers. Good for approvals.
- **Warning:** poorly cut services become a distributed monolith. ([§16](0-interview-prep.md#16-microservices-when-pitfalls-culture-patterns))


**Level 2: more detail**
- **Choose by workflow:** fast pipeline, choreography plus idempotent consumers. Human approval with timers and rework, orchestration plus compensations. Audit-sensitive state, event sourcing.
- **Pitfalls:** distributed monolith (shared database, long sync chains), and culture (teams must own services end to end).
- **Versioning and tests:** version APIs so consumers don't break, use consumer-driven contract tests, and keep schema changes compatible.

## 17. Conflict stories
- Use one of three shapes: a culture clash, a cross-team cost impact, or a peer with no shared manager. ([§17](0-interview-prep.md#17-conflict-scenarios-for-behavioral-questions))

## 18. AWS
- **Foundation:** VPC with private subnets, EKS, EC2, S3, IAM, KMS, ALB, Route 53, ACM.
- **Managed vs native:** native means only AWS offers it (IAM, API Gateway). Managed means AWS runs software that exists elsewhere (EKS, MSK, ElastiCache).
- **Self-managed nodes and databases:** AWS runs the EKS control plane. We managed worker nodes and PostgreSQL and MongoDB on EC2.
- **Service-to-service auth:** Okta client-credentials tokens. IRSA is only for calls to AWS APIs. ([§18](0-interview-prep.md#18-aws-likely-questions-and-dcp-mapped-concepts), [§26.15](0-interview-prep.md#2615-dcp-on-aws-the-full-footprint-native-vs-managed-spot-secrets-and-uploads))


**Level 2: more detail**
- **Service map:** EKS, EC2 worker nodes, MSK, ElastiCache, S3, Okta for identity, Vault with KMS for secrets, Prometheus, Jaeger and Splunk for monitoring, CloudTrail for audit.
- **Uploads:** up to 10 MB through API Gateway. Larger files use pre-signed S3 URLs, so the gateway never carries a large payload.
- **Spot:** a two-minute warning. Drain the node and let idempotent consumers re-run the work.

## 19. Behavioral questions
- Use STAR, with one clear number per story. The index lists which story fits which question. ([§19](0-interview-prep.md#19-behavioral-qa-index))

## 20. System design reference
- **Fundamentals:** scale estimation, load balancing, caching, partitioning, replication.
- **Consistency:** CAP (choose consistency or availability during a partition), PACELC (without a partition, latency vs consistency). ([§20](0-interview-prep.md#20-system-design-reference))

## 21. Spring
- **@SpringBootApplication** = @EnableAutoConfiguration + @Configuration + @ComponentScan.
- **@Component vs @Bean:** @Component for your own classes, @Bean for third-party classes or custom setup. ([§21](0-interview-prep.md#21-spring-framework-reference))


**Level 2: more detail**
- **Startup order:** `main()` runs `SpringApplication.run()`, which creates the ApplicationContext, scans components, auto-configures, creates beans, and starts embedded Tomcat.
- **Scopes:** singleton for shared, stateless services. Prototype for per-request or stateful objects.
- **CORS:** blocked when the origins differ and the backend doesn't allow the frontend origin.

## 22. OOP and design
- **Encapsulation:** hides data. **Abstraction:** hides detail. **Polymorphism:** one method, many behaviors. **Inheritance:** reuse.
- **SOLID:** one reason to change; open for extension; subclasses must substitute; small interfaces; depend on abstractions. ([§22](0-interview-prep.md#22-oops-object-oriented-design-reference))


**Level 2: more detail**
- **Aggregation:** "has-a", the parts can exist alone. **Composition:** "owns", the parts die with the whole.
- **Interview example:** an Order owns its LineItems (composition). A Customer places orders, but orders outlive the customer record only if the business allows it (aggregation). Use the business rule to decide.

## 23. Advanced Java
- **Thread states:** NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.
- **Race conditions:** fix with synchronization, atomic operations, or immutable data.
- **Memory:** the JVM heap and GC generations; use heap dumps for OOM.
- **Transactions:** Spring propagation; two-phase commit trades availability for atomicity. ([§23](0-interview-prep.md#23-advanced-java))


**Level 2: more detail**
- **Sections in the full guide:** CAS, race conditions and fixes, JVM and GC, deadlock detection, OOM scenarios, two-phase commit, serialization, ExecutorService and thread pools, Spring transaction propagation, the Spring annotations, and how Spring Boot starts.
- **Thread states:** RUNNABLE means running or ready. BLOCKED waits for a lock. WAITING waits for a signal. TIMED_WAITING waits up to a limit.

## 24. Karat screen (Citi)
- 60 minutes, rubric-scored, screen-recorded. Explain your approach before you code, and don't go silent. ([§24](0-interview-prep.md#24-citi-karat-screening-round))

## 25. Redwood site-lead round
- Build the Hyderabad centre: hiring, ownership, AI-first delivery, enterprise SaaS reliability. ([§25](0-interview-prep.md#25-redwood--director-of-engineering-ai--full-stack-saas-site-lead-round))

## 26. My resume (DCP and career)
- **DCP:** the four numbers in one breath: throughput, latency, accuracy, availability. Each is met by a different part of the design.
- **Architecture:** split fast from slow; tenants as sectors; schema per tenant.
- **Availability:** 99.9% is about 44 minutes of downtime a month. Each extra nine needs more redundancy, faster detection, and safer change. ([§26](0-interview-prep.md#26-my-resume))

## 27. Java scenario Q&A
- **Slow API:** find the slow hop with traces, thread dumps and pool metrics.
- **HashMap under concurrency:** use ConcurrentHashMap.
- **Lost update:** optimistic locking (version column) or pessimistic locking.
- **Retry storm:** few retries, exponential backoff with jitter, retry transient errors only.
- **Distributed monolith:** shared database and long sync chains. Fix with database per service and async events. ([§27](0-interview-prep.md#27-java-scenario-qa))


**Level 2: more detail**
- **Connection pool:** many pending connections in HikariCP means pool sizing, not a slow query.
- **Lost update:** optimistic locking with a version column. Pessimistic locking with `SELECT ... FOR UPDATE` when conflicts are frequent.
- **Kafka lag with healthy consumers:** check per-record processing time, partition count, hot partitions and rebalances.
- **Idempotency key:** the server stores the key with the result, in the same transaction as the write.

## 28. WFS / ADP architect
- **Core themes:** multi-tenant SaaS, policy-driven calculation per assignment, governed integrations.
- **Policy engine:** rules as versioned, effective-dated data. Same input and version always give the same result.
- **Payroll exports:** staging, validation, control totals, quarantine, idempotent batch IDs. ([§28](0-interview-prep.md#28-wfs-senior-solution-architect-adp-qa))


**Level 2: more detail**
- **Tenant isolation:** shared schema with row-level security for most tenants. Dedicated schema or database for the largest or regulated ones.
- **Policy engine:** versioned, effective-dated rules. Each result stores the policy version used.
- **Balances:** an append-only ledger, with an idempotency key on each entry.
- **Time zones:** define the business day in the employee's local zone. It's an architecture concern.

## 29. OAuth 2.0 and JWT
- **OAuth:** permission, not login. The client gets a scoped, short-lived access token.
- **JWT:** header (key ID), payload (issuer, audience, expiry, scope), signature (Okta's private key).
- **API check:** verify the signature with the public key, then issuer, audience, expiry, scope. 401 means untrusted, 403 means not allowed. ([§29](0-interview-prep.md#29-oauth-20-and-jwt-service-to-api-story))

## 30. Spark Structured Streaming
- Treat the stream as a table that keeps growing. Same query as batch, run in micro-batches.
- Checkpoint for restart, watermark for late data, output mode for what to write. ([§30](0-interview-prep.md#30-spark-structured-streaming-simple-explanation))


**Level 2: more detail**
- **Example:** three micro-batches of sector events. Complete output mode rewrites the full count each time, so USPF goes 2 then 3, and CORP goes 1 then 3.
- **Late data:** a watermark tells Spark how long to wait before closing a window.
- **Exactly-once:** checkpoint plus idempotent sink.

## 31. System design notes
- Estimation, load balancing, caching, partitioning, replication, ACID, SQL vs NoSQL, CAP, PACELC, consistent hashing, long polling vs WebSockets vs SSE, Bloom filters. ([§31](0-interview-prep.md#31-system-design-notes))

## 32. Final revision notes
- Kafka delivery modes: at-most-once (commit first, may lose), at-least-once (process first, may duplicate, so consumers must be idempotent), exactly-once (transactional, Kafka only).
- Consumer groups subscribe to topics; partitions are assigned to consumers. ([§32](0-interview-prep.md#32-final-revision-notes-23-sep-2026))

---


**Level 2: more detail**
- **Consumer group rule:** a group subscribes to topics. Consumers in the group are assigned partitions. One partition is read by one consumer per group.
- **Kafka trade-offs:** eventual consistency, ordering per partition only, more partitions add overhead, exactly-once doesn't cover external databases.
- **Idempotent producer:** stops producer retries from duplicating records, but not consumer side effects. Consumers still need checks.

## Final checklist before you walk in
- Can you explain the DCP architecture in 60 seconds?
- Can you name one incident, its cause, and the fix?
- Do you know the three NFR numbers and how each was met?
- Do you have one honest gap and a ramp-up plan?
- Are your questions for the interviewer ready?
