import sys, os, getopt

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from inputs import get_inputs_gbx



def usage():
    print('''\
Usage: ./visualize.py [OPTION]... [FILE]...

  -h, --help    show this help message
  -W, --width   set figure width
  -H, --height  set figure height per graph
  -s, --save    save figure to image\
''');


def fname_from_gbx(gbx_fname, repl):
    return os.path.basename(gbx_fname).replace('.Replay.Gbx', repl)

def plot_stepfill(axis, x, y, color):
    axis.step(x, y, where='post', color=color)
    axis.fill_between(x, y, step='post', alpha=0.3, color=color)

# Plot inputs
def plot_inputs(axis, inputs, label=''):
    plot_stepfill(axis, inputs['steerR'][:,0]/1000, inputs['steerR'][:,1], u'#1f77b4')
    plot_stepfill(axis, inputs['steerL'][:,0]/1000, -inputs['steerL'][:,1], u'#1f77b4')
    plot_stepfill(axis, inputs['brake'][:,0]/1000, inputs['brake'][:,1]*32768, u'#ff7f0e')
    plot_stepfill(axis, inputs['accel'][:,0]/1000, (inputs['accel'][:,1]-1)*32768, u'#2ca02c')
    axis.set_xlim(-2.5, inputs['racetime']/1000)
    axis.set_ylim(-65536, 65536)
    axis.grid()
    axis.set_title(label, fontsize='small', loc='left')

    axis.xaxis.set_major_locator(MultipleLocator(1))
    #axis.xaxis.set_minor_locator(MultipleLocator(0.1))
    axis.set_yticks([-32768,0,32768])
    axis.set_yticklabels([])

# Plot ms inputs
def plot_ms_inputs(axis, inputs, label=''):
    xrange = np.arange(0, int(inputs['racetime']/10)+1)/100
    plot_stepfill(axis, xrange, inputs['ms_steerR'], u'#1f77b4')
    plot_stepfill(axis, xrange, -np.asarray(inputs['ms_steerL']), u'#1f77b4')
    plot_stepfill(axis, xrange, np.asarray(inputs['ms_brake'])*32768, u'#ff7f0e')
    plot_stepfill(axis, xrange, (np.asarray(inputs['ms_accel'])-1)*32768, u'#2ca02c')
    axis.set_xlim(-2.5, inputs['racetime']/1000)
    axis.set_ylim(-65536, 65536)
    axis.grid()
    axis.set_title(label, fontsize='small', loc='left')

    axis.xaxis.set_major_locator(MultipleLocator(1))
    #axis.xaxis.set_minor_locator(MultipleLocator(0.1))
    axis.set_yticks([-32768,0,32768])
    axis.set_yticklabels([])


# Plot from replay file names
def plot_replays(gbxFileNames, fig_width=20, fig_height=2, savefig=False):
    n_plots = len(gbxFileNames)
    if n_plots == 0:
        return

    fig, axs = plt.subplots(n_plots, 1, figsize=(fig_width, fig_height*n_plots),
        constrained_layout=True, sharex=True, sharey=True, squeeze=False)

    for nn, ax in enumerate(axs.flat):
        gbxFileName = gbxFileNames[nn]
        inputs = get_inputs_gbx(gbxFileName)
        plot_inputs(ax, inputs, fname_from_gbx(gbxFileName, ''))

    if savefig:
        plt.savefig(fname_from_gbx(gbxFileName, '.png'))
    else:
        plt.show()


def main():
    # Read options & arguments
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hW:H:s",
            ["help", "width=", "height=", "save"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    # Default values
    fig_width  = 20
    fig_height = 2
    savefig = False

    # Process options
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-W", "--width"):
            fig_width = int(a)
        elif o in ("-H", "--height"):
            fig_height = int(a)
        elif o in ("-s", "--save"):
            savefig = True

    plot_replays(args, fig_width, fig_height, savefig)
    return

    # Process arguments
    n_plots = len(args)
    if n_plots == 0:
        print('No provided files!')
        sys.exit(2)

    # Create figure + axis
    fig, axs = plt.subplots(n_plots, 1, figsize=(fig_width, fig_height*n_plots),
        constrained_layout=True, sharex=True, sharey=True, squeeze=False)

    # Plot
    for nn, ax in enumerate(axs.flat):
        gbx_fname = args[nn]
        print(gbx_fname)

        inputs = get_inputs_gbx(gbx_fname)

        plot_inputs(ax, inputs, fname_from_gbx(gbx_fname, ''))

    if savefig:
        plt.savefig(fname_from_gbx(gbx_fname, '.png'))
    else:
        plt.show()



if __name__ == '__main__':
    main()
