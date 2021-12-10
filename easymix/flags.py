#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
from easymix.utils.define_flags import DEFINE_string
from easymix.utils.define_flags import DEFINE_integer
from easymix.utils.define_flags import DEFINE_float
from easymix.utils.define_flags import DEFINE_bool
from easymix.utils.define_flags import DEFINE_list


parser = argparse.ArgumentParser()

DEFINE_bool(parser, 'is_test', False, '是否是测试，测试的话使用假数据')
DEFINE_string(parser, 'model_type', '', '')
DEFINE_string(parser, 'model_dir', '', '模型训练过程的模型数据目录')
DEFINE_string(parser, 'export_model_dir', '', '模型导出目录')
DEFINE_integer(parser, 'period_export_interval_second', 300,
              '定时导出模型时间，秒')
DEFINE_integer(parser, 'period_monitor_interval_second', 120,
              '定时打印监控日志时间，秒')
DEFINE_integer(parser, 'dataset_num_process', 1, 'Dataset数据处理线程数量')
DEFINE_string(parser, 'kafka_subscribe_topic', '', 'kafka订阅topic')
DEFINE_integer(parser, 'kafka_consumer_num', 1, 'kafka消费者数量')
DEFINE_integer(parser, 'msg_queue_maxsize', 10000000, '消息队列大小')
DEFINE_string(parser, 'kafka_boostrap_servers', '', 'kafka地址')
DEFINE_string(parser, 'kafka_security_protocol', 'SASL_PLAINTEXT', '')
DEFINE_string(parser, 'kafka_sasl_mechanism', 'SCRAM-SHA-256', '')
DEFINE_string(parser, 'kafka_sasl_username', '', '')
DEFINE_string(parser, 'kafka_sasl_password', '', '')
DEFINE_string(parser, 'kafka_group_id', '', '')
DEFINE_string(parser, 'kafka_client_id', '', '')
DEFINE_integer(parser, 'kafka_session_timeout_ms', 15000, '')
DEFINE_integer(parser, 'kafka_heartbeat_interval_ms', 60000, '')
DEFINE_integer(parser, 'kafka_max_poll_interval_ms', 60000, '')

DEFINE_string(parser, 'model_name', '_UNKNOW_', '')
DEFINE_float(parser, 'linucb_reward_beta', 1.0, '')
DEFINE_float(parser, 'linucb_reward_theta', 0.1, '')
DEFINE_string(parser, 'feature_conf_path', '', '特征处理配置文件路径')
DEFINE_string(parser, 'transform_func_path', '', '特征转换配置文件路径')

DEFINE_string(parser, 'logfile', 'easymix.log', '日志文件路径前缀')
DEFINE_string(parser, 'loglevel', 'info', '日志级别: debug, info, warn, error')

DEFINE_float(parser, 'linucb_alpha', 1.0, '')
DEFINE_integer(parser, 'linucb_score_type', 0, '')
DEFINE_float(parser, 'linucb_min_arm', 0, '')
DEFINE_float(parser, 'linucb_arm_step', 0.01, '')
DEFINE_integer(parser, 'linucb_arm_num', 100, '')
DEFINE_float(parser, 'linucb_matrix_a_initial', 1.0, '')
DEFINE_float(parser, 'linucb_vector_b_initial', 0.0, '')
DEFINE_float(parser, 'linucb_explore_prob', 0.0, '')
DEFINE_string(parser, 'linucb_decay_type', 'step', '"step", "time"')
DEFINE_integer(parser, 'linucb_decay_step', 100, '')
DEFINE_float(parser, 'linucb_matrix_a_decay_rate', 1.0, '')
DEFINE_float(parser, 'linucb_vector_b_decay_rate', 1.0, '')
DEFINE_float(parser, 'linucb_learning_rate', 1.0, '')

DEFINE_string(parser, 'export_postprocess_script', '',
              '导出模型后处理脚本, 例如推送到HDFS, 参数为导出模型目录')


DEFINE_integer(parser, 'qlearning_score_type', 101, 'qlearning浮点数作用的类型')
DEFINE_float(parser, 'qlearning_explore_prob', 0.15, 'qlearning探索概率')
DEFINE_integer(parser, 'qlearning_action_type', 2, 'qlearning动作类型')
DEFINE_integer(parser, 'qlearning_item_type_cnt', 2, 'qlearning作用模板个数')
DEFINE_list(parser, 'qlearning_feature_num_list', [5,8,6,2,5], 'qlearning用户模板个数')
DEFINE_float(parser, 'qlearning_boundary_lower', 0.14, 'qlearning探索边界下界')
DEFINE_float(parser, 'qlearning_boundary_upper', 0.24, 'qlearning探索边界下界')
DEFINE_float(parser, 'qlearning_boundary_step', 0.005, 'qlearning探索步伐')
DEFINE_float(parser, 'qlearning_init_qvalue', 1.0, 'qlearning探索边界下界')
DEFINE_string(parser, 'qlearning_update_method', 'step',
              'qlearning numeric模型以步长更新')
DEFINE_float(parser, 'qlearning_learning_rate', 0.7, 'qlearning步长更新学习率')
DEFINE_float(parser, 'qlearning_gamma', 0.0, 'qlearning gamma参数')
DEFINE_float(parser, 'qlearning_ltv_alpha', 1.0, '')
DEFINE_float(parser, 'qlearning_bid_beta', 1.0, '')
DEFINE_float(parser, 'qlearning_decay_rate', 0.999, 'Q value decay rate')
DEFINE_float(parser, 'pay_alpha', 1.0, '')
DEFINE_float(parser, 'user_duration_beta', 1.0, '')
DEFINE_float(parser, 'qlearning_reward_theta', 0.1, '')
