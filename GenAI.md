# AI & ML Fundamentals

## **AI (Artificial Intelligence)**
The broadest field — any system that mimics human intelligence. Includes rule-based systems, chatbots, recommendation engines, everything below.

---

## **ML (Machine Learning)**
Subset of AI where systems *learn from data* instead of following hard-coded rules.

### **Three Main Types:**

1. **Supervised Learning** — learn from labeled examples
   - Data: questions + answers (input + correct output)
   - Example: spam detection (emails labeled "spam" or "not spam")
   - Output: predict for new unlabeled data

2. **Unsupervised Learning** — find hidden patterns in unlabeled data
   - Data: just the questions, no answers
   - Example: group customers by behavior (no predefined groups)
   - Output: clusters or relationships

3. **Reinforcement Learning** — learn by trial-and-error with rewards
   - Data: actions that give rewards or penalties
   - Example: chess AI learns by playing games
   - Output: optimal strategy

---

## **Deep Learning**
Subset of ML using **neural networks** (layers of interconnected nodes). Excellent at learning from raw data (images, text, audio).
- Example: image recognition, language translation

---

## **Foundation Model (FM)**
A large neural network pre-trained on *massive amounts of unlabeled data*, then fine-tuned for specific tasks. Often uses **semi-supervised learning** (mix of labeled + unlabeled data).
- Example: BERT, GPT models

---

## **LLM (Large Language Model)**
Foundation Model specialized for **text understanding & generation**.
- Trained on billions of words from the internet
- Can: answer questions, write code, translate, summarize

---

## **GenAI (Generative AI)**
AI that *creates new content* (text, images, code, music).
- Foundation: LLMs + image models + other generative models
- Examples: ChatGPT, DALL-E, Copilot

---

## **Diffusion Models**
A type of **generative model** that creates images, text, or other data by gradually refining random noise into coherent output.

### **How They Work (Simple Analogy):**

**Forward process (noise):** Take a clear image → add noise step-by-step → ends up as pure random noise

**Reverse process (denoising):** Start with random noise → remove noise step-by-step → get back a clear image

The model learns the *reverse process* and uses it to generate new things from scratch.

### **Key Steps:**

1. **Training:** Learn to denoise (remove noise from images)
2. **Generation:** Start with random noise, denoise iteratively → new image appears

Example: 50 steps of denoising → DALL-E quality image

### **Where They Fit:**

```
GenAI (generative models)
 ├─ LLMs (transformer-based, text generation)
 └─ Diffusion Models ← image, audio, video generation
     ├─ DALL-E, Stable Diffusion (images)
     ├─ Imagen (Google, images)
     └─ Suno, Udio (music)
```

### **Advantages vs LLMs:**
- ✅ Better at image quality & control
- ✅ Faster than some alternatives
- ❌ Slower than LLM text generation (multiple steps needed)
- ❌ More compute-intensive for training

### **Real Examples:**
- **DALL-E 3** — text → photorealistic images
- **Stable Diffusion** — open-source image generation
- **Midjourney** — artistic image generation
- **Suno** — text → music

### **Key Difference from LLMs:**
| LLM | Diffusion |
|-----|-----------|
| Token-by-token generation | Iterative refinement |
| One pass → output | Multiple denoising steps |
| Text-focused | Image/audio-focused |

---

# GenAI & LLM Integration Guide

## Table of Contents

