import numpy as np
import matplotlib.pylab as plt
from izhikevichModel import izhikevichModel
from matplotlib import animation
from matplotlib.pyplot import  Button
from matplotlib.widgets import Slider

#a describes the time scale of the recovery variable u. Smaller values result in slower recovery. a = 0.02 is a typical value
a = 0.02

# Parameter b describes the sensitivity of the recovery variable u to the subthreshold fluctuations of the membran potential v.
# Greater values couple v and u more strongly resulting in possible subthreshold oscillations and low threshold spiking. b = 0.2 is a typical value.
b = 0.2

# The parameter c describes the after-spike reset value of the membrane potential v caused by the fast high-threshold K+ conductances. 
# A typical value is c = -65 mV.
c = -65.0

# The parameter d describes after-spike reset of the recovery variable u caused by slow high-threshold Na+ and K+ conductances.
# A typical value is d = 2.
d = 8.0

# Parameter v is the membrane potential. A typical value is -70mV
v0 = -70.0

# Parameter u represents a membrane recovery variable, which accounts for for the activation of K+ ionic currents and inactivation of Na+ ionic currents
u0 = -20.0

# Parameter I is the current that was inserted in the neuron
I = 20.0

l = 2000            # simulation length [ms]
dt = 0.2            # step size [ms]
time = np.arange(0, l , dt)
index = 0
I_val = np.zeros(len(time))
I_val[0: len(time) - 1]  = 0.0
v = izhikevichModel(a, b, c, d, I_val, v0, u0, dt)
constantC = False
#Measurements that are visible at a time
visible = 500

