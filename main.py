

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
    

def main():

    aichor_write_tensorboard()

    time.sleep(600)

if __name__ == "__main__":
    main()



"""

kubectl exec -it experiment-eb916239-46a5-master-0-0-d4zsq -- sh -lc '
python - <<PY
import os, time, threading, posixpath
import tensorflow as tf, tensorflow_io as tfio
from tensorboard.main import run_main
DST = "/tmp/tb-mirror"
import sys
sys.argv = ["tensorboard","--logdir", DST,"--port","16013","--bind_all","--reload_interval","2","--load_fast","false"]
run_main()
PY'



kubectl -n prj-tb26aout-e964674e723b4bb7 port-forward pod/experiment-eb916239-46a5-master-0-0-d4zsq 16013:16013

"""