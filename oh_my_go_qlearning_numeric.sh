#! /usr/bin/env bash

export ANACONDA2_ROOT=/data/aimaker/pyenv/anaconda2_tf1_14/
export PATH="${ANACONDA2_ROOT}/bin:$PATH"
export LD_LIBRARY_PATH="${ANACONDA2_ROOT}/lib/python2.7/site-packages/tensorflow/:$LD_LIBRARY_PATH"

set -e

cd "$( dirname "${BASH_SOURCE[0]}" )"

model_dir=`pwd`/qlearning_numeric_model_dir
export_model_dir=`pwd`/qlearning_numeric_export_model_dir
is_test=false

rm -rf ${model_dir}

python main.py \
    --is_test=${is_test} \
    --model_dir=${model_dir} \
    --export_model_dir=${export_model_dir} \
    --model_type=cpc_browser_recommend_numeric_qlearning \
    --period_export_interval_second=60 \
    --period_monitor_interval_second=10 \
    --dataset_num_process=1 \
    --kafka_subscribe_topic=mix_cpc_sum \
    --kafka_consumer_num=1 \
    --msg_queue_maxsize=100000 \
    --kafka_boostrap_servers=shizhu-kafka.prd.vivo.lan:9092 \
    --kafka_sasl_username=aimaker \
    --kafka_sasl_password=YXdxZ0xpSEYxVlB3 \
    --kafka_group_id=mix_cpc_sum_nqlearn_v1 \
    --kafka_client_id=aimaker \
    --model_name=cpc_recommend_nqlearning_v1 \
    --export_postprocess_script=push_model_to_hdfs.sh \
    --feature_conf_path=./data/cpc_nqlearn_conf_v1.json \
    --transform_func_path=./data/transform_func.json \
    --logfile=easymix_qlearning_numeric.log \
    --loglevel=INFO \
    --qlearning_score_type=1 \
    --qlearning_explore_prob=0.15 \
    --qlearning_action_type=2 \
    --qlearning_item_type_cnt=2 \
    --3,4,5,5,5,7\
    --qlearning_boundary_lower=0.0003 \
    --qlearning_boundary_upper=0.0004 \
    --qlearning_boundary_step=0.00001 \
    --qlearning_init_qvalue=0.8 \
    --qlearning_update_method=step \
    --qlearning_learning_rate=0.8 \
    --qlearning_ltv_alpha=1.0 \
    --qlearning_bid_beta=1.0 \
    --pay_alpha=0.0015 \
    --user_duration_beta=0.000055 \