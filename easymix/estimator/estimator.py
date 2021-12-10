#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from easymix.utils.logger import logger
import threading
import time


class Estimator(object):
    """类似Tensorflow Estimator接口，提供模型接口封装.

    作为基类使用，提供模型训练需要的通用接口和通用代码封装.
    """

    def __init__(self,
                 model_dir,
                 export_model_dir,
                 period_export_interval_second,
                 period_monitor_interval_second,
                 dataset):
        """创建 Estimator 对象.

        Args:
            model_dir: 模型目录，存储训练过程产出的文件，例如断点文件，调试数据
                等.
            export_model_dir: 模型导出目录.
            period_export_interval_second: 定时导出模型间隔时间，单位秒
            period_monitor_interval_second: 定时执行监控，单位秒
            dataset: 模型数据来源, 提供 get 接口，返回 (feature, label).
        """
        self._model_dir = model_dir
        self._export_model_dir = export_model_dir
        self._period_export_interval_second = period_export_interval_second
        self._period_monitor_interval_second = period_monitor_interval_second
        self._dataset = dataset

        # 控制训练是否停止
        self._should_stop = False

        # 定时导出模型线程
        self._period_export_thread = None
        self._period_monitor_thread = None

        self._export_lock = threading.Lock()

    def train(self):
        """模型训练接口."""
        self._start_period_export()
        self._start_period_monitor()
        while not self._should_stop:
            try:
                logger.debug("train ...")
                feature, label = self._dataset.get()
                logger.debug("feature = {}".format(feature))
                logger.debug("label = {}".format(label))
                with self._export_lock:
                    self.update(feature, label)
                logger.debug("train one step")
            except Exception as e:
                logger.error("train exception = '{}'".format(e))

        if self._period_export_thread:
            self._period_export_thread.join()

    def update(self, feature, label):
        """模型单步更新，

        该方法需要由子类实现.

        Args:
            feature: 样本特征，可以是任意python对象，子类负责解析
            label: 样本label，可以是任意python对象，子类负责解析
        """
        raise NotImplementedError('Estimator.update')

    def eval(self):
        raise NotImplementedError('Estimator.eval')

    def predict(self):
        raise NotImplementedError('Estimator.predict')

    def export(self):
        """导出模型，可由子类实现"""
        logger.info("export: do nothing.")

    def monitor(self):
        """监控，可由子类实现."""
        logger.info("monitor: do nothing.")

    def period_export(self):
        """定时导出模型.

        定时执行 self.export() 接口.
        """
        while not self._should_stop:
            try:
                self.export()
            except Exception as e:
                logger.error("export exception = {}".format(e))
            time.sleep(self._period_export_interval_second)

    def period_monitor(self):
        """定时执行 self.monitor() 方法."""
        while not self._should_stop:
            try:
                self.monitor()
            except Exception as e:
                logger.error("monitor exception = {}".format(e))
            time.sleep(self._period_monitor_interval_second)

    def _start_period_export(self):
        """启动定时导出模型线程."""
        self._period_export_thread = threading.Thread(
            target=Estimator.period_export, args=(self,))
        self._period_export_thread.start()

    def _start_period_monitor(self):
        """启动定时监控线程."""
        self._period_monitor_thread = threading.Thread(
            target=Estimator.period_monitor, args=(self,))
        self._period_monitor_thread.start()
