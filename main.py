

import os
import time
import argparse

from tensorboardX import SummaryWriter


def aichor_write_tensorboard():

    vcs_commit_msg = os.getenv("VCS_COMMIT_MESSAGE") or "VCS_COMMIT_MESSAGE env var not found"

    # TensorBoard remote log path from env var (optional)
    tb_remote_log_path = os.getenv("AICHOR_LOGS_PATH")
    if not tb_remote_log_path:
        print("### AICHOR_LOGS_PATH not set — will write locally only")
    else:
        print(f"### AICHOR_LOGS_PATH={tb_remote_log_path}")

    # If AICHOR_LOGS_PATH starts with s3 and Azure endpoint is provided, convert to Azure path
    if tb_remote_log_path and os.getenv("AZURE_STORAGE_ENDPOINT"):
        if tb_remote_log_path.startswith("s3://"):
            tb_remote_log_path = os.getenv("AZURE_STORAGE_ENDPOINT") + "/" + tb_remote_log_path[5:]  # Remove "s3://"
            print(f"### Azure TB log path: {tb_remote_log_path}")

    # TensorBoard local log path (always enabled)
    tb_local_log_path = os.getenv("AICHOR_LOCAL_LOGS_PATH", "/tmp/tb-mirror")
    os.makedirs(tb_local_log_path, exist_ok=True)

    remote_writer = None 
    local_writer = None

    # Initialize writers with basic error handling
    try:
        if tb_remote_log_path:
            try:
                remote_writer = SummaryWriter(tb_remote_log_path)
                print(f"### Remote writer initialized at: {tb_remote_log_path}")
            except Exception as e:
                print(f"### Failed to init remote writer at '{tb_remote_log_path}': {e}")
        try:
            local_writer = SummaryWriter(tb_local_log_path)
            print(f"### Local writer initialized at: {tb_local_log_path}")
        except Exception as e:
            print(f"### Failed to init local writer at '{tb_local_log_path}': {e}")

        writers = [w for w in (remote_writer, local_writer) if w is not None]
        if not writers:
            print("### No TensorBoard writers available; skipping writes")
            return

        values = [0.31, 0.28, 0.24, 0.20, 0.18]
        for step, val in enumerate(values, start=5):
            for w in writers:
                w.add_scalar("demo/loss", val, step)
                w.add_text("testing text", vcs_commit_msg, step)
            for w in writers:
                w.flush()
            time.sleep(1)
    finally:
        # Close writers at the very end
        try:
            if remote_writer is not None:
                remote_writer.close()
        except Exception as e:
            print(f"### Failed to close remote writer: {e}")
        try:
            if local_writer is not None:
                local_writer.close()
        except Exception as e:
            print(f"### Failed to close local writer: {e}")

    print("Appended points to", tb_remote_log_path or "<no remote>", "and", tb_local_log_path)



def main():

    aichor_write_tensorboard()

    time.sleep(600)

if __name__ == "__main__":
    main()
