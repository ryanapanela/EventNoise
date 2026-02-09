import numpy as np
import random
import pandas as pd
import os, sys
import json
from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']
from psychopy import visual, core, event, gui, logging, sound


# %% Create Function
def speech_intelligibility(subjID, group):

    # %% Initialize Experiment Window
    # win = visual.Window(size=(800, 600), allowGUI=True, color='grey', units='height', pos=[100, 100])
    win = visual.Window(size=(800, 600), fullscr=True, allowGUI=True, color='grey', units='height', pos=[100, 100])
    win.mouseVisible = False

    # Quality check ensure refresh rate is accurate
    win.recordFrameIntervals = True
    win.refreshThreshold = 1 / 60 + 0.005
    logging.console.setLevel(logging.WARNING)

    # %% Prepare Output File
    outputFolderName = 'data' + os.sep + 'en' + format(subjID, '02d') + 'Auditory'
    outputFileName = 'en' + format(subjID, '02d') + '_intelligibility'

    if os.path.exists(outputFolderName + os.sep + 'Speech Intelligibility'):
        print('Data for this participant already exists.')
        #sys.exit('Data for this participant already exists.')

    elif os.path.exists(outputFolderName):
        os.mkdir(outputFolderName + os.sep + 'Speech Intelligibility')

    else:
        os.mkdir(outputFolderName)
        os.mkdir(outputFolderName + os.sep + 'Speech Intelligibility')

    # Initialize Output Variables
    outVars = ['Subject', 'Group', 'Trial', 'Sentence ID', 'Noise Condition', 'Audio', 'Response', 'Running Time']

    out = pd.DataFrame(columns=outVars)
    outDict = dict.fromkeys(outVars, None)

    # %% Initialize Experimental Parameters

    # Instruction Image
    instructionFile = 'instructions' + os.sep + 'speech_intelligibility' + os.sep + 'Slide1.png'
    textBox = 'instructions' + os.sep + 'speech_intelligibility' + os.sep + 'Slide3.png'
    endExperiment = 'instructions' + os.sep + 'speech_intelligibility' + os.sep + 'Slide4.png'

    # Fixation Cross
    fixationFile = 'instructions' + os.sep + 'speech_intelligibility' + os.sep + 'Slide2.png'
    fixation = visual.ImageStim(win, image=fixationFile, interpolate=True, size=(1.8, 1))

    # Randomize Stimuli
    SNR_folder = ['clear', '+4 SNR', '-2 SNR'] * 10
    random.shuffle(SNR_folder)

    sentenceNum = np.linspace(1, 30, 30)
    random.shuffle(sentenceNum)

    # %% Initialize Instructions

    # Prepare Image
    instr = visual.ImageStim(win, image=instructionFile, interpolate=True, size=(1.8, 1))

    # Draw Image to Buffer
    instr.draw()

    # Flip to Reveal
    win.flip()

    # Initialize Key Waiting
    event.waitKeys(keyList=['space'])
    win.flip()
    core.wait(1.0)

    # %% Experiment Loop

    # Initialize Running Experiment Clock
    expClock = core.Clock()

    # Initialized Trial Clock
    trialClock = core.Clock()

    for trial in range(30):
        # Draw Fixation Cross
        fixation.draw()
        win.flip()

        # Wait 3 seconds
        core.wait(3.0)

        currentSentence = 'audio/Speech Intelligibility Task/sentences/' + SNR_folder[trial] + '/Sentence ' + \
                          str(int(sentenceNum[trial])) + '.wav'

        currentAudio = sound.Sound(currentSentence, stereo=True)
        currentAudio.setVolume(1)

        # Reset Trial Clock and Play Audio
        trialClock.reset()
        currentAudio.play()

        core.wait(currentAudio.getDuration(), hogCPUperiod=currentAudio.getDuration())

        currentAudio.stop()

        core.wait(1.0)

        # Initialize Text Box
        text = visual.ImageStim(win, image=textBox, interpolate=True, size=(1.8, 1))

        # Draw Image to Buffer
        text.draw()

        # Flip to Reveal
        win.flip()

        # Create Response Object
        responseText = visual.TextStim(win, text='', height=0.1, pos=(0, 0), color='black', wrapWidth=1.5)

        # Collect and Display Response
        continueRoutine = True

        while continueRoutine:
            response = event.getKeys()

            if response:
                if response[0] == 'return':
                    continueRoutine = False

                elif response[0] == 'backspace':
                    responseText.text = responseText.text[:-1]

                elif response[0] == 'space':
                    responseText.text += ' '  # Add a space if 'space' is pressed

                elif response[0] == 'apostrophe':
                    responseText.text += '\''

                elif response[0] == 'period':
                    responseText.text += '.'

                elif response[0] == 'comma':
                    responseText.text += ','

                elif response[0] == 'lshift' or response[0] == 'rshift':
                    pass

                else:
                    responseText.text += response[0]

            # Redraw the image and text stimuli
            text.draw()
            responseText.draw()
            win.flip()

        print(responseText.text)

        # Add response to Data Frame
        out.loc[trial + 1, 'Response'] = outDict['Response'] = responseText.text
        out.loc[trial + 1, 'Subject'] = outDict['Subject'] = subjID
        out.loc[trial + 1, 'Group'] = outDict['Group'] = group
        out.loc[trial + 1, 'Sentence ID'] = outDict['Sentence ID'] = int(sentenceNum[trial])
        out.loc[trial + 1, 'Noise Condition'] = outDict['Noise Condition'] = SNR_folder[trial]
        out.loc[trial + 1, 'Audio'] = outDict['Audio'] = currentSentence
        out.loc[trial + 1, 'Trial'] = outDict['Trial'] = trial + 1
        out.loc[trial + 1, 'Running Time'] = outDict['Running Time'] = expClock.getTime()

        out.to_csv(outputFolderName + os.sep + 'Speech Intelligibility' + os.sep + outputFileName + '.csv', index=False)

        with open(outputFolderName + os.sep + 'Speech Intelligibility' + os.sep + outputFileName + '_trial' +
                  str(trial + 1) + '.json', 'w') as f:
            json.dump(outDict, f)

        core.wait(1.0)

    # %% Complete Experiment

    # Initialize Completion Text
    win.flip()
    goodbye = visual.ImageStim(win, image=endExperiment, interpolate=True, size=(1.8, 1))

    # Draw Image to Buffer
    goodbye.draw()

    # Flip to Reveal
    win.flip()

    core.wait(5.0)

    # End Experiment
    win.close()
    core.quit()

    return 'Speech Intelligibility Experiment Complete: ' + str(expClock.getTime())


# %% Collect Subject Data
if __name__ == '__main__':
    # Create a gui object
    subgui = gui.Dlg()

    # Add fields. The strings become the labels in the gui
    subgui.addField("Subject ID:")
    subgui.addField("Stimulus Group:", choices=['Auditory', 'Visual'])

    # Show gui
    subgui.show()

    # Assign variables to the outputs
    subjID = int(subgui.data[0])
    group = subgui.data[1]

    # Initialize Global Shutdown Key
    event.globalKeys.add(key='escape', func=os._exit, func_args=[1], func_kwargs=None)

    speech_intelligibility(subjID, group)

    core.quit()
