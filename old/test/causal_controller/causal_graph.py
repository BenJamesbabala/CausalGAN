'''
To use a particular causal graph, just specify it here


Strings specified have to match *exactly* to keys in attribute text file


A graph lists each node and it's parents in pairs

A->B, C->D, D->B:
    [['A',[]],
     ['B',['A','D']],
     ['C',[]],
     ['D',[]]]

'''

#A reminder of what labels are available
#Make sure to use caps-sensitive correct spelling
all_nodes=[
        ['5_o_Clock_Shadow',[]],
        ['Arched_Eyebrows',[]],
        ['Attractive',[]],
        ['Bags_Under_Eyes',[]],
        ['Bald',[]],
        ['Bangs',[]],
        ['Big_Lips',[]],
        ['Big_Nose',[]],
        ['Black_Hair',[]],
        ['Blond_Hair',[]],
        ['Blurry',[]],
        ['Brown_Hair',[]],
        ['Bushy_Eyebrows',[]],
        ['Chubby',[]],
        ['Double_Chin',[]],
        ['Eyeglasses',[]],
        ['Goatee',[]],
        ['Gray_Hair',[]],
        ['Heavy_Makeup',[]],
        ['High_Cheekbones',[]],
        ['Male',[]],
        ['Mouth_Slightly_Open',[]],
        ['Mustache',[]],
        ['Narrow_Eyes',[]],
        ['No_Beard',[]],
        ['Oval_Face',[]],
        ['Pale_Skin',[]],
        ['Pointy_Nose',[]],
        ['Receding_Hairline',[]],
        ['Rosy_Cheeks',[]],
        ['Sideburns',[]],
        ['Smiling',[]],
        ['Straight_Hair',[]],
        ['Wavy_Hair',[]],
        ['Wearing_Earrings',[]],
        ['Wearing_Hat',[]],
        ['Wearing_Lipstick',[]],
        ['Wearing_Necklace',[]],
        ['Wearing_Necktie',[]],
        ['Young',[]]
    ]

