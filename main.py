#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import easymix.utils.logger as utils_logger
from easymix.estimator.dataset import KafkaDataset, TestDataset
from easymix.flags import parser
from easymix.linucb.linucb import LinucbEstimator
from easymix.qlearning.qlearning import QLearningEstimator
from easymix.linucb.process_fn import cpd_home_process_fn as linucb_cpd_home_process_fn
from easymix.qlearning.process_fn import cpd_home_qlearning_numeric_process_fn as numeric_qlearning_cpd_home_process_fn
from easymix.qlearning.process_fn import cpc_recommend_qlearning_numeric_process_fn as numeric_qlearning_cpc_recommend_process_fn
from easymix.transform import transform
from easymix.utils.kafka_wrapper import KafkaWrapper
from easymix.utils.logger import logger


def build_estimator(opts):
    """构建 Estimator 对象."""
    logger.info("build estimator ...")
    estimator = None
    model_type = opts.model_type
    if model_type == 'linucb':
        estimator = make_linucb_estimator(opts)
    elif model_type == 'numeric_qlearning' or \
        model_type == 'cpc_browser_recommend_numeric_qlearning':
        estimator = make_numeric_qlearning_estimator(opts)
    else:
        raise ValueError("Unknown model_type '{}'".format(model_type))
    logger.info("build estimator done, estimator = {}".format(estimator))
    return estimator


def make_linucb_estimator(opts):
    """构建 LinucbEstimator."""
    logger.info("build linucb estimator ...")

    if opts.is_test:
        dataset = TestDataset()
    else:
        dataset = make_kafka_dataset(opts)

    if not transform.init(opts.feature_conf_path):
        raise ValueError("init feature conf error")

    feature_dim = len(transform.transform(''))

    params = {}
    params['alpha'] = opts.linucb_alpha
    params['score_type'] = opts.linucb_score_type
    params['feature_dim'] = feature_dim
    params['min_arm'] = opts.linucb_min_arm
    params['arm_step'] = opts.linucb_arm_step
    params['arm_num'] = opts.linucb_arm_num
    params['matrix_a_initial'] = opts.linucb_matrix_a_initial
    params['vector_b_initial'] = opts.linucb_vector_b_initial
    params['explore_prob'] = opts.linucb_explore_prob
    params['decay_type'] = opts.linucb_decay_type
    params['decay_step'] = opts.linucb_decay_step
    params['matrix_a_decay_rate'] = opts.linucb_matrix_a_decay_rate
    params['vector_b_decay_rate'] = opts.linucb_vector_b_decay_rate
    params['learning_rate'] = opts.linucb_learning_rate
    params['export_postprocess_script'] = opts.export_postprocess_script
    params['assets'] = {
        opts.feature_conf_path: 'conf.json',
        opts.transform_func_path: 'transform_func.json',
    }
    logger.info("params = {}".format(params))
    estimator = LinucbEstimator(
        model_dir=opts.model_dir,
        export_model_dir=opts.export_model_dir,
        period_export_interval_second=opts.period_export_interval_second,
        period_monitor_interval_second=opts.period_monitor_interval_second,
        dataset=dataset,
        warmup_from=None,
        params=params)
    logger.info("build linucb estimator done, estimator = {}".format(estimator))
    return estimator


def make_numeric_qlearning_estimator(opts):
    """构建 QlearningEstimator."""
    logger.info("build qlearning estimator ...")

    if opts.is_test:
        dataset = TestDataset()
    else:
        dataset = make_kafka_dataset(opts)

    logger.info("opts.feature_conf_path is {}".format(opts.feature_conf_path))
    if not transform.init(opts.feature_conf_path):
        raise ValueError("init feature conf error")

    params = {}
    params['score_type'] = opts.qlearning_score_type
    params['explore_prob'] = opts.qlearning_explore_prob
    params['action_type'] = opts.qlearning_action_type
    params['item_type_cnt'] = opts.qlearning_item_type_cnt
    params['feature_num_list'] = opts.qlearning_feature_num_list
    params['boundary_lower'] = opts.qlearning_boundary_lower
    params['boundary_upper'] = opts.qlearning_boundary_upper
    params['boundary_step'] = opts.qlearning_boundary_step
    params['init_qvalue'] = opts.qlearning_init_qvalue
    params['update_method'] = opts.qlearning_update_method
    params['gamma'] = opts.qlearning_gamma
    params['learning_rate'] = opts.qlearning_learning_rate
    params['ltv_alpha'] = opts.qlearning_ltv_alpha
    params['bid_beta'] = opts.qlearning_bid_beta
    params['pay_alpha'] = opts.pay_alpha
    params['user_duration_beta'] = opts.user_duration_beta
    params['decay_rate'] = opts.qlearning_decay_rate
    params['export_postprocess_script'] = opts.export_postprocess_script
    params['assets'] = {
        opts.feature_conf_path: 'conf.json',
        opts.transform_func_path: 'transform_func.json',
    }
    logger.info("params = {}".format(params))
    estimator = QLearningEstimator(
        model_dir=opts.model_dir,
        export_model_dir=opts.export_model_dir,
        period_export_interval_second=opts.period_export_interval_second,
        period_monitor_interval_second=opts.period_monitor_interval_second,
        dataset=dataset,
        params=params)
    logger.info("build qlearning estimator done, estimator = {}".format(estimator))
    return estimator

def make_kafka_dataset(opts):
    """构建 KafkaDataset."""
    logger.info("make_kafka_dataset ...")
    transform_fn = transform.transform
    if opts.model_type == 'numeric_qlearning':
        logger.info("use numeric_qlearning_cpd_home_process_fn")
        process_fn = lambda msg: numeric_qlearning_cpd_home_process_fn(
            msg, opts.model_name, opts.qlearning_ltv_alpha, opts.qlearning_bid_beta, transform_fn)
    elif opts.model_type == 'cpc_browser_recommend_numeric_qlearning':
        logger.info("user numeric_qlearning_cpc_browser_recommend_process_fn")
        process_fn = lambda msg: numeric_qlearning_cpc_recommend_process_fn(
            msg, opts.model_name, opts.pay_alpha, opts.user_duration_beta,
            opts.qlearning_reward_theta, transform_fn)
    else:
        logger.info("use linucb_cpd_home_process_fn")
        process_fn = lambda msg: linucb_cpd_home_process_fn(
            msg, opts.model_name, opts.linucb_reward_beta,
            opts.linucb_reward_theta, transform_fn)
    dataset = KafkaDataset(process_fn,
                           opts.dataset_num_process,
                           opts.kafka_subscribe_topic,
                           opts.kafka_consumer_num,
                           opts.msg_queue_maxsize,
                           opts.kafka_boostrap_servers,
                           opts.kafka_security_protocol,
                           opts.kafka_sasl_mechanism,
                           opts.kafka_sasl_username,
                           opts.kafka_sasl_password,
                           opts.kafka_group_id,
                           opts.kafka_client_id,
                           opts.kafka_session_timeout_ms,
                           opts.kafka_heartbeat_interval_ms,
                           opts.kafka_max_poll_interval_ms)
    logger.info("make_kafka_dataset done, dataset = {}".format(dataset))
    return dataset

def main():
    """main函数."""
    opts = parser.parse_args()
    utils_logger.set_logfile(opts.logfile)
    utils_logger.set_loglevel(opts.loglevel)
    utils_logger.start()
    estimator = build_estimator(opts)
    estimator.train()


if __name__ == '__main__':
    main()
