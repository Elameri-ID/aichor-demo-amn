

import os
import time
import argparse
# import tensorflow as tf
# import tensorflow_io as tfio
# from tensorboard.main import run_main

from tensorboardX import SummaryWriter


def aichor_write_tensorboard():

    # Tensorboard remote log path from env var
    tb_remote_log_path = os.getenv("AICHOR_LOGS_PATH")
    if not tb_remote_log_path:
        print('### AICHOR_LOGS_PATH env var not found')
        return
    else:
        print(f"### AICHOR_LOGS_PATH={tb_remote_log_path}")
    
    # Tensorboard local log path 
    tb_local_log_path = os.getenv("AICHOR_LOCAL_LOGS_PATH", "/tmp/tb-mirror")
    os.makedirs(tb_local_log_path, exist_ok=True)

    writers = [
        SummaryWriter(tb_remote_log_path),
        SummaryWriter(tb_local_log_path),
    ]


    msg = os.getenv("VCS_COMMIT_MESSAGE") or "VCS_COMMIT_MESSAGE env var not found"

    # logdir="az://prjtb26aoute964674e723b4/prj-tb26aout-e964674e723b4bb7-outputs/tb-write-test"

    values = [0.31, 0.28, 0.24, 0.20, 0.18]
    for step, val in enumerate(values, start=5):
        for w in writers:
            w.add_scalar("demo/loss", val, step)
            w.add_text("testing text", msg, step)
            w.flush()
        time.sleep(1)

    print("Appended points to", tb_remote_log_path, "and", tb_local_log_path)






def main():

    aichor_write_tensorboard()

    time.sleep(300)

if __name__ == "__main__":
    main()