1. [LangChain](#langchain)
2. [LanGraph](#langgraph)
3. [RAG (Retrieval Augmented Generation)](#rag-retrieval-augmented-generation)
4. [Embeddings](#embeddings)
5. [Vector Stores](#vector-stores)
6. [Chains & Prompts](#chains--prompts)
7. [MCP (Model Context Protocol)](#mcp-model-context-protocol)
8. [Agents vs Tools](#agents-vs-tools)
9. [Workflow Orchestration](#workflow-orchestration)
10. [Best Practices](#best-practices)

---

## LangChain

### What is LangChain?

**LangChain** = Python/JS framework for building LLM applications with reusable abstractions

```
Your business logic
    ↓
LangChain (abstractions)
    ↓
LLMs + External tools + Databases
```

**Components:**
- **Document loaders** → Load PDFs, CSVs, APIs
- **Text splitters** → Chunk documents smartly
- **Embeddings** → Convert text to vectors
- **Vector stores** → Cache embeddings
- **Chains** → Connect LLM calls together
- **Agents** → Let LLM decide what to do

### LangChain Example

```python
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Define LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Define prompt template
prompt = ChatPromptTemplate.from_template(
    "Extract vendor and amount from this invoice:\n{invoice_text}"
)

# Create chain (LLM + prompt)
chain = LLMChain(llm=llm, prompt=prompt)

# Use chain
result = chain.run(invoice_text="Invoice from Acme Corp for $5000")
print(result)
# Output: {"vendor": "Acme Corp", "amount": "$5000"}
```

### Why Use LangChain?

**Without LangChain:**
```python
# You manage everything manually
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Extract vendor and amount"},
        {"role": "user", "content": invoice_text}
    ]
)
result = parse_json(response["choices"][0]["message"]["content"])
```

**With LangChain:**
```python
# Framework handles boilerplate
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(invoice_text)
```

---

## LanGraph

### What is LanGraph?

**LanGraph** = Framework for building **agentic workflows** with LangChain

```
LangChain = Basic LLM chains
LanGraph = Complex agent workflows with state & loops
```

Think: Graph-based state machine where LLM decides paths

### LanGraph Example

```python
from langgraph.graph import StateGraph
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# Define workflow nodes
def extract_node(state):
    """Extract invoice data"""
    result = llm.invoke(f"Extract from: {state['document']}")
    state['extracted'] = result
    return state

def validate_node(state):
    """Validate extracted data"""
    result = llm.invoke(f"Validate this data: {state['extracted']}")
    state['validated'] = result['is_valid']
    return state

def categorize_node(state):
    """Categorize expense"""
    result = llm.invoke(f"Categorize this amount: {state['amount']}")
    state['category'] = result
    return state

# Build graph
graph = StateGraph(dict)
graph.add_node("extract", extract_node)
graph.add_node("validate", validate_node)
graph.add_node("categorize", categorize_node)

# Define edges (workflow paths)
graph.add_edge("extract", "validate")  # Always validate after extract
graph.add_conditional_edges(
    "validate",
    lambda state: "categorize" if state['validated'] else "extract"
    # If valid, categorize. Else, extract again
)

# Compile and run
workflow = graph.compile()
result = workflow.invoke({"document": "Invoice from Acme..."})
print(result)
```

### LanGraph vs Simple Loop

**Without LanGraph (manual loop):**
```python
# You manage state and loops
state = {"document": "..."}

# Extract
state['extracted'] = extract(state['document'])

# Validate
if validate(state['extracted']):
    # Categorize
    state['category'] = categorize(state['amount'])
else:
    # Retry extract
    state['extracted'] = extract(state['document'])
```

**With LanGraph (declarative):**
```python
# Framework manages state and loops
graph = StateGraph(dict)
graph.add_node("extract", extract_node)
graph.add_conditional_edges("validate", router)
workflow = graph.compile()
result = workflow.invoke({"document": "..."})
```

---

## RAG (Retrieval Augmented Generation)

### What is RAG?

**RAG** = Pattern that combines retrieval + generation for better answers

```
Without RAG:
User: "What's in my company handbook?"
Claude: Uses only training data (outdated, generic)

With RAG:
User: "What's in my company handbook?"
Claude: Retrieves relevant handbook pages first
        Then generates answer from actual handbook
```

### RAG Architecture

```
User question
    ↓
1. Retrieve (search for relevant documents)
    ↓
2. Augment (add retrieved docs to prompt)
    ↓
3. Generate (LLM answers using retrieved context)
    ↓
Answer
```

### RAG Example

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 1. Load documents and store embeddings
embeddings = OpenAIEmbeddings()
vector_store = Pinecone.from_documents(
    docs,  # Your documents (handbook, policies, etc.)
    embeddings,
    index_name="company-handbook"
)

# 2. Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 3. Create RAG chain
llm = ChatOpenAI(model="gpt-4")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"  # Combine retrieved docs + question
)

# 4. Query
response = qa_chain.run("What's the vacation policy?")
# Behind the scenes:
# - Retrieves 3 most relevant handbook pages
# - Adds them to prompt: "Using this handbook: [...], answer: ..."
# - LLM answers from actual handbook
```

### Why RAG?

```
Problem: LLM training data is old
Solution: Retrieve current docs → LLM generates from them

Example:
Q: "What's our Q3 revenue?"
Without RAG: "I don't know, my training data ends in April 2024"
With RAG: Retrieves latest financial doc → "Q3 revenue is $15M"
```

---

## Embeddings

### What are Embeddings?

**Embedding** = Vector representation of text

```
Text → AI Model → Vector (list of numbers)

"The cat sat on the mat"
    ↓
[0.234, -0.156, 0.891, 0.456, ...] (1536 dimensions)
```

**Key insight:** Similar meanings = nearby vectors

```
Vector 1: "The cat sat" → [0.234, -0.156, ...]
Vector 2: "The dog sat" → [0.235, -0.157, ...]
                            ↑ Similar (nearby in space)

Vector 3: "Flying airplane" → [0.891, 0.234, ...]
                              ↑ Different (far away)
```

### Embeddings Example

```python
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Embed single text
vector = embeddings.embed_query("The cat sat on the mat")
print(len(vector))  # 1536 dimensions

# Embed multiple texts
vectors = embeddings.embed_documents([
    "The cat sat on the mat",
    "The dog sat on the mat",
    "Flying airplane"
])

# Calculate similarity (closer = more similar)
import numpy as np
similarity = np.dot(vectors[0], vectors[1])
print(f"Similarity between cat and dog: {similarity}")  # 0.98 (very similar)
print(f"Similarity between cat and airplane: {np.dot(vectors[0], vectors[2])}")  # 0.21 (different)
```

### Why Embeddings?

```
Problem: How to find "similar documents"?
Solution: Convert to vectors → Find nearby vectors

Use cases:
1. Search: User query → embedding → find similar docs
2. Clustering: Group similar documents
3. Recommendations: "Users who liked this, also liked..."
4. Duplicate detection: Same embedding = duplicate
```

---

## Vector Stores

### What is a Vector Store?

**Vector Store** = Database optimized for storing & searching embeddings

```
Traditional DB: Stores text
Vector Store: Stores vectors + text, searches by similarity

Query: "vacation policy"
  ↓
Convert to vector
  ↓
Find 3 nearest vectors in store
  ↓
Return matching documents
```

### Vector Store Examples

```python
from langchain.vectorstores import Pinecone, Chroma, FAISS
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

# Option 1: Pinecone (cloud, scalable)
vector_store = Pinecone.from_documents(
    documents=docs,
    embedding=embeddings,
    index_name="my-index"
)

# Option 2: Chroma (local, simple)
vector_store = Chroma.from_documents(docs, embeddings)

# Option 3: FAISS (local, fast)
vector_store = FAISS.from_documents(docs, embeddings)

# Search
results = vector_store.similarity_search("vacation policy", k=3)
for doc in results:
    print(doc.page_content)  # Top 3 matching documents
```

### Vector Store vs Regular DB

| Feature | Regular DB | Vector Store |
|---------|-----------|--------------|
| **Search** | Exact match | Similarity match |
| **Query** | `WHERE name = 'John'` | `Find similar to 'John'` |
| **Use case** | Structured data | Document search, RAG |
| **Speed** | Fast for exact | Fast for similarity |

---

## Chains & Prompts

### What are Chains?

**Chain** = Sequence of LLM calls linked together

```
Without chain:
response1 = llm("Summarize: " + text)
response2 = llm("Translate to Spanish: " + response1)
response3 = llm("Make it fun: " + response2)

With chain:
chain = Summarize → Translate → Make fun
result = chain.invoke(text)
```

### Chains Example

```python
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# Chain 1: Summarize
summarize_prompt = ChatPromptTemplate.from_template(
    "Summarize this in 2 sentences:\n{text}"
)
summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt)

# Chain 2: Translate
translate_prompt = ChatPromptTemplate.from_template(
    "Translate to Spanish:\n{summary}"
)
translate_chain = LLMChain(llm=llm, prompt=translate_prompt)

# Chain 3: Make fun
fun_prompt = ChatPromptTemplate.from_template(
    "Make this funny and engaging:\n{translation}"
)
fun_chain = LLMChain(llm=llm, prompt=fun_prompt)

# Combine chains
overall_chain = SequentialChain(
    chains=[summarize_chain, translate_chain, fun_chain],
    input_variables=["text"],
    output_variables=["fun_version"]
)

result = overall_chain(text="Long document here...")
print(result["fun_version"])
```

### Prompt Templates

**Prompt Template** = Reusable template with placeholders

```python
from langchain.prompts import ChatPromptTemplate

# Simple template
template = "Summarize this: {text}"
prompt = ChatPromptTemplate.from_template(template)

# Use it
formatted = prompt.format(text="Long document...")
# Output: "Summarize this: Long document..."

# Complex template
template = """
You are a {role}.
Extract the following from this document:
- Name
- Email
- Phone

Document:
{document}

Output as JSON.
"""
prompt = ChatPromptTemplate.from_template(template)

formatted = prompt.format(
    role="customer service rep",
    document="Customer: John, email john@example.com..."
)
```

---

## Summary Comparison

| Tool | Purpose | Use Case |
|------|---------|----------|
| **LangChain** | Build LLM apps | Simple chains, document Q&A |
| **LanGraph** | Build agent workflows | Multi-step agentic workflows |
| **RAG** | Retrieve + Generate | Query company documents, handbooks |
| **Embeddings** | Vector representation | Search, similarity, clustering |
| **Vector Store** | Store embeddings | Fast similarity search |
| **MCP** | LLM calls tools | Claude calling your APIs |

---

## Quick Decision Tree

```
Q: Do you need to call multiple LLMs?
  ├─ YES → Use LangChain (abstractsion)
  └─ NO → Direct API calls are fine

Q: Do you need smart multi-step workflows?
  ├─ YES → Use LanGraph
  └─ NO → Use LangChain

Q: Do you need to search documents?
  ├─ YES → Use RAG (retrieval + generation)
  └─ NO → Direct LLM calls

Q: Do you need LLM to call your APIs?
  ├─ YES → Use MCP
  └─ NO → Direct API calls

Q: Do you need to find similar documents?
  ├─ YES → Use Embeddings + Vector Store
  └─ NO → Database search is fine
```

---

## MCP (Model Context Protocol)

### What is MCP?

**MCP** = Standard protocol for LLMs to call external tools/APIs

```
Any LLM → MCP Protocol → Your Services
```

Works with:
- Claude ✓
- GPT-4 ✓
- Any LLM ✓

### When to Use MCP

**MCP is good when:**
```
LLM orchestrates workflow
  ↓
LLM decides what to do next
  ↓
LLM calls your APIs/tools (via MCP)
  ↓
LLM sees result
  ↓
LLM decides next step
```

### Real-World Example: Invoice Processing Workflow

**Scenario:** User says to Claude: "Process these invoices and update accounting"

#### Without MCP (User orchestrates):
```
User → "Extract invoice" → API → Gemini → Result
User → "Validate data" → API → Check → Result
User → "Categorize" → API → Assign code → Result
User → "Update CRM" → API → Record → Result

Problem: User must manage each step
```

#### With MCP (LLM orchestrates):
```
Claude (Agent) receives: "Process invoices"
  ↓
Claude thinks: "I need to extract first"
Claude calls Tool: extract_invoice()
  ↓ MCP Protocol
Your Service: Returns {"vendor": "Acme Corp", "amount": 5000}
  ↓
Claude thinks: "Now validate this"
Claude calls Tool: validate_data()
  ↓ MCP Protocol
Your Service: Returns {"valid": true}
  ↓
Claude thinks: "Now categorize"
Claude calls Tool: categorize_expense()
  ↓ MCP Protocol
Your Service: Returns {"account_code": "ACC-001"}
  ↓
Claude thinks: "Now update accounting"
Claude calls Tool: update_accounting_system()
  ↓ MCP Protocol
Your Service: Records in QuickBooks
  ↓
Claude thinks: "Now notify approver"
Claude calls Tool: send_notification()
  ↓ MCP Protocol
Your Service: Sends email
  ↓
Claude: "Done! Processed 10 invoices, updated accounting, notified approvers"
```

---

## Agents vs Tools

### Key Distinction

```
Claude = AGENT (orchestrator, decides what to do)
  ↓
extract_invoice() = TOOL (Claude calls it)
validate_data() = TOOL (Claude calls it)
categorize_expense() = TOOL (Claude calls it)
update_accounting_system() = TOOL (Claude calls it)
send_notification() = TOOL (Claude calls it)
```

**Important:** Not 5 agents. **1 agent + 5 tools.**

### Manager & Worker Analogy

```
Claude = Manager (orchestrates, makes decisions)

Tool 1 = Worker A (extract invoices)
Tool 2 = Worker B (validate data)
Tool 3 = Worker C (categorize expenses)
Tool 4 = Worker D (update systems)
Tool 5 = Worker E (send notifications)

Manager: "Worker A, extract the invoice"
Worker A: "Done! Here's the data"

Manager: "Worker B, validate it"
Worker B: "Done! It's valid"

Manager: "Worker C, categorize it"
Worker C: "Done! Account code is ACC-001"

Manager: "Worker D, update accounting"
Worker D: "Done! Updated QuickBooks"

Manager: "Worker E, notify approver"
Worker E: "Done! Email sent"

Manager: "All done! 10 invoices processed"
```

### With MCP

```
Each tool becomes an MCP Server function
Claude calls them via MCP protocol

Claude is STILL the agent (orchestrator)
Tools are STILL just functions
MCP is the communication protocol
```

**Your MCP Server:**
```python
from mcp.server import Server

server = Server("invoice-processor")

@server.tool()
def extract_invoice(file_path: str) -> dict:
    """Extract invoice data"""
    return {
        "vendor": "Acme Corp",
        "amount": 5000.00,
        "date": "2024-06-23"
    }

@server.tool()
def validate_data(data: dict) -> dict:
    """Validate invoice data"""
    return {"valid": True, "errors": []}

@server.tool()
def categorize_expense(amount: float) -> dict:
    """Categorize expense by amount"""
    return {"account_code": "ACC-001", "category": "Office Supplies"}

@server.tool()
def update_accounting_system(data: dict) -> dict:
    """Update QuickBooks or accounting system"""
    return {"status": "updated", "transaction_id": "TXN-123"}

@server.tool()
def send_notification(recipient: str, message: str) -> dict:
    """Send notification to approver"""
    return {"status": "sent", "timestamp": "2024-06-23T10:00:00Z"}
```

**Claude uses all these tools:**
```
Claude: "I'll extract, validate, categorize, update, and notify"
Claude → extract_invoice("invoice.pdf") → MCP → Tool executes
Claude → validate_data(extracted) → MCP → Tool executes
Claude → categorize_expense(5000) → MCP → Tool executes
Claude → update_accounting_system(data) → MCP → Tool executes
Claude → send_notification("approver@company.com", message) → MCP → Tool executes
Claude: "Done! Processed successfully"
```

---

## Tools Can Call ANY System

### Key Insight

```
MCP doesn't care WHAT the tool calls
It only cares that tool returns a result

Each tool = wrapper around external system
Tool can call:
✓ APIs (REST, GraphQL)
✓ Databases (SQL, NoSQL)
✓ Message queues (Kafka, RabbitMQ)
✓ External services (SendGrid, Stripe, AWS)
✓ Internal microservices
✓ File systems
✓ Anything with a client library
```

### Real Example: Tools Calling Different Systems

```python
from mcp.server import Server
import requests
import redis
from kafka import KafkaProducer
import sendgrid

server = Server("invoice-processor")

@server.tool()
def extract_invoice(file_path: str) -> dict:
    """Extract invoice data"""
    # Calls Gemini API
    response = requests.post(
        "https://gemini-api/extract",
        json={"file": file_path}
    )
    return response.json()

@server.tool()
def validate_data(data: dict) -> dict:
    """Validate invoice data"""
    # Calls your internal validation microservice API
    response = requests.post(
        "http://validation-service:8000/validate",
        json=data
    )
    return response.json()

@server.tool()
def categorize_expense(amount: float) -> dict:
    """Categorize expense"""
    # Queries PostgreSQL database directly
    r = redis.Redis(host='localhost')
    cached = r.get(f"category:{amount}")
    if cached:
        return json.loads(cached)
    
    # Fall back to DB query
    result = db.query(
        "SELECT account_code FROM expense_categories WHERE min <= ? AND max >= ?",
        amount
    )
    return {"account_code": result[0]}

@server.tool()
def update_accounting_system(data: dict) -> dict:
    """Update accounting system"""
    # Publishes to Kafka topic → accounting microservice consumes
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    producer.send('accounting-topic', value=data)
    return {"status": "published"}

@server.tool()
def send_notification(recipient: str, message: str) -> dict:
    """Send notification"""
    # Calls SendGrid email API
    sg = sendgrid.SendGridAPIClient("SENDGRID_API_KEY")
    response = sg.client.mail.send.post(request_body={
        "personalizations": [{"to": [{"email": recipient}]}],
        "from": {"email": "noreply@company.com"},
        "subject": "Invoice Processed",
        "content": [{"type": "text/plain", "value": message}]
    })
    return {"status": "sent", "message_id": response.headers.get("X-Message-Id")}
```

### Visualization

```
Claude (Agent orchestrates)
  ↓
  ├→ Tool 1 (extract_invoice)
  │    → Calls Gemini API
  │
  ├→ Tool 2 (validate_data)
  │    → Calls internal validation microservice
  │
  ├→ Tool 3 (categorize_expense)
  │    → Queries PostgreSQL DB (with Redis cache)
  │
  ├→ Tool 4 (update_accounting_system)
  │    → Publishes to Kafka
  │         ↓
  │      Accounting microservice consumes event
  │
  └→ Tool 5 (send_notification)
       → Calls SendGrid API
```

### For VoxAlchemy Example

```
If you had agentic document processing:

Claude orchestrates:

Tool 1: extract_document()
  → Calls your Gemini extraction API

Tool 2: validate_quality()
  → Calls internal validation API

Tool 3: categorize_document()
  → Queries PostgreSQL (document types)

Tool 4: update_user_account()
  → Publishes to Kafka → Billing service consumes

Tool 5: notify_user()
  → Calls SendGrid API
```

### Key Takeaway

```
Tools are just wrappers
They hide the complexity of different backends
Claude orchestrates at a high level
Backend can be anything: APIs, DBs, Kafka, etc.
```

---

## Workflow Orchestration

### User Orchestrates (Current VoxAlchemy)

```
User is the decision-maker

User → "Extract this PDF" → API → Gemini → Result
User → "Validate result" → API → Check → Result
User → "Download output" → API → Return → File
```

**Pros:**
- Simple, predictable
- User has full control
- Clear error handling

**Cons:**
- User must manage each step
- Multi-step workflows are tedious

### LLM Orchestrates (With MCP)

```
LLM is the decision-maker

User: "Process invoices end-to-end"
Claude → Tool 1 → Tool 2 → Tool 3 → Tool 4 → Tool 5
Claude: "Done! Here's your report"
```

**Pros:**
- Multi-step workflows are seamless
- LLM handles complexity
- Natural language interface

**Cons:**
- Less control over each step
- Harder to debug
- More expensive (more API calls)

---

## Best Practices

### When to Use MCP

**Use MCP if:**
```
✓ LLM orchestrates complex multi-step workflows
✓ User says "do this end-to-end" (not step-by-step)
✓ You want agentic AI (Claude makes decisions)
✓ You want to switch between LLMs easily
```

**Don't use MCP if:**
```
✗ User controls workflow (simple transactional)
✗ Direct API is simpler
✗ Performance is critical (MCP adds latency)
✗ Single-step operations
```

### For VoxAlchemy

**Current architecture (CORRECT):**
```
User → Web UI → API → Gemini → Result
```

**If you wanted LLM orchestration:**
```
Claude → MCP → extract_invoice() → Gemini
      ↓ MCP → validate_data()
      ↓ MCP → categorize_expense()
      ↓ MCP → update_accounting()
      ↓ MCP → send_notification()
```

**Verdict:** Your current approach is right for transactional use. MCP would be overkill.

---

## Summary

| Concept | Definition | Example |
|---------|-----------|---------|
| **Agent** | Orchestrates workflow, makes decisions | Claude (the LLM) |
| **Tool** | Does specific task, called by agent | extract_invoice(), validate_data() |
| **MCP** | Protocol for agent to call tools | LLM → Tool via MCP Server |
| **Workflow** | Sequence of tools executed by agent | Extract → Validate → Categorize → Update |

---

## Interview Answer

### Q: "What's MCP and when would you use it?"

> "MCP (Model Context Protocol) is a standard protocol that lets LLMs call external tools and APIs.
> 
> **Key insight:** MCP is useful when an **LLM orchestrates a workflow**, not when a user does.
> 
> **Example:**
> User: \"Process these invoices and update accounting\"
> 
> Claude (the agent) orchestrates:
> 1. Call extract_invoice() tool
> 2. Call validate_data() tool
> 3. Call categorize_expense() tool
> 4. Call update_accounting_system() tool
> 5. Call send_notification() tool
> 
> Claude sees each result and decides the next step.
> 
> **For VoxAlchemy:**
> - Current: User orchestrates (upload → process → download) ✓
> - Wouldn't use MCP (users aren't LLM agents)
> - Would use MCP only if: \"Let Claude handle document processing end-to-end\"
> 
> **When to use MCP:**
> - Multi-step agentic workflows
> - LLM is the decision-maker
> - Not for simple transactional APIs"

---
