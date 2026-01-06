import tenseal as ts
import numpy as np
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class SecureVectorEngine:
    """
    Handles CKKS context initialization and secure vector operations.
    """
    def __init__(self, poly_modulus_degree=8192, coeff_mod_bit_sizes=None):
        if coeff_mod_bit_sizes is None:
            coeff_mod_bit_sizes = [60, 40, 40, 60]
            
        self.poly_modulus_degree = poly_modulus_degree
        self.coeff_mod_bit_sizes = coeff_mod_bit_sizes
        self.context = self._build_context()

    def _build_context(self):
        try:
            ctx = ts.context(
                ts.SCHEME_TYPE.CKKS,
                poly_modulus_degree=self.poly_modulus_degree,
                coeff_mod_bit_sizes=self.coeff_mod_bit_sizes
            )
            ctx.global_scale = 2**40
            ctx.generate_galois_keys()
            return ctx
        except Exception as e:
            logger.error(f"Failed to initialize TenSEAL context: {e}")
            raise

    def get_max_slots(self):
        return self.context.max_slots()

    def encrypt(self, vector):
        return ts.ckks_vector(self.context, vector)

class BenchmarkRunner:
    def __init__(self, vector_size=784):
        self.vector_size = vector_size
        self.engine = SecureVectorEngine()
        
        max_slots = self.engine.get_max_slots()
        if self.vector_size > max_slots:
            raise ValueError(f"Vector size ({self.vector_size}) exceeds context max slots ({max_slots}).")

    def _generate_data(self):
        # Generate normalized float data
        np.random.seed(42) 
        return np.random.rand(self.vector_size), np.random.rand(self.vector_size)

    def _calculate_mse(self, actual, decrypted):
        return np.mean((np.array(decrypted) - actual) ** 2)

    def run(self):
        logger.info(f"--- Running Secure Benchmark (N={self.vector_size}) ---")
        
        # Prepare Data
        vec_a, vec_b = self._generate_data()
        
        # SOME FIXES TO BE MADE HERE ASK THE PROFESSOR
        t_start = time.perf_counter()
        enc_a = self.engine.encrypt(vec_a)
        enc_b = self.engine.encrypt(vec_b)
        duration_enc = time.perf_counter() - t_start
        logger.info(f"Encryption Time:      {duration_enc:.5f}s")

    
        t_start = time.perf_counter()
        
        enc_add = enc_a + enc_b
        enc_sub = enc_a - enc_b
        enc_mult = enc_a * enc_b
        
        duration_compute = time.perf_counter() - t_start
        logger.info(f"Computation Time:     {duration_compute:.5f}s (Add, Sub, Mult)")

        #Decryption
        t_start = time.perf_counter()
        
        dec_add = enc_add.decrypt()
        dec_sub = enc_sub.decrypt()
        dec_mult = enc_mult.decrypt()
        
        duration_dec = time.perf_counter() - t_start
        logger.info(f"Decryption Time:      {duration_dec:.5f}s")

        #Accuracy Veification
        self._verify_results(vec_a, vec_b, dec_add, dec_sub, dec_mult)

    def _verify_results(self, vec_a, vec_b, dec_add, dec_sub, dec_mult):
        true_add = vec_a + vec_b
        true_sub = vec_a - vec_b
        true_mult = vec_a * vec_b

        # Error Metrics
        mse_add = self._calculate_mse(true_add, dec_add)
        mse_sub = self._calculate_mse(true_sub, dec_sub)
        mse_mult = self._calculate_mse(true_mult, dec_mult)

        logger.info(f"\n--- Precision Report (MSE) ---")
        logger.info(f"Addition Error:       {mse_add:.5e}")
        logger.info(f"Subtraction Error:    {mse_sub:.5e}")
        logger.info(f"Multiplication Error: {mse_mult:.5e}")

        #Validation Threshold
        if mse_mult < 1e-5:
            logger.info(">> Validation: PASSED")
        else:
            logger.warning(">> Validation: FAILED (High Noise Detected)")

if __name__ == "__main__":
    try:
        runner = BenchmarkRunner(vector_size=784)
        runner.run()
    except Exception as e:
        logger.critical(f"Benchmark failed: {e}")
