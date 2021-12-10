#! /usr/bin/env bash

export ANACONDA2_ROOT=/data/aimaker/env/anaconda2/
export PATH="${ANACONDA2_ROOT}/bin:$PATH"
export LD_LIBRARY_PATH="${ANACONDA2_ROOT}/lib/python2.7/site-packages/tensorflow/:$LD_LIBRARY_PATH"

set -e

cd "$( dirname "${BASH_SOURCE[0]}" )"

model_dir=`pwd`/model_dir
export_model_dir=`pwd`/export_model_dir
is_test=true

rm -rf ${model_dir}

python main.py \
    --is_test=${is_test} \
    --model_dir=${model_dir} \
    --export_model_dir=${export_model_dir} \
    --model_type=linucb \
    --period_export_interval_second=60 \
    --period_monitor_interval_second=10 \
    --dataset_num_process=1 \
    --kafka_subscribe_topic=dw_mix_cpd_feature_statis \
    --kafka_consumer_num=1 \
    --msg_queue_maxsize=100000 \
    --kafka_boostrap_servers=shizhu-kafka.prd.vivo.lan:9092 \
    --kafka_sasl_username=aimaker \
    --kafka_sasl_password=YXdxZ0xpSEYxVlB3 \
    --kafka_group_id=mix_sort_linucb_v6_feature \
    --kafka_client_id=aimaker \
    --model_name=cpc_recommend_nqlearning_v1 \
    --export_postprocess_script='' \
    --linucb_reward_beta=1.0 \
    --feature_conf_path=./data/cpc_nqlearn_conf_v1.json \
    --logfile=easymix.log \
    --loglevel=DEBUG \
    --linucb_alpha=0.1 \
    --linucb_score_type=101 \
    --linucb_min_arm=0.5 \
    --linucb_arm_step=0.1 \
    --linucb_arm_num=2 \
    --linucb_matrix_a_initial=1.0 \
    --linucb_vector_b_initial=0.0