#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import threading
import queue
import time
import numpy as np
from easymix.utils.logger import logger
from easymix.utils.kafka_wrapper import KafkaWrapper


class KafkaDataset(object):
    """Kafka数据Dataset类.

    从 kafka 消费数据，经过过滤和处理.
    """

    def __init__(
        self,
        process_fn,
        num_process,
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
        """创建 KafkaDataset 对象.

        Args:
            process_fn: kafka消息处理函数，参数为 kafka 字符串消息，
                正确则返回(True, feature, label)元组. 若出错，
                返回 (False, None, None).
            num_process: 处理kafka消息进程数.
        """

        self._process_fn = process_fn
        self._num_process = num_process
        self._msg_queue = queue.Queue(msg_queue_maxsize)

        self._process_threads = []

        self._kafka_wrapper = KafkaWrapper(
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

        self._start = False

    def get(self):
        """返回一条格式化的数据，即特征转换后的数据

        Returns:
            feature: 样本特征，可以是任意python对象，子类负责解析
            label: 样本label，可以是任意python对象，子类负责解析
        """
        if not self._start:
            self._kafka_wrapper.start_consume()
            self._start_process()
            self._start = True
        msg = self._msg_queue.get()
        return msg

    def _process_msg(self):
        """处理kafka消息，将处理后的数据放到消息队列中.

        Args:
            msg: kafka消息，字符串类型.
        """
        while True:
            msg = self._kafka_wrapper.get()
            is_good, feature, label = self._process_fn(msg)
            if is_good:
                self._msg_queue.put((feature, label))

    def _start_process(self):
        logger.info("KafkaDataset start process ...")
        for i in range(self._num_process):
            th = threading.Thread(target=KafkaDataset._process_msg,
                                  args=(self,))
            th.start()
            self._process_threads.append(th)
        logger.info("KafkaDataset start process done")


class TestDataset(object):
    """用于测试的dataset类.

    返回假数据，一秒返回一条数据.
    """

    def __init__(self):
        pass

    def get(self):
        """返回一条假数据."""
        time.sleep(1)
        return np.array([1, 0, 1, 0, 0]), (1, 0.1, 2.3)
