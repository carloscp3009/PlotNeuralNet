
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

w_scaler = 1.5
arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_source( '../static/robot.png', to='(-7,0,-2)' ,width=4, height=7, straight=True),
    to_source( '../static/rgb.png', to='(-7,-12,-2)', straight=True),
    to_source( '../static/depth.png', to='(-7,-27,-2)', straight=True),
    #input
    to_source( '../static/robot.png', to='(-6,0.2,-1)' ,width=4, height=7, straight=True),
    to_source( '../static/rgb.png', to='(-6,-11.8,-1)', straight=True),
    to_source( '../static/depth.png', to='(-6,-26.8,-1)', straight=True),

    #input
    to_source( '../static/robot.png', to='(-5,0,0)' ,width=4, height=7, caption='Robot State', straight=True),
    to_source( '../static/rgb.png', to='(-5,-12,0)', caption='RGB', straight=True),
    to_source( '../static/depth.png', to='(-5,-27,0)', caption='Depth', straight=True),

    #input layer
    to_input( name='sensors', s_filer="", n_filer="", offset="(3,0,0)", to="(-1,0,0)", width=w_scaler*1, height=1, depth=5, caption='32x1' ),
    to_input( name='rgb', s_filer="", n_filer="", offset="(3,0,0)", to="(-1,-10,0)", width=w_scaler*0.9, height=45, depth=45, caption='224x224x3' ),
    to_input( name='depth', s_filer="", n_filer="", offset="(3,0,0)", to="(-1,-25,0)", width=w_scaler*0.4, height=45, depth=45, caption='224x224x1' ),
   
    #Feature Extraction
    to_Conv( name='sensors_fx1', s_filer="", n_filer="", offset="(5,0,0)", to="(sensors-east)", width=w_scaler*1, height=1, depth=40, caption='512x1', ),
    to_Conv( name='sensors_fx', s_filer="", n_filer="", offset="(4,0,0)", to="(sensors_fx1-east)", width=w_scaler*1, height=1, depth=40, caption='512x1', ),
    to_ConeBox( name='rgb_fx', s_filer="", n_filer="", offset="(3,0,0)", to="(rgb-east)", width=w_scaler*35, height=1.5, depth=1.5, caption='YOLOv8 Backbone', opacity=0.3 ),
    *custom_CNN( name='depth_block', botton='depth', top='depth_fx', offset="(3,0,0)", opacity=0.5, n_scaler=10/w_scaler , s_scaler=5),
    to_connection('sensors_fx1', 'sensors_fx'),
    to_connection('sensors', 'sensors_fx1'),
    to_connection('rgb', 'rgb_fx'),
    
    to_Box( name='rgb_fxt', s_filer="", n_filer=256, offset="(2,0,0)", to="(rgb_fx-east)", width=w_scaler*25, height=1.5, depth=1.5, caption='RGB Features' ),
    to_Box( name='depth_fxt', s_filer="", n_filer=256, offset="(0,0,0)", to="(rgb_fxt-east)", width=w_scaler*25, height=1.5, depth=1.5, caption='Depth Features' ),
    to_Box( name='stack', s_filer="", n_filer="", offset="(0,0,0)", to="(rgb_fxt-west)", width=w_scaler*50, height=7, depth=7, caption='Channel Stacking', color="\ConcatColor", opacity=0.4 ),
    to_skip( "rgb_fx", "rgb_fxt", 4),
    to_skip( of="depth_fx", to="depth_fxt", up=True),
    to_text("7x7x512", to="(25,-13.5,0)", name="7x7x512", caption_size=20),
    to_text("7x7x256", to="(29,-26,0)", name="7x7x256", caption_size=20),
    

    # #Mid-Fusion
    to_ConvRelu( 'flat_conv', s_filer="", n_filer="", offset="(3,0,0)", to="(stack-east)", width=w_scaler*1, height=1, depth=50, caption="512x1" ),
    to_Box( 'flat_conv_copy', s_filer="", n_filer="", offset="(3,0,0)", to="(flat_conv-east)", width=w_scaler*1, height=1, depth=50, caption="1024x1" ),
    to_Box( name='Sensors_copy', s_filer="", n_filer="", offset="(0,0,-10)", to="(flat_conv_copy-west)", width=w_scaler*1, height=1, depth=50, caption="" ),
    to_Box( name='concat', s_filer="", n_filer="", offset="(6,0,-5)", to="(stack-east)", width=w_scaler*3, height=3, depth=100, caption="", color="\ConcatColor", opacity=0.4 ),
    to_text("Concat", to="(38,-14.5,0)", name="Concat", caption_size=20),
    to_skip( "sensors_fx", "Sensors_copy", 4),
    to_skip( "flat_conv", "flat_conv_copy", 4),
    to_connection('stack', 'flat_conv'),

    # #Decoder
    to_Box( name='lstm', s_filer="", n_filer="", offset="(3,0,0)", to="(concat-east)", width=w_scaler*1, height=1, depth=50, caption="512", color="\SoftmaxColor", opacity=0.4 ),
    to_lstm('lstm'),   
    to_Conv( name='head_1', s_filer="", n_filer="", offset="(3,0,0)", to="(lstm-east)", width=w_scaler*1, height=1, depth=50, caption="512",),
    to_Box( name='output', s_filer="", n_filer="", offset="(3,0,0)", to="(head_1-east)", width=w_scaler*1, height=1, depth=5, caption="24", color='\SumColor'),
    to_text("LSTM", to="(43,-12.5,0)", name="LSTM", caption_size=20),
    to_connection('concat', 'lstm'),
    to_connection('lstm', 'head_1'),
    to_connection('head_1', 'output'),
    to_text("Joints Position ", to="(52,-12,0)", name="output", caption_size=20),
    to_text(" + ", to="(52,-13,0)", name="output1", caption_size=20),
    to_text("Walking Speed", to="(52,-14,0)", name="output2", caption_size=20),

    # # Legends
    # to_input( name='INPUT', s_filer="", n_filer="", offset="(7,12,0)", to="(output-east)", width=w_scaler*5, height=5, depth=5, caption='INPUT TENSOR' ),
    # to_Conv( name='FC', s_filer="", n_filer="", offset="(0,-4,0)", to="(INPUT-west)", width=w_scaler*5, height=5, depth=5, caption="FC RELU",),
    # to_ConvRelu( 'CONVRELU', s_filer="", n_filer="", offset="(0,-4,0)", to="(FC-west)", width=w_scaler*5, height=5, depth=5, caption="CONV RELU" ),
    # to_Box( name='POOL', s_filer="", n_filer="", offset="(0,-4,0)", to="(CONVRELU-west)", width=w_scaler*5, height=5, depth=5, caption="POOLING", color="\PoolColor", opacity=0.4 ),
    # to_Box( name='COPY', s_filer="", n_filer="", offset="(0,-4,0)", to="(POOL-west)", width=w_scaler*5, height=5, depth=5, caption="TENSOR COPY" ),
    # to_Box( name='CONCAT', s_filer="", n_filer="", offset="(0,-4,0)", to="(COPY-west)",width=w_scaler*5, height=5, depth=5, caption="TENSOR CONCAT", color="\ConcatColor", opacity=0.4 ),
    # to_Box( name='LSTM', s_filer="", n_filer="", offset="(0,-4,0)", to="(CONCAT-west)", width=w_scaler*5, height=5, depth=5, caption="LSTM", color="\SoftmaxColor", opacity=0.4 ),
    # to_lstm('LSTM'),   
    # to_Box( name='FC', s_filer="", n_filer="", offset="(0,-4,0)", to="(LSTM-west)", width=w_scaler*5, height=5, depth=5, caption="FC", color="\SumColor", opacity=0.4 ),
     
    to_end() 
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
