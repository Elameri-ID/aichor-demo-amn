import os
import argparse
import time

def dummy_tb_write():
    log_path = os.getenv("AICHOR_LOGS_PATH")
    if not log_path:
        print('AICHOR_LOGS_PATH env var not found')
        return

    msg = os.getenv("VCS_COMMIT_MESSAGE") or "VCS_COMMIT_MESSAGE env var not found"
    mirror_dir = os.getenv("AICHOR_TB_LOCAL_MIRROR", "/tmp/tb-dummy")

    def write_local(dirpath: str, text: str):
        try:
            from tensorboardX import SummaryWriter
            os.makedirs(dirpath, exist_ok=True)
            w = SummaryWriter(dirpath)
            w.add_text("testing text", text, 0)
            w.flush(); w.close()
            print(f"local mirror (tensorboardX): {dirpath}")
        except Exception as e1:
            try:
                import tensorflow as tf
                os.makedirs(dirpath, exist_ok=True)
                w = tf.summary.create_file_writer(dirpath)
                with w.as_default():
                    tf.summary.text("testing text", text, step=0)
                w.flush(); w.close()
                print(f"local mirror (TF): {dirpath}")
            except Exception as e2:
                print(f"local mirror failed: {e1} ; {e2}")

    # Azure path → write to Blob via TF+TF-IO, then write a local mirror
    if log_path.startswith(("az://", "azfs://")):
        try:
            import tensorflow as tf  # TF event writer
            import tensorflow_io as tfio  # registers az:// filesystem
            azure_dir = log_path.rstrip("/")
            try:
                tf.io.gfile.makedirs(azure_dir)  # safe no-op if exists
            except Exception:
                pass
            w = tf.summary.create_file_writer(azure_dir)
            with w.as_default():
                tf.summary.text("testing text", msg, step=0)
            w.flush(); w.close()
            print(f"wrote TF event to Azure: {azure_dir}")
        except Exception as e:
            print(f"Azure write failed ({e}) — still writing local mirror.")
        write_local(mirror_dir, msg)
        return

    # Non-Azure path → original behavior
    try:
        from tensorboardX import SummaryWriter
        os.makedirs(log_path, exist_ok=True)
        w = SummaryWriter(log_path)
        w.add_text("testing text", msg, 0)
        w.flush(); w.close()
        print(f"wrote TF event to: {log_path}")
    except Exception as e:
        print(f"tensorboardX not installed: {e}")

def print_tf_env():
    tf_config_raw = os.getenv("TF_CONFIG")
    print("tf_config:", tf_config_raw)
    if tf_config_raw is None:
        print("tf_config is None because worker count = 1")

def main():
    parser = argparse.ArgumentParser(description="AIchor smoke test on any operator")
    parser.add_argument("--operator", choices=["ray", "jax", "tf"], default="tf")
    parser.add_argument("--sleep", type=int, default=0, help="sleep time in seconds")
    parser.add_argument("--tb-write", dest="tb_write", action="store_true",
                        help="write a dummy event to TB (and Azure if az://)")
    args = parser.parse_args()

    if args.tb_write:
        dummy_tb_write()

    if args.sleep > 0:
        print(f"sleeping for {args.sleep}s before exiting")
        time.sleep(args.sleep)

if __name__ == "__main__":
    main()
