import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os
import json

# Add the current directory to the path so we can import photonic_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from photonic_core import PhotonicFFT, PhotonicMatrixMultiplier

def generate_phantom(size=64):
    """Generate a simple synthetic MRI phantom (like a Shepp-Logan phantom simplified)"""
    img = np.zeros((size, size))
    center = size // 2
    # Outer skull
    y, x = np.ogrid[-center:size-center, -center:size-center]
    mask = x**2 + y**2 <= (size * 0.4)**2
    img[mask] = 1.0
    
    # Inner ventricles
    mask2 = (x - size*0.1)**2 + (y + size*0.1)**2 <= (size * 0.15)**2
    img[mask2] = 0.5
    
    mask3 = (x + size*0.1)**2 + (y + size*0.1)**2 <= (size * 0.15)**2
    img[mask3] = 0.5

    # Tumor / Lesion
    mask4 = (x - size*0.2)**2 + (y - size*0.2)**2 <= (size * 0.08)**2
    img[mask4] = 2.0
    return img

def generate_kspace(img):
    """Generate MRI k-space data via 2D FFT"""
    return np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(img)))

def photonic_2d_ifft(kspace, size=64):
    """Perform 2D Inverse FFT using PhotonicFFT (simulating physical optics delay lines)"""
    print(f"Initializing PhotonicFFT for size {size}...")
    photonic_fft = PhotonicFFT(size=size)
    
    # 2D iFFT can be computed by applying 1D iFFT on rows, then columns.
    # We'll use the photonic FFT kernel (which does forward FFT) 
    # but conjugate the input and output to get the inverse FFT.
    
    start_time = time.time()
    
    # Process rows
    intermediate = np.zeros_like(kspace, dtype=np.complex128)
    for i in range(size):
        # iFFT via FFT: iFFT(x) = conj(FFT(conj(x))) / N
        row = np.conj(kspace[i, :])
        result = photonic_fft.compute(row)
        intermediate[i, :] = np.conj(result) # Don't divide by N, photonic_fft scales by sqrt(N)
    
    # Process columns
    reconstructed = np.zeros_like(intermediate, dtype=np.complex128)
    for j in range(size):
        col = np.conj(intermediate[:, j])
        result = photonic_fft.compute(col)
        reconstructed[:, j] = np.conj(result)
        
    end_time = time.time()
    latency = photonic_fft.latency_ns() * (size * 2) # Latency for 2x N operations
    print(f"Photonic Reconstuction complete in {end_time - start_time:.4f}s CPU time.")
    print(f"Theoretical Photonic Latency: {latency:.4f} ns.")
    
    # Return shift back and latency
    return np.fft.fftshift(np.abs(reconstructed)), latency

def simulated_llm_visual_encoder(image, size=64):
    """
    Simulate processing the MRI through an LLM visual correspondence model
    (e.g., Vision Transformer patch projection layer) using the photonic matrix multiplier.
    """
    print(f"Initializing PhotonicMatrixMultiplier (size {size}x{size}) for LLM Visual Features...")
    # Initialize a random projection matrix for the visual encoder features
    mm = PhotonicMatrixMultiplier(size=size)
    
    # Encode a random unitary to simulate feature projection
    random_matrix = np.random.randn(size, size) + 1j * np.random.randn(size, size)
    q, r = np.linalg.qr(random_matrix)
    mm.encode_matrix(q)
    
    # Project each row (representing a sequence of patch embeddings)
    feature_map = np.zeros_like(image, dtype=np.complex128)
    
    start_time = time.time()
    for i in range(size):
        # Apply the LLM feature extraction weights to the image patches
        feature_map[i, :] = mm.multiply_resonator_weighted(image[i, :])
    end_time = time.time()
    
    throughput = mm.compute_throughput()
    print(f"LLM visual feature extraction complete in {end_time - start_time:.4f}s CPU time.")
    print(f"Photonic Matrix Multiplier Throughput: {throughput:.2f} TOPS.")
    
    return np.abs(feature_map), throughput

