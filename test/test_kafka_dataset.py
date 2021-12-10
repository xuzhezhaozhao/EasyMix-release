#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from easymix.estimator.dataset import KafkaDataset

dataset_num_process = 1
kafka_subscribe_topic = 'dw_mix_cpd_feature_statis'
kafka_consumer_num = 1
kafka_msg_queue_maxsize = 100000
kafka_boostrap_servers = 'shizhu-kafka.prd.vivo.lan:9092'
kafka_security_protocol = 'SASL_PLAINTEXT'
kafka_sasl_mechanism = 'SCRAM-SHA-256'
kafka_sasl_username = 'aimaker'
kafka_sasl_password = 'YXdxZ0xpSEYxVlB3'
kafka_group_id = 'mix_sort_linucb_v6_feature'
kafka_client_id = 'aimaker'
kafka_session_timeout_ms = 300
kafka_heartbeat_interval_ms = 60000
kafka_max_poll_interval_ms = 600
msg_queue_maxsize = 100000


def process_fn(msg):
    return (True, msg, None)


dataset = KafkaDataset(process_fn,
                       dataset_num_process,
                       kafka_subscribe_topic,
                       kafka_consumer_num,
                       msg_queue_maxsize,
                       kafka_boostrap_servers,
                       kafka_security_protocol,
                       kafka_sasl_mechanism,
                       kafka_sasl_username,
                       kafka_sasl_password,
                       kafka_group_id,
                       kafka_client_id,
                       kafka_session_timeout_ms,
                       kafka_heartbeat_interval_ms,
                       kafka_max_poll_interval_ms)

msg = dataset.get()
print(msg)
