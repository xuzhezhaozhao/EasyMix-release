#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from google.protobuf import text_format
from easymix.utils.logger import logger
from easymix.estimator.estimator import Estimator
import os
import time
import shutil
import numpy as np
import easymix.protos.linucb_model_pb2 as linucb


MODEL_FILENAME = 'linucb.model'


def _make_arm_list(min_arm, arm_step, arm_num):
    """构造 linucb arm 列表.
    Args:
        min_arm: arm 最小值
        arm_step: arm 步长
        arm_num: arm 数量

    Returns:
        arm_list: arm列表
    """
    arm_list = []
    for index in range(arm_num):
        arm_list.append(round(min_arm, 4))
        min_arm = min_arm + arm_step
    return arm_list


class LinucbEstimator(Estimator):
    """Linucb 模型."""

    def __init__(self,
                 model_dir,
                 export_model_dir,
                 period_export_interval_second,
                 period_monitor_interval_second,
                 dataset,
                 warmup_from,
                 params):
        """创建 LinucbEstimator 对象.

        Args:
            warmup_from: 训练恢复目录.
        """
        logger.info("LinucbEstimator params = {}".format(params))

        # 监控信息变量
        self._global_step = 0               # 训练步数
        self._action_counts = {}            # aciton 对应样本数
        self._reward_zero_count = 0         # reward 为 0 样本数

        self._alpha = params['alpha']
        self._score_type = params['score_type']
        self._dim = params['feature_dim']
        self._min_arm = params['min_arm']
        self._arm_step = params['arm_step']
        self._arm_num = params['arm_num']
        self._matrix_a_initial = params['matrix_a_initial']
        self._vector_b_initial = params['vector_b_initial']
        self._explore_prob = params['explore_prob']
        self._decay_type = params['decay_type']
        self._decay_step = params['decay_step']
        self._matrix_a_decay_rate = params['matrix_a_decay_rate']
        self._vector_b_decay_rate = params['vector_b_decay_rate']
        self._learning_rate = params['learning_rate']
        self._assets = params['assets']
        self._export_postprocess_script = params['export_postprocess_script']
        self._arm_list = _make_arm_list(min_arm=self._min_arm,
                                        arm_step=self._arm_step,
                                        arm_num=self._arm_num)
        self._matrix_a_list = []
        self._vector_b_list = []
        for i in range(self._arm_num):
            matrix_a = np.diag([self._matrix_a_initial] * self._dim)
            vector_b = np.array([self._vector_b_initial] * self._dim)
            self._matrix_a_list.append(matrix_a)
            self._vector_b_list.append(vector_b)

        super(LinucbEstimator, self).__init__(
            model_dir=model_dir,
            export_model_dir=export_model_dir,
            period_export_interval_second=period_export_interval_second,
            period_monitor_interval_second=period_monitor_interval_second,
            dataset=dataset)

    def update(self, feature, label):
        """Linucb 模型单步更新.

        Args:
            feature: 特征数据，double数组.
            label: 三元组 (boost_index, boost_value, reward)
        """
        logger.debug('feature = {}, label = {}'.format(feature, label))
        arm_index, arm_value, reward = label
        matrix_a = self._matrix_a_list[arm_index]
        vector_b = self._vector_b_list[arm_index]
        x_vector_c = feature.reshape(self._dim, 1)  # [dim, 1]
        x_vector_r = feature.reshape(1, self._dim)  # [1, dim]
        x_matirx = np.dot(x_vector_c, x_vector_r)

        matrix_a_decay_rate = 1.0
        vector_b_decay_rate = 1.0
        if self._decay_type == 'step':
            if arm_index in self._action_counts and \
                    self._action_counts[arm_index] % self._decay_step == 0:
                matrix_a_decay_rate = self._matrix_a_decay_rate
                vector_b_decay_rate = self._vector_b_decay_rate

        # 参数更新
        # 注意：这里必须使用 *=, += 操作符，否则更新的并不是模型参数，而是新的
        # 变量
        matrix_a *= matrix_a_decay_rate
        matrix_a += self._learning_rate * x_matirx
        vector_b *= vector_b_decay_rate
        vector_b += self._learning_rate * reward * feature

        self._global_step += 1

        # 监控信息
        if arm_index not in self._action_counts:
            self._action_counts[arm_index] = 0
        self._action_counts[arm_index] += 1
        if reward == 0:
            self._reward_zero_count += 1

    def export(self):
        """导出模型."""
        logger.info("export model ...")
        model = linucb.LinucbModel()
        model.config_info.alpha = self._alpha
        model.config_info.score_type = self._score_type
        model.config_info.explore_prob = self._explore_prob
        model.model_info.feature_dimension = self._dim
        model.model_info.arm.MergeFrom(self._arm_list)

        with self._export_lock:
            # 导出模型变量时加锁
            for i in range(len(self._matrix_a_list)):
                matrix_a = model.model_info.matrix_a.add()
                matrix_a.num_row = self._dim
                matrix_a.num_col = self._dim
                matrix_a.elements.MergeFrom(self._matrix_a_list[i].reshape(-1))

                inverse_matrix_a = model.model_info.inverse_matrix_a.add()
                inverse_matrix_a.num_row = self._dim
                inverse_matrix_a.num_col = self._dim
                inverse_matrix_a.elements.MergeFrom(
                    np.linalg.inv(self._matrix_a_list[i]).reshape(-1))

                vector_b = model.model_info.vector_b.add()
                vector_b.elements.MergeFrom(self._vector_b_list[i])

        serialized = model.SerializeToString()
        ts = str(int(time.time()))
        model_dir = os.path.join(self._export_model_dir, ts)
        os.makedirs(model_dir)
        with open(os.path.join(model_dir, MODEL_FILENAME), 'w') as f:
            f.write(serialized)
        for asset in self._assets:
            target = self._assets[asset]
            shutil.copy(asset, os.path.join(model_dir, target))

        if self._export_postprocess_script != '':
            cmd = 'bash ' + self._export_postprocess_script + ' ' + model_dir
            os.system(cmd)

        logger.debug("model = '{}'".format(model))
        logger.info("export model done")

    def monitor(self):
        """打印监控日志."""
        logger.info("linucb monitor ...")
        logger.info("global_step = {}".format(self._global_step))
        logger.info("action_counts info:")
        for action in self._action_counts:
            logger.info("  action '{}', boost = {}, count = {}".format(
                action, self._arm_list[action], self._action_counts[action]))
        logger.info("matrix_a_list info:")
        for i in range(len(self._matrix_a_list)):
            logger.info("  matrix_a[{}] max = {}, min = {}, mean = {}, "
                        "std = {}".format(
                i, self._matrix_a_list[i].max(), self._matrix_a_list[i].min(),
                self._matrix_a_list[i].mean(), self._matrix_a_list[i].std()))
        logger.info("vector_b_list info:")
        for i in range(len(self._vector_b_list)):
            logger.info("  vector_b[{}] max = {}, min = {}, mean = {}, "
                        "std = {}".format(
                i, self._vector_b_list[i].max(), self._vector_b_list[i].min(),
                self._vector_b_list[i].mean(), self._vector_b_list[i].std()))
        logger.info("linucb monitor done")