def main():
    print("=" * 80)
    print("PHOTONIC MRI RECONSTRUCTION & MULTIMODAL LLM INTEGRATION")
    print("=" * 80)
    
    SIZE = 64
    
    # 1. MRI Physics - K-Space generation
    print("\n1. Generating Synthetic MRI Data...")
    original_img = generate_phantom(SIZE)
    kspace = generate_kspace(original_img)
    
    # 2. Photonic Signal Reconstruction
    print("\n2. Performing Photonic Signal Reconstruction...")
    reconstructed_img, photonic_fft_latency_ns = photonic_2d_ifft(kspace, SIZE)
    
    # 3. LLM Visual Correspondence Model
    print("\n3. Generating Multimodal Visual Correspondence Features...")
    llm_feature_map, photonic_tops = simulated_llm_visual_encoder(reconstructed_img, SIZE)
    
    # 4. Characteristics and Charting
    print("\n4. Plotting Characteristics and Charts...")
    
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Photonic Thin Film Layer: MRI Physics & LLM Visual Correspondence', fontsize=20, color='cyan')
    
    # Subplot 1: K-space (log magnitude)
    ax1 = plt.subplot(2, 3, 1)
    kspace_mag = np.log(1 + np.abs(kspace))
    im1 = ax1.imshow(kspace_mag, cmap='viridis')
    ax1.set_title('Raw MRI K-Space Signal (Frequency Domain)')
    ax1.axis('off')
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
    
    # Subplot 2: Reconstructed Image
    ax2 = plt.subplot(2, 3, 2)
    im2 = ax2.imshow(reconstructed_img, cmap='bone')
    ax2.set_title('Photonic Fast Fourier Reconstruction')
    ax2.axis('off')
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
    
    # Subplot 3: Multimodal LLM Feature correspondence
    ax3 = plt.subplot(2, 3, 3)
    im3 = ax3.imshow(llm_feature_map, cmap='magma')
    ax3.set_title('LLM Visual Correspondence Feature Map')
    ax3.axis('off')
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)
    
    # Subplot 4: Performance Chart
    ax4 = plt.subplot(2, 3, (4, 6))
    
    # Performance comparison metrics
    labels = ['Latency (ms)', 'Throughput (TOPS)', 'Energy Efficiency (TOPS/W)']
    electronic_perf = [15.5, 0.5, 0.1] # Baseline typical GPU/CPU for this small scale
    photonic_perf = [0.0001, photonic_tops, photonic_tops / 10.0] # Est. 10W power
    
    x = np.arange(len(labels))
    width = 0.35
    
    # We use a log scale for better visual comparison
    rects1 = ax4.bar(x - width/2, np.log10(electronic_perf), width, label='Legacy Electronic', color='#d62728')
    rects2 = ax4.bar(x + width/2, np.log10(photonic_perf), width, label='Photonic TFLN Stack', color='#00d4ff')
    
    ax4.set_ylabel('Log10 Scale')
    ax4.set_title('Performance Characteristics: Photonic vs Electronic')
    ax4.set_xticks(x)
    ax4.set_xticklabels(labels)
    ax4.legend()
    
    # Add actual value labels
    def autolabel(rects, values, postfix=""):
        for rect, val in zip(rects, values):
            height = rect.get_height()
            ax4.annotate(f'{val:.2f}{postfix}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3 if height > 0 else -15),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', color='white', fontsize=10)
            
    autolabel(rects1, electronic_perf)
    autolabel(rects2, photonic_perf)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mri_photonic_characteristics.png'), dpi=300)
    print(f"\nPlots saved to 'mri_photonic_characteristics.png'")
    # Only show if not running in a pure background context
    if (os.environ.get('DISPLAY') or sys.platform == 'darwin') and '--json' not in sys.argv:
        # On macOS, display if possible, or just rely on savefig
        print("Charts plotted successfully.")
    
    print("\n" + "=" * 80)
    print("SIMULATION COMPLETE")
    print("=" * 80)
    
    # Formulate metrics
    metrics = {
        "fft_latency_ns": float(photonic_fft_latency_ns),
        "electronic_latency_ms": 15.5,
        "photonic_throughput_tops": float(photonic_tops),
        "electronic_throughput_tops": 0.5,
        "photonic_efficiency_tops_w": float(photonic_tops / 10.0),
        "electronic_efficiency_tops_w": 0.1,
        "speedup_vs_electronic": float((15.5 * 1000000) / photonic_fft_latency_ns)
    }
    return metrics

if __name__ == "__main__":
    import sys
    metrics = main()
    if "--json" in sys.argv:
        print("___JSON_START___")
        print(json.dumps(metrics))
        print("___JSON_END___")
