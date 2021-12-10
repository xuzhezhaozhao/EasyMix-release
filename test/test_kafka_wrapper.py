#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from easymix.utils.kafka_wrapper import KafkaWrapper

subscribe_topic = 'dw_mix_cpd_feature_statis'
consumer_num = 1
msg_queue_maxsize = 100000
boostrap_servers = 'shizhu-kafka.prd.vivo.lan:9092'
security_protocol = 'SASL_PLAINTEXT'
sasl_mechanism = 'SCRAM-SHA-256'
sasl_username = 'aimaker'
sasl_password = 'YXdxZ0xpSEYxVlB3'
group_id = 'mix_sort_linucb_v6_feature'
client_id = 'aimaker'
session_timeout_ms = 300
heartbeat_interval_ms = 60000
max_poll_interval_ms = 600

kafka_wrapper = KafkaWrapper(
    subscribe_topic,
    consumer_num,
    msg_queue_maxsize,
    boostrap_servers,
    security_protocol,
    sasl_mechanism,
    sasl_username,
    sasl_password,
    group_id,
    client_id,
    session_timeout_ms,
    heartbeat_interval_ms,
    max_poll_interval_ms)

kafka_wrapper.start_consume()

while True:
    msg = kafka_wrapper.get()
    print(msg)
