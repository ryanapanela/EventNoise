# %%
import os
from psychopy import gui, event, core
from Auditory import auditory_experiment
from SpeechIntelligibility import speech_intelligibility

# Initialize Global Shutdown Key
event.globalKeys.add(key='escape', func=os._exit, func_args=[1], func_kwargs=None)

# %% Collect Subject Data

# Create a gui object
subgui = gui.Dlg() 

# Add fields. The strings become the labels in the gui
subgui.addField('Subject ID:')
subgui.addField('Stimulus Group:', choices=['Auditory'])
subgui.addField('Start From:', choices=['Practice', 'Story 1', 'Story 2', 'Story 3', 'Speech Intelligibility'])

# Show gui
subgui.show()

# Assign variables to the outputs
subjID = int(subgui.data[0])
group = subgui.data[1]
start = subgui.data[2]


# %% Run Group Experiment
if group == 'Auditory' and start != 'Speech Intelligibility':
	# Run Auditory.py
	auditory_experiment(subjID, group, start)

# %% Run Speech Intelligibility

if group == 'Auditory' or start == 'Speech Intelligibility':
	speech_intelligibility(subjID, group)

core.quit()
