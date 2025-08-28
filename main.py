

import os
import time
import argparse
import tensorflow as tf
import tensorflow_io as tfio
# from tensorboard.main import run_main


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
    tf.io.gfile.makedirs(tb_local_log_path)

    writers = [
        tf.summary.create_file_writer(tb_remote_log_path),
        tf.summary.create_file_writer(tb_local_log_path),
    ]


    msg = os.getenv("VCS_COMMIT_MESSAGE") or "VCS_COMMIT_MESSAGE env var not found"

    # logdir="az://prjtb26aoute964674e723b4/prj-tb26aout-e964674e723b4bb7-outputs/tb-write-test"

    values = [0.31, 0.28, 0.24, 0.20, 0.18]
    for step, val in enumerate(values, start=5):
        for w in writers:
            with w.as_default():
                tf.summary.scalar("demo/loss", val, step=step)
                tf.summary.text("testing text", msg, step=0)
            w.flush()
        time.sleep(1)

    print("Appended points to", tb_remote_log_path, "and", tb_local_log_path)






def main():
    parser = argparse.ArgumentParser(description="AIchor smoke test on any operator")
    parser.add_argument("--operator", choices=["ray", "jax", "tf"], default="tf")
    parser.add_argument("--sleep", type=int, default=0, help="sleep time in seconds")
    parser.add_argument("--tb-write", dest="tb_write", action="store_true",
                        help="write a dummy event to TB (and Azure if az://)")
    args = parser.parse_args()

    if args.tb_write:
        aichor_write_tensorboard()

    if args.sleep > 0:
        print(f"sleeping for {args.sleep}s before exiting")
        time.sleep(args.sleep)

if __name__ == "__main__":
    main()
