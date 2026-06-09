import os
import sys
import time


def write_large_file_local(path, target_bytes):
    chunk = b"x" * (256 * 1024 ** 2)
    print(f"Writing {target_bytes / 1024**3:.1f} GiB to {path} ...", flush=True)
    os.makedirs(path, exist_ok=True)
    dest = os.path.join(path, "large_test_file.bin")
    written = 0
    with open(dest, "wb") as f:
        while written < target_bytes:
            n = min(len(chunk), target_bytes - written)
            f.write(chunk[:n])
            written += n
            print(f"  {written / 1024**3:.2f} GiB written", flush=True)
    print(f"Done. {os.path.getsize(dest) / 1024**3:.2f} GiB at {dest}", flush=True)


def main():
    print("=== START ===", flush=True)

    tb_path = os.environ.get("AICHOR_LOGS_PATH", "NOT_SET")
    print(f"AICHOR_LOGS_PATH={tb_path}", flush=True)

    if tb_path == "NOT_SET":
        print("ERROR: AICHOR_LOGS_PATH not set", flush=True)
        sys.exit(1)

    target_bytes = 2 * 1024 ** 3

    # Wait for GCS Fuse mount to be ready
    mount = "/mnt/tensorboard"
    for i in range(30):
        try:
            os.listdir(mount)
            print(f"Mount ready after {i}s", flush=True)
            break
        except Exception as e:
            print(f"Waiting for mount ({i}s): {e}", flush=True)
            time.sleep(1)

    write_large_file_local(tb_path, target_bytes)

    # Write tensorboard events
    try:
        from tensorboardX import SummaryWriter
        writer = SummaryWriter(tb_path)
        for step, val in enumerate([0.31, 0.28, 0.24, 0.20, 0.18], start=1):
            writer.add_scalar("demo/loss", val, step)
            print(f"wrote step {step}", flush=True)
        writer.flush()
        writer.close()
        print("tensorboard write OK", flush=True)
    except Exception as e:
        print(f"ERROR writing tensorboard: {e}", flush=True)

    print("=== sleeping 1800s ===", flush=True)
    time.sleep(1800)


if __name__ == "__main__":
    main()
