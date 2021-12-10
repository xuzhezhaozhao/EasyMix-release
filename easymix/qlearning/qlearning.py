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
import itertools
import numpy as np
import easymix.protos.QLearning_pb2 as qlearning


MODEL_FILENAME = 'qlearning.model'


def _make_coldstart_qtable_numeric(feature_init_list, boundary_lower,
                                   boundary_upper, boundary_step, init_qvalue):

    """构造初始化 Qtable 列表.
    Args:
        feature_init_list: 每个特征配置值
        boundary_lower: qlearning_numeric表下界
        boundary_upper: qlearning_numeric表上界
        boundary_step: qlearning_numeric表更新步长值
        init_qvalue: qlearning_numeric表初始化值

    Returns:
        coldstart_table: 初始化q表
        boost_list: 填入action_type.values的值
        boost_action: boost_value对应的index
    """
    logger.info("init _make_coldstart_qtable_numeric ")
    coldstart_table = {}
    boost_list = []
    boost_action = {}

    lower = boundary_lower
    upper = boundary_upper

    count = 0
    while lower <= upper:
        boost_list.append(round(lower, 5))
        boost_action[str(round(lower, 5))] = count
        lower += boundary_step
        count += 1

    data_list = []
    for elem in feature_init_list:
        data_list.append(range(int(elem)))

    init_boost_dict = {}
    for i in range(len(boost_list)):
        init_boost_dict[str(boost_list[i])] = init_qvalue

    for elem in itertools.product(*data_list):
        elem_list = list(elem)
        elem_str_list = [str(i) for i in elem_list]
        status_elem = "_".join(elem_str_list)
        status_elem = "s_" + status_elem
        coldstart_table[status_elem] = init_boost_dict

    return coldstart_table, boost_list, boost_action


class QLearningEstimator(Estimator):
    """Qlearning 模型."""
    def __init__(self,
                 model_dir,
                 export_model_dir,
                 period_export_interval_second,
                 period_monitor_interval_second,
                 dataset,
                 params):
        """创建 QLearningEstimator 对象.

        Args:
            warmup_from：训练恢复目录.
        """
        logger.info("QLearningEstimator params = {}".format(params))

        # 监控信息变量
        self._global_step = 0               # 训练步数
        self._action_counts = {}            # action 对应的样本数
        self._reward_zero_count = 0         # reward 为 0 样本数
        self._mean_update_dict = {}         # 均值更新对应的dict值

        self._score_type = params['score_type']
        self._explore_prob = params['explore_prob']
        self._action_type = params['action_type']
        self._item_type_cnt = params['item_type_cnt']

        # qlearning_numeric初始化时维度表
        self._feature_num_list = params['feature_num_list']

        # qlearning_numeric的下界
        self._boundary_lower = params['boundary_lower']

        # qlearning_numeric的上界
        self._boundary_upper = params['boundary_upper']

        # 步长更新的界限
        self._boundary_step = params['boundary_step']

        # q表初始化的值
        self._init_qvalue = params['init_qvalue']

        # q表更新方式
        self._update_method = params['update_method']

        # qlearning 更新的步长
        self._learning_rate = params['learning_rate']

        # qlearning gamma 参数
        self._gamma = params['gamma']

        # ltv归一化系数
        self._ltv_alpha = params['ltv_alpha']

        # bid归一化系数
        self._bid_beta = params['bid_beta']

        # doc_score调参系数alpha(新增)
        self._pay_alpha = params['pay_alpha']

        self._user_duration_beta = params['user_duration_beta']

        self._decay_rate = params['decay_rate']

        self._assets = params['assets']
        self._export_postprocess_script = params['export_postprocess_script']

        qtable, boost_list, boost_action = _make_coldstart_qtable_numeric(
                                       feature_init_list=self._feature_num_list,
                                       boundary_lower=self._boundary_lower,
                                       boundary_upper=self._boundary_upper,
                                       boundary_step=self._boundary_step,
                                       init_qvalue=self._init_qvalue)

        self._qtable = qtable
        self._boost_list = boost_list
        self._boost_action = boost_action

        super(QLearningEstimator, self).__init__(
            model_dir=model_dir,
            export_model_dir=export_model_dir,
            period_export_interval_second=period_export_interval_second,
            period_monitor_interval_second=period_monitor_interval_second,
            dataset=dataset)


    def update(self, feature, label):
        """Qlearning 模型单步更新

        Args:
            feature：特征数据，double数组
            label： 三元组 (boost_index, boost_value, reward)
        """
        logger.debug("model update...")
        feature = self._list_to_string(feature)
        boost_index, boost_value, reward = label
        boost_value_dict = self._qtable[feature]
        logger.info("state = {}".format(feature))
        boost_value_str = str(boost_value)
        if boost_value_str not in boost_value_dict:
            logger.info("invalid boost value '{}'".format(boost_value_str))
            return

        if self._update_method == 'mean':
            pass
        elif self._update_method == 'step':
            logger.info("reward = {}".format(reward))
            boost_value_dict[boost_value_str] *= self._decay_rate
            current_q = boost_value_dict[boost_value_str]
            next_q = max(boost_value_dict.values())
            boost_value_dict[boost_value_str] = current_q + \
                self._learning_rate * (reward + self._gamma * next_q - current_q)
            logger.info("boost_value_dict[{}] = {}".format(boost_value_str,
                boost_value_dict[boost_value_str]))
        else:
            logger.error("model update error, update_method is error")

        self._qtable[feature] = boost_value_dict
        self._global_step += 1

        # 监控信息
        if reward == 0:
            self._reward_zero_count += 1


    def _list_to_string(self, features):
        return_feature = 's_'
        for i in range(len(features)):
            return_feature += str(int(features[i]))
            if i >= len(features) - 1:
                continue
            return_feature += '_'
        return return_feature


    def export(self):
        """导出模型."""
        logger.info("export model ...")
        model = qlearning.QlearningModel()
        action_info = qlearning.ActionInfo()
        action_info.action_type = self._action_type
        action_info.score_type = self._score_type
        action_info.values.extend(self._boost_list)
        model.explore_prob = self._explore_prob
        model.action_info.CopyFrom(action_info)

        with self._export_lock:
            # 导出模型变量时加锁
            for _use_feature in list(self._qtable.keys()):
                tmp_boost_dict = self._qtable[_use_feature]
                for boost_value in tmp_boost_dict.keys():
                    table_record = qlearning.TableRecord()
                    table_record.key = str(_use_feature)
                    table_record.action = int(self._boost_action[boost_value])
                    table_record.reward = float(tmp_boost_dict[boost_value])
                    model.table.extend([table_record])

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
        logger.info("qlearning monitor ...")
        logger.info("global_step = {}".format(self._global_step))
        logger.info("qlearning monitor done")
