# Fully Homomorphic Encrypted Vector Arithmetic using TenSEAL

This repository demonstrates **vector addition, subtraction, and multiplication**
performed directly on **encrypted data** using **Fully Homomorphic Encryption (FHE)**.

The implementation uses the **CKKS scheme** via the **TenSEAL** library, which enables
approximate arithmetic on real-valued vectors — a common requirement in
privacy-preserving machine learning and secure federated learning.

---

## 🔐 Key Concepts

- Fully Homomorphic Encryption (FHE)
- CKKS approximate arithmetic scheme
- Encrypted vector operations
- Noise-aware computation
- Secure computation without plaintext access

---

## 📁 Project Structure

.
├── fhe_vector_arithmetic_tenseal.py
└── README.md

yaml
Copy code

---

## ⚙️ Requirements

- Python 3.8+
- TenSEAL

Install dependencies using:

```bash
pip install tenseal
▶️ How to Run
bash
Copy code
python fhe_vector_arithmetic_tenseal.py
The script will:

Initialize a CKKS encryption context

Encrypt two vectors

Perform addition, subtraction, and multiplication homomorphically

Decrypt and display results

Report approximation error introduced by CKKS

🧪 Operations Supported
Encrypted Vector Addition

Encrypted Vector Subtraction

Encrypted Vector Multiplication (element-wise)

All operations are performed without decrypting intermediate values.

🎯 Academic Relevance
This code can serve as:

A minimal research demo for FHE

A base for secure federated learning aggregation

A teaching example for CKKS-based encrypted computation

📌 Notes
CKKS introduces small numerical errors due to its approximate nature

Cryptographic parameters are chosen for ~128-bit security

Multiplicative depth is limited by coefficient modulus chain
