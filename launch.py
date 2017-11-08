import argparse
import os
import random
import subprocess
import numpy as np

parser = argparse.ArgumentParser(description='Run the ReferringRelationships model with varying parameters.')
parser.add_argument('--gpu', type=str, default='1')
parser.add_argument('--nruns', type=int, default=50)
parser.add_argument('--workers', type=str, default='8')
parser.add_argument('--epochs', type=str, default='50')
parser.add_argument('--models-dir', type=str,
                    default='/data/chami/ReferringRelationships/models/VRD/10_24_2017/baseline')
parser.add_argument('--train-data-dir', type=str,
                    default='/data/ranjaykrishna/ReferringRelationships/data/dataset-vrd/train')
parser.add_argument('--val-data-dir', type=str,
                    default='/data/ranjaykrishna/ReferringRelationships/data/dataset-vrd/val')
parser.add_argument('--test-data-dir', type=str,
                    default='/data/ranjaykrishna/ReferringRelationships/data/dataset-vrd/test')
parser.add_argument('--model', type=str, default='baseline')
parser.add_argument('--categorical-predicate', action='store_true')
parser.add_argument('--use-internal-loss', action='store_true')
parser.add_argument('--num-predicates', type=str, default='70')
parser.add_argument('--num-objects', type=str, default='100')
parser.add_argument('--use-predicate', type=str, default='1', help='1/0 indicating whether to use the predicates.')
args = parser.parse_args()


for _ in range(args.nruns):
    params = {
        'lr': 0.001, 
        'patience': 4,
        'lr-reduce-rate': 0.8,
        'dropout': 0.2, #'%.1f' % random.uniform(0.0, 0.5),
        'opt': "rms", 
        'batch-size': 32, 
        'hidden-dim': 512, 
        'input-dim': 224, 
        'cnn': 'vgg', 
        'feat-map-layer': 'block3_conv4',
        'feat-map-dim': 56,
        'nb-conv-im-map': 1,
        'conv-im-kernel': 1,
        'nb-conv-att-map': 3, #np.random.choice([1, 2, 3, 4, 5]),
        'conv-predicate-kernel': 5, #np.random.choice([3, 4, 5, 7]),
        'heatmap-threshold': 0.5,
        'conv-predicate-channels': 10, #np.random.choice([1, 3, 5, 10]),
        'w1': 5., #np.random.choice([2.5, 5., 7.5, 10.]),
        'loss-func': 'weighted',
        #'internal-loss-weight': np.random.choice([5., 10.]),
        'iterations': 3, #np.random.choice([1, 2, 3, 4, 5])
    }
    arguments = ' '.join(['--' + k + ' ' + str(params[k]) for k in params])
    train = 'CUDA_VISIBLE_DEVICES=' + args.gpu + ' python train.py --use-models-dir --model ' + args.model + ' --epochs ' + args.epochs + ' --workers ' + args.workers
    train += ' --models-dir ' + args.models_dir + ' --train-data-dir ' + args.train_data_dir + ' --val-data-dir ' + args.val_data_dir + ' --test-data-dir ' + args.test_data_dir
    if args.categorical_predicate:
        train += ' --categorical-predicate'
    if args.use_internal_loss:
        train += ' --use-internal-loss'
    train += ' --num-predicates ' + args.num_predicates + ' --num-objects ' + args.num_objects + ' --use-predicate ' + args.use_predicate
    train += ' ' + arguments
    print('\n' +'*'*89 + '\n')
    print(train)
    subprocess.call(train, shell=True)