causal_graphs={

'subset1_nodes':[
    ['Bald',[]],
#        ['Blurry',[]],
#        ['Brown_Hair',[]],
#        ['Bushy_Eyebrows',[]],
#        ['Chubby',[]],
    ['Double_Chin',[]],
#        ['Eyeglasses',[]],
#        ['Goatee',[]],
#        ['Gray_Hair',[]],
    ['Male',[]],
    ['Mustache',[]],
    ['No_Beard',[]],
    ['Smiling',[]],
#        ['Straight_Hair',[]],
#        ['Wavy_Hair',[]],
    ['Wearing_Earrings',[]],
#        ['Wearing_Hat',[]],
    ['Wearing_Lipstick',[]],
    ['Young',[]]
],


'standard_graph':[
   ['Male'   , []              ],
   ['Young'  , []              ],
   ['Smiling', ['Male','Young']]
   ],

'male_causes_beard':[
    ['Male',[]],
    ['No_Beard',['Male']],
],
'male_causes_mustache':[
    ['Male',[]],
    ['Mustache',['Male']],
],

'mustache_causes_male':[
    ['Male',['Mustache']],
    ['Mustache',[]],
],

'young_causes_gray':[
    ['Young',[]],
    ['Gray_Hair',['Young']],
    ],

'gray_causes_young':[
    ['Young',['Gray_Hair']],
    ['Gray_Hair',[]],
    ],

'young_ind_gray':[
        ['Young',[]],
        ['Gray_Hair',[]],
        ],

'old_big_causal_graph':[
        ['Young',[]],
        ['Male',[]],
        ['Eyeglasses',['Young']],
        ['Bald',            ['Male','Young']],
        ['Mustache',        ['Male','Young']],
        ['Smiling',         ['Male','Young']],
        ['Wearing_Lipstick',['Male','Young']],
        ['Mouth_Slightly_Open',['Smiling']],
        ['Narrow_Eyes',        ['Smiling']],
    ],

'small_causal_graph':[
        ['Young',[]],
        ['Male',[]],
        ['Mustache',        ['Male','Young']],
        ['Smiling',         ['Male','Young']],
        ['Wearing_Lipstick',['Male','Young']],
        ['Mouth_Slightly_Open',['Male','Young','Smiling']],
        ['Narrow_Eyes',        ['Male','Young','Smiling']],
    ],


'big_causal_graph':[
        ['Young',[]],
        ['Male',[]],
        ['Eyeglasses',['Young']],
        ['Bald',            ['Male','Young']],
        ['Mustache',        ['Male','Young']],
        ['Smiling',         ['Male','Young']],
        ['Wearing_Lipstick',['Male','Young']],
        ['Mouth_Slightly_Open',['Young','Smiling']],
        ['Narrow_Eyes',        ['Male','Young','Smiling']],
    ],

'complete_big_causal_graph':[
        ['Young',[]],
        ['Male',['Young']],
        ['Eyeglasses',['Male','Young']],
        ['Bald',            ['Male','Young','Eyeglasses']],
        ['Mustache',        ['Male','Young','Eyeglasses','Bald']],
        ['Smiling',         ['Male','Young','Eyeglasses','Bald','Mustache']],
        ['Wearing_Lipstick',['Male','Young','Eyeglasses','Bald','Mustache','Smiling']],
        ['Mouth_Slightly_Open',['Male','Young','Eyeglasses','Bald','Mustache','Smiling','Wearing_Lipstick']],
        ['Narrow_Eyes',['Male','Young','Eyeglasses','Bald','Mustache','Smiling','Wearing_Lipstick','Mouth_Slightly_Open']],
    ],

'complete_minimal_graph':[
        ['Young',[]],
        ['Male',['Young']],
        ['Mustache',        ['Male','Young']],
        ['Wearing_Lipstick',['Male','Young','Mustache']],
        ['Smiling',         ['Male','Young','Mustache','Wearing_Lipstick']],
    ],

'male_ind_mustache ': [
        ['Male',[]],
        ['Mustache',[]]
    ],
'Smiling_MSO ': [
        ['Smiling',[]],
        ['Mouth_Slightly_Open',['Smiling']]
       ],

'Male_Young_Eyeglasses':[
    ['Male',[]],
    ['Young',[]],
    ['Eyeglasses',['Male','Young']]
    ],

'MYESO':[
    ['Male',[]],
    ['Young',['Male']],
    ['Eyeglasses',['Male','Young']],
    ['Smiling',['Male','Young','Eyeglasses']],
    ['Mouth_Slightly_Open',['Male','Young','Eyeglasses','Smiling']],
    ],

'mustache':[
    ['Mustache',[]]
    ],

'male_ind_mustache ': [
        ['Male',[]],
        ['Mustache',[]]
    ],

'male_smiling_lipstick':[
       ['Male'   , []],
       ['Wearing_Lipstick'  , ['Male']],
       ['Smiling', ['Male']]
       ],
'SLM':[
       ['Smiling'   , []],
       ['Wearing_Lipstick'  , ['Smiling']],
       ['Male', ['Smiling','Wearing_Lipstick']]
       ],
'MLS':[
       ['Male'   , []],
       ['Wearing_Lipstick'  , ['Male']],
       ['Smiling', ['Male','Wearing_Lipstick']]
       ],
'M':[
    ['Male',[]]
    ],

'Smiling_MSO ': [
        ['Smiling',[]],
        ['Mouth_Slightly_Open',['Smiling']]
       ],
'MYESO':[
    ['Male',[]],
    ['Young',['Male']],
    ['Eyeglasses',['Male','Young']],
    ['Smiling',['Male','Young','Eyeglasses']],
    ['Mouth_Slightly_Open',['Male','Young','Eyeglasses','Smiling']],
    ],

'MSO_smiling ': [
        ['Smiling',['Mouth_Slightly_Open']],
        ['Mouth_Slightly_Open',[]]
       ],
'Male_Young_Eyeglasses ': [
        ['Male',[]],
        ['Young',[]],
        ['Eyeglasses',['Male','Young']]
        ],
'Male_Young_Eyeglasses_complete ': [
        ['Male',[]],
        ['Young',['Male']],
        ['Eyeglasses',['Male','Young']]
        ],
'male_mustache_lipstick':[
       ['Male'   , []],
       ['Mustache', ['Male']],
       ['Wearing_Lipstick'  , ['Male','Mustache']]
       ]
}

def get_causal_graph(causal_model=None,*args,**kwargs):

    if not causal_model in causal_graphs.keys():
        raise ValueError('the specified graph:',causal_model,' was not one of\
                         those listed in ',__file__)

    else:
        return causal_graphs[causal_model]
