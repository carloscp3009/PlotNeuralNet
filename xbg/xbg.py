
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_source( '../static/robot.png' ),
    to_source( '../static/rgb.png', to='(-3,-15,0)'),
    to_source( '../static/depth.png', to='(-3,-30,0)'),

    #input layer
    to_input( name='sensors', s_filer=24, n_filer=1, offset="(0,0,0)", to="(0,0,0)", width=1, height=1, depth=5, caption='Robot State' ),
    to_input( name='rgb', s_filer=224, n_filer=3, offset="(0,0,0)", to="(0,-15,0)", width=0.6, height=45, depth=45, caption='RGB' ),
    to_input( name='depth', s_filer=224, n_filer=1, offset="(0,0,0)", to="(0,-30,0)", width=0.2, height=45, depth=45, caption='Depth' ),
   
    #Feature Extraction
    to_Conv( name='sensors_fx', s_filer=7, n_filer=512, offset="(3,0,0)", to="(sensors-east)", width=1, height=1, depth=40, caption='Custom Layers' ),
    to_Conv( name='rgb_fx', s_filer=7, n_filer=256, offset="(3,0,0)", to="(rgb-east)", width=25, height=1.5, depth=1.5, caption='YOLOv8 Backbone' ),
    *custom_CNN( name='depth_block', botton='depth', top='depth_fx', offset="(0,0,0)", opacity=0.5 ),
    # to_depth_fx( name='depth_fx', s_filer=7, n_filer=256, offset="(1,0,0)", to="(depth-east)", width=20, height=10, depth=10, caption='Custom CNNs' ),
    
    to_Conv( name='depth_fxt', s_filer=7, n_filer=256, offset="(1,15,0)", to="(depth_fx-south)", width=25, height=1.5, depth=1.5, caption='Custom CNNs' ),
    to_Conv( name='rgb_fxt', s_filer=7, n_filer=256, offset="(2,0,0)", to="(rgb_fx-east)", width=25, height=1.5, depth=1.5, caption='YOLO Backbone' ),
    to_skip( "rgb_fx", "rgb_fxt", 3),
    to_skip( of="depth_fx", to="depth_fxt", up=True),
    
    # *block_2ConvPool( name='b2', botton='pool_b1', top='pool_b2', s_filer=256, n_filer=128, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    # *block_2ConvPool( name='b3', botton='pool_b2', top='pool_b3', s_filer=128, n_filer=256, offset="(1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    # *block_2ConvPool( name='b4', botton='pool_b3', top='pool_b4', s_filer=64,  n_filer=512, offset="(1,0,0)", size=(16,16,5.5), opacity=0.5 ),

    # #Bottleneck
    # #block-005
    # to_ConvConvRelu( name='ccr_b5', s_filer=32, n_filer=(1024,1024), offset="(2,0,0)", to="(pool_b4-east)", width=(8,8), height=8, depth=8, caption="Bottleneck"  ),
    # to_connection( "pool_b4", "ccr_b5"),

    # #Decoder
    # *block_Unconv( name="b6", botton="ccr_b5", top='end_b6', s_filer=64,  n_filer=512, offset="(2.1,0,0)", size=(16,16,5.0), opacity=0.5 ),
    # to_skip( of='ccr_b4', to='ccr_res_b6', pos=1.25),
    # *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer=128, n_filer=256, offset="(2.1,0,0)", size=(25,25,4.5), opacity=0.5 ),
    # to_skip( of='ccr_b3', to='ccr_res_b7', pos=1.25),    
    # *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer=256, n_filer=128, offset="(2.1,0,0)", size=(32,32,3.5), opacity=0.5 ),
    # to_skip( of='ccr_b2', to='ccr_res_b8', pos=1.25),    
    
    # *block_Unconv( name="b9", botton="end_b8", top='end_b9', s_filer=512, n_filer=64,  offset="(2.1,0,0)", size=(40,40,2.5), opacity=0.5 ),
    # to_skip( of='ccr_b1', to='ccr_res_b9', pos=1.25),
    
    # to_ConvSoftMax( name="soft1", s_filer=512, offset="(0.75,0,0)", to="(end_b9-east)", width=1, height=40, depth=40, caption="SOFT" ),
    # to_connection( "end_b9", "soft1"),
     
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
