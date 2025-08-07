Parallel & Distributed Computing Exercises
==========================================

This repository contains the solutions for the laboratory exercises of the "Parallel and Distributed Computing" course.

*   **Institution:** University of Macedonia (UoM)
    
*   **Department:** Applied Informatics
    
*   **Academic Year:** 2023-2024
    

📝 Description
--------------

The purpose of this repository is to archive and present the solutions developed during the course's laboratory sessions. The exercises were implemented in **Python** and cover a wide range of topics, from basic parallelism with threads and processes to complex synchronization problems, distributed algorithms, and network programming (sockets, RMI).

📂 Repository Structure
-----------------------

The repository is organized into folders, where each folder corresponds to a laboratory session (Lab).

🔬 Labs Overview
----------------

**Lab 1: Introduction to Threads**

*   **Content:** Basic creation and management of threads using the threading library.
    
*   **Techniques:** Inheriting from the Thread class, start() and join() methods.
    

**Lab 3: Data Parallelism**

*   **Content:** Application of parallel computations on vectors, matrices, and image processing (grayscale conversion, saturation adjustment).
    
*   **Techniques:** Using multiprocessing to leverage multiple cores for computationally intensive tasks.
    

**Lab 4: Synchronization Problems & Race Conditions**

*   **Content:** Investigating the "Race Condition" phenomenon through shared counters and introducing synchronization mechanisms.
    
*   **Techniques:** multiprocessing.Value, multiprocessing.Array, multiprocessing.Lock.
    

**Lab 5: Parallel Computation Algorithms**

*   **Content:** Implementation of parallel algorithms for numerical integration (calculating π) and the Monte Carlo method.
    
*   **Techniques:** Synchronizing access to shared variables using Lock.
    

**Lab 6: Workload Distribution Strategies**

*   **Content:** Implementation of parallel string search (Brute-force) and the Sieve of Eratosthenes for finding prime numbers.
    
*   **Techniques:** Comparison of different data distribution strategies (static, cyclic, dynamic) in parallel systems.
    

**Lab 7: Classic Synchronization Problems**

*   **Content:** Implementation of solutions for classic problems like the **Producer-Consumer** (SPSC, MPSC, SPMC) and the **Cyclic Barrier**.
    
*   **Techniques:** Using advanced synchronization mechanisms like Semaphore, Condition, and Event with both threading and multiprocessing.
    

**Lab 8 & 9: Network Programming & Concurrent Servers**

*   **Content:** Creation of a simple, iterative TCP Echo Server and its conversion to a multithreaded one to serve multiple clients concurrently.
    
*   **Techniques:** socket, bind(), listen(), accept(), sending and receiving data, serialization with pickle.
    

**Lab 10: Distributed Applications (Master-Worker)**

*   **Content:** Development of two distributed applications: a multithreaded Chat Server and a Master-Worker system for the parallel calculation of π.
    
*   **Techniques:** Client-Server architecture, Master-Worker pattern.
    

**Lab 11: Remote Method Invocation (RMI)**

*   **Content:** Implementation of RMI for calling remote methods. Creation of a simple Echo Server with RMI and its extension to a distributed Master-Worker system.
    
*   **Techniques:** Simulating RMI over TCP sockets, sending objects, and executing methods on remote machines.
    

⚠️ Disclaimer
-------------

This code is provided for **educational and archival purposes only**. It should not be used as a means of copying or plagiarism for solving corresponding university assignments. Plagiarism is a serious academic offense.
