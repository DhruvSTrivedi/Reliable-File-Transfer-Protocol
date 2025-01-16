# 🛠 Computer Networks: Reliable File Transfer Protocol

**Author**: Dhruv Trivedi  
**Course**: CS 436 - Networks and Distributed Computer Systems  
**Instructor**: Noura Limam

---

## 🔍 Overview

This project implements a **reliable file transfer protocol**, facilitating the transfer of text files from one host to another over **UDP**. Designed to tackle network errors efficiently, the protocol offers **unidirectional data flow**—transferring data from the sender to the receiver while acknowledgements (ACKs) flow in the opposite direction.

---

## 📊 Prerequisites

- **Python Version**: Ensure you have Python 3.6 or higher installed.
- **Logs & Output**: Before testing, remove the output file and all four log files:
  - `ack.log`
  - `arrival.log`
  - `drop.log`
  - `seqnum.log`

---

## 🚀 Running the Program

### 1. Start the Receiver

Navigate to the `source` directory:

```bash
cd ./source
```

The receiver program accepts three command-line arguments: `<receiver_port>`, `<drop_probability>`, and `<output_filename>`.

Execute the command:

```bash
python3 receiver.py <receiver_port> <drop_probability> <output_filename>
```

**Example**:

```bash
python3 receiver.py 9994 0.5 output.txt
```

### 2. Run the Sender

Once the receiver is up and running, initiate the sender. The sender needs five command-line arguments: `<receiver_hostname>`, `<receiver_port>`, `<sender_port>`, `<timeout(in milliseconds)>`, and `<input_filename>`.

Execute the command:

```bash
python3 sender.py <receiver_hostname> <receiver_port> <sender_port> <timeout> <input_filename>
```

**Example**:

```bash
python3 sender.py ubuntu2004-010 9994 9992 50 input.txt
```

---

## 🌐 Test Environments

The program has been successfully tested on the following machines:

1. **🔹 Hostname**: ubuntu2004-008.student.cs.uwaterloo.ca  
   **CPU**: Intel(R) Xeon(R) CPU E5-2697A v4 @ 2.60GHz  
   **Make**: Dell Inc.

2. **🔹 Hostname**: ubuntu2004-010.student.cs.uwaterloo.ca  
   **CPU**: Intel(R) Xeon(R) Gold 6148 CPU @ 2.40GHz  
   **Make**: Supermicro

---