def plot_Izhikevich():

    #Initalize the plot configurations
    fig, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot(range(visible), range(visible))
    line1.set_label("Membrane Potential")
    line2, = ax.plot(range(visible), range(visible))
    line2.set_label("Current")
    
    ax.set_ylim(-95, 80)
    ax.set_xlim(0,visible -1)

    plt.title("Interactive Izhikevich Neuron Simulation")
    fig.subplots_adjust(left=0.1, bottom=0.5)
    
    # removes the ticks on the x axes
    plt.tick_params(
    axis ='x',          # changes apply to the x-axis
    which ='both',      # both major and minor ticks are affected
    bottom = False,      # ticks along the bottom edge are off
    top = False,         # ticks along the top edge are off
    labelbottom = False) # labels along the bottom edge are off
    
   
    # add legend
    plt.legend(loc="upper right")

    # add axis labels
    plt.ylabel("Potential [V]/ Current [A]")
    plt.xlabel("Time [s]")
   
   
    #puts the button un its position
    Current_button_ax = plt.axes([0.1, 0.4, 0.15, 0.04])

    #Defines the CURRENT button
    Current_button = Button(
        Current_button_ax,
        'Current',
        color='chocolate',
        hovercolor='0.975')    
    
    #event when the button was clicked
    def Current_button_was_clicked(event):
        I_val[index+visible-1] = I
        global v
        v = izhikevichModel(a, b, c, d, I_val, v0, u0, dt)
        
    Current_button.on_clicked(Current_button_was_clicked)
    
      #puts the button un its position
    ConstantCurrent_button_ax = plt.axes([0.1, 0.35, 0.15, 0.04])

    #Defines the CURRENT button
    ConstantCurrent_button = Button(
        ConstantCurrent_button_ax,
        'Constant Current',
        color='chocolate',
        hovercolor='0.975')    
    
    
    #event when the button was clicked
    def ConstantCurrent_button_was_clicked(event):
        global constantC
        global v
        if (constantC == False):
            I_val[index +visible-1: len(time) - 1]  = I
         
            v = izhikevichModel(a, b, c, d, I_val, v0, u0, dt)
            constantC = True
            ConstantCurrent_button.color = 'darkorange'
        else:
            I_val[index +visible-1: len(time) - 1]  = 0.0
         
            v = izhikevichModel(a, b, c, d, I_val, v0, u0, dt)
            constantC = False
            ConstantCurrent_button.color = 'chocolate'
    
    ConstantCurrent_button.on_clicked(ConstantCurrent_button_was_clicked)
    
    # Create axes for Current slider
    ax_Current = fig.add_axes([0.4, 0.4, 0.2, 0.02])
    ax_Current.spines['top'].set_visible(True)
    ax_Current.spines['right'].set_visible(True)
    
    #Create slider
    s_Current = Slider(ax=ax_Current, label='Current ', valmin=-50, valmax=50, valinit=20, valfmt='%d mA', facecolor='darkorange')

    #Slider event
    def sliderUpdate(val):
        global I
        global constantC
        I = val
        if (constantC):
            constantC = False
            ConstantCurrent_button_was_clicked(None)
        
    s_Current.on_changed(sliderUpdate)
    
    #updates for the animation
    def update(i):
        global index
        global v
        
        #Resets the graph
        if(i == len(v)-visible-1):
            I_val[0: len(time) - 1]  = 0.0
            v = izhikevichModel(a, b, c, d, I_val, v0, u0, dt)     
            
        index = i
        newData=v[i:i+visible]
        line1.set_ydata(newData)
        line2.set_ydata(I_val[i:i+visible])
        return [line1,line2]
    
    anim = animation.FuncAnimation(fig, update, frames=len(v)-visible, interval=40, blit=True)

    neuronButtons_ax={}
    neuronButtons={}
    neuronValues={}

    #All Neuron Buttons
    ax.text(5, -188, "Excitatory Cortical Neurons")
    neuronButtons_ax['RS'] = plt.axes([0.1, 0.24, 0.2, 0.05])
    neuronButtons['RS'] = Button(neuronButtons_ax['RS'], 'Regular Spiking', color='skyblue', hovercolor='0.975')
    neuronValues['RS'] = [0.1,0.2,-65.0,8.0]
    
    neuronButtons_ax['IB'] = plt.axes([0.1, 0.18, 0.2, 0.05])
    neuronButtons['IB'] = Button(neuronButtons_ax['IB'], 'Intrinsically Bursting', color='steelblue', hovercolor='0.975')
    neuronValues['IB'] = [0.02,0.2,-55.0,4.0]

    neuronButtons_ax['CH'] = plt.axes([0.1, 0.12, 0.2, 0.05])
    neuronButtons['CH'] = Button(neuronButtons_ax['CH'], 'Chattering', color='steelblue', hovercolor='0.975')
    neuronValues['CH'] = [0.02,0.2,-50.0,2.0]
 
     
    ax.text(190, -188, "Inhibitory Cortical Neurons")
    neuronButtons_ax['FS'] = plt.axes([0.4, 0.24, 0.2, 0.05])
    neuronButtons['FS'] = Button(neuronButtons_ax['FS'], 'Fast Spiking', color='steelblue', hovercolor='0.975')
    neuronValues['FS'] = [0.1,0.2,-65.0,2.0]
    
    neuronButtons_ax['LTS'] = plt.axes([0.4, 0.18, 0.2, 0.05])
    neuronButtons['LTS'] = Button(neuronButtons_ax['LTS'], 'Low-Threshold Spiking', color='steelblue', hovercolor='0.975')
    neuronValues['LTS'] = [0.02,0.25,-65.0,2.0]

    ax.text(395, -188, "Resonator Neurons")    
    neuronButtons_ax['RZ'] = plt.axes([0.7, 0.24, 0.2, 0.05])
    neuronButtons['RZ'] = Button(neuronButtons_ax['RZ'], 'Resonator', color='steelblue', hovercolor='0.975')
    neuronValues['RZ'] = [0.1,0.26,-65.0,8.0]

    #Changes the model's configuration
    def changeNeuron(event):
        for btn in ["RS", "IB", "CH", "FS", "LTS", "RZ"]:
            if neuronButtons[btn].ax == event.inaxes:
                global a, b, c, d, v0, u0, v
                a = neuronValues[btn][0]
                b = neuronValues[btn][1]
                c = neuronValues[btn][2]
                d = neuronValues[btn][3]
                v = izhikevichModel(a, b, c, d, I_val, v0, u0, dt)
                
    #Changes the button color of the selected button
    def changeColor(event):
        for btn in ["RS", "IB", "CH", "FS", "LTS", "RZ"]:
            if neuronButtons[btn].ax == event.inaxes:
                neuronButtons[btn].ax.set_facecolor('skyblue')
                neuronButtons[btn].color = 'skyblue'
            else:
                neuronButtons[btn].ax.set_facecolor('steelblue')
                neuronButtons[btn].color = 'steelblue'
    
    #Initalizes the button fuctions
    for btn in ["RS", "IB", "CH", "FS", "LTS", "RZ"]:
        neuronButtons[btn].on_clicked(changeColor)
        neuronButtons[btn].on_clicked(changeNeuron)               
    
    #plots the graph
    plt.show()
    
if (__name__ == '__main__'):
    plot_Izhikevich()
 
