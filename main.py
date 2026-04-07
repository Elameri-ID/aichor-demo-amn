

import os
import time
import argparse


import time
import tensorflow as tf
import tensorflow_io as tfio




def aichor_write_tensorboard():

    # TensorBoard remote log path from env var (optional)
    tb_remote_log_path = os.getenv("AICHOR_TENSORBOARD_PATH")
    print(f"### AICHOR_LOGS_PATH={tb_remote_log_path}")
    

    remote_writer = tf.summary.create_file_writer(tb_remote_log_path) 
    # local_writer = tf.summary.create_file_writer(tb_local_log_path) 

    with remote_writer.as_default():
        for step,val in enumerate([0.31,0.28,0.24,0.20,0.18], start=5):
            tf.summary.scalar("demo/loss", val, step=step)
            remote_writer.flush(); time.sleep(1)
        print("Appended points to", tb_remote_log_path) 

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

