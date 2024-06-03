
from .tikzeng import *

#define new block
def block_2ConvPool( name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5, autoscale=(1,1)):
    if autoscale:
        size = (s_filer/autoscale[0], s_filer/autoscale[0], n_filer/autoscale[1])
    return [
    to_ConvConvRelu( 
        name=f"ccr_{name}",
        s_filer="", 
        n_filer=("",""), 
        offset=offset, 
        to=f"({botton}-east)", 
        width=(size[2],size[2]), 
        height=size[0], 
        depth=size[1],
        caption=f'{s_filer}x{s_filer}x{n_filer}',   
        ),    
    to_Pool(         
        name=f"{top}", 
        offset="(0,0,0)", 
        to=f"(ccr_{name}-east)",  
        width=0.5,         
        height=(size[0]/2), 
        depth=(size[1]/2), 
        opacity=opacity, ),
    # to_connection( 
    #     f"{botton}", 
    #     f"ccr_{name}"
    #     )
    ]
def block_ConvPool( name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5, autoscale=(1,1)):
    if autoscale:
        size = (s_filer/autoscale[0], s_filer/autoscale[0], n_filer/autoscale[1])
    return [
    to_ConvRelu( f"cr_{name}", s_filer="", n_filer="", offset=offset, to=f"({botton}-east)", width=size[2], height=size[0], depth=size[1], caption=f'{s_filer}x{s_filer}x{n_filer}' ),   
    to_Pool(         
        name=f"{top}", 
        offset="(0,0,0)", 
        to=f"(cr_{name}-east)",  
        width=0.5,         
        height=(size[0]/2), 
        depth=(size[1]/2), 
        opacity=opacity, ),
    # to_connection( 
    #     f"{botton}", 
    #     f"ccr_{name}"
    #     )
    ]

def custom_CNN( name, botton, top, offset="(1,0,0)", opacity=0.5 , n_scaler = 10,  s_scaler = 5):
    return [
    *block_2ConvPool( f"b1_{name}", botton, f'pool_1_{name}', s_filer=224, n_filer=32, offset=offset, autoscale=(s_scaler, n_scaler)),
    *block_2ConvPool( f"b2_{name}", f'pool_1_{name}', f'pool_2_{name}', s_filer=112, n_filer=64, autoscale=(s_scaler, n_scaler)),
    *block_ConvPool( f"b3_{name}", f'pool_2_{name}', f'pool_3_{name}', s_filer=56, n_filer=128, autoscale=(s_scaler, n_scaler)),
    *block_ConvPool( f"b4_{name}", f'pool_3_{name}', f'pool_4_{name}', s_filer=28, n_filer=128, autoscale=(s_scaler, n_scaler)),
    *block_ConvPool( f"b5_{name}", f'pool_4_{name}', f'{top}', s_filer=14, n_filer=256, autoscale=(s_scaler, n_scaler)),
    to_connection( 
        f"{botton}", 
        f"ccr_b1_{name}"
        )
    ]


def block_Unconv( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=1,              height=size[0],       depth=size[1], opacity=opacity ),
        to_ConvRes( name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),    s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_ConvRes( name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),       s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='{}'.format(top),            offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name), s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]

def block_Res( num, name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5 ):
    lys = []
    layers = [ *[ '{}_{}'.format(name,i) for i in range(num-1) ], top]
    for name in layers:        
        ly = [ to_Conv( 
            name='{}'.format(name),       
            offset=offset, 
            to="({}-east)".format( botton ),   
            s_filer=str(s_filer), 
            n_filer=str(n_filer), 
            width=size[2],
            height=size[0],
            depth=size[1]
            ),
            to_connection( 
                "{}".format( botton  ), 
                "{}".format( name ) 
                )
            ]
        botton = name
        lys+=ly
    
    lys += [
        to_skip( of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


