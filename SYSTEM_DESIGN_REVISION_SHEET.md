# SYSTEM DESIGN: QUICK REVISION SHEET
**All Formulas + Twitter Example (Side-by-Side)**

---

## 1. QPS FORMULA

| Formula | Twitter Calculation |
|---------|-------------------|
| **Off-peak QPS** = (DAU × Requests/user) ÷ 100K | (300M × 20) ÷ 100K = **60,000 QPS** |
| **Peak QPS** = Off-peak × Peak_mult | 60,000 × 4 = **240,000 QPS** |
| **Daily Requests** = Off-peak × 3,600 × avg_hrs + Peak × 3,600 × peak_hrs | (60K × 3.6K × 20) + (240K × 3.6K × 4) = **7.8B requests/day** |
| **Servers** = Peak QPS ÷ Server_capacity | 240,000 ÷ 500 = **480 servers** |
| **With 2X Redundancy** = Servers × 2 | 480 × 2 = **960 servers** |
| **Auto-scale** = Peak_servers - Off-peak_servers | 960 - 240 = **+720 servers for peak_hrs** |

---

## 2. STORAGE FORMULA

| Formula | Twitter Calculation |
|---------|-------------------|
| **Daily Data** = DAU × data_per_user | 300M × 10 MB = **3 PB/day** |
| **Retention Total** = Daily_data × retention_days | 3 PB × 1,825 = **5,475 PB** |
| **With Redundancy** = Total × redundancy | 5,475 PB × 2 = **10,950 PB** |
| **With Compression** = With_redundancy ÷ compression_ratio | 10,950 ÷ 1.5 = **7,300 PB final** |
| **Tiered Storage (Hot)** = Daily × 365 × hot_years | 3 PB × 365 × 1 = **1,095 PB** @ $0.023/GB/mo |
| **Tiered Storage (Warm)** = Daily × 365 × warm_years | 3 PB × 365 × 4 = **4,380 PB** @ $0.003/GB/mo |
| **Total Annual Cost** | Hot: $303M + Warm: $158M = **~$462M/year** |

---

## 3. BANDWIDTH FORMULA

| Formula | Twitter Calculation |
|---------|-------------------|
| **Bytes Per Second** = Peak_QPS × response_size | 240K × 2 KB = **480 MB/sec** |
| **Gbps** = (Bytes/sec × 8) ÷ 10^9 | (480 × 8) ÷ 10^9 = **3.84 Gbps** |
| **With Redundancy** = Gbps × bw_redundancy | 3.84 × 10 = **38.4 Gbps** |
| **Annual Cost** | Gbps × unit_cost = **~$2M/year** |

---

## 4. DATABASE CAPACITY FORMULA

| Formula | Twitter Calculation |
|---------|-------------------|
| **Write QPS** = Peak_QPS ÷ read_write_ratio | 240K ÷ 11 = **21,818 writes/sec** |
| **Records Per Day** = Write_QPS × 86400 | 21,818 × 86,400 = **1.88B records/day** |
| **Daily Data Volume** = Records × record_size | 1.88B × 500 B = **0.94 TB/day** |
| **Total With Retention** = Daily × 365 × retention_yrs | 0.94 TB × 1,825 = **1.7 PB** |
| **With Index Overhead** = Total × index_mult | 1.7 PB × 1.5 = **2.55 PB** |
| **With Replication** = With_indexes × db_redundancy | 2.55 PB × 2 = **5.1 PB** |
| **Annual Cost** | 5.1 PB × storage_cost = **~$150M/year** |

---

## 5. CACHING LAYER FORMULA

| Formula | Twitter Calculation |
|---------|-------------------|
| **Cache Hit Rate** = hit_rate | **80%** of requests from cache |
| **Cache Miss Rate** = 1 - hit_rate | 1 - 0.80 = **20%** miss rate |
| **DB Hits QPS** = Peak_QPS × (1 - hit_rate) | 240K × 0.20 = **48K QPS** (vs 240K!) |
| **Working Set** = DB_size × hot_data_ratio | 5.1 PB × 0.20 = **1.02 PB** |
| **Cache Size** = Working_set × cache_redundancy | 1.02 PB × 2 = **2.04 PB** |
| **Cache Servers** = Cache_size ÷ ram_per_server | 2.04 PB ÷ 0.512 PB = **~4K servers** |
| **DB Load Reduction** = hit_rate | **80%** load reduction |
| **Annual Savings** | $40M DB cost - $3M cache cost = **$37M saved** |

