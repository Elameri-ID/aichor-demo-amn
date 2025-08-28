

import os
import time
import argparse

from tensorboardX import SummaryWriter


def aichor_write_tensorboard():

    vcs_commit_msg = os.getenv("VCS_COMMIT_MESSAGE") or "VCS_COMMIT_MESSAGE env var not found"

    # Tensorboard remote log path from env var
    tb_remote_log_path = os.getenv("AICHOR_LOGS_PATH")
    if not tb_remote_log_path:
        print('### AICHOR_LOGS_PATH env var not found')
        return
    else:
        print(f"### AICHOR_LOGS_PATH={tb_remote_log_path}")

    if os.getenv("AZURE_STORAGE_ENDPOINT"): # if AICHOR_LOGS_PATH starts with s3, convert to Azure path
        
        if tb_remote_log_path.startswith("s3://"):

            tb_remote_log_path = os.getenv("AZURE_STORAGE_ENDPOINT") + tb_remote_log_path[5:]  # Remove "s3://"
            print(f"### Azure TB log path: {tb_remote_log_path}")  


    # Tensorboard local log path 
    tb_local_log_path = os.getenv("AICHOR_LOCAL_LOGS_PATH", "/tmp/tb-mirror")
    os.makedirs(tb_local_log_path, exist_ok=True)


    # logdir="az://prjtb26aoute964674e723b4/prj-tb26aout-e964674e723b4bb7-outputs/tb-write-test"

    remote_writer = SummaryWriter(tb_remote_log_path)
    local_writer  = SummaryWriter(tb_local_log_path)

    try:
        values = [0.31, 0.28, 0.24, 0.20, 0.18]
        for step, val in enumerate(values, start=5):
            for w in (remote_writer, local_writer):
                w.add_scalar("demo/loss", val, step)
                w.add_text("testing text", vcs_commit_msg, step)
            # optional: flush if you need near-real-time visibility
            remote_writer.flush()
            local_writer.flush()
            time.sleep(1)
    finally:
        # close once, at the very end
        remote_writer.close()
        local_writer.close()

    print("Appended points to", tb_remote_log_path, "and", tb_local_log_path)





def main():

    aichor_write_tensorboard()

    time.sleep(300)

if __name__ == "__main__":
    main()
