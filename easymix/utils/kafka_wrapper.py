#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from confluent_kafka import Consumer, KafkaError, TopicPartition
from easymix.utils.logger import logger

import threading
import json
import queue


class KafkaWrapper(object):
    """封装 kafka."""

    def __init__(
        self,
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
        max_poll_interval_ms):
        """
        创建 KafkaWrapper 对象.

        Args:
            subscribe_topic: kafka消费topic
            consumer_num: 消费者数量
            msg_queue_maxsize: 消息队列大小
            boostrap_servers: kafka参数
            security_protocol: kafka参数
            sasl_mechanism: kafka参数
            sasl_username: kafka参数
            sasl_password: kafka参数
            group_id: kafka参数
            client_id: kafka参数
            session_timeout_ms: kafka参数
            heartbeat_interval_ms: kafka参数
            max_poll_interval_ms: kafka参数
        """
        self._consumers = []
        self._consumer_threads = []
        self._msg_queue = queue.Queue(maxsize=msg_queue_maxsize)
        self._msg_queue_maxsize = msg_queue_maxsize

        for i in range(consumer_num):
            consumer = Consumer({
                'bootstrap.servers': boostrap_servers,
                'security.protocol': security_protocol,
                'sasl.mechanism': sasl_mechanism,
                'sasl.username': sasl_username,
                'sasl.password': sasl_password,
                'session.timeout.ms': session_timeout_ms,
                'heartbeat.interval.ms': heartbeat_interval_ms,
                'max.poll.interval.ms': max_poll_interval_ms,
                'group.id': group_id,
                'client.id': client_id
            })
            consumer.subscribe([subscribe_topic])

            topic = consumer.list_topics(topic=subscribe_topic)
            partitions = [
                TopicPartition(subscribe_topic, partition) for partition in
                list(topic.topics[subscribe_topic].partitions.keys())
            ]
            # 计算每个消费者消费partition的数量
            num_partition = int((len(partitions) + consumer_num - 1) / consumer_num)
            tp_c_list = []
            for index, p in enumerate(partitions):
                _, high_offset = consumer.get_watermark_offsets(p)
                new_offset = int(high_offset) - 1
                tp_c = TopicPartition(subscribe_topic, index, new_offset)
                tp_c_list.append(tp_c)
            tp_c_list = tp_c_list[i * num_partition : (i + 1) * num_partition]
            if len(tp_c_list) == 0:
                continue
            consumer.assign(tp_c_list)
        self._consumers.append(consumer)

    def start_consume(self):
        logger.info("KafkaWrapper start_consume ...")
        for consumer in self._consumers:
            thread = threading.Thread(
                target=KafkaWrapper._consume, args=(self, consumer))
            thread.start()
            self._consumer_threads.append(thread)
        logger.info("KafkaWrapper start_consume done")

    def _consume(self, consumer):
        while True:
            msg = consumer.poll(1.0)        # 逐条去拉取数据
            if msg is None:
                continue
            if msg.error():
                msg_error = "Consumer error: {error}".format(error=msg.error())
                logger.error(msg_error)
                continue
            msg = msg.value()
            logger.debug("consum msg = {}".format(msg))
            self._msg_queue.put(msg)
        consumer.close()

    def get(self):
        logger.debug("kafka get msg, queue size = {}".format(self._msg_queue.qsize()))
        return self._msg_queue.get()