---

## 6. KEY CONSTANTS (Memorize These!)

| Constant | Value | Why It Matters |
|----------|-------|----------------|
| **Seconds per day** | 100K | Base unit for QPS calculation |
| **Seconds per hour** | 3,600 | For peak hour calculations |
| **Network speed** | 125 MB/s per Gbps | 1 Gbps = 125 MB/s |
| **Server capacity** | 500-10,000 QPS | Depends on operation complexity |
| **Peak multiplier** | 2-5X (typically 4X) | Traffic during peak hours |
| **Redundancy** | 2-3X | Replication for HA |
| **Cache hit rate** | 70-90% | Typical for well-designed systems |
| **Working set ratio** | 20-30% | Hot data that gets accessed 80% |
| **SSD cost** | $0.023/GB/month | Hot storage (fast, expensive) |
| **HDD cost** | $0.003/GB/month | Warm storage (slow, cheap) |

---

## 7. COMPLETE INFRASTRUCTURE COST BREAKDOWN

| Component | Metric | Cost |
|-----------|--------|------|
| **Servers** | 960 peak (240K QPS ÷ 500) | $50M/year |
| **Bandwidth** | 38.4 Gbps | $2M/year |
| **Database Storage** | 5.1 PB | $150M/year |
| **Cache (RAM)** | 2.04 PB | $3M/year |
| **Operations & Other** | Monitoring, logging, etc. | $250M/year |
| **TOTAL** | **Twitter-scale system** | **~$455M/year** |

---

## 8. CALCULATION FLOW

```
INPUT: 300M DAU, 20 requests/user/day
           ↓
    [QPS FORMULA]
    Average: 60,000 QPS
    Peak: 240,000 QPS
           ↓
    ├─→ [SERVERS] = 240K ÷ 500 = 480 → 960 with 2X
    │
    ├─→ [BANDWIDTH] = 240K × 2KB × 8 ÷ 10^9 × 10X = 38.4 Gbps
    │
    ├─→ Write_QPS = 240K ÷ 11 = 21.8K writes/sec
    │       ↓
    │   [DATABASE] = 21.8K × 500B × Retention × 2X = 5.1 PB
    │
    └─→ [CACHING] = 5.1 PB × 20% × 2X = 2.04 PB (80% hit rate)

OUTPUT: $455M/year infrastructure cost
```

---

## 9. QUICK DECISION MATRIX

| Question | Formula to Use | Example |
|----------|----------------|---------|
| How many servers? | Peak QPS ÷ capacity | 240K ÷ 500 = 480 |
| How much bandwidth? | QPS × response_size × 8 ÷ 10^9 | 240K × 2KB = 38.4 Gbps |
| How much storage? | Write_QPS × record_size × retention | 21.8K × 500B × 5yr = 5.1 PB |
| How much cache? | DB_size × 20% × 2X | 5.1 PB × 20% × 2 = 2.04 PB |
| Total infrastructure cost? | Add all components | $455M/year |
| Will peak break us? | Peak QPS > (servers × capacity)? | 240K > 480 × 500? NO, safe |

---

## 10. TWITTER NUMBERS AT A GLANCE

```
INPUT ASSUMPTIONS:
├─ DAU: 300 Million
├─ Requests/user/day: 20
├─ Peak multiplier: 4X
├─ Peak hours: 4 hours
├─ Retention: 5 years
└─ Response size: 2 KB

OUTPUT METRICS:
├─ QPS: 60K avg, 240K peak
├─ Servers: 480 (960 with redundancy)
├─ Bandwidth: 38.4 Gbps
├─ Database: 5.1 PB
├─ Cache: 2.04 PB
└─ Cost: $455M/year

KEY INSIGHTS:
├─ Only WRITES create DB records (21.8K/sec)
├─ 80% cache hit reduces DB load from 240K to 48K QPS
├─ Response size matters as much as QPS for bandwidth
├─ Redundancy 2-3X for all metrics (HA)
└─ Peak hour planning is critical (4 hours = $2B+/year)
```

---

**Print this sheet. Keep it with you. Master these 5 formulas and you can estimate any system.** 🎯
