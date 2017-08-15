import numpy as np
import tensorflow as tf

from trainer import Trainer
from config import get_config
from causal_graph import get_causal_graph
from data_loader import get_loader
from utils import prepare_dirs_and_logger, save_config

from IPython.core import debugger
debug = debugger.Pdb().set_trace


'''
TODO:
    Get rid of Supervisor. It's creating backwards compatability issues
    Allow config to default to json during loading
    Allow causal controller to train on its own without began (lower gpu mem)

    Allow batch_size PlaceHolder for causal controller
        faster tvd calculation
        larger batch might help pretraining(limited at 16 right now)

    speedup crosstab
    allow only creation of causal controller graph (should also come with pt speedup)

    #This should be switched for node.label
        tf_parents=[self.z]+[node.label_logit for node in self.parents]

'''

'''
Feeding round(labels) instead of label_logits within cc made a huge difference

Feeding real parents was a bit of a disaster. Not sure why.
Try not doing that but with passing label instead of label_logit
        print 'WARNING: cc passes labels and rounds them before use'
        tf_parents=[self.z]+[tf.round(node.label) for node in self.parents]


Trying to feed real parents:
    real_inputs=tf.concat([label_loader[n] for n in parent_names]+[label_loader[self.name]],axis=1)
    fake_inputs=tf.concat([label_loader[n] for n in parent_names]+[self.label],axis=1)
    #real_inputs=tf.concat([label_loader[n] for n in parent_names]+[label_loader[self.name]],axis=1)
    #fake_inputs=tf.concat([p.label for p in self.parents]+[self.label],axis=1)

Also should pass label in causal controller, not logit
    #tf_parents=[self.z]+[node.label_logit for node in self.parents]
    #tf_parents=[self.z]+[node.label for node in self.parents]
    tf_parents=[self.z]+[tf.round(node.label) for node in self.parents]


There was immediate cc output mode collapse.. not sure what happened. I did decrease
n_critic to 5. I also increased batch_size. I also changed a lot of the code.
Now to experiment.


    config.py
    misc_arg.add_argument('--build_all', type=str2bool, default=False,
                         help='normally specifying is_pretrain=False will cause
                         the pretraining components not to be built and likewise
                          with is_train=False only the pretrain compoenent will
                          (possibly) be built. This is here as a debug helper to
                          enable building out the whole model without doing any
                          training')



Probably each factor should have its own optimizer
Need to finally move pt stuff inside of Causal_Controller.py

#CC
    cc.batch_size is now placeholder

    #def __init__(self,graph,batch_size=1,indep_causal=False,n_layers=3,n_hidden=10,input_dict=None,reuse=None):
    def __init__(self,graph,config,batch_size=1,input_dict=None,reuse=None):


#Trainer
        #self.cc=CausalController(self.graph,config,self.batch_size)
        #                indep_causal=self.config.indep_causal,
        #                n_layers=self.config.cc_n_layers,
        #                n_hidden=self.config.cc_n_hidden,
        #                config=config)
        self.cc=CausalController(self.graph,config,self.batch_size)

        #self.fake_labels=self.cc.labels
        #self.fake_labels_logits= tf.concat( self.cc.list_label_logits(),-1 )
        self.fake_labels=self.cc.fake_labels
        self.fake_labels_logits=self.cc.fake_labels_logits

        #self.var=self.G_var+self.D_var+self.dcc_var+self.cc.var+[self.g_step]
        self.var=self.G_var+self.D_var+self.cc.dcc_var+self.cc.var+[self.g_step]


        #split up to allow batch_size issues
            self.D_fake_labels_logits,self.DL_var=Discriminator_labeler(
                G, len(self.cc), self.repeat_num,
                self.conv_hidden_num, self.data_format)

            self.D_real_labels_logits,  _        =Discriminator_labeler(
                x, len(self.cc), self.repeat_num,
                self.conv_hidden_num, self.data_format, reuse=True)

            #label_logits,self.DL_var=Discriminator_labeler(
            #        tf.concat([G, x], 0), len(self.cc.nodes), self.repeat_num,
            #        self.conv_hidden_num, self.data_format)
            #self.D_fake_labels_logits,self.D_real_labels_logits=tf.split(label_logits,2)

            self.D_var += self.DL_var



Small but modest improvement from fixing gradient penalty.
DiscW only has 4 layers.. so I think best to try to increase that.
Maybe also increase n neurons to 15

def DiscriminatorW(labels,batch_size, n_hidden, config, reuse=None):
def DiscriminatorW(labels,batch_size, n_hidden=10, reuse=None):

        h=labels
        act_fn=lrelu
        n_neurons=n_hidden
        for i in range(config.critic_layers):
            if i==config.critic_layers-1:
                act_fn=None
                n_neurons=1

            scp='WD'+str(i)
            h = slim.fully_connected(h,n_neurons,activation_fn=act_fn,scope=scp)

        #h0 = slim.fully_connected(labels,n_hidden,activation_fn=lrelu,scope='WD0')
        #h1 = slim.fully_connected(h0,n_hidden,activation_fn=lrelu,scope='WD1')
        #h2 = slim.fully_connected(h1,n_hidden,activation_fn=lrelu,scope='WD2')
        #h3 = slim.fully_connected(h2,1,activation_fn=None,scope='WD3')

        return tf.nn.sigmoid(h),h,variables
        #return tf.nn.sigmoid(h3),h3,variables

I'm making several changes that are necessary to penalize the gradient of each
dcc component.


self.dcc_dict=self.DCC(self.real_labels,self.batch_size,n_hidden=n_hidden)
#self.dcc_real,self.dcc_real_logit,self.dcc_var=self.DCC(self.real_labels,self.batch_size,n_hidden=n_hidden)
#self.dcc_fake,self.dcc_fake_logit,self.dcc_var=self.DCC(self.fake_labels,self.batch_size,n_hidden=n_hidden)


models.py
for n,rx,fx in zip(node_names,real_inputs,fake_inputs):
    with tf.variable_scope(n):
        prob,log,var=Net(rx,batch_size,n_hidden,reuse)
        dcc_dict['real_prob'][n]=prob
        dcc_dict['real_logit'][n]=log
        dcc_dict['var'][n]=var

        prob,log,_  =Net(rx,batch_size,n_hidden,reuse=True)
        dcc_dict['fake_prob'][n]=prob
        dcc_dict['fake_logit'][n]=log

        list_logits.append(log)
        logit_sum+=log
        net_var+=var

        grad_cost,slopes=Grad_Penalty(rx,fx,Net,config)
        dcc_dict['grad_cost']=grad_cost
        dcc_dict['slopes']=slopes






----------------
Turns out yes!
Im testing to see if the third margin is necessary at all:
        if not self.config.no_third_margin:
            #normal mode
            #Careful on z_t sign!
            self.g_loss = self.g_loss_image + self.z_t*self.g_loss_label
        else:
            #can we get away without this complicated third margin?
            print('Warning: not using third margin')
            self.g_loss = self.g_loss_image + 1.*self.g_loss_label



'''

