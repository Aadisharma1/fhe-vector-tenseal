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

```

Copy code
python fhe_vector_arithmetic_tenseal.py
The script will:

Initialize a CKKS encryption context

Encrypt two vectors

Perform addition, subtraction, and multiplication homomorphically

Decrypt and display results

Report approximation error introduced by CKKS

