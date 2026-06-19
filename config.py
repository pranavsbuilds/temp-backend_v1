import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# App settings
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# API keys and paths
QUIZ_API_KEY = os.getenv("QUIZ_API_KEY", "")
# Default Vosk model path is the sibling folder
VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "../backend/vosk-model-small-en-us-0.15")

# Interview settings
CHEAT_PENALTY = float(os.getenv("CHEAT_PENALTY", 0.2))
TOTAL_QUESTIONS = 10

# High-quality mock questions and explanations for fallback
MOCK_QUESTIONS = {
    "programming": {
        "easy": [
            {
                "text": "What is the difference between a compiler and an interpreter?",
                "explanation": "A compiler translates the entire source code into machine code before execution, creating an executable file. An interpreter translates and executes the code line-by-line at runtime."
            },
            {
                "text": "Explain the concept of recursion in programming.",
                "explanation": "Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller, self-similar sub-problems, requiring a base case to terminate."
            },
            {
                "text": "What is Object-Oriented Programming (OOP)?",
                "explanation": "OOP is a programming paradigm based on the concept of 'objects' containing data (attributes) and code (methods), organized into classes supporting encapsulation, inheritance, and polymorphism."
            },
            {
                "text": "Explain the difference between a stack and a queue.",
                "explanation": "A stack is a Last-In-First-Out (LIFO) data structure where elements are added and removed from the same end. A queue is a First-In-First-Out (FIFO) structure where elements are added at the rear and removed from the front."
            },
            {
                "text": "What is Big O notation?",
                "explanation": "Big O notation is a mathematical notation used to describe the limiting behavior and efficiency of an algorithm in terms of execution time or memory space as the input size grows."
            },
            {
                "text": "What is inheritance in OOP?",
                "explanation": "Inheritance is a mechanism where a new class (subclass) inherits properties and methods from an existing class (superclass), promoting code reusability."
            },
            {
                "text": "What is the difference between a function parameter and an argument?",
                "explanation": "A parameter is the variable defined in the function signature. An argument is the actual value passed to the function when it is called."
            },
            {
                "text": "Explain compile-time versus runtime.",
                "explanation": "Compile-time is the phase when source code is translated into machine code. Runtime is the phase when the compiled executable is actually running on the system."
            },
            {
                "text": "What is a pure function?",
                "explanation": "A pure function is a function that always returns the same output for the same input and has no side effects (doesn't modify global state or input variables)."
            },
            {
                "text": "What is the purpose of version control systems like Git?",
                "explanation": "Version control systems track changes to source code over time, allowing multiple developers to collaborate, manage code history, and revert to previous versions."
            }
        ],
        "medium": [
            {
                "text": "Explain runtime polymorphism.",
                "explanation": "Runtime polymorphism (dynamic binding) is achieved through method overriding, where the method to be executed is resolved at runtime based on the actual object type rather than the reference type."
            },
            {
                "text": "What is a closure in programming?",
                "explanation": "A closure is a function that retains access to its lexical scope (outer variables) even when the function is executed outside its original scope."
            },
            {
                "text": "What is a deadlock and how is it prevented?",
                "explanation": "A deadlock is a state where two or more processes are blocked because each is holding a resource the other needs. Prevented by avoiding circular waits, enforcing lock ordering, or using lock timeouts."
            },
            {
                "text": "Explain the difference between synchronous and asynchronous execution.",
                "explanation": "Synchronous execution blocks the current thread until the operation completes. Asynchronous execution returns control immediately, notifying the program via callbacks or promises when done."
            },
            {
                "text": "What is a hash collision and how is it resolved?",
                "explanation": "A hash collision occurs when two different keys hash to the same index. Resolved using chaining (linked lists at the index) or open addressing (searching for the next free slot)."
            },
            {
                "text": "Explain memory leaks and how garbage collection helps.",
                "explanation": "A memory leak occurs when a program allocates memory but fails to release it when no longer needed. Garbage collection automatically reclaims memory occupied by objects that are no longer reachable."
            },
            {
                "text": "What is method overloading versus method overriding?",
                "explanation": "Method overloading defines multiple methods with the same name but different parameters in the same class. Method overriding redefines a superclass method in a subclass with the same signature."
            },
            {
                "text": "What is a design pattern? Give one example.",
                "explanation": "A design pattern is a reusable solution to a commonly occurring software design problem. An example is the Singleton pattern, which ensures a class has only one instance."
            },
            {
                "text": "What is the difference between an abstract class and an interface?",
                "explanation": "An abstract class can contain member variables and concrete method implementations. An interface defines a contract (method signatures) that implementing classes must fulfill."
            },
            {
                "text": "Explain the Single Responsibility Principle from SOLID.",
                "explanation": "The Single Responsibility Principle states that a class should have only one reason to change, meaning it should focus on a single, well-defined responsibility."
            }
        ],
        "hard": [
            {
                "text": "Describe the difference between process and thread synchronization (e.g., Mutex vs Semaphore).",
                "explanation": "A Mutex is a locking mechanism allowing only one thread access to a resource (ownership). A Semaphore is a signaling mechanism using counters to allow up to N threads access concurrently."
            },
            {
                "text": "How does the TCP three-way handshake work?",
                "explanation": "The client sends a SYN packet, the server responds with a SYN-ACK packet, and the client sends back an ACK packet to establish a reliable, full-duplex connection."
            },
            {
                "text": "Explain the actor model of concurrency.",
                "explanation": "The actor model uses 'actors' as primitive units of execution. Actors do not share state; they communicate solely by passing asynchronous messages to each other, avoiding locks."
            },
            {
                "text": "Describe the internal workings of a garbage collector (e.g., mark-and-sweep, generational).",
                "explanation": "Generational GC divides objects by age (young, old) because most objects die young. It runs frequent, fast collections on the young generation and promotes survivors to the old generation."
            },
            {
                "text": "Explain the difference between deep copying and shallow copying in memory.",
                "explanation": "A shallow copy duplicates object references, sharing nested objects. A deep copy recursively copies all objects, creating completely independent duplicates in memory."
            },
            {
                "text": "Describe how dynamic dispatch is implemented under the hood (vtable).",
                "explanation": "Dynamic dispatch uses a virtual method table (vtable). The compiler creates a table of function pointers for virtual methods, and each object contains a pointer (vptr) to its class vtable."
            },
            {
                "text": "What is tail call optimization and how does it work?",
                "explanation": "Tail call optimization (TCO) allows a compiler to execute a recursive function call without adding a new stack frame if the recursive call is the absolute last operation in the function."
            },
            {
                "text": "Explain the difference between optimistic and pessimistic concurrency control.",
                "explanation": "Pessimistic locking locks resources immediately upon access. Optimistic concurrency allows operations without locks, checking for conflicts before committing and rolling back if a conflict is found."
            },
            {
                "text": "What is a monad in functional programming?",
                "explanation": "A monad is a design pattern represented as a type constructor that wraps values, providing mechanisms to chain operations (bind/flatMap) while managing side effects."
            },
            {
                "text": "Explain how compile-time templates or generics work (e.g., monomorphization vs type erasure).",
                "explanation": "Monomorphization (C++) generates concrete code for every template type parameter during compilation. Type erasure (Java) replaces type parameters with bounds (Object) and inserts casts, saving binary size."
            }
        ]
    },
    "devops-and-cloud": {
        "easy": [
            {
                "text": "What is DevOps?",
                "explanation": "DevOps is a set of practices combining software development (Dev) and IT operations (Ops) to shorten the systems development life cycle and provide high-quality continuous delivery."
            },
            {
                "text": "What is containerization?",
                "explanation": "Containerization is a lightweight virtualization method that packages an application and its dependencies into a single container running on a shared host OS kernel."
            },
            {
                "text": "What is a CI/CD pipeline?",
                "explanation": "A CI/CD pipeline automates software delivery. Continuous Integration compiles and tests code changes, while Continuous Deployment automatically deploys approved changes to production."
            },
            {
                "text": "What is the difference between git merge and git rebase?",
                "explanation": "Git merge combines branches preserving history with a merge commit. Git rebase moves the base of the current branch onto another branch, producing a linear commit history."
            },
            {
                "text": "What is Infrastructure as Code (IaC)?",
                "explanation": "IaC is the practice of managing and provisioning computing infrastructure through machine-readable configuration files (like Terraform, Ansible) rather than manual setup."
            },
            {
                "text": "What is a load balancer?",
                "explanation": "A load balancer distributes incoming network traffic across a group of backend servers to prevent overload, increase availability, and ensure redundancy."
            },
            {
                "text": "What is public cloud vs private cloud?",
                "explanation": "Public cloud resources are owned and operated by a third-party provider (AWS, Azure) and shared. Private cloud resources are used exclusively by one organization on private infrastructure."
            },
            {
                "text": "What is a Docker image vs a Docker container?",
                "explanation": "A Docker image is a read-only template defining container instructions. A Docker container is a runnable, isolated instance of that image."
            },
            {
                "text": "What is serverless computing?",
                "explanation": "Serverless computing is a cloud-execution model where the provider dynamically manages machine resources, and developers write functions charged by execution time (FaaS)."
            },
            {
                "text": "What is a virtual machine?",
                "explanation": "A virtual machine is a software emulation of a physical computer running a complete guest operating system on top of a physical host using a hypervisor."
            }
        ],
        "medium": [
            {
                "text": "Explain the difference between container virtualization and VM virtualization.",
                "explanation": "Containers share the host OS kernel and isolate processes, making them lightweight. VMs run a full guest OS on top of a hypervisor, consuming more memory and storage."
            },
            {
                "text": "What is Kubernetes (K8s) and what is a Pod?",
                "explanation": "Kubernetes is an open-source container orchestration platform. A Pod is the smallest deployable unit in Kubernetes, representing a group of one or more co-located containers."
            },
            {
                "text": "Explain blue-green deployment vs canary deployment.",
                "explanation": "Blue-green maintains two identical environments, switching 100% of traffic once verified. Canary deploys updates to a small subset of servers first, gradually rolling it out."
            },
            {
                "text": "What is the purpose of a Docker multi-stage build?",
                "explanation": "Multi-stage builds optimize Dockerfile readability and size by separating build and runtime environments, leaving build tools out of the final runtime image."
            },
            {
                "text": "Describe the role of a reverse proxy like Nginx.",
                "explanation": "A reverse proxy sits between clients and backend servers, handling tasks like SSL termination, URL routing, load balancing, caching, and rate limiting."
            },
            {
                "text": "What is horizontal scaling vs vertical scaling?",
                "explanation": "Vertical scaling increases the resources (CPU, RAM) of a single server. Horizontal scaling adds more servers to the pool, distributing load across them."
            },
            {
                "text": "Explain git stash and when you would use it.",
                "explanation": "Git stash temporarily shelves uncommitted local changes, giving you a clean working directory so you can switch tasks without losing current progress."
            },
            {
                "text": "What is configuration drift and how does IaC prevent it?",
                "explanation": "Configuration drift is when servers develop unique manual changes over time. IaC prevents this by enforcing declaration-based configurations, automatically correcting drift."
            },
            {
                "text": "Explain the concept of container orchestration.",
                "explanation": "Container orchestration is the automated lifecycle management of containers, handling scheduling, replication, service discovery, load balancing, and self-healing."
            },
            {
                "text": "What is the difference between rolling updates and recreate deployments in Kubernetes?",
                "explanation": "Rolling updates replace pods gradually to ensure zero-downtime. Recreate terminates all existing pods first before creating new ones, causing temporary downtime."
            }
        ],
        "hard": [
            {
                "text": "Explain how container networking works under the hood (CNI, namespaces, veth pairs).",
                "explanation": "Container networking uses Linux network namespaces, virtual ethernet pairs (veth), and bridges. A CNI plugin dynamically creates these interfaces to route container packets."
            },
            {
                "text": "Describe the CAP theorem and its implications on distributed databases.",
                "explanation": "The CAP theorem states that a distributed system can guarantee at most two of: Consistency, Availability, and Partition Tolerance. In practice, systems choose AP or CP."
            },
            {
                "text": "Explain consistent hashing and its application in distributed caching.",
                "explanation": "Consistent hashing maps keys and nodes to a virtual ring. Adding or removing a node only requires remapping a small fraction of keys, preventing cache stampedes."
            },
            {
                "text": "Describe the GitOps workflow and how tools like ArgoCD work.",
                "explanation": "GitOps uses Git as the single source of truth for infrastructure. ArgoCD continuously monitors Git configurations, pulling changes and reconciling them on K8s clusters."
            },
            {
                "text": "Explain how service mesh (like Istio) handles traffic routing and mTLS.",
                "explanation": "A service mesh uses sidecar proxies (Envoy) next to application containers. Proxies intercept network traffic, handling load balancing, mTLS encryption, and telemetry."
            },
            {
                "text": "Describe the transactional outbox pattern in distributed microservices.",
                "explanation": "Instead of writing to database and message queue separately, database updates and events are written in a single local transaction, and a relay process publishes outbox events."
            },
            {
                "text": "How do you handle split-brain scenarios in high-availability distributed systems?",
                "explanation": "Split-brain is mitigated using consensus algorithms (Raft/Paxos) requiring a quorum (majority) of nodes to elect a leader, or node fencing (STONITH) to disable failed nodes."
            },
            {
                "text": "Explain log-structured merge (LSM) trees vs B-Trees for database storage engines.",
                "explanation": "B-Trees organize data in disk pages, optimizing read-heavy workloads. LSM trees write sequentially to an in-memory buffer before flushing to disk, optimizing write-heavy workloads."
            },
            {
                "text": "Describe the circuit breaker pattern in microservice communication.",
                "explanation": "A circuit breaker monitors calls to external services. If failures cross a threshold, the breaker opens, returning errors immediately instead of calling the service, allowing it recovery time."
            },
            {
                "text": "Explain the Raft or Paxos consensus algorithm.",
                "explanation": "Raft achieves consensus by electing a leader who replicates logs to follower nodes, guaranteeing safety and consistency across the cluster even under network splits."
            }
        ]
    },
    "cybersecurity": {
        "easy": [
            {
                "text": "What is encryption?",
                "explanation": "Encryption is the process of converting readable text (plaintext) into an unreadable format (ciphertext) using cryptographic algorithms and keys."
            },
            {
                "text": "What is the difference between HTTP and HTTPS?",
                "explanation": "HTTP transmits data in plain text, vulnerable to sniffing. HTTPS encrypts data transmission using TLS/SSL to secure communications."
            },
            {
                "text": "What is multi-factor authentication (MFA)?",
                "explanation": "MFA is a security system requiring multiple separate credentials for authentication, typically combining something you know, have, and are."
            },
            {
                "text": "What is a firewall?",
                "explanation": "A firewall is a network security device that monitors and filters incoming and outgoing network traffic based on established security rules."
            },
            {
                "text": "What is a phishing attack?",
                "explanation": "Phishing is a social engineering attack where attackers send fraudulent messages disguised as trustworthy entities to steal sensitive data."
            },
            {
                "text": "What is malware?",
                "explanation": "Malware is any software intentionally designed to cause disruption, damage, or unauthorized access to a computer, server, or network."
            },
            {
                "text": "What is a VPN?",
                "explanation": "A Virtual Private Network (VPN) encrypts internet traffic and routes it through a secure server, masking the user's IP address and location."
            },
            {
                "text": "What is SQL injection?",
                "explanation": "SQL injection is an attack where malicious SQL statements are inserted into input fields, manipulating backend databases to extract or delete data."
            },
            {
                "text": "What is a Denial of Service (DoS) attack?",
                "explanation": "A DoS attack attempts to shut down a machine or network, making it inaccessible to its intended users by flooding it with excessive traffic."
            },
            {
                "text": "What is salt in password hashing?",
                "explanation": "A salt is a random string of data appended to a password before hashing, protecting against precomputed table attacks like rainbow tables."
            }
        ],
        "medium": [
            {
                "text": "Explain symmetric vs asymmetric encryption.",
                "explanation": "Symmetric encryption uses the same key for both encryption and decryption. Asymmetric encryption uses a mathematically linked public-private key pair."
            },
            {
                "text": "What is Cross-Site Scripting (XSS) and how is it prevented?",
                "explanation": "XSS is an attack inserting malicious scripts into web pages viewed by other users. Prevented by escaping inputs, output encoding, and Content Security Policies."
            },
            {
                "text": "How does a TLS handshake establish a secure connection?",
                "explanation": "The client and server exchange handshakes, verify the server's certificate, agree on cipher suites, and generate a symmetric session key for encryption."
            },
            {
                "text": "What is a Man-in-the-Middle (MitM) attack?",
                "explanation": "A MitM attack is when an attacker secretly relays and alters communications between two parties who believe they are directly talking to each other."
            },
            {
                "text": "Explain the concept of Least Privilege.",
                "explanation": "The Principle of Least Privilege states that users, programs, and systems should only be given the minimum permissions necessary to perform their tasks."
            },
            {
                "text": "What is Cross-Site Request Forgery (CSRF) and how is it prevented?",
                "explanation": "CSRF forces users to execute unwanted actions on web apps where they are authenticated. Prevented using anti-CSRF tokens and SameSite cookie attributes."
            },
            {
                "text": "What is hashing vs encryption?",
                "explanation": "Hashing is a one-way function that maps input to fixed-size hashes (irreversible). Encryption is a two-way function that encrypts and decrypts (reversible with key)."
            },
            {
                "text": "What is a Web Application Firewall (WAF)?",
                "explanation": "A WAF monitors and filters HTTP traffic between a web application and the Internet, defending against attacks like XSS, SQLi, and cookie poisoning."
            },
            {
                "text": "Explain public key infrastructure (PKI) and certificates.",
                "explanation": "PKI is a framework managing digital certificates. Certificate Authorities (CAs) digitally sign certificates to bind public keys to identities."
            },
            {
                "text": "What is DNS spoofing or DNS cache poisoning?",
                "explanation": "DNS spoofing introduces corrupt DNS data into a resolver's cache, causing it to return incorrect IP addresses and redirecting traffic to malicious sites."
            }
        ],
        "hard": [
            {
                "text": "Explain how zero-knowledge proofs work.",
                "explanation": "A zero-knowledge proof allows one party (prover) to prove to another party (verifier) that a statement is true without revealing any actual information beyond that statement."
            },
            {
                "text": "Describe the Diffie-Hellman key exchange protocol and its vulnerability to MitM.",
                "explanation": "Diffie-Hellman allows two parties to establish a shared secret key over an insecure channel. It is vulnerable to MitM unless authenticated using signatures or certificates."
            },
            {
                "text": "Explain buffer overflow attacks and modern mitigations (ASLR, DEP/NX, Stack Canaries).",
                "explanation": "Buffer overflows write data past block boundaries. Mitigated by ASLR (randomizing memory layout), DEP/NX (non-executable stacks), and Stack Canaries (sentinel values checking stack integrity)."
            },
            {
                "text": "Describe the difference between OAuth 2.0 and SAML protocols.",
                "explanation": "OAuth 2.0 is an authorization framework using JSON Web Tokens (JWT) for APIs. SAML is an XML-based authentication standard used primarily for enterprise Single Sign-On."
            },
            {
                "text": "Explain how the RSA encryption algorithm works mathematically.",
                "explanation": "RSA is based on the difficulty of factoring the product of two large prime numbers. It uses modular exponentiation with public key (e, n) and private key (d, n) parameters."
            },
            {
                "text": "What is a side-channel attack and how is it mitigated?",
                "explanation": "A side-channel attack exploits physical implementation details (timing, power, acoustics) to extract keys. Mitigated by constant-time algorithms and noise injection."
            },
            {
                "text": "Describe the concept of Zero Trust architecture.",
                "explanation": "Zero Trust is a security framework assuming all network traffic is hostile. It requires continuous verification of every user and device access request before granting trust."
            },
            {
                "text": "Explain how ARP poisoning works and how to detect/prevent it.",
                "explanation": "ARP poisoning associates an attacker's MAC address with a target's IP on a local network. Detected using ARP monitors, and prevented using static tables or Dynamic ARP Inspection."
            },
            {
                "text": "Describe the details of DNSSEC and how it protects DNS queries.",
                "explanation": "DNSSEC signs DNS records cryptographically, ensuring data origin authenticity and integrity, and preventing cache poisoning and man-in-the-middle redirects."
            },
            {
                "text": "Explain how Kerberos authentication protocol works in Active Directory.",
                "explanation": "Kerberos uses symmetric key cryptography. A Key Distribution Center (KDC) issues Ticket Granting Tickets (TGT) and service tickets to prove identity without passing passwords."
            }
        ]
    },
    "database": {
        "easy": [
            {
                "text": "What is a relational database?",
                "explanation": "A relational database organizes data into tables of rows and columns, establishing relationships between tables using keys, queryable via SQL."
            },
            {
                "text": "What is a primary key?",
                "explanation": "A primary key is a column or set of columns that uniquely identifies each row in a database table. It cannot contain null values."
            },
            {
                "text": "What is a foreign key?",
                "explanation": "A foreign key is a column in one table that references the primary key of another table, enforcing referential integrity between the two tables."
            },
            {
                "text": "Explain SQL versus NoSQL.",
                "explanation": "SQL databases are relational and structured with rigid schemas. NoSQL databases are non-relational with dynamic schemas, designed for unstructured data and horizontal scaling."
            },
            {
                "text": "What is database normalization?",
                "explanation": "Normalization is the process of structuring a relational database to minimize data redundancy and dependency by organizing columns and tables."
            },
            {
                "text": "Explain SQL JOIN operations (Inner, Left, Right).",
                "explanation": "Inner Join returns rows with matches in both tables. Left Join returns all rows from the left table and matched rows from the right. Right Join is the reverse of Left Join."
            },
            {
                "text": "What is a database transaction?",
                "explanation": "A database transaction is a sequence of operations performed as a single logical unit of work, which must succeed or fail as a whole."
            },
            {
                "text": "What is the purpose of database indexing?",
                "explanation": "Indexing is a data structure technique that speeds up data retrieval operations on a table, although it increases writing time and disk usage."
            },
            {
                "text": "Explain the NULL value in databases.",
                "explanation": "NULL is a marker used to indicate that a data value does not exist in the database, representing missing or unknown information."
            },
            {
                "text": "What is a database schema?",
                "explanation": "A database schema is the formal structure or layout of a database, representing tables, fields, relationships, and constraints."
            }
        ],
        "medium": [
            {
                "text": "Explain the difference between clustered and non-clustered indexes.",
                "explanation": "A clustered index determines the physical order of data storage in the table (one per table). A non-clustered index stores index pointers separately from the data rows (multiple allowed)."
            },
            {
                "text": "Describe the 1NF, 2NF, and 3NF normalization forms.",
                "explanation": "1NF requires atomic values and no repeating groups. 2NF requires 1NF and no partial dependencies on primary keys. 3NF requires 2NF and no transitive dependencies."
            },
            {
                "text": "What are database views and why are they used?",
                "explanation": "A view is a virtual table representing the result of a saved SQL query. It is used to simplify complex queries, enforce security, and provide data abstraction."
            },
            {
                "text": "Explain transaction isolation levels.",
                "explanation": "Isolation levels control transaction visibility. Levels from lowest to highest isolation: Read Uncommitted, Read Committed, Repeatable Read, and Serializable."
            },
            {
                "text": "What is database denormalization and when is it appropriate?",
                "explanation": "Denormalization adds redundant data to speed up complex queries. It is used in read-heavy applications or data warehouses to reduce join overhead."
            },
            {
                "text": "What is a database deadlock and how is it resolved?",
                "explanation": "A deadlock occurs when two transactions wait for locks held by each other. The database engine resolves deadlocks by killing one transaction, rolling back its changes."
            },
            {
                "text": "Explain the differences between replication and sharding.",
                "explanation": "Replication copies the entire database across servers for read capacity and redundancy. Sharding partitions data subsets across servers to distribute write load and storage."
            },
            {
                "text": "What is a database cursor?",
                "explanation": "A database cursor is a control structure that enables traversal over query result rows one by one, allowing procedural processing of SQL results."
            },
            {
                "text": "Explain ACID versus BASE.",
                "explanation": "ACID guarantees strict consistency for relational databases. BASE (Basically Available, Soft state, Eventual consistency) prioritizes availability and scalability for NoSQL systems."
            },
            {
                "text": "What are triggers and stored procedures?",
                "explanation": "Stored procedures are precompiled SQL statements executed on request. Triggers are SQL scripts executed automatically in response to database events (like INSERT, UPDATE)."
            }
        ],
        "hard": [
            {
                "text": "Explain how Multi-Version Concurrency Control (MVCC) works.",
                "explanation": "MVCC provides concurrent database access by keeping multiple physical versions of a data row. Readers do not block writers, and writers do not block readers, ensuring consistent snapshots."
            },
            {
                "text": "Describe the difference between Write-Ahead Logging (WAL) and shadowing.",
                "explanation": "WAL writes modifications to a sequential log on disk before modifying actual database pages, ensuring recovery. Shadowing writes updates to duplicate pages, swapping pointers on commit."
            },
            {
                "text": "Explain the Two-Phase Commit (2PC) protocol in distributed databases.",
                "explanation": "2PC achieves consensus in distributed transactions. In the Prepare phase, the coordinator asks participants if they can commit. In the Commit phase, it commands them to commit or abort based on responses."
            },
            {
                "text": "What is a database split-brain scenario and how is it mitigated?",
                "explanation": "Split-brain happens when communication fails between database replicas, and multiple nodes claim to be primary. It is mitigated using quorum voting or fencing mechanisms."
            },
            {
                "text": "Explain the internal structure of B+ Trees and why databases prefer them over B-Trees.",
                "explanation": "B+ Trees store actual data records only in leaf nodes, while internal nodes store keys/pointers. Leaves are linked sequentially, optimizing range scans and maximizing page key density."
            },
            {
                "text": "Describe indexing strategies for NoSQL databases (e.g., secondary indexes in DynamoDB).",
                "explanation": "DynamoDB uses Global Secondary Indexes (GSIs) and Local Secondary Indexes (LSIs). LSIs share the partition key but have a different sort key, while GSIs partition and sort by completely different attributes."
            },
            {
                "text": "Explain phantom reads and how databases prevent them under Repeatable Read.",
                "explanation": "A phantom read happens when a transaction queries a range, and another transaction inserts rows matching the range. Prevented using range locks (next-key locks) in InnoDB or serialization."
            },
            {
                "text": "Describe log-structured merge (LSM) trees and compaction strategies.",
                "explanation": "LSM trees write to MemTable, flushing to SSTables. Compaction (Leveled or Size-Tiered) merges and deduplicates SSTables sequentially to reclaim space and optimize future reads."
            },
            {
                "text": "Explain the difference between row-oriented and column-oriented databases.",
                "explanation": "Row-oriented stores rows contiguously, ideal for transactional (OLTP) writes. Column-oriented stores columns contiguously, ideal for analytical (OLAP) aggregations on specific fields."
            },
            {
                "text": "What is database replication lag and how do you handle it in a master-slave system?",
                "explanation": "Lag is the delay for updates to reach slaves. Mitigated by routing critical reads to the master, using synchronous replication for key transactions, or enforcing sticky sessions to read from the master after writes."
            }
        ]
    },
    "python": {
        "easy": [
            {
                "text": "What is the key difference between a list and a tuple in Python?",
                "explanation": "Lists are mutable, meaning their elements can be modified after creation. Tuples are immutable, meaning they cannot be modified once created."
            },
            {
                "text": "What is PEP 8?",
                "explanation": "PEP 8 is the official Style Guide for Python Code, providing guidelines and best practices for writing readable and consistent Python code."
            },
            {
                "text": "Explain list comprehensions in Python.",
                "explanation": "List comprehensions offer a concise syntax to create new lists from existing iterables by evaluating an expression for each item."
            },
            {
                "text": "What is the purpose of the '__init__' method in Python?",
                "explanation": "The '__init__' method is Python's constructor, called automatically to initialize the attributes of a new object when it is created."
            },
            {
                "text": "What is the difference between 'is' and '=='?",
                "explanation": "The 'is' operator checks if two references point to the exact same object in memory. The '==' operator checks if the values of the two objects are equal."
            },
            {
                "text": "What is a docstring?",
                "explanation": "A docstring is a string literal written as the first statement in a module, function, class, or method, used to document what the code does."
            },
            {
                "text": "Explain the use of 'try...except' blocks in Python.",
                "explanation": "The 'try...except' block is used for exception handling. Code in the 'try' block runs, and if an exception occurs, execution jumps to the 'except' block to handle the error."
            },
            {
                "text": "What is the difference between range() and xrange()?",
                "explanation": "In Python 2, range() returns a list in memory while xrange() returns a generator object. In Python 3, range() behaves like xrange() and returns a generator."
            },
            {
                "text": "What are Python decorators?",
                "explanation": "Decorators are functions that take another function as an argument, extending or modifying its behavior without changing its source code directly."
            },
            {
                "text": "What is a lambda function in Python?",
                "explanation": "A lambda function is a small, anonymous, single-expression function defined using the 'lambda' keyword, often used for short, throwaway operations."
            }
        ],
        "medium": [
            {
                "text": "Explain the Global Interpreter Lock (GIL) and its impact on multi-threading.",
                "explanation": "The GIL is a mutex in CPython preventing multiple threads from executing Python bytecodes at once, restricting CPU-bound tasks to a single core."
            },
            {
                "text": "What is a generator and how does the 'yield' keyword work?",
                "explanation": "A generator is an iterator created using a function containing 'yield'. When called, yield pauses execution and returns a value, resuming from that spot on the next request."
            },
            {
                "text": "Explain the difference between deepcopy and copy in Python.",
                "explanation": "copy() creates a shallow copy, duplicating outer references. deepcopy() recursively copies all nested objects, creating a completely independent duplicate."
            },
            {
                "text": "What are '*args' and '**kwargs' used for in function definitions?",
                "explanation": "'*args' allows a function to accept a variable number of positional arguments as a tuple. '**kwargs' allows a function to accept a variable number of keyword arguments as a dictionary."
            },
            {
                "text": "Explain how memory management and garbage collection work in Python.",
                "explanation": "Python uses reference counting to automatically delete objects whose reference count drops to zero. It also uses a cyclic garbage collector to detect and clean up reference cycles."
            },
            {
                "text": "What are dunder (double underscore) methods? Give an example.",
                "explanation": "Dunder methods (like '__str__' or '__len__') are special pre-defined methods in Python classes that allow objects to hook into native syntax and operators."
            },
            {
                "text": "What is the difference between static methods (@staticmethod) and class methods (@classmethod)?",
                "explanation": "Class methods take 'cls' as their first argument and can access class attributes. Static methods take no implicit arguments and behave like regular functions bound to the class namespace."
            },
            {
                "text": "Explain the concept of decorators and how to write a custom one.",
                "explanation": "A decorator wraps a function. A custom decorator is a function returning a nested wrapper function that executes additional logic before or after the wrapped function."
            },
            {
                "text": "What is a context manager and how does the 'with' statement work?",
                "explanation": "A context manager sets up and tears down resources. The 'with' statement automates this by executing the object's '__enter__' and '__exit__' methods automatically."
            },
            {
                "text": "Explain method resolution order (MRO) in Python multiple inheritance.",
                "explanation": "MRO is the order in which Python searches for a method in a class hierarchy. It uses the C3 Linearization algorithm to maintain hierarchy consistency."
            }
        ],
        "hard": [
            {
                "text": "Explain how Python descriptors work and their role in properties and methods.",
                "explanation": "Descriptors are objects defining any of '__get__', '__set__', or '__delete__' methods. Properties, methods, classmethods, and staticmethods are all implemented using the descriptor protocol."
            },
            {
                "text": "Describe how asynchronous programming works in Python using 'asyncio'.",
                "explanation": "asyncio uses an event loop to run coroutines. When a coroutine awaits an I/O operation, the event loop pauses it and runs other tasks, achieving concurrency on a single thread."
            },
            {
                "text": "Explain how Python's metaclasses work and when you would use them.",
                "explanation": "A metaclass is the class of a class. It defines how a class is constructed. You use them to automatically modify or validate classes during module load time."
            },
            {
                "text": "Describe how the CPython compiler optimizes list and dictionary access internally.",
                "explanation": "CPython lists are dynamic arrays of pointers. CPython dictionaries are hash tables using open addressing, utilizing index tables to minimize memory and collision overhead."
            },
            {
                "text": "Explain the concept of weak references (weakref) and when to use them.",
                "explanation": "A weak reference is a reference that does not prevent the object from being garbage collected. Used to build caches or circular structures without causing memory leaks."
            },
            {
                "text": "Describe the difference between frame objects, code objects, and function objects in CPython.",
                "explanation": "Code objects represent compiled bytecode (read-only). Function objects wrap code objects, adding environment bindings (closures, defaults). Frame objects represent execution frames on the stack."
            },
            {
                "text": "How does memory allocation for small objects work in CPython (PyMalloc)?",
                "explanation": "CPython bypasses the OS allocator for small objects (<= 512 bytes) using PyMalloc. It allocates memory in Arenas, Pools, and Blocks, optimizing speed and reducing fragmentation."
            },
            {
                "text": "Explain how to write a C extension for Python and memory management between C and CPython.",
                "explanation": "C extensions define module methods calling PyObject APIs. C code must manually manage Python reference counts using Py_INCREF and Py_DECREF to prevent leaks and crashes."
            },
            {
                "text": "Describe how Python's import system resolves modules and imports circular dependencies.",
                "explanation": "The import system checks 'sys.modules' cache first, searching 'sys.path' if missing. Circular imports fail if they reference uninitialized module attributes before the import completes."
            },
            {
                "text": "Explain the GIL release mechanism in C extensions or I/O bound tasks.",
                "explanation": "CPython automatically releases the GIL during blocking I/O calls or when explicitly triggered in C extensions using 'Py_BEGIN_ALLOW_THREADS' blocks, enabling parallel execution."
            }
        ]
    },
    "frontend": {
        "easy": [
            {
                "text": "What is the DOM?",
                "explanation": "The Document Object Model (DOM) is a programming interface representing HTML documents as a node tree, allowing languages like JavaScript to modify structure and styles."
            },
            {
                "text": "What is the difference between HTML and CSS?",
                "explanation": "HTML defines the structure and content of a web page. CSS defines the styling, layout, and visual presentation of that content."
            },
            {
                "text": "What is a CSS selector?",
                "explanation": "A CSS selector is a pattern used to select and target HTML elements for styling (such as class selectors, ID selectors, and attribute selectors)."
            },
            {
                "text": "Explain the box model in CSS.",
                "explanation": "The CSS box model treats every HTML element as a box composed of: Content (text/images), Padding (internal space), Border (edge line), and Margin (external space)."
            },
            {
                "text": "What is a React component?",
                "explanation": "A React component is a modular, reusable block of UI code that returns JSX (HTML structure) and manages its own state and lifecycle."
            },
            {
                "text": "What is the difference between let, const, and var in JavaScript?",
                "explanation": "var is function-scoped and hoisted. let and const are block-scoped. const variables cannot be reassigned after initialization, while let variables can."
            },
            {
                "text": "What is a callback function?",
                "explanation": "A callback is a function passed as an argument to another function, intended to be executed after some event or asynchronous task completes."
            },
            {
                "text": "What is the purpose of the 'alt' attribute on an image tag?",
                "explanation": "The 'alt' attribute provides alternative description text for screen readers (accessibility) and displays if the image fails to load."
            },
            {
                "text": "What is CSS Flexbox?",
                "explanation": "Flexbox (Flexible Box Layout) is a one-dimensional layout model providing space distribution and alignment capabilities among items in a container."
            },
            {
                "text": "What is the difference between client-side rendering (CSR) and server-side rendering (SSR)?",
                "explanation": "CSR downloads a blank HTML shell and executes JS in the browser to build the page. SSR pre-renders the full HTML on the server for each request, improving SEO."
            }
        ],
        "medium": [
            {
                "text": "Explain closures in JavaScript and give a practical example.",
                "explanation": "A closure is when a function remembers its outer lexical environment. Practical example: a function generating private counters by returning nested functions."
            },
            {
                "text": "What is the Virtual DOM and how does React's reconciliation work?",
                "explanation": "The Virtual DOM is an in-memory representation of real DOM nodes. Reconciliation compares the Virtual DOM diffs using a diffing algorithm, writing only changes to the real DOM."
            },
            {
                "text": "Explain the difference between 'useEffect' and 'useLayoutEffect' in React.",
                "explanation": "useEffect runs asynchronously after the browser paints the screen. useLayoutEffect runs synchronously after DOM mutations but before the browser paints, preventing flickers."
            },
            {
                "text": "What is event bubbling and capturing in the DOM?",
                "explanation": "Event capturing propagates the event down from the root to the target element. Event bubbling propagates the event up from the target back to the root node."
            },
            {
                "text": "Explain CSS Grid vs Flexbox and when to use which.",
                "explanation": "Flexbox is designed for one-dimensional layouts (rows OR columns). CSS Grid is designed for two-dimensional layouts (rows AND columns simultaneously)."
            },
            {
                "text": "What is the JavaScript event loop and how do microtasks and macrotasks differ?",
                "explanation": "The event loop coordinates execution. Microtasks (promises, queueMicrotask) run immediately after the current script. Macrotasks (setTimeout, events) run in the next loop tick."
            },
            {
                "text": "Explain the difference between 'interface' and 'type' in TypeScript.",
                "explanation": "Interfaces are open for declaration merging (adding fields later) and extend other classes/interfaces. Types are closed and can represent unions, intersections, and primitives."
            },
            {
                "text": "What is React context and how does it compare to state management libraries like Redux?",
                "explanation": "React Context passes values down without prop-drilling, but triggers re-renders on all consumers. Redux uses a central store with selectors, optimizing selective component updates."
            },
            {
                "text": "Explain promise chains vs async/await in JavaScript.",
                "explanation": "Promise chains use '.then()' and '.catch()' methods. async/await is syntactic sugar over promises, allowing asynchronous code to be written sequentially with try/catch."
            },
            {
                "text": "What is cross-origin resource sharing (CORS) and how does it work?",
                "explanation": "CORS is a browser security mechanism. It uses HTTP headers (like Access-Control-Allow-Origin) sent by the server to authorize browsers to read resource responses."
            }
        ],
        "hard": [
            {
                "text": "Explain how the React Fiber architecture works and its scheduling phase.",
                "explanation": "React Fiber is a rewrite of React's core reconciliation algorithm. It supports incremental rendering, breaking work into chunks and prioritizing updates using a scheduler."
            },
            {
                "text": "Describe micro-frontends architecture and how module federation works.",
                "explanation": "Micro-frontends split a website into independent applications. Module Federation allows Webpack/Vite bundles to load dynamically compiled code from other remote projects at runtime."
            },
            {
                "text": "Explain how the browser rendering pipeline works (DOM, CSSOM, Render Tree, Layout, Paint, Composite).",
                "explanation": "The browser parses HTML to DOM and CSS to CSSOM, combines them into a Render tree, calculates sizes/positions (Layout), draws pixels (Paint), and blends layers (Composite) on the GPU."
            },
            {
                "text": "Describe React Server Components (RSC) and how they differ from SSR.",
                "explanation": "SSR renders HTML on the server and hydrates it with JS on the client. RSCs execute solely on the server, generating static JSX streamed to the client without client-side bundle size."
            },
            {
                "text": "Explain how JavaScript engines (like V8) optimize code execution (hidden classes, inline caches).",
                "explanation": "V8 assigns hidden classes to objects with matching layouts, allowing fast property lookups. Inline caches remember lookup offsets, bypassing slow dictionary lookups during loops."
            },
            {
                "text": "Describe strategies for optimizing Web Vitals (LCP, FID/INP, CLS) in a Next.js application.",
                "explanation": "Optimized by using next/image (LCP/CLS), deferring non-critical JS (INP), dynamic code splitting, optimizing font loading, pre-sizing ad containers, and utilizing ISR caching."
            },
            {
                "text": "Explain how WebSockets and Server-Sent Events (SSE) differ and when to use HTTP/2 push.",
                "explanation": "WebSockets are full-duplex TCP connections. SSE is a uni-directional stream over standard HTTP. HTTP/2 push sends assets to client caches proactively before requested."
            },
            {
                "text": "Describe security threats in frontend (XSS, CSRF, Clickjacking) and how Content Security Policy (CSP) mitigates them.",
                "explanation": "CSP is an HTTP header specifying trusted resource domains. It prevents XSS by disabling inline scripts and restricting fetch locations, and clickjacking by blocking iframe rendering."
            },
            {
                "text": "Explain how state managers like MobX (observables) differ from React state (immutability) under the hood.",
                "explanation": "React uses immutable state comparison to trigger renders. MobX uses ES6 Proxies to detect read/writes on observables, executing re-renders automatically for matching components."
            },
            {
                "text": "Describe the structure and purpose of source maps in build tools.",
                "explanation": "Source maps map compiled, minified production JavaScript back to original source files, allowing developers to debug clean source code directly inside browser DevTools."
            }
        ]
    }
}
