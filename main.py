

import os
import time

from tensorboardX import SummaryWriter


def print_env_vars():
    keywords = ["S3", "AWS", "AICHOR", "MINIO", "ENDPOINT", "TENSOR", "LOG"]
    for k, v in sorted(os.environ.items()):
        if any(x in k.upper() for x in keywords):
            print(f"  {k}={v}")


def aichor_write_tensorboard():
    print("### Relevant env vars:")
    print_env_vars()

    log_path = os.getenv("AICHOR_LOGS_PATH")
    print(f"### AICHOR_LOGS_PATH={log_path}")

    writer = SummaryWriter(log_path)
    for step, val in enumerate([0.31, 0.28, 0.24, 0.20, 0.18], start=5):
        writer.add_scalar("demo/loss", val, step)
        time.sleep(1)
    writer.flush()
    writer.close()
    print("Appended points to", log_path)
    print("### TEST 123")


def print_test():
    # do math multiplications and then print test

    for i in range(10):
        a = i * 2
        b = i * 3
        c = a + b
        print(f"Test {i}: {c}")

    

def main():
    aichor_write_tensorboard()

    print_test()

    time.sleep(1800)

if __name__ == "__main__":
    main()

