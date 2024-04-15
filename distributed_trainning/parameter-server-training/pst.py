import json
import math
import os
import tempfile
from time import time

import constants
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data


def main():
    tf_config = json.loads(os.environ.get("TF_CONFIG") or "{}")

    print("*" * 70)
    print("Debugging tf config..")
    print(tf_config)

    task_config = tf_config.get("task", {})
    task_type = task_config.get("type")  # worker or ps
    task_index = task_config.get("index")

    # Get configurations for ps and worker hosts
    cluster_config = tf_config.get("cluster", {})
    ps_hosts = cluster_config.get("ps")
    worker_hosts = cluster_config.get("worker")

    # Construct the cluster
    cluster_spec = tf.train.ClusterSpec({"ps": ps_hosts, "worker": worker_hosts})

    # Construct the server,
    server = tf.train.Server(cluster_spec, job_name=task_type, task_index=task_index)
    # and tell the server to wait and stay alive
    # to share and coordinate accumulated updates
    # to the model's parameters
    if task_type == "ps":
        server.join()
    else:
        # Allocate CPU to workers
        with tf.device(
            tf.train.replica_device_setter(
                cluster=cluster_spec,
                worker_device="/job:worker/task:{}/cpu:0".format(
                    task_index
                ),  # If using GPU, please replace task_index with an GPU index, and `cpu` by `gpu`
                ps_device="/job:ps/cpu:0",
            )
        ):
            # Variables of the hidden layer with weights and biases
            hid_w = tf.Variable(
                tf.truncated_normal(
                    [
                        constants.IMAGE_PIXELS * constants.IMAGE_PIXELS,
                        constants.HIDDEN_UNITS,
                    ],
                    stddev=1.0 / constants.IMAGE_PIXELS,
                ),
                name="hid_w",
            )
            hid_b = tf.Variable(tf.zeros([constants.HIDDEN_UNITS]), name="hid_b")

            # Variables of the softmax layer
            sm_w = tf.Variable(
                tf.truncated_normal(
                    [constants.HIDDEN_UNITS, 10],
                    stddev=1.0 / math.sqrt(constants.HIDDEN_UNITS),
                ),
                name="sm_w",
            )
            sm_b = tf.Variable(tf.zeros([10]), name="sm_b")

            # Define input placeholder variables
            x = tf.placeholder(
                tf.float32, [None, constants.IMAGE_PIXELS * constants.IMAGE_PIXELS]
            )
            y_ = tf.placeholder(tf.float32, [None, 10])

            # Define the calculations
            hid_lin = tf.nn.xw_plus_b(x, hid_w, hid_b)
            hid = tf.nn.relu(hid_lin)
            y = tf.nn.softmax(tf.nn.xw_plus_b(hid, sm_w, sm_b))
            cross_entropy = -tf.reduce_sum(y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0)))

            # Define the optimizer
            opt = tf.train.AdamOptimizer(constants.LEARNING_RATE)
            global_step = tf.Variable(0, name="global_step", trainable=False)
            train_step = opt.minimize(cross_entropy, global_step=global_step)

            # Define the saver to save the model
            saver = tf.train.Saver()

            # Check if the current pod is the chief
            # by task_index in tf config
            is_chief = task_index == 0

            # The chief worker will create the session,
            # while the remaining workers will wait for the preparation to complete.
            if is_chief:
                print("Worker {}: Initializing session...".format(task_index))
            else:
                print(
                    "Worker {}: Waiting for session to be initialized...".format(task_index)
                )

            # The Supervisor takes care of session initialization,
            # restoring from a checkpoint, and closing the session
            # when done or any errors occur.
            sv = tf.train.Supervisor(
                is_chief=is_chief,
                logdir=tempfile.mkdtemp(),
                recovery_wait_secs=1,
                init_op=tf.global_variables_initializer(), # Initialization of variables such as random, and zero
                global_step=global_step, # The value from `global_step` is used in summaries and checkpoint filenames
            )
            # Configure our session
            sess_config = tf.ConfigProto(
                allow_soft_placement=True,
                log_device_placement=True,
                # Specify the devices to join the session
                device_filters=[
                    "/job:ps", 
                    "/job:worker/task:{}".format(task_index)],
            )

            server_grpc_url = "grpc://" + worker_hosts[task_index]
            print("Using existing server at: {}".format(server_grpc_url))
            sess = sv.prepare_or_wait_for_session(server_grpc_url, config=sess_config)

            print("Worker {}: Session initialization complete.".format(task_index))

            # Perform training
            time_begin = time()
            print("Training begins @ {}".format(time_begin))

            # Define the local_step to mark the progress of training
            local_step = 0

            # Read datasets from tensorflow
            mnist = input_data.read_data_sets("/tmp/mnist", one_hot=True)

            while True:
                batch_xs, batch_ys = mnist.train.next_batch(constants.BATCH_SIZE)
                train_feed = {x: batch_xs, y_: batch_ys}

                _, step = sess.run([train_step, global_step], feed_dict=train_feed)
                local_step += 1

                now = time()
                print(
                    "{}: Worker {}: training step {} done (global step: {})".format(
                        now, task_index, local_step, step
                    )
                )

                if step >= constants.TRAIN_STEPS:
                    break

                time_end = time()
                print("Training ends @ {}".format(time_end))
                training_time = time_end - time_begin
                print("Training elapsed time: {} s".format(training_time))

                # Validation feed
                val_feed = {x: mnist.validation.images, y_: mnist.validation.labels}
                val_xent = sess.run(cross_entropy, feed_dict=val_feed)
                print(
                    "After {} training step(s), validation cross entropy = {}".format(
                        constants.TRAIN_STEPS, val_xent
                    )
                )

            # Save the sess
            if is_chief:
                print("Saving the session to {}".format(constants.SAVED_MODEL_DIR))
                saver.save(sess, os.path.join(constants.SAVED_MODEL_DIR, "pst"))


if __name__ == "__main__":
    main()
