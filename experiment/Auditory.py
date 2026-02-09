# %%
import numpy as np
import pandas as pd
import os, sys
import json
from psychopy import prefs

prefs.hardware['audioLib'] = ['pygame']
from psychopy import visual, core, event, gui, logging, sound
from psychopy.sound import Microphone


# %% Create Function
def auditory_experiment(subjID, group, start):
	# %% Skip Function If Starting at Speech Intelligibility Task
	if start == 'Speech Intelligibility':
		return None

	# %% Prepare Output File
	outputFolderName = 'data' + os.sep + 'en' + format(subjID, '02d') + 'Auditory'
	outputPracticeFileName = 'en' + format(subjID, '02d') + '_practice'
	outputFileName = 'en' + format(subjID, '02d') + '_block'
	outputRecallFileName = 'en' + format(subjID, '02d') + '_recall'

	# Check for Repeated Subjects
	if os.path.exists(outputFolderName + os.sep + 'Practice'):
		print('Practice Data for this participant already exists.')

	elif os.path.exists(outputFolderName):
		os.mkdir(outputFolderName + os.sep + 'Practice')
		print('Data for this participant already exists.')
	# sys.exit('Data for this participant already exists.')

	else:
		os.mkdir(outputFolderName)
		os.mkdir(outputFolderName + os.sep + 'Practice')

	practiceVars = ['Subject', 'Group', 'Trial', 'Audio', 'stimOn', 'trialOn', 'trialOff', 'Times', 'Running Time']

	outPractice = pd.DataFrame(columns=practiceVars)
	dictPractice = dict.fromkeys(practiceVars, None)

	outVars = ['Subject', 'Group', 'Trial', 'Story ID', 'Audio', 'Noise Condition', 'stimOn', 'trialOn', 'trialOff',
			   'Times', 'Running Time']

	out = pd.DataFrame(columns=outVars)
	outDict = dict.fromkeys(outVars, None)

	# %% Initialize Experiment Window
	# win = visual.Window(size=(800, 600), allowGUI=True, color='grey', units='height', pos=[100, 100])
	win = visual.Window(size=(800, 600), fullscr=True, allowGUI=True, color='grey', units='height', pos=[100, 100])
	win.mouseVisible = False

	# Quality check ensure refresh rate is accurate
	win.recordFrameIntervals = True
	win.refreshThreshold = 1 / 60 + 0.005
	logging.console.setLevel(logging.WARNING)

	# %% Initialize Experimental Parameters

	# Instruction Image
	imageFolder = 'instructions' + os.sep + 'auditory' + os.sep
	practiceInstructions = imageFolder + 'Slide1.png'
	practiceTaskOne = imageFolder + 'Slide2.png'
	practiceTaskTwo = imageFolder + 'Slide3.png'
	recallTask = imageFolder + 'Slide4.png'
	recallContinued = imageFolder + 'Slide16.png'
	endPractice = imageFolder + 'Slide5.png'
	mainInstructions = imageFolder + 'Slide6.png'
	mainExperiment = imageFolder + 'Slide7.png'
	storyOne = imageFolder + 'Slide8.png'
	endStoryOne = imageFolder + 'Slide9.png'
	storyTwo = imageFolder + 'Slide10.png'
	endStoryTwo = imageFolder + 'Slide11.png'
	storyThree = imageFolder + 'Slide12.png'
	endExperiment = imageFolder + 'Slide13.png'
	listeningFixationFile = imageFolder + 'Slide14.png'
	recallFixationFile = imageFolder + 'Slide15.png'

	# Practice Story Names
	practiceNames = ['Robert']

	# Story Names
	storyNames = ['Run!', 'Go Hitler!', 'My Mother\'s Life']

	# Fixation Cross
	listeningFixation = visual.ImageStim(win, image=listeningFixationFile, interpolate=True, size=(1.8, 1))
	recallFixation = visual.ImageStim(win, image=recallFixationFile, interpolate=True, size=(1.8, 1))

	# Counterbalancing Information
	counterbalance = pd.read_csv('order' + os.sep + 'auditoryCounterbalancing.csv')
	stimuliInfo = counterbalance.loc[subjID - 1]

	# Story IDs
	storyID = stimuliInfo.array[1:4]

	# Noise Conditions
	noiseConditions = stimuliInfo.array[4:]

	# Practice Experimental Stimuli Pathname
	practicePath = 'audio' + os.sep + 'Robert' + os.sep +'Robert_clear.wav'

	# Experimental Stimuli Pathname
	stimuliPath = pd.read_csv('order/audioStories.csv')

	# Identify Number of Trials
	numTrials = len(stimuliPath)

	# %% PRACTICE TASK

	if start == 'Practice':

		# Prepare Image
		practiceInstr = visual.ImageStim(win, image=practiceInstructions, interpolate=True, size=(1.8, 1))
		practiceOne = visual.ImageStim(win, image=practiceTaskOne, interpolate=True, size=(1.8, 1))
		practiceTwo = visual.ImageStim(win, image=practiceTaskTwo, interpolate=True, size=(1.8, 1))

		# Draw Image to Buffer
		practiceInstr.draw()

		# Flip to Reveal
		win.flip()

		# Initialize Key Waiting
		event.waitKeys(keyList=['space'])

		# Show Blank Screen
		win.flip()
		core.wait(1.0)

		# Draw Image to Buffer
		practiceOne.draw()

		# Flip to Reveal
		win.flip()

		# Initialize Key Waiting
		event.waitKeys(keyList=['space'])

		# Show Blank Screen
		win.flip()
		core.wait(1.0)

		# %% Practice Experiment Loop

		# Initialize Running Experiment Clock
		expClock = core.Clock()

		# Initialized Trial Clock
		trialClock = core.Clock()

		# Initialize Trial For Loop
		num1 = 0
		num2 = 0
		for trial in range(2):
			# Draw Fixation Cross
			listeningFixation.draw()
			win.flip()

			# Wait 3 seconds
			core.wait(3.0)

			# Initialize Sound
			currentStory = practicePath

			currentAudio = sound.Sound(currentStory, stereo=True)
			currentAudio.setVolume(1)

			# Reset Trial Clock and Play Audio
			trialClock.reset()
			currentAudio.play()

			# Record Time When Stimuli Presented
			outPractice.loc[1, 'stimOn'] = dictPractice['stimOn'] = expClock.getTime()
			outPractice.loc[1, 'trialOn'] = dictPractice['trialOn'] = trialClock.getTime()

			core.wait(currentAudio.getDuration(), hogCPUperiod=currentAudio.getDuration())

			# if trialClock.getTime() < currentAudio.getDuration():
			# continue

			# Initialize Keyboard Responses
			keys = event.getKeys(keyList=['space'], timeStamped=trialClock)

			currentAudio.stop()

			# Record Time When Stimuli Completed
			outPractice.loc[1, 'trialOff'] = dictPractice['trialOff'] = trialClock.getTime()
			outPractice.loc[1, 'Running Time'] = dictPractice['Running Time'] = expClock.getTime()

			# Record Keyboard Responses
			if keys is not None:
				trialResp = [i[0] for i in keys]
				trialTimes = [i[1] for i in keys]
				# out.at[1, 'Responses'] = trialResp
				outPractice.at[1, 'Times'] = dictPractice['Times'] = trialTimes

				if trial == 0:
					num1 = len(trialTimes)
				else:
					num2 = len(trialTimes)

			# Record Trial Parameters
			outPractice.loc[1, 'Trial'] = dictPractice['Trial'] = trial + 1
			outPractice.loc[1, 'Audio'] = dictPractice['Audio'] = practicePath
			outPractice.loc[1, 'Subject'] = dictPractice['Subject'] = subjID
			outPractice.loc[1, 'Group'] = dictPractice['Group'] = group

			print(len(trialTimes))

			# Save File
			outPractice.to_csv(outputFolderName + os.sep + 'Practice' + os.sep + outputPracticeFileName +
							   str(trial + 1) + '.csv', index=False)

			with open(outputFolderName + os.sep + 'Practice' + os.sep + outputPracticeFileName + str(trial + 1) +
					  '.json', 'w') as f:
				json.dump(dictPractice, f)

			# Wait 1.0 second
			win.flip()
			core.wait(1.0)

			# %% End the Current Trial
			if trial == 0:
				# Draw Image to Buffer
				practiceTwo.draw()

				# Flip to Reveal
				win.flip()

				# Wait for Key Press to Start Next Trial
				event.waitKeys()
				core.wait(1.0)

		# %% Introduce Recall Task

		# Prepare and Launch Instructions
		instr = visual.ImageStim(win, image=recallTask, interpolate=True, size=(1.8, 1))

		instr.draw()
		win.flip()
		event.waitKeys(keyList=['space'])
		core.wait(1.0)

		# Draw Fixation
		recallFixation.draw()
		win.flip()

		recallClock = core.Clock()

		# Start Audio Recording
		mic = Microphone(sampleRateHz=44100, streamBufferSecs=1500, maxRecordingSize=200000)
		recallClock.reset()
		mic.start()

		while not event.getKeys(keyList=['space']):
			mic.poll()

		# event.waitKeys(keyList=['space'])
		mic.stop()
		audioClip = mic.getRecording()
		audioClip.save(outputFolderName + os.sep + 'Practice' + os.sep + outputRecallFileName + '.wav')
		mic.clear()
		mic.close()

		win.flip()
		core.wait(1.0)

		# Recall Task Continued
		instr = visual.ImageStim(win, image=recallContinued, interpolate=True, size=(1.8, 1))
		instr.draw()
		win.flip()
		event.waitKeys(keyList=['space'])

		# Draw Fixation
		recallFixation.draw()
		win.flip()

		recallClock = core.Clock()

		# Start Audio Recording
		mic = Microphone(sampleRateHz=44100, streamBufferSecs=1200, maxRecordingSize=200000)
		recallClock.reset()
		mic.start()
		mic.poll()

		event.waitKeys(keyList=['space'])
		mic.stop()
		audioClip = mic.getRecording()
		audioClip.save(outputFolderName + os.sep + 'Practice' + os.sep + outputRecallFileName + '_continued.wav')
		mic.clear()
		mic.close()
		win.flip()
		core.wait(1.0)

		# %% Complete Experiment

		# Initialize Completion Text
		goodbye = visual.ImageStim(win, image=endPractice, interpolate=True, size=(1.8, 1))
		event_num1 = visual.TextStim(win, text=num1, height=0.02, pos=(-0.75, -0.4), color='dimgray', wrapWidth=1.5)
		event_num2 = visual.TextStim(win, text=num2, height=0.02, pos=(-0.75, -0.42), color='dimgray', wrapWidth=1.5)

		# Draw Image to Buffer
		goodbye.draw()
		event_num1.draw()
		event_num2.draw()

		# Flip to Reveal
		win.flip()

		# Initialize Key Waiting
		event.waitKeys(keyList=['space'])

	# %% MAIN EXPERIMENT
	# Initialize Main Experiment Instructions

	# Prepare Image
	instr = visual.ImageStim(win, image=mainExperiment, interpolate=True, size=(1.8, 1))

	# Draw Image to Buffer
	instr.draw()

	# Flip to Reveal
	win.flip()

	# Initialize Key Waiting
	event.waitKeys(keyList=['space'])

	# Show Blank Screen
	win.flip()
	core.wait(1.0)

	# %% Experiment Loop

	# Initialize Running Experiment Clock
	expClock = core.Clock()

	# Initialized Trial Clock
	trialClock = core.Clock()

	if start == 'Story 2':
		trial = 1
	elif start == 'Story 3':
		trial = 2
	else:
		trial = 0

	# Initialize Trial For Loop
	while trial < numTrials:

		# Initialize Image for Specific Trials
		if trial == 0:
			startStory = visual.ImageStim(win, image=storyOne, interpolate=True, size=(1.8, 1))
			endStory = visual.ImageStim(win, image=endStoryOne, interpolate=True, size=(1.8, 1))

		elif trial == 1:
			startStory = visual.ImageStim(win, image=storyTwo, interpolate=True, size=(1.8, 1))
			endStory = visual.ImageStim(win, image=endStoryTwo, interpolate=True, size=(1.8, 1))

		else:
			startStory = visual.ImageStim(win, image=storyThree, interpolate=True, size=(1.8, 1))

		# Draw Start of Story
		startStory.draw()
		win.flip()
		event.waitKeys(keyList=['space'])

		# Draw Fixation Cross
		listeningFixation.draw()
		win.flip()

		# Wait 3 seconds
		core.wait(3.0)

		# Initialize Sound
		currentStory = stimuliPath.loc[storyID[trial] - 1, 'Path']

		if noiseConditions[trial] == 1:
			condition = 'clear'
		elif noiseConditions[trial] == 2:
			condition = '+4SNR'
		else:
			condition = '-2SNR'

		currentAudio = sound.Sound(currentStory + os.sep + storyNames[storyID[trial] - 1] + '_' + condition + '.wav',
								   stereo=True)
		currentAudio.setVolume(1)

		# Reset Trial Clock and Play Audio
		trialClock.reset()
		currentAudio.play()

		# Record Time When Stimuli Presented
		out.loc[1, 'stimOn'] = outDict['stimOn'] = expClock.getTime()
		out.loc[1, 'trialOn'] = outDict['trialOn'] = trialClock.getTime()

		core.wait(currentAudio.getDuration(), hogCPUperiod=currentAudio.getDuration())

		# Initialize Keyboard Responses
		keys = event.getKeys(keyList=['space'], timeStamped=trialClock)

		currentAudio.stop()

		# Record Time When Stimuli Completed
		out.loc[1, 'trialOff'] = outDict['trialOff'] = trialClock.getTime()
		out.loc[1, 'Running Time'] = outDict['Running Time'] = expClock.getTime()

		# Record Keyboard Responses
		if keys is not None:
			trialResp = [i[0] for i in keys]
			trialTimes = [i[1] for i in keys]
			# out.at[1, 'Responses'] = trialResp
			out.at[1, 'Times'] = outDict['Times'] = trialTimes

		# Record Trial Parameters
		out.loc[1, 'Trial'] = outDict['Trial'] = trial + 1
		out.loc[1, 'Story ID'] = outDict['Story ID'] = int(storyID[trial])
		out.loc[1, 'Audio'] = outDict['Audio'] = stimuliPath.loc[storyID[trial] - 1, 'Path']
		out.loc[1, 'Noise Condition'] = outDict['Noise Condition'] = condition
		out.loc[1, 'Subject'] = outDict['Subject'] = subjID
		out.loc[1, 'Group'] = outDict['Group'] = group

		# Save File
		out.to_csv(outputFolderName + os.sep + outputFileName + str(trial + 1) + '.csv', index=False)
		with open(outputFolderName + os.sep + outputFileName + str(trial + 1) + '.json', 'w') as f:
			json.dump(outDict, f)

		# Wait 1.0 second
		core.wait(1.0)

		# %% Introduce Recall Task

		# Prepare and Launch Instructions
		instr = visual.ImageStim(win, image=recallTask, interpolate=True, size=(1.8, 1))
		instr.draw()
		win.flip()
		event.waitKeys(keyList=['space'])

		# Draw Fixation
		recallFixation.draw()
		win.flip()

		recallClock = core.Clock()

		# Start Audio Recording
		mic = Microphone(sampleRateHz=44100, streamBufferSecs=1200, maxRecordingSize=200000)
		recallClock.reset()
		mic.start()

		# core.wait(120.0)
		mic.poll()

		event.waitKeys(keyList=['space'])

		mic.stop()
		audioClip = mic.getRecording()
		audioClip.save(outputFolderName + os.sep + outputRecallFileName + str(trial + 1) + '.wav')
		mic.clear()
		mic.close()

		# %% End the Current Trial
		if trial < numTrials - 1:
			endStory.draw()
			win.flip()

			event.waitKeys(keyList=['space'])

			# Show Blank Screen
			win.flip()
			core.wait(1.0)

		# Increase Trial Counter
		trial += 1

	# %% Complete Experiment
	core.wait(1.0)

	# Initialize Completion Text
	goodbye = visual.ImageStim(win, image=endExperiment, interpolate=True, size=(1.8, 1))

	# Draw Image to Buffer
	goodbye.draw()

	# Flip to Reveal
	win.flip()

	event.waitKeys(keyList=['space'])

	# End Experiment
	win.close()
	# core.quit()

	return 'Auditory Experiment Complete: ' + str(expClock.getTime())


# %% Collect Subject Data

if __name__ == '__main__':
	# Create a gui object
	subgui = gui.Dlg()

	# Add fields. The strings become the labels in the gui
	subgui.addField("Subject ID:")
	subgui.addField("Stimulus Group:", choices=['Auditory'])
	subgui.addField('Start From:', choices=['Practice', 'Story 1', 'Story 2', 'Story 3'])

	# Show gui
	subgui.show()

	# Assign variables to the outputs
	subjID = int(subgui.data[0])
	group = subgui.data[1]
	start = subgui.data[2]

	# Initialize Global Shutdown Key
	event.globalKeys.add(key='escape', func=os._exit, func_args=[1], func_kwargs=None)

	auditory_experiment(subjID, group, start)

	core.quit()