def get_trainer(config):
    print 'tf: resetting default graph!'
    tf.reset_default_graph()

    prepare_dirs_and_logger(config)

    rng = np.random.RandomState(config.random_seed)
    #tf.set_random_seed(config.random_seed)

    if config.is_train:
        data_path = config.data_path
        batch_size = config.batch_size
        do_shuffle = True
    else:
        #setattr(config, 'batch_size', 64)
        if config.test_data_path is None:
            data_path = config.data_path
        else:
            data_path = config.test_data_path
        #batch_size = config.sample_per_image
        batch_size = config.batch_size
        do_shuffle = False

    data_loader, label_stats= get_loader(config,
            data_path,config.batch_size,config.input_scale_size,
            config.data_format,config.split,
            do_shuffle,config.num_worker,config.is_crop)

    config.graph=get_causal_graph(config.causal_model)

    print 'Config:'
    print config

    trainer = Trainer(config, data_loader, label_stats)
    return trainer


def main(trainer,config):
    if config.dry_run:
        #debug()
        return

    #if config.is_pretrain or config.is_train:
    if not config.load_path:
        print('saving config because load path not given')
        save_config(config)

    if config.is_pretrain:
        trainer.pretrain()
    if config.is_train:
        trainer.train()
    else:
        if not config.load_path:
            raise Exception("[!] You should specify `load_path` to load a pretrained model")

        trainer.intervention()

def get_model(config=None):
    if not None:
        config, unparsed = get_config()
    return get_trainer(config)

if __name__ == "__main__":
    config, unparsed = get_config()
    trainer=get_trainer(config)
    main(trainer,config)
    ##debug mode: below is main() code