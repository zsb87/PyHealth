from __future__ import division
from __future__ import print_function

# environment setting
import os
import sys
from pathlib import Path

# this should be learning_models
curr_dir = os.getcwd()

# this should be pyhealth, which is two level up from learning_models library
root_dir = Path(curr_dir).parents[1]
os.chdir(root_dir)

### May choose any of these models
# from pyhealth.models.sequence.dipole import Dipole as model
from pyhealth.models.sequence.lstm import LSTM as model
# from pyhealth.models.sequence.gru import GRU as GRU
# from pyhealth.models.sequence.embedgru import EmbedGRU as model
# from pyhealth.models.sequence.retain import Retain as model
# from pyhealth.models.sequence.raim import RAIM as model
# from pyhealth.models.sequence.tlstm import tLSTM as model
# from pyhealth.models.sequence.xgboost import XGBoost as model
# from pyhealth.models.sequence.rf import RandomForest as model

from pyhealth.data.expdata_generator import sequencedata as expdata_generator
from pyhealth.evaluation.evaluator import func

if __name__ == "__main__":
    # override here to specify where the data locates
    # root_dir = ''
    # root_dir = os.path.abspath(os.path.join(__file__, "../../.."))
    data_dir = os.path.join(root_dir, 'datasets', 'cms')

    expdata_id = '2020.0810.data.mortality.mimic'

    # set up the datasets
    cur_dataset = expdata_generator(expdata_id, root_dir=root_dir)
    cur_dataset.get_exp_data(sel_task='mortality', data_root=data_dir)
    cur_dataset.load_exp_data()
    cur_dataset.show_data()

    # initialize the model for training
    # turn on GPU by setting use_gpu to True
    expmodel_id = '2020.0810.gru.data.mortality.mimic.gpu'
    clf = model(expmodel_id=expmodel_id, n_batchsize=20, use_gpu=True,
                n_epoch=100, gpu_ids='0,1')
    clf.fit(cur_dataset.train, cur_dataset.valid)

    # load the best model for inference
    clf.load_model()
    clf.inference(cur_dataset.test)
    pred_results = clf.get_results()
    print(pred_results['hat_y'])

    # evaluate the model
    r = func(pred_results['hat_y'], pred_results['y'])
    print(r)
