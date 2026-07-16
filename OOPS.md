# Object-Oriented Programming Systems (OOPS) - Technology Architect Guide

*For Technology Architect interviews: Focus on design principles, scalability implications, and real-world trade-offs.*

## Table of Contents
- [Encapsulation](#encapsulation)
- [Inheritance](#inheritance)
- [Polymorphism](#polymorphism)
- [Abstraction](#abstraction)
- [SOLID Principles](#solid-principles)
  - [Single Responsibility Principle (SRP)](#srp)
  - [Open/Closed Principle (OCP)](#ocp)
  - [Liskov Substitution Principle (LSP)](#lsp)
  - [Interface Segregation Principle (ISP)](#isp)
  - [Dependency Inversion Principle (DIP)](#dip)
- [Design Patterns](#design-patterns)
- [Common Interview Questions](#common-interview-questions)

---

## Encapsulation {#encapsulation}

**Simple Definition:** Bundle data and methods together, hide internal details.

**Realistic Architect View:** Encapsulation is about controlling the contract your component exposes to others.

### Why It Matters at Scale
- **API Stability:** Change internals without breaking 100+ dependent services
- **Security Boundary:** Prevent direct field access that could corrupt state
- **Predictability:** Callers don't depend on implementation details

### Example 1: Database Connection Wrapper

```java
// ✅ Good encapsulation
public class DatabaseConnection {
    // Hidden: internal connection pooling, retry logic, metrics
    private HikariDataSource connectionPool;
    private RetryPolicy retryPolicy = new ExponentialBackoffRetry();
    private MetricsCollector metrics;
    
    // Exposed: clean, simple contract
    public Result executeQuery(String sql, Object... params) throws SQLException {
        // Retry logic, pooling, metrics collection - ALL HIDDEN
        return retryPolicy.execute(() -> {
            try (Connection conn = connectionPool.getConnection()) {
                metrics.recordQueryStart(sql);
                return executeWithConnection(conn, sql, params);
            } finally {
                metrics.recordQueryEnd(sql);
            }
        });
    }
    
    // Private helper - hidden implementation detail
    private Result executeWithConnection(Connection conn, String sql, Object[] params) {
        // Query execution logic
    }
}

// Caller: knows nothing about pooling, retries, or metrics
DatabaseConnection db = new DatabaseConnection();
Result result = db.executeQuery("SELECT * FROM users WHERE id = ?", 123);
```

**Why this matters:**
- Tomorrow you switch from HikariCP to Druid → no caller changes needed
- You add automatic retry logic → transparent to all services
- Metrics collection → zero impact on calling code

---

### Example 2: HTTP Client Wrapper (Multi-Region)

```java
// ❌ Bad: Exposes implementation details
public class HttpClient {
    public HttpResponse send(HttpRequest request) {
        try {
            return httpClient.send(request, HttpResponse.BodyHandlers.ofString());
        } catch (IOException e) {
            throw e;  // Caller must handle IOException - implementation detail
        } catch (InterruptedException e) {
            throw e;  // Implementation detail leaks
        }
    }
}

// ✅ Good: Encapsulates resilience strategy
public class ResilientHttpClient {
    private HttpClient httpClient;
    private RetryPolicy retryPolicy;
    private CircuitBreaker circuitBreaker;
    private LoadBalancer regionBalancer;
    
    public Response send(Request request) throws ServiceException {
        // Hidden: multi-region failover, circuit breaking, retries
        try {
            return circuitBreaker.execute(() -> 
                retryPolicy.executeWithFallback(() ->
                    regionBalancer.send(request)
                )
            );
        } catch (Exception e) {
            throw new ServiceException("Request failed: " + e.getMessage(), e);
        }
    }
}

// Caller: simple, predictable
ResilientHttpClient client = new ResilientHttpClient();
Response response = client.send(request);  // Failover, retries, circuit breaking all automatic
```

---

### Example 3: Configuration Management

```java
// ❌ Bad: Public fields, callers read direct config
public class AppConfig {
    public String DATABASE_HOST = "localhost";
    public int DATABASE_PORT = 5432;
    public String API_KEY = System.getenv("API_KEY");
    
    // If API_KEY is empty, caller finds out at runtime
}

// ✅ Good: Validated, encapsulated config
public class ConfigService {
    private final String databaseHost;
    private final int databasePort;
    private final String apiKey;
    private final boolean isProduction;
    
    public ConfigService() {
        // Validation happens here, once, at startup
        this.databaseHost = getAndValidate("DATABASE_HOST", "localhost");
        this.databasePort = Integer.parseInt(getAndValidate("DATABASE_PORT", "5432"));
        this.apiKey = getAndValidateRequired("API_KEY");  // Throws if missing
        this.isProduction = "prod".equals(System.getenv("ENVIRONMENT"));
    }
    
    public DatabaseConfig getDatabaseConfig() {
        // Returns immutable config object
        return new DatabaseConfig(databaseHost, databasePort);
    }
    
    public String getApiKey() {
        if (!isProduction) {
            throw new IllegalStateException("API Key not available in dev environment");
        }
        return apiKey;
    }
    
    private String getAndValidate(String key, String defaultValue) {
        String value = System.getenv(key);
        return value != null ? value : defaultValue;
    }
    
    private String getAndValidateRequired(String key) {
        String value = System.getenv(key);
        if (value == null || value.isEmpty()) {
            throw new IllegalStateException("Required config missing: " + key);
        }
        return value;
    }
}

// Caller: gets safe, validated config
ConfigService config = new ConfigService();  // Fails fast if config is invalid
DatabaseConfig dbConfig = config.getDatabaseConfig();  // Immutable, safe
```

### Trade-offs
- **Pro:** Easier to maintain (change internals), better security (validate once), refactoring safety
- **Con:** More boilerplate (getters/setters), potential performance overhead if not cached properly

**Architect Insight:** Encapsulation is the foundation for microservice contracts. When you expose a clean API, you can change implementation across 50 services without coordination.

---

## Inheritance {#inheritance}

**Simple Definition:** Derive new classes from existing ones, reuse and extend behavior.

**Realistic Architect View:** Inheritance can be powerful or problematic depending on hierarchy depth and design.

### When to Use (The Right Way)
- **Clear IS-A relationship:** A `Manager` IS-A `Employee` (real concept, not just code reuse)
- **Shallow hierarchies:** 2-3 levels deep is ideal; avoid deep chains
- **Shared implementation:** Common methods actually used by subclasses

### When NOT to Use (The Red Flag)
- Deep inheritance chains (5+ levels) → Hard to reason about, high maintenance cost
- Using inheritance just for code reuse → Use composition instead
- Mixing unrelated concepts → Leads to bloated base classes

### Example 1: Payment Processors (Correct Shallow Hierarchy)

```java
// ✅ Good: Clear IS-A, shallow (1 level)
public interface PaymentProcessor {
    PaymentResult process(Payment payment) throws PaymentException;
    boolean supports(PaymentMethod method);
}

public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment p) throws PaymentException {
        // Validate card, call Stripe API, handle fraud detection
        return stripe.charge(p.getCard(), p.getAmount());
    }
    
    @Override
    public boolean supports(PaymentMethod method) {
        return method == PaymentMethod.CREDIT_CARD;
    }
}

public class PayPalProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment p) throws PaymentException {
        // PayPal OAuth flow, charge via PayPal API
        return paypal.chargeAccount(p.getPayPalEmail(), p.getAmount());
    }
    
    @Override
    public boolean supports(PaymentMethod method) {
        return method == PaymentMethod.PAYPAL;
    }
}

// Caller doesn't care which processor, just uses the interface
PaymentProcessor processor = processorFactory.getProcessor(payment.getMethod());
PaymentResult result = processor.process(payment);
```

---

### Example 2: Document Processing (Hierarchy Depth Problem)

```java
// ❌ Bad: Deep, fragile inheritance (4+ levels)
public class Document { 
    public void save() { } 
}

public class Report extends Document {  // Level 2
    public void generateReport() { }
}

public class FinancialReport extends Report {  // Level 3
    public void calculateTotals() { }
}

public class QuarterlyFinancialReport extends FinancialReport {  // Level 4
    public void generateQuarterlyReport() { }
}

public class AnnualQuarterlyFinancialReport extends QuarterlyFinancialReport {  // Level 5 - NIGHTMARE
    // What is this even supposed to do?
    // Bug in Document.save()? All 5 classes break
    // Need to override calculateTotals()? Which level to do it at?
}

// ✅ Good: Flat, composition-based design
public class Document {
    private DocumentMetadata metadata;
    private ReportGenerator reportGenerator;
    private DataStore dataStore;
    
    public void save() {
        dataStore.persist(this);
    }
}

public class FinancialReport {
    private Document document;
    private FinancialCalculator calculator;
    private ReportTemplate template;
    
    public void generate() {
        FinancialData data = calculator.compute();
        document.setContent(template.render(data));
        document.save();
    }
}

public class QuarterlyReport {
    private FinancialReport financialReport;
    private QuarterlyAggregator aggregator;
    
    public void generate() {
        AggregatedData quarterly = aggregator.aggregateByQuarter();
        financialReport.generate();
    }
}

// Much clearer: each class has one responsibility
// Easy to test, modify, extend
```

---

### Example 3: Cache Implementations (When Inheritance Works)

```java
// ✅ Good: Inheritance when strategy is similar
public abstract class BaseCache<K, V> implements Cache<K, V> {
    protected Map<K, CacheEntry<V>> store;
    protected CacheEvictionPolicy evictionPolicy;
    
    @Override
    public void put(K key, V value) {
        store.put(key, new CacheEntry<>(value, System.currentTimeMillis()));
        evictionPolicy.markAccess(key);
    }
    
    @Override
    public V get(K key) {
        CacheEntry<V> entry = store.get(key);
        if (entry == null || isExpired(entry)) {
            return null;
        }
        evictionPolicy.markAccess(key);
        return entry.getValue();
    }
    
    protected abstract boolean isExpired(CacheEntry<V> entry);
}

public class LRUCache<K, V> extends BaseCache<K, V> {
    public LRUCache(int maxSize) {
        this.store = new LinkedHashMap<K, CacheEntry<V>>(maxSize, 0.75f, true) {
            protected boolean removeEldestEntry(Map.Entry eldest) {
                return size() > maxSize;
            }
        };
        this.evictionPolicy = new LRUEvictionPolicy(maxSize);
    }
    
    @Override
    protected boolean isExpired(CacheEntry<V> entry) {
        return System.currentTimeMillis() - entry.getCreatedAt() > TTL_MS;
    }
}

public class LFUCache<K, V> extends BaseCache<K, V> {
    private Map<K, Integer> frequencyMap = new HashMap<>();
    
    @Override
    public V get(K key) {
        V value = super.get(key);
        if (value != null) {
            frequencyMap.put(key, frequencyMap.getOrDefault(key, 0) + 1);
        }
        return value;
    }
    
    @Override
    protected boolean isExpired(CacheEntry<V> entry) {
        return System.currentTimeMillis() - entry.getCreatedAt() > TTL_MS;
    }
}

// Clear IS-A relationship: both are caches with similar behavior
```

### Trade-offs
- **Pro:** Code reuse, natural modeling for certain hierarchies
- **Con:** Fragile base class problem, tight coupling, deep hierarchies are hard to maintain

---

## Polymorphism {#polymorphism}

**Simple Definition:** Same method name, different implementations. Objects behave differently based on type.

**Realistic Architect View:** Polymorphism enables flexibility and testability. Critical for building loosely coupled systems.

### Types

#### 1. Compile-time (Method Overloading)
```java
public class Calculator {
    public int add(int a, int b) { return a + b; }
    public double add(double a, double b) { return a + b; }
}
```
- Resolved at compile time
- Less powerful than runtime polymorphism

#### 2. Runtime (Method Overriding)

```java
public interface DataStore {
    Data read(String key);
    void write(String key, Data data);
}

public class RedisDataStore implements DataStore {
    @Override
    public Data read(String key) { 
        return redis.get(key);  // ~1ms, in-memory
    }
    
    @Override
    public void write(String key, Data data) { 
        redis.set(key, data);  // ~1ms, fast
    }
}

public class DatabaseDataStore implements DataStore {
    @Override
    public Data read(String key) { 
        return db.query("SELECT * FROM data WHERE key = ?", key);  // ~10ms, persistent
    }
    
    @Override
    public void write(String key, Data data) { 
        db.execute("INSERT INTO data VALUES (?, ?)", key, data);  // ~10ms, durable
    }
}

// Caller code: doesn't know which implementation
public class UserService {
    private DataStore dataStore;  // Injected - could be any implementation
    
    public User getUser(String userId) {
        return dataStore.read("user:" + userId);
    }
    
    public void saveUser(String userId, User user) {
        dataStore.write("user:" + userId, user);
    }
}

// Swap at deployment time
UserService service = new UserService(new RedisDataStore());    // For fast reads
// or
UserService service = new UserService(new DatabaseDataStore()); // For persistence
// Caller code doesn't change
```

---

#### 3. Serialization Strategy (Multiple Implementations)

```java
public interface DataSerializer {
    String serialize(Object obj);
    Object deserialize(String data, Class<?> clazz);
}

public class JsonSerializer implements DataSerializer {
    private ObjectMapper mapper = new ObjectMapper();
    
    @Override
    public String serialize(Object obj) {
        return mapper.writeValueAsString(obj);  // Fast, human-readable
    }
    
    @Override
    public Object deserialize(String data, Class<?> clazz) {
        return mapper.readValue(data, clazz);
    }
}

public class ProtobufSerializer implements DataSerializer {
    @Override
    public String serialize(Object obj) {
        return Base64.encode(ProtoConverter.toProto(obj).toByteArray());  // Compact, fast
    }
    
    @Override
    public Object deserialize(String data, Class<?> clazz) {
        return ProtoConverter.fromProto(Base64.decode(data), clazz);
    }
}

public class MessageQueue {
    private DataSerializer serializer;
    
    public void publish(String topic, Object message) {
        String serialized = serializer.serialize(message);
        kafka.send(topic, serialized);
    }
    
    public Object consume(String topic, Class<?> clazz) {
        String data = kafka.receive(topic);
        return serializer.deserialize(data, clazz);
    }
}

// Switch serialization format without touching MessageQueue
MessageQueue queue = new MessageQueue(new JsonSerializer());     // Development
// or
MessageQueue queue = new MessageQueue(new ProtobufSerializer()); // Production (40% smaller messages)
```

### Why It Matters at Scale
- **Loose Coupling:** Services depend on interfaces, not concrete implementations
- **Testability:** Easy to mock implementations for testing
- **Extensibility:** Add new implementations without changing calling code
- **Swappability:** Replace Redis with Memcached without touching 50 services

### Trade-offs
- **Pro:** Flexibility, testability, enables dependency injection
- **Con:** Runtime overhead (method lookup), can hide complexity

---

## Abstraction {#abstraction}

**Simple Definition:** Hide complexity behind a simple interface.

**Realistic Architect View:** Abstraction is about exposing the right level of detail to callers.

### Example 1: Order Processing (Workflow Abstraction)

```java
// ❌ Bad: Exposes internal complexity - caller must know all steps
public class OrderService {
    public void createOrder(OrderDTO dto) {
        validateOrder(dto);                 // Validation
        checkInventory(dto.items);          // Inventory check
        deductFromWarehouse(dto.items);     // Warehouse update
        processPayment(dto);                // Payment processing
        publishToKafka(dto);                // Event publishing
        updateCache(dto.orderId);           // Cache invalidation
        logToAnalytics(dto);                // Analytics
        // Adding a new step? Every caller code breaks
    }
}

// ✅ Good: Complex workflow hidden behind simple interface
public class OrderService {
    private OrderWorkflow workflow;  // Encapsulates all complexity
    
    public OrderResult createOrder(OrderDTO dto) {
        return workflow.process(dto);  // That's it!
    }
}

public class OrderWorkflow {
    private OrderValidator validator;
    private InventoryService inventory;
    private PaymentProcessor payment;
    private EventPublisher eventPublisher;
    private CacheService cache;
    private AnalyticsService analytics;
    
    public OrderResult process(OrderDTO dto) {
        // All complexity hidden here
        validator.validate(dto);
        inventory.deduct(dto.items);
        PaymentResult paymentResult = payment.process(dto.payment);
        
        if (!paymentResult.isSuccess()) {
            inventory.refund(dto.items);  // Rollback on payment failure
            return OrderResult.failure("Payment failed");
        }
        
        eventPublisher.publish("order.created", dto);
        cache.invalidate("orders:" + dto.orderId);
        analytics.track("order_created", dto);
        
        return OrderResult.success(dto.orderId);
    }
}

// Caller: simple, clean
OrderResult result = orderService.createOrder(orderDTO);
// Tomorrow add fraud detection? Modify OrderWorkflow, not 50 caller sites
```

---

### Example 2: Search Abstraction (Hide Engine Details)

```java
// ❌ Bad: Exposes search engine internals
public class UserSearchService {
    public List<User> search(String query) {
        // Caller must know about Elasticsearch internals
        SearchRequest request = new SearchRequest("users");
        SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();
        sourceBuilder.query(QueryBuilders.matchQuery("name", query));
        sourceBuilder.from(0);
        sourceBuilder.size(100);
        sourceBuilder.timeout(new TimeValue(60, TimeUnit.SECONDS));
        request.source(sourceBuilder);
        
        SearchResponse response = client.search(request, RequestOptions.DEFAULT);
        return parseResponse(response);
    }
}

// ✅ Good: Search implementation hidden
public interface SearchEngine {
    List<User> search(String query, SearchOptions options);
}

public class ElasticSearchEngine implements SearchEngine {
    private RestHighLevelClient client;
    
    @Override
    public List<User> search(String query, SearchOptions options) {
        // Elasticsearch details: scoring, aggregations, timeouts - ALL HIDDEN
        SearchRequest request = buildRequest(query, options);
        SearchResponse response = client.search(request, RequestOptions.DEFAULT);
        return parseResponse(response);
    }
}

public class SolrSearchEngine implements SearchEngine {
    private SolrClient client;
    
    @Override
    public List<User> search(String query, SearchOptions options) {
        // Solr-specific implementation
        return client.search(query, options);
    }
}

// Caller: knows nothing about Elasticsearch or Solr
public class UserService {
    private SearchEngine searchEngine;
    
    public List<User> findByName(String name) {
        return searchEngine.search(name, new SearchOptions(0, 100));
    }
}

// Change from Elasticsearch to OpenSearch? Just swap implementations
```

---

### Example 3: File System Abstraction

```java
// ❌ Bad: Code tied to local file system
public class DocumentService {
    public void save(Document doc) throws IOException {
        Path path = Paths.get("/data/documents/" + doc.getId() + ".txt");
        Files.write(path, doc.getContent().getBytes());
    }
    
    public Document load(String docId) throws IOException {
        Path path = Paths.get("/data/documents/" + docId + ".txt");
        String content = new String(Files.readAllBytes(path));
        return new Document(docId, content);
    }
}

// ✅ Good: Abstract file storage
public interface FileStore {
    void write(String path, byte[] content);
    byte[] read(String path);
}

public class LocalFileStore implements FileStore {
    @Override
    public void write(String path, byte[] content) {
        Files.write(Paths.get("/data/" + path), content);
    }
    
    @Override
    public byte[] read(String path) {
        return Files.readAllBytes(Paths.get("/data/" + path));
    }
}

public class S3FileStore implements FileStore {
    private AmazonS3 s3Client;
    
    @Override
    public void write(String path, byte[] content) {
        s3Client.putObject(BUCKET, path, new ByteArrayInputStream(content), null);
    }
    
    @Override
    public byte[] read(String path) {
        S3Object obj = s3Client.getObject(BUCKET, path);
        return obj.getObjectContent().readAllBytes();
    }
}

// DocumentService: clean, storage-agnostic
public class DocumentService {
    private FileStore fileStore;
    
    public void save(Document doc) {
        fileStore.write("documents/" + doc.getId(), doc.getContent().getBytes());
    }
    
    public Document load(String docId) {
        byte[] content = fileStore.read("documents/" + docId);
        return new Document(docId, new String(content));
    }
}

// Production: use S3
DocumentService service = new DocumentService(new S3FileStore());
// Development: use local files
DocumentService service = new DocumentService(new LocalFileStore());
```

### At Architect Level
- **Data Models:** Expose domain concepts, not database schemas
- **APIs:** Hide distributed system complexity (retries, timeouts, fallbacks)
- **Configuration:** Hide infrastructure details from business logic

---

## SOLID Principles {#solid-principles}

### Single Responsibility Principle (SRP) {#srp}

**Definition:** A class should have only one reason to change.

**Realistic View:** If you're struggling to name a class or writing comments like "This also handles...", it's violating SRP.

#### Example 1: User Management (Multiple Responsibilities)

```java
// ❌ Bad: Too many reasons to change (validation + persistence + notifications + auditing)
public class UserManager {
    public boolean validateUser(User u) {
        // Email format, password strength, age verification
        return u.getEmail().matches(EMAIL_REGEX) && 
               u.getPassword().length() >= 12 &&
               u.getAge() >= 18;
    }
    
    public void saveUser(User u) throws SQLException {
        // Database logic
        db.execute("INSERT INTO users VALUES (?, ?, ?)", u.getId(), u.getEmail(), u.getPassword());
    }
    
    public void notifyUserCreated(User u) {
        // Email notification
        emailService.send(u.getEmail(), "Welcome!");
    }
    
    public void auditUserCreation(User u) {
        // Audit logging
        auditLog.write("USER_CREATED", u.getId(), System.currentTimeMillis());
    }
}

// Reasons to change:
// 1. Change validation rules → modify validateUser()
// 2. Switch database → modify saveUser()
// 3. Change notification logic → modify notifyUserCreated()
// 4. Change audit format → modify auditUserCreation()
// = 4 reasons! This violates SRP

// ✅ Good: Each class has ONE reason to change
public class UserValidator {
    public ValidationResult validate(User u) {
        List<String> errors = new ArrayList<>();
        
        if (!isValidEmail(u.getEmail())) {
            errors.add("Invalid email format");
        }
        if (!isStrongPassword(u.getPassword())) {
            errors.add("Password too weak");
        }
        if (u.getAge() < 18) {
            errors.add("User must be 18+");
        }
        
        return new ValidationResult(errors);
    }
    
    private boolean isValidEmail(String email) { /* ... */ }
    private boolean isStrongPassword(String password) { /* ... */ }
}
// Reason to change: Validation rules change

public class UserRepository {
    private DataSource dataSource;
    
    public void save(User u) throws SQLException {
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(
                "INSERT INTO users (id, email, password) VALUES (?, ?, ?)"
            );
            stmt.setString(1, u.getId());
            stmt.setString(2, u.getEmail());
            stmt.setString(3, hashPassword(u.getPassword()));
            stmt.executeUpdate();
        }
    }
}
// Reason to change: Database schema changes

public class UserNotificationService {
    private EmailService emailService;
    
    public void notifyUserCreated(User u) {
        Email email = new Email()
            .to(u.getEmail())
            .subject("Welcome to our service!")
            .body(buildWelcomeMessage(u));
        emailService.send(email);
    }
}
// Reason to change: Notification strategy changes

public class UserAuditLogger {
    private AuditLog auditLog;
    
    public void logUserCreation(User u) {
        AuditEvent event = new AuditEvent()
            .setEventType("USER_CREATED")
            .setUserId(u.getId())
            .setTimestamp(System.currentTimeMillis())
            .setMetadata(Map.of("email", u.getEmail()));
        auditLog.write(event);
    }
}
// Reason to change: Audit requirements change

// Orchestrator: brings everything together
public class UserRegistrationService {
    private UserValidator validator;
    private UserRepository repository;
    private UserNotificationService notifier;
    private UserAuditLogger auditLogger;
    
    public void registerUser(User u) throws RegistrationException {
        // Step 1: Validate
        ValidationResult validation = validator.validate(u);
        if (!validation.isValid()) {
            throw new RegistrationException(validation.getErrors());
        }
        
        // Step 2: Save
        repository.save(u);
        
        // Step 3: Notify
        notifier.notifyUserCreated(u);
        
        // Step 4: Audit
        auditLogger.logUserCreation(u);
    }
}
```

**Key Insight:** UserRegistrationService coordinates, but doesn't do the work. Each specialist class has ONE job.

---

#### Example 2: Order Processing (Complex Domain)

```java
// ❌ Bad: OrderService does everything (30+ methods)
public class OrderService {
    // Validation logic
    public boolean validateOrder(Order order) { /* ... */ }
    
    // Payment processing
    public boolean processPayment(Order order) { /* ... */ }
    
    // Inventory management
    public void deductInventory(Order order) { /* ... */ }
    
    // Shipping coordination
    public void arrangeShipping(Order order) { /* ... */ }
    
    // Email notifications
    public void sendConfirmation(Order order) { /* ... */ }
    
    // Database persistence
    public void saveOrder(Order order) { /* ... */ }
    
    // Reporting/analytics
    public void recordSale(Order order) { /* ... */ }
}

// ✅ Good: Each responsibility is a separate class
public class OrderValidator {
    public ValidationResult validate(Order order) { /* ... */ }
}

public class PaymentProcessor {
    public PaymentResult process(Order order) { /* ... */ }
}

public class InventoryService {
    public void deduct(Order order) { /* ... */ }
    public void refund(Order order) { /* ... */ }
}

public class ShippingService {
    public ShipmentId arrangeShipping(Order order) { /* ... */ }
}

public class OrderNotificationService {
    public void sendConfirmation(Order order) { /* ... */ }
    public void sendShipmentUpdate(Order order) { /* ... */ }
}

public class OrderRepository {
    public void save(Order order) { /* ... */ }
}

public class OrderAnalytics {
    public void recordSale(Order order) { /* ... */ }
}

// Orchestration: brings it all together
public class OrderWorkflow {
    private OrderValidator validator;
    private PaymentProcessor payment;
    private InventoryService inventory;
    private ShippingService shipping;
    private OrderNotificationService notifier;
    private OrderRepository repository;
    private OrderAnalytics analytics;
    
    public OrderResult process(Order order) {
        // Validate
        if (!validator.validate(order).isValid()) {
            return OrderResult.failure("Validation failed");
        }
        
        // Process payment
        PaymentResult paymentResult = payment.process(order);
        if (!paymentResult.isSuccess()) {
            return OrderResult.failure("Payment failed");
        }
        
        // Deduct inventory
        inventory.deduct(order);
        
        // Arrange shipping
        ShipmentId shipmentId = shipping.arrangeShipping(order);
        
        // Save & notify
        repository.save(order);
        notifier.sendConfirmation(order);
        analytics.recordSale(order);
        
        return OrderResult.success(shipmentId);
    }
}
```

**Architect Perspective:** SRP at scale means each microservice has one domain responsibility. OrderService, PaymentService, InventoryService, ShippingService are separate services in a microservice architecture.

---

### Open/Closed Principle (OCP) {#ocp}

**Definition:** Open for extension, closed for modification. Add new behavior without changing existing code.

#### Example 1: Payment Processing (Classic OCP)

```java
// ❌ Bad: Every new payment type requires modifying PaymentService
public class PaymentService {
    public PaymentResult process(Payment p) {
        if (p.getType().equals("CREDIT_CARD")) {
            return processCreditCard(p);
        } else if (p.getType().equals("PAYPAL")) {
            return processPayPal(p);
        } else if (p.getType().equals("APPLE_PAY")) {
            return processApplePay(p);
        } else if (p.getType().equals("GOOGLE_PAY")) {
            return processGooglePay(p);
        }
        // Add Square? Bank transfer? Modify this method AGAIN
        // 50 services depend on this - risky to change
        throw new UnsupportedOperationException("Unknown payment type: " + p.getType());
    }
    
    private PaymentResult processCreditCard(Payment p) { /* ... */ }
    private PaymentResult processPayPal(Payment p) { /* ... */ }
    private PaymentResult processApplePay(Payment p) { /* ... */ }
    private PaymentResult processGooglePay(Payment p) { /* ... */ }
}

// ✅ Good: Extend with new implementations, don't modify existing code
public interface PaymentProcessor {
    boolean supports(PaymentType type);
    PaymentResult process(Payment payment) throws PaymentException;
}

public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public boolean supports(PaymentType type) {
        return type == PaymentType.CREDIT_CARD;
    }
    
    @Override
    public PaymentResult process(Payment p) throws PaymentException {
        // Stripe integration
        return stripe.charge(p.getCard(), p.getAmount());
    }
}

public class PayPalProcessor implements PaymentProcessor {
    @Override
    public boolean supports(PaymentType type) {
        return type == PaymentType.PAYPAL;
    }
    
    @Override
    public PaymentResult process(Payment p) throws PaymentException {
        // PayPal OAuth + charge
        return paypal.chargeAccount(p.getEmail(), p.getAmount());
    }
}

public class ApplePayProcessor implements PaymentProcessor {
    @Override
    public boolean supports(PaymentType type) {
        return type == PaymentType.APPLE_PAY;
    }
    
    @Override
    public PaymentResult process(Payment p) throws PaymentException {
        // Apple Pay token validation + charge
        return applePayService.processToken(p.getToken(), p.getAmount());
    }
}

// Add Square? Just add a new class - don't modify existing code!
public class SquareProcessor implements PaymentProcessor {
    @Override
    public boolean supports(PaymentType type) {
        return type == PaymentType.SQUARE;
    }
    
    @Override
    public PaymentResult process(Payment p) throws PaymentException {
        return square.charge(p.getSourceId(), p.getAmount());
    }
}

// Factory finds the right processor
public class PaymentProcessorFactory {
    private List<PaymentProcessor> processors;
    
    public PaymentProcessor getProcessor(PaymentType type) {
        return processors.stream()
            .filter(p -> p.supports(type))
            .findFirst()
            .orElseThrow(() -> new PaymentException("No processor for: " + type));
    }
}

// Service doesn't change when new payment types are added
public class PaymentService {
    private PaymentProcessorFactory factory;
    
    public PaymentResult process(Payment payment) throws PaymentException {
        PaymentProcessor processor = factory.getProcessor(payment.getType());
        return processor.process(payment);
    }
}
```

---

#### Example 2: Discount Calculation (Multiple Strategies)

```java
// ❌ Bad: Every discount type requires modifying OrderService
public class OrderService {
    public double calculateTotal(Order order) {
        double subtotal = order.getSubtotal();
        double discount = 0;
        
        if (order.hasStudentDiscount()) {
            discount = subtotal * 0.15;  // 15% off
        } else if (order.hasBlackFridayDiscount()) {
            discount = subtotal * 0.30;  // 30% off
        } else if (order.hasReferralDiscount()) {
            discount = Math.min(50, subtotal * 0.20);  // Up to $50 off
        } else if (order.hasSeasonalDiscount()) {
            // Complex seasonal logic...
        }
        // Add loyalty program discount? Modify again!
        
        return subtotal - discount;
    }
}

// ✅ Good: Each discount strategy is a separate class
public interface DiscountStrategy {
    double calculateDiscount(Order order);
}

public class StudentDiscount implements DiscountStrategy {
    @Override
    public double calculateDiscount(Order order) {
        return order.getSubtotal() * 0.15;  // 15% off
    }
}

public class BlackFridayDiscount implements DiscountStrategy {
    @Override
    public double calculateDiscount(Order order) {
        return order.getSubtotal() * 0.30;  // 30% off
    }
}

public class ReferralDiscount implements DiscountStrategy {
    @Override
    public double calculateDiscount(Order order) {
        return Math.min(50, order.getSubtotal() * 0.20);
    }
}

public class LoyaltyDiscount implements DiscountStrategy {
    private LoyaltyService loyaltyService;
    
    @Override
    public double calculateDiscount(Order order) {
        int points = loyaltyService.getPoints(order.getCustomerId());
        return points / 100.0;  // 1 point = 1 cent
    }
}

// Add seasonal discount? Just implement DiscountStrategy!
public class SeasonalDiscount implements DiscountStrategy {
    @Override
    public double calculateDiscount(Order order) {
        // Complex seasonal logic
    }
}

// OrderService never changes
public class OrderService {
    private DiscountStrategy discountStrategy;
    
    public double calculateTotal(Order order) {
        double subtotal = order.getSubtotal();
        double discount = discountStrategy.calculateDiscount(order);
        return subtotal - discount;
    }
}
```

**Key:** Use composition + strategy pattern to enable extension without modification.

---

### Liskov Substitution Principle (LSP) {#lsp}

**Definition:** Derived classes must be substitutable for their base classes. Subclass behavior must match parent's contract.

**The Rule:** If `S` is a subtype of `T`, then objects of type `S` may be substituted for objects of type `T` without breaking the program.

---

#### Example 1: The Classic Rectangle-Square Problem

```java
// ❌ Bad: Square violates LSP
public class Rectangle {
    protected int width, height;
    
    public void setWidth(int w) { this.width = w; }
    public void setHeight(int h) { this.height = h; }
    public int area() { return width * height; }
}

public class Square extends Rectangle {
    @Override
    public void setWidth(int w) { 
        this.width = w; 
        this.height = w;  // VIOLATION: Caller expects independent width/height
    }
    @Override
    public void setHeight(int h) { 
        this.width = h;   // This breaks the contract
        this.height = h;
    }
}

// This breaks:
Rectangle r = new Square();
r.setWidth(5);
r.setHeight(10);
System.out.println(r.area()); // Expected 50, got 100. Caller is shocked.

// ✅ Good: Use composition, not inheritance
public class Square {
    private int side;
    
    public void setSide(int s) { this.side = s; }
    public int area() { return side * side; }
}
```

---

#### Example 2: Cache Implementations (Real Architect Scenario)

```java
// Contract: Cache stores and retrieves values, may return null if missing
public interface Cache {
    void put(String key, Object value);
    Object get(String key);
}

// ✅ Correct: InMemoryCache follows the contract
public class InMemoryCache implements Cache {
    private Map<String, Object> store = new HashMap<>();
    
    @Override
    public void put(String key, Object value) {
        store.put(key, value);
    }
    
    @Override
    public Object get(String key) {
        return store.get(key);  // Returns null if missing - OK
    }
}

// ✅ Correct: RedisCache follows the contract
public class RedisCache implements Cache {
    private JedisCluster redis;
    
    @Override
    public void put(String key, Object value) {
        redis.set(key, serialize(value));
    }
    
    @Override
    public Object get(String key) {
        String val = redis.get(key);
        return val == null ? null : deserialize(val);
    }
}

// ❌ Wrong: StrictCache violates contract (throws on missing key)
public class StrictCache implements Cache {
    private Map<String, Object> store = new HashMap<>();
    
    @Override
    public void put(String key, Object value) {
        store.put(key, value);
    }
    
    @Override
    public Object get(String key) {
        // VIOLATION: Throws exception instead of returning null
        if (!store.containsKey(key)) {
            throw new CacheKeyNotFoundException("Key not found: " + key);
        }
        return store.get(key);
    }
}

// This breaks code that uses Cache polymorphically:
Cache cache = new StrictCache();
Object user = cache.get("user:123"); // Caller expects null or Object
                                      // But gets exception! Violates contract.

// Usage code that worked with InMemoryCache now crashes:
for (String key : keys) {
    Object val = cache.get(key);
    if (val != null) {  // What if cache throws exception? Code breaks.
        process(val);
    }
}
```

**Key Insight:** Contract includes return values AND exceptions. If base class returns null, subclass can't throw exception.

---

#### Example 3: Data Store Repository (Multi-implementation)

```java
// Contract: query() returns results, may be empty; must handle timeouts
public interface UserRepository {
    List<User> findByAge(int age) throws TimeoutException;
}

// ✅ Correct: Database implementation
public class SqlUserRepository implements UserRepository {
    @Override
    public List<User> findByAge(int age) throws TimeoutException {
        try {
            // DB query with timeout handling
            return executeQueryWithTimeout(age, 5000);
        } catch (SQLException e) {
            throw new TimeoutException("Query exceeded timeout");
        }
    }
}

// ✅ Correct: ElasticSearch implementation
public class ElasticSearchUserRepository implements UserRepository {
    @Override
    public List<User> findByAge(int age) throws TimeoutException {
        // ES query with timeout
        return searchWithTimeout(age, 5000);
    }
}

// ❌ Wrong: In-memory implementation that doesn't handle timeout
public class InMemoryUserRepository implements UserRepository {
    @Override
    public List<User> findByAge(int age) {  // VIOLATION: Doesn't throw TimeoutException
        // No timeout handling - just iterates memory
        return users.stream()
                    .filter(u -> u.getAge() == age)
                    .collect(toList());
    }
}

// Caller code breaks:
UserRepository repo = new InMemoryUserRepository();
try {
    List<User> results = repo.findByAge(25);  // Never throws TimeoutException
    // What if data grows to millions? No protection from hanging.
} catch (TimeoutException e) {
    // This catch block never executes, defeating resilience strategy
}
```

---

#### Example 4: Payment Processing (Preconditions/Postconditions)

```java
public interface PaymentProcessor {
    // Contract: Input must have amount > 0, returns success/failure
    PaymentResult process(Payment payment) throws PaymentException;
    
    // Precondition: balance must be >= amount
    // Postcondition: if success, balance decreases by amount
}

// ✅ Correct: Stripe processor enforces contract
public class StripeProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment payment) throws PaymentException {
        if (payment.getAmount() <= 0) {
            throw new PaymentException("Amount must be positive");  // Enforces precondition
        }
        
        PaymentResult result = stripe.charge(payment);
        
        if (result.isSuccess()) {
            // Postcondition: balance is reduced
            accountService.deductBalance(payment.getAmount());
        }
        return result;
    }
}

// ❌ Wrong: MockPaymentProcessor violates postcondition
public class MockPaymentProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment payment) throws PaymentException {
        // Just returns success without deducting balance!
        // VIOLATION: Postcondition not satisfied
        return PaymentResult.success();
    }
}

// Test code that worked breaks in production:
PaymentProcessor processor = new MockPaymentProcessor();
double balanceBefore = account.getBalance();
processor.process(new Payment(100, account));
// With real processor, balance would be 100 less
// With mock, balance is unchanged - test passes but production fails!
```

---

#### Example 5: Message Queue Publishing (Guarantee violations)

```java
public interface MessageQueue {
    // Contract: Message is guaranteed to be delivered to all subscribers
    void publish(String topic, String message) throws QueueException;
}

// ✅ Correct: Kafka implementation guarantees delivery
public class KafkaQueue implements MessageQueue {
    @Override
    public void publish(String topic, String message) throws QueueException {
        // Kafka: Replicated, persistent, guaranteed delivery
        kafka.send(new ProducerRecord(topic, message));
    }
}

// ✅ Correct: RabbitMQ implementation with persistence
public class RabbitMQQueue implements MessageQueue {
    @Override
    public void publish(String topic, String message) throws QueueException {
        // RabbitMQ with durable queue: guaranteed delivery
        channel.basicPublish(topic, "", MessageProperties.PERSISTENT_TEXT_PLAIN, message.getBytes());
    }
}

// ❌ Wrong: In-memory queue loses messages on crash
public class InMemoryQueue implements MessageQueue {
    private List<String> messages = new ArrayList<>();  // Not persistent!
    
    @Override
    public void publish(String topic, String message) {
        messages.add(message);  // VIOLATION: No delivery guarantee
    }
}

// Caller code fails silently:
MessageQueue queue = new InMemoryQueue();
queue.publish("orders", "user:123 ordered item:456");
// System crashes, message is lost
// With Kafka, message would be replicated and recover
```

---

#### Why LSP Matters at Architect Level

| Scenario | Bad Design | Good Design |
|----------|-----------|------------|
| **Caching Strategy** | Cache impl throws on missing key | All implementations return null consistently |
| **Multi-region Deployment** | Different datastores have different guarantees | All datastores have same SLA/timeout behavior |
| **Microservice Upgrades** | New implementation has different error handling | All versions handle errors identically |
| **Testing** | Mock behaves differently than real impl | Mock follows exact same contract |
| **Scaling** | Different implementations timeout differently | All scale with same timeout guarantees |

**The Golden Rule:** 
- If callers write code that works with `DatabaseRepository`, it must work with `CacheRepository` too
- If one implementation throws exception on timeout, all must
- If one implementation guarantees consistency, all must
- If one caches results, all must (or none should)

---

### Interface Segregation Principle (ISP) {#isp}

**Definition:** Clients shouldn't depend on interfaces they don't use. Split fat interfaces into smaller, focused ones.

**The Problem:** Large interfaces force implementations to provide methods they don't need, creating dead code and confusion.

---

#### Example 1: Robot vs Human (Classic)

```java
// ❌ Bad: Fat interface forces Robot to implement irrelevant methods
public interface Worker {
    void work();
    void eat();
    void sleep();
    void payTaxes();
}

public class Robot implements Worker {
    @Override
    public void work() { /* ok */ }
    
    @Override
    public void eat() { /* throws UnsupportedOperationException! */ }
    
    @Override
    public void sleep() { /* throws UnsupportedOperationException! */ }
    
    @Override
    public void payTaxes() { /* throws UnsupportedOperationException! */ }
}

// Caller code breaks:
Worker w = factory.getWorker("robot");
w.eat();  // Crashes! Robot can't eat

// ✅ Good: Segregated interfaces
public interface Workable {
    void work();
}

public interface Eatable {
    void eat();
}

public interface Sleepable {
    void sleep();
}

public interface TaxPayer {
    void payTaxes();
}

public class Robot implements Workable {
    @Override
    public void work() { /* assembly line logic */ }
}

public class Human implements Workable, Eatable, Sleepable, TaxPayer {
    @Override
    public void work() { /* job logic */ }
    
    @Override
    public void eat() { /* nutrition logic */ }
    
    @Override
    public void sleep() { /* rest logic */ }
    
    @Override
    public void payTaxes() { /* tax logic */ }
}

// Caller code is type-safe:
Workable worker = factory.getWorker();
worker.work();  // Always works, interface only has work()
```

---

#### Example 2: Payment Interface (Real Architect Scenario)

```java
// ❌ Bad: Fat payment interface
public interface PaymentProcessor {
    // Core processing
    PaymentResult process(Payment p);
    
    // Refund
    RefundResult refund(String transactionId);
    
    // Webhooks
    void handleWebhook(WebhookEvent event);
    
    // Reporting
    List<Transaction> getTransactionHistory(String accountId);
    
    // Settlement
    SettlementResult settleAccount(String accountId);
    
    // Reconciliation
    ReconciliationReport reconcile(LocalDate date);
}

// Many processors don't need all these methods!
public class SimplePaymentProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment p) { /* ok */ }
    
    @Override
    public RefundResult refund(String transactionId) { 
        throw new UnsupportedOperationException("This processor doesn't support refunds");
    }
    
    @Override
    public void handleWebhook(WebhookEvent event) {
        // Never called, but must implement
    }
    
    @Override
    public List<Transaction> getTransactionHistory(String accountId) {
        throw new UnsupportedOperationException("No history tracking");
    }
    
    // More empty/exception methods...
}

// ✅ Good: Segregated interfaces
public interface PaymentProcessor {
    PaymentResult process(Payment payment) throws PaymentException;
}

public interface Refundable {
    RefundResult refund(String transactionId) throws PaymentException;
}

public interface WebhookHandler {
    void handleWebhook(WebhookEvent event);
}

public interface TransactionHistory {
    List<Transaction> getHistory(String accountId);
}

public interface SettlementProcessor {
    SettlementResult settle(String accountId) throws SettlementException;
}

public interface Reconcilable {
    ReconciliationReport reconcile(LocalDate date) throws ReconciliationException;
}

// Now implementations only take what they need
public class StripeProcessor implements PaymentProcessor, Refundable, WebhookHandler, TransactionHistory {
    @Override
    public PaymentResult process(Payment payment) { /* stripe charge */ }
    
    @Override
    public RefundResult refund(String transactionId) { /* stripe refund */ }
    
    @Override
    public void handleWebhook(WebhookEvent event) { /* stripe webhook processing */ }
    
    @Override
    public List<Transaction> getHistory(String accountId) { /* stripe transaction history */ }
}

// Simple processor only implements what it needs
public class OfflineProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment payment) { /* manual processing */ }
    
    // No refunds, no webhooks, no history - and that's OK!
}

// Type-safe client code
public class CheckoutService {
    private PaymentProcessor processor;
    
    public PaymentResult checkout(Payment payment) {
        return processor.process(payment);  // Works with any processor
    }
}

public class AdminService {
    private TransactionHistory history;  // Only needs history capability
    
    public List<Transaction> getTransactions(String account) {
        return history.getHistory(account);
    }
}
```

---

#### Example 3: Data Repository (Multiple Capabilities)

```java
// ❌ Bad: Fat repository interface
public interface UserRepository {
    // CRUD
    void save(User user);
    User findById(String id);
    List<User> findAll();
    void delete(String id);
    
    // Search
    List<User> findByName(String name);
    List<User> findByEmail(String email);
    
    // Batch
    void batchSave(List<User> users);
    void batchDelete(List<String> ids);
    
    // Caching
    void clearCache();
    void preloadCache();
    
    // Audit
    List<AuditLog> getAuditLog(String userId);
}

// In-memory implementation shouldn't implement all these
public class InMemoryUserRepository implements UserRepository {
    @Override
    public void save(User user) { /* ok */ }
    
    @Override
    public void clearCache() { 
        // What does "clear cache" even mean for in-memory storage?
        throw new UnsupportedOperationException();
    }
    
    @Override
    public List<AuditLog> getAuditLog(String userId) {
        throw new UnsupportedOperationException("Audit not implemented");
    }
    
    // Many unneeded methods...
}

// ✅ Good: Segregated interfaces
public interface UserRepository {
    void save(User user);
    User findById(String id);
    void delete(String id);
}

public interface UserSearch {
    List<User> findByName(String name);
    List<User> findByEmail(String email);
}

public interface BatchUserOperation {
    void batchSave(List<User> users);
    void batchDelete(List<String> ids);
}

public interface CacheManagement {
    void clearCache();
    void preloadCache();
}

public interface AuditableUserRepository {
    List<AuditLog> getAuditLog(String userId);
}

// In-memory only implements what makes sense
public class InMemoryUserRepository implements UserRepository, UserSearch {
    @Override
    public void save(User user) { /* ok */ }
    
    @Override
    public User findById(String id) { /* ok */ }
    
    @Override
    public void delete(String id) { /* ok */ }
    
    @Override
    public List<User> findByName(String name) { /* ok */ }
    
    @Override
    public List<User> findByEmail(String email) { /* ok */ }
}

// Database implementation with full features
public class SqlUserRepository implements UserRepository, UserSearch, BatchUserOperation, CacheManagement, AuditableUserRepository {
    // All methods implemented
}
```

**Architect View:** ISP is about client respect. Don't force implementations to handle capabilities they don't use. Keep interfaces focused and composable.

---

### Dependency Inversion Principle (DIP) {#dip}

**Definition:** Depend on abstractions, not concrete implementations. High-level modules shouldn't depend on low-level details.

**The Rule:** 
1. High-level modules should not depend on low-level modules; both should depend on abstractions
2. Abstractions should not depend on details; details should depend on abstractions

---

#### Example 1: Payment Processing (Testability)

```java
// ❌ Bad: PaymentService hard-coded to Stripe
public class PaymentService {
    private StripeProcessor stripe = new StripeProcessor();  // Tight coupling!
    
    public PaymentResult pay(Payment p) {
        return stripe.process(p);
    }
}

// Testing this is hard:
@Test
public void testPayment() {
    PaymentService service = new PaymentService();
    // service is hard-wired to Stripe
    // Can't test with mock processor
    // Stripe API calls hit test environment (slow, unreliable)
}

// ✅ Good: Depend on abstraction via dependency injection
public interface PaymentProcessor {
    PaymentResult process(Payment payment) throws PaymentException;
}

public class PaymentService {
    private PaymentProcessor processor;  // Abstract dependency
    
    public PaymentService(PaymentProcessor processor) {
        this.processor = processor;  // Injected at construction time
    }
    
    public PaymentResult pay(Payment p) throws PaymentException {
        return processor.process(p);
    }
}

public class StripeProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(Payment p) throws PaymentException {
        // Call real Stripe API
        return stripe.charge(p.getCard(), p.getAmount());
    }
}

// For testing: mock processor
public class MockPaymentProcessor implements PaymentProcessor {
    private List<Payment> capturedPayments = new ArrayList<>();
    
    @Override
    public PaymentResult process(Payment p) {
        capturedPayments.add(p);
        return PaymentResult.success("mock-txn-123");
    }
    
    public List<Payment> getCapturedPayments() {
        return capturedPayments;
    }
}

// Testing is clean and fast
@Test
public void testPayment() {
    MockPaymentProcessor mock = new MockPaymentProcessor();
    PaymentService service = new PaymentService(mock);
    
    PaymentResult result = service.pay(new Payment(100, card));
    
    assertTrue(result.isSuccess());
    assertEquals(1, mock.getCapturedPayments().size());  // No real API calls!
}

// Production: inject real processor
PaymentService service = new PaymentService(new StripeProcessor());
// Development: inject mock
PaymentService service = new PaymentService(new MockPaymentProcessor());
```

---

#### Example 2: Logger Injection (Decoupling)

```java
// ❌ Bad: UserService tightly coupled to specific logger
public class UserService {
    private ConsoleLogger logger = new ConsoleLogger();  // Hard-wired!
    
    public void registerUser(User user) {
        logger.info("Registering user: " + user.getEmail());  // Goes to console only
        // ...registration logic...
    }
}

// To change logging to file, email, or Datadog, you must modify UserService!
// Modify 50 services? Nightmare.

// ❌ Also bad: Using static logger
public class UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
    
    public void registerUser(User user) {
        logger.info("Registering user: " + user.getEmail());
    }
}
// Still can't swap logger implementations without changing code

// ✅ Good: Depend on Logger abstraction
public interface Logger {
    void info(String message);
    void error(String message, Exception e);
    void debug(String message);
}

public class ConsoleLogger implements Logger {
    @Override
    public void info(String message) {
        System.out.println("[INFO] " + message);
    }
    
    @Override
    public void error(String message, Exception e) {
        System.err.println("[ERROR] " + message);
        e.printStackTrace();
    }
    
    @Override
    public void debug(String message) {
        System.out.println("[DEBUG] " + message);
    }
}

public class FileLogger implements Logger {
    private FileWriter writer;
    
    @Override
    public void info(String message) {
        writer.write("[INFO] " + message + "\n");
    }
    
    @Override
    public void error(String message, Exception e) {
        writer.write("[ERROR] " + message + "\n");
        writer.write(ExceptionUtils.getStackTrace(e));
    }
    
    @Override
    public void debug(String message) {
        writer.write("[DEBUG] " + message + "\n");
    }
}

public class DatadogLogger implements Logger {
    private DatadogClient client;
    
    @Override
    public void info(String message) {
        client.log("info", message, LogLevel.INFO);
    }
    
    @Override
    public void error(String message, Exception e) {
        client.log("error", message, LogLevel.ERROR);
        client.log("stack_trace", ExceptionUtils.getStackTrace(e), LogLevel.ERROR);
    }
    
    @Override
    public void debug(String message) {
        client.log("debug", message, LogLevel.DEBUG);
    }
}

// UserService: depends on abstraction, not concrete logger
public class UserService {
    private Logger logger;  // Abstraction, not concrete class
    
    public UserService(Logger logger) {
        this.logger = logger;  // Injected
    }
    
    public void registerUser(User user) {
        logger.info("Registering user: " + user.getEmail());
        // ...registration logic...
    }
}

// Swap loggers at runtime
UserService service = new UserService(new ConsoleLogger());       // Dev
UserService service = new UserService(new FileLogger());          // Staging
UserService service = new UserService(new DatadogLogger());       // Prod
// No code changes needed!
```

---

#### Example 3: Data Access (Multi-Database Support)

```java
// ❌ Bad: OrderService hard-wired to PostgreSQL
public class OrderService {
    private PostgresConnection postgresConn = new PostgresConnection();  // Tight coupling
    
    public void saveOrder(Order order) {
        postgresConn.insert("orders", order.toMap());
    }
    
    public Order getOrder(String orderId) {
        Map row = postgresConn.query("SELECT * FROM orders WHERE id = ?", orderId);
        return Order.fromMap(row);
    }
}

// Moving to MongoDB? Must rewrite OrderService!

// ✅ Good: Depend on abstraction (Repository pattern)
public interface OrderRepository {
    void save(Order order) throws PersistenceException;
    Order findById(String orderId) throws PersistenceException;
}

public class PostgresOrderRepository implements OrderRepository {
    private DataSource dataSource;
    
    @Override
    public void save(Order order) throws PersistenceException {
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(
                "INSERT INTO orders (id, customer_id, total) VALUES (?, ?, ?)"
            );
            stmt.setString(1, order.getId());
            stmt.setString(2, order.getCustomerId());
            stmt.setDouble(3, order.getTotal());
            stmt.executeUpdate();
        } catch (SQLException e) {
            throw new PersistenceException("Failed to save order", e);
        }
    }
    
    @Override
    public Order findById(String orderId) throws PersistenceException {
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(
                "SELECT * FROM orders WHERE id = ?"
            );
            stmt.setString(1, orderId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return mapRow(rs);
            }
        } catch (SQLException e) {
            throw new PersistenceException("Failed to fetch order", e);
        }
        return null;
    }
}

public class MongoOrderRepository implements OrderRepository {
    private MongoCollection<Document> collection;
    
    @Override
    public void save(Order order) throws PersistenceException {
        Document doc = new Document()
            .append("_id", order.getId())
            .append("customerId", order.getCustomerId())
            .append("total", order.getTotal());
        collection.insertOne(doc);
    }
    
    @Override
    public Order findById(String orderId) throws PersistenceException {
        Document doc = collection.find(new Document("_id", orderId)).first();
        if (doc != null) {
            return mapDocument(doc);
        }
        return null;
    }
}

// OrderService: depends on abstraction
public class OrderService {
    private OrderRepository repository;  // Abstraction, not concrete DB
    
    public OrderService(OrderRepository repository) {
        this.repository = repository;  // Injected
    }
    
    public void createOrder(Order order) throws PersistenceException {
        // ... business logic ...
        repository.save(order);  // Works with any database!
    }
    
    public Order getOrder(String orderId) throws PersistenceException {
        return repository.findById(orderId);
    }
}

// Switch databases without touching OrderService
OrderService service = new OrderService(new PostgresOrderRepository());  // Production
OrderService service = new OrderService(new MongoOrderRepository());     // Migration
```

**Architect Impact:** 
- **Testability:** Inject mocks for unit tests
- **Flexibility:** Swap implementations without code changes
- **Scalability:** Different implementations for different scale scenarios
- **Maintainability:** Changes to implementations don't affect business logic

---

## Design Patterns {#design-patterns}

*Will add patterns as we discuss specific questions. Common ones for architects:*
- Singleton, Factory, Builder, Strategy, Observer, Proxy, Adapter, Decorator

---

## Common Interview Questions {#common-interview-questions}

### Q1: Why use encapsulation when we can make all fields public?

*Add detailed answer based on your questions...*

### Q2: When would you use inheritance vs composition?

*Add detailed answer based on your questions...*

### Q3: How do SOLID principles apply to microservices design?

*Add detailed answer based on your questions...*

### Q4: Design a payment system with multiple processors (Stripe, PayPal, Square). How do you make it extensible?

*Add detailed answer based on your questions...*

---

**Last Updated:** 2026-07-16  
**Status:** In Progress - Questions pending
