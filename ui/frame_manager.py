from enum import Enum
import libtcodpy as libtcod

class FrameState(Enum):
	Okay = 1
	Remove = 2
	Hide = 3
	Show = 4

class FrameManager:

	def __init__(self, parent_menu):
		self.frames = []
		self.parent_menu = parent_menu
		self.should_measure = False

	def add_frame(self, frame):
		self.frames.append({
				'frame':frame,
				'visible':True
			})

	def handle_ui_event(self, event):
		for frame in self.frames:
			frame['frame'].handle_ui_event(event)

	def update(self, delta):
		for frame in self.frames:
			status = frame['frame'].update(delta)
			if status == FrameState.Remove:
				self.frames.remove(frame)
			elif status == FrameState.Hide:
				frame['visible'] = False
			elif status == FrameState.Show:
				frame['visible'] = True


	def draw(self):
		total_milli = 0
		for frame in self.frames:
			pre_action_milli = libtcod.sys_elapsed_milli()
			if frame['visible']:
				frame['frame'].draw()
			post_action_milli = libtcod.sys_elapsed_milli()
			if self.should_measure:
				print 'Frame ' + frame['frame'].__class__.__name__ + ' took ' + str(post_action_milli - pre_action_milli) + ' MS to draw'
				total_milli += post_action_milli - pre_action_milli
		if self.should_measure:
			print 'Total draw call duration: ' + str(total_milli) + ' MS'
			self.should_measure = False
		libtcod.console_flush()