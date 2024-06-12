import os
import numpy as np
from scipy.fftpack import fft
import hashlib
from concurrent.futures import ProcessPoolExecutor, as_completed

def extract_entropy_per_segment(segment):
    try:
        # Apply FFT
        freq_data = np.abs(fft(segment))

        # Convert to binary and extract bits directly from FFT output
        binary_data = ''.join(format(int(f), '016b') for f in freq_data)

        # Apply hash for unbiasing
        hash_output = hashlib.sha256(binary_data.encode()).digest()
        return ''.join(format(byte, '08b') for byte in hash_output)
    except Exception as e:
        print(f"Exception in segment processing: {e}")
        return ""
    
def extract_entropy(audio_data, segment_size=1024, overlap=1024):
    entropy_bits = []
    num_segments = (len(audio_data) - segment_size) // overlap + 1

    max_workers = os.cpu_count() // 2
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i in range(num_segments):
            start = i * overlap
            end = start + segment_size
            segment = audio_data[start:end]

            if len(segment) < segment_size:
                print(f"Skipping segment {i} because its length is {len(segment)}")
                continue

            print(f"Processing segment {i} from {start} to {end}")
            futures.append(executor.submit(extract_entropy_per_segment, segment))

        for future in as_completed(futures):
            try:
                result = future.result()
                entropy_bits.append(result)
            except Exception as e:
                print(f"Exception in future result: {e}")
    
    return "".join(entropy_bits)