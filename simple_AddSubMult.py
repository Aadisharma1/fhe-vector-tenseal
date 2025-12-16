import tenseal as ts
import numpy as np
import time

def create_context():
    
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    context.generate_galois_keys()
    return context

def run_scalable_benchmark(vector_size=784):
    """
    Runs HE operations on vectors of size N.
    Default 784 corresponds to a flattened 28x28 MNIST image.
    """
    print(f"STARTING BENCHMARK (Vector Size: {vector_size})")
    
    # 1. Setup contxet
    ctx = create_context()
    print(f"[+] Context Created. Max Batch Size (Slots): {ctx.max_slots()}")

    # 2. Data Gen
    np.random.seed(42)
    vec_a = np.random.rand(vector_size)
    vec_b = np.random.rand(vector_size)
    
    print(f"[+] Generated 2 random vectors of size {vector_size}")

    # 3. Encryption
    start_time = time.time()
    enc_a = ts.ckks_vector(ctx, vec_a)
    enc_b = ts.ckks_vector(ctx, vec_b)
    enc_time = time.time() - start_time
    print(f"[+] Encryption Complete. Time: {enc_time:.4f}s")

    # 4. Computation
    start_time = time.time()
    
    enc_sum = enc_a + enc_b
    enc_sub = enc_a - enc_b  
    enc_prod = enc_a * enc_b 
    
    compute_time = time.time() - start_time
    print(f"[+] Computation (Add, Sub, Mult) Complete. Time: {compute_time:.4f}s")

    # 5. Decryption & Verification
    start_time = time.time()
    res_sum = enc_sum.decrypt()
    res_sub = enc_sub.decrypt() 
    res_prod = enc_prod.decrypt()
    dec_time = time.time() - start_time
    print(f"[+] Decryption Complete. Time: {dec_time:.4f}s")

    # 6. Accuracy Check (MSE)
    actual_sum = vec_a + vec_b
    actual_sub = vec_a - vec_b   
    actual_prod = vec_a * vec_b
    
    # Calculate Mean Squared Error
    mse_sum = np.mean((np.array(res_sum) - actual_sum)**2)
    mse_sub = np.mean((np.array(res_sub) - actual_sub)**2) 
    mse_prod = np.mean((np.array(res_prod) - actual_prod)**2)

    print("\nACCURACY REPORT-")
    print(f"MSE (Addition):       {mse_sum:.10f}")
    print(f"MSE (Subtraction):    {mse_sub:.10f}")
    print(f"MSE (Multiplication): {mse_prod:.10f}")
    
    if mse_prod < 1e-5:
        print(">> SUCCESS: Accuracy is within acceptable bounds for ML.")
    else:
        print(">> WARNING: High noise detected. Parameters may need tuning.")

if __name__ == "__main__":
    run_scalable_benchmark(vector_size=784)
    # run_scalable_benchmark(vector_size=4096)