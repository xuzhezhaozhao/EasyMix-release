#! /usr/bin/env python
# -*-coding=utf8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from easymix.utils.logger import logger
import json
import numpy as np


LTV_KEY = 'ltv'
BID_KEY = 'bid'
FEATURES_KEY = 'features'
ACTION_KEY = 'action'
STRATEGY_ID_KEY = 'strategyId'
KAKFA_FIELD_LIST=[
    "dt",
    "imei",
    "reqId",
    LTV_KEY,
    BID_KEY,
    FEATURES_KEY,
    ACTION_KEY,
    STRATEGY_ID_KEY,
]


def cpd_home_process_fn(msg, model_name, beta, theta, transform_fn):
    """kafka原始数据处理函数，适用于商店首页 linucb 模型.

    Args:
        msg: kafka原始数据.
        model_name: 模型名, 用于过滤样本.
        beta: reward相关参数, reward = beta * ltv + bid - theta
        theta: reward相关参数, reward = beta * ltv + bid - theta
        transform_fn: 特征处理函数, 参数为字符串，返回值为double数组.

    Returns:
        is_good: Bool 类型，是否成功.
        feature: 处理后的特征，double数组. 失败为 None.
        label: 返回三元组 (boost_index, boost_value, reward). 失败为 None.
    """
    try:
        return _do_process(msg, model_name, beta, theta, transform_fn)
    except Exception as e:
        logger.info("cpd_home_process_fn exception = {}".format(e))
        return False, None, None

def _do_process(msg, model_name, beta, theta, transform_fn):
    """同cpd_home_process_fn, 但不捕获异常."""
    bad = (False, None, None)
    msg = json.loads(msg)
    for key in KAKFA_FIELD_LIST:
        if key not in msg:
            logger.error("msg error: '{}' not in msg".format(key))
            return bad
    if model_name != msg[STRATEGY_ID_KEY]:
       return bad
    ltv = float(msg[LTV_KEY] or 0.0)
    bid = float(msg[BID_KEY] or 0.0)
    reward = beta * ltv + bid - theta
    feature = msg[FEATURES_KEY]
    action = msg[ACTION_KEY]
    tokens = action.split(';')
    if len(tokens) < 2:
        return bad
    boost_value = float(tokens[0])
    boost_index = int(tokens[1])
    feature = np.array(transform_fn(feature.encode('utf-8')))
    return True, feature, (boost_index, boost_value, reward)
