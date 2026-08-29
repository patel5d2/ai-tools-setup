"""§3.8 — inventory CPU, memory, and GPU on whatever platform this runs on.

Framework query: torch (MPS on Apple silicon, CUDA on Linux/Colab/Jetstream2).
System utility: platform-appropriate (system_profiler / nvidia-smi / lscpu).
An accurate "no GPU" is a correct result, not a failure.
"""
import os
import platform
import shutil
import subprocess


def sys_utility() -> None:
    print("=== system utility ===")
    if shutil.which("nvidia-smi"):  # Colab / Jetstream2 GPU instances / Linux+NVIDIA
        subprocess.run(["nvidia-smi"])
    elif platform.system() == "Darwin":
        subprocess.run(["system_profiler", "SPHardwareDataType", "SPDisplaysDataType"])
    elif shutil.which("lscpu"):  # Linux without NVIDIA
        subprocess.run(["lscpu"])
    else:
        print("no known system utility on this platform")


def framework_query() -> None:
    print("\n=== framework query (torch) ===")
    print(f"CPUs (os.cpu_count): {os.cpu_count()}")
    try:
        import torch
    except ImportError:
        print("torch not installed — install from requirements.txt")
        return
    print(f"torch {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    mps = getattr(torch.backends, "mps", None)
    print(f"MPS (Apple GPU) available: {mps.is_available() if mps else False}")


if __name__ == "__main__":
    sys_utility()
    framework_query()
