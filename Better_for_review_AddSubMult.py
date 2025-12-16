
import tenseal as ts
import numpy as np
import time

class SecureInferenceBenchmark:
    def __init__(self, vector_size=784):
        """
        Initialize the HE Context.
        vector_size: 784 corresponds to a flattened 28x28 MedMNIST image.
        """
        self.vector_size = vector_size
        self.ctx = self._create_context()
        
    def _create_context(self):
        """
        Creates a TenSEAL context optimized for arithmetic on floating point numbers (CKKS).
        - poly_modulus_degree=8192: Standard security (approx 128-bit).
        - coeff_mod_bit_sizes: Defines the noise budget for multiplications.
        """
        print(f"[Init] Initializing TenSEAL Context (CKKS Scheme)...")
        context = ts.context(
            ts.SCHEME_TYPE.CKKS,
            poly_modulus_degree=8192,
            coeff_mod_bit_sizes=[60, 40, 40, 60]
        )
        context.global_scale = 2**40
        context.generate_galois_keys()
        print(f"[Init] Context Ready. Max SIMD Slots: {context.max_slots()}")
        return context

    def generate_dummy_data(self):
        
        #  Generates random normalized data [0,1] simulating pixel intensities
        
        np.random.seed(42)  
        # Simulating two flattened images or an image and a weight vector
        vec_a = np.random.rand(self.vector_size)
        vec_b = np.random.rand(self.vector_size)
        return vec_a, vec_b

    def run_benchmark(self):
        
        #Executes the Encrypt -> Compute -> Decrypt pipeline and measures metrics.
        
        vec_a, vec_b = self.generate_dummy_data()
        
        print(f"\n[Benchmark] Starting Pipeline for Vector Size: {self.vector_size}")
        print("-" * 60)

        # 1. Encryption (Client Side)
        t0 = time.time()
        enc_a = ts.ckks_vector(self.ctx, vec_a)
        enc_b = ts.ckks_vector(self.ctx, vec_b)
        t_enc = time.time() - t0
        print(f"1. Encryption Time:       {t_enc:.4f} sec")

        # 2. Computation (Server Side)
        # Simulating a linear layer operation (Dot product approximation via element-wise mult + sum)
        t0 = time.time()
        enc_sum = enc_a + enc_b
        enc_prod = enc_a * enc_b
        t_ops = time.time() - t0
        print(f"2. Computation Time:      {t_ops:.4f} sec (Add + Mult)")

        # 3. Decryption (Client Side)
        t0 = time.time()
        dec_sum = enc_sum.decrypt()
        dec_prod = enc_prod.decrypt()
        t_dec = time.time() - t0
        print(f"3. Decryption Time:       {t_dec:.4f} sec")

        # 4. Accuracy Verification (MSE)
        self._verify_accuracy(vec_a, vec_b, dec_sum, dec_prod)

    def _verify_accuracy(self, vec_a, vec_b, dec_sum, dec_prod):
        
    # Compares encrypted results against plaintext ground truth.
    
        # Ground Truth
        true_sum = vec_a + vec_b
        true_prod = vec_a * vec_b

        # Mean Squared Error
        mse_sum = np.mean((np.array(dec_sum) - true_sum) ** 2)
        mse_prod = np.mean((np.array(dec_prod) - true_prod) ** 2)

        print("-" * 60)
        print("ACCURACY REPORT (Noise Analysis)")
        print(f"MSE (Addition):       {mse_sum:.10f}")
        print(f"MSE (Multiplication): {mse_prod:.10f}")

        if mse_prod < 1e-5:
            print(">> STATUS: PASSED. Noise is within acceptable limits for ML.")
        else:
            print(">> STATUS: WARNING. High noise detected. Check bit_sizes.")
        print("-" * 60)

if __name__ == "__main__":
    # 784 represents a flattened 28x28 MedMNIST image
    benchmark = SecureInferenceBenchmark(vector_size=784)
    benchmark.run_benchmark()