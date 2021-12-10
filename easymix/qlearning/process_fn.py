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
REPORT_INFO = 'report_info'
STRATEGY_ID_KEY = 'strategy_id'
CLICK_CNT_SUM = 'click_cnt_sum'
EXP_CNT_SUM = 'exp_cnt_sum'
USER_DURATION_SUM = 'user_duration_sum'
PAY_SUM = 'pay_sum'
ECPM_SUM = 'ecpm_sum'
DOC_SCORE_SUM = 'doc_score_sum'

KAKFA_FIELD_LIST=[
    "dt",
    "req_id",
    "imei",
    STRATEGY_ID_KEY,
    REPORT_INFO,
    FEATURES_KEY,
    CLICK_CNT_SUM,
    EXP_CNT_SUM,
    USER_DURATION_SUM,
    PAY_SUM,
    ECPM_SUM,
    DOC_SCORE_SUM
]


def cpc_recommend_qlearning_numeric_process_fn(msg, model_name, alpha, beta, theta, transform_fn):
    """kafka原始数据处理函数，适用于信息流首页推荐页的 qlearning 数值型模型.

    Args:
        msg: kafka原始数据.
        model_name：模型名，用于过滤样本
        alpha, beta, eta：reward相关参数：alpha*bid_ad + beta*doc_score - eta*negativefeedback
        由于negativefeedback是在用户模板中体现，故将公式简化为: alpha*bid_ad + beta*doc_score
        transform_fn：特征处理函数，参数为字符串，返回值为double数组.

    Returns：
        is_good：Bool 类型，是否成功.
        feature：处理后的特征，double数组，失败为 None
        label：返回三元组 (boost_index, boost_value, reward). 失败为 None.
    """
    try:
        return _do_cpc_recommend_page_process(msg, model_name, alpha, beta, theta, transform_fn)
    except Exception as e:
        logger.info("cpc_recommend_page_qlearning_numeric_process_fn exception = {}".format(e))
        return False, None, None


def cpd_home_qlearning_numeric_process_fn(msg, model_name, alpha, beta, transform_fn):
    """kafka原始数据处理函数，适用于商店首页 qlearning 数值型模型.

    Args:
        msg: kafka原始数据.
        model_name: 模型名, 用于过滤样本.
        beta: reward相关参数, reward = alpha * ltv + beta * bid
        transform_fn: 特征处理函数, 参数为字符串，返回值为double数组.

    Returns:
        is_good: Bool 类型，是否成功.
        feature: 处理后的特征，double数组. 失败为 None.
        label: 返回三元组 (boost_index, boost_value, reward). 失败为 None.
    """
    try:
        return _do_process(msg, model_name, alpha, beta, transform_fn)
    except Exception as e:
        logger.info("cpd_home_qlearning_numeric_process_fn exception = {}".format(e))
        return False, None, None


def _do_process(msg, model_name, alpha, beta, transform_fn):
    """同cpd_home_qlearning_numeric_process_fn，但不捕获异常"""
    bad = (False, None, None)
    msg = json.loads(msg)
    for key in KAKFA_FIELD_LIST:
        if key not in msg:
            logger.error("msg error: '{}' not in msg".format(key))
            return bad
    if model_name != msg[STRATEGY_ID_KEY]:
        return bad
    ltv = float(msg[LTV_KEY] or -0.05)
    bid = float(msg[BID_KEY] or -0.05)
    reward = alpha * ltv + beta * bid
    feature = msg[FEATURES_KEY]
    action = msg[ACTION_KEY]
    tokens = action.split(';')       # token可能由于kafka数据异常而导致输入错误
    if len(tokens) < 2:
        return bad
    boost_value = float(tokens[3])
    boost_index = float(tokens[1])
    feature = transform_fn(feature.encode('utf-8'))
    return True, feature, (boost_index, boost_value, reward)


def _do_cpc_recommend_page_process(msg, model_name, alpha, beta, theta, transform_fn):
    """对于浏览器首页推荐页而言，做情况的try catch..."""
    bad = (False, None, None)
    msg = json.loads(msg)
    for key in KAKFA_FIELD_LIST:
        if key not in msg:
            logger.error("msg error: '{}' not in msg".format(key))
            return bad
    if model_name != msg[STRATEGY_ID_KEY]:
        return bad

    # alpha*pay_sum + beta*user_duration_sum - theta
    pay_sum = float(msg[PAY_SUM] or 0.0)
    user_duration_sum = float(msg[USER_DURATION_SUM] or 0.0)
    reward = alpha * pay_sum + beta * user_duration_sum - theta
    feature = msg[FEATURES_KEY]
    action = msg[REPORT_INFO]
    # action:is_explore/action/reward/value
    tokens = action.split(';')
    if len(tokens) < 2:
        return bad
    boost_value = float(tokens[3])
    boost_index = float(tokens[1])
    feature = transform_fn(feature.encode('utf-8'))
    return True, feature, (boost_index, boost_value, reward)
