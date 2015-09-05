from enum import Enum
import libtcodpy as libtcod

class FrameState(Enum):
	Okay = 1
	Remove = 2
	Hide = 3
	Show = 4

class FrameManager:

	def __init__(self):
		self.frames = []

	def add_frame(self, frame):
		self.frames.append({
				'frame':frame,
				'visible':True
			})

	def update(self, delta):
		for frame in self.frames:
			status = frame['frame'].update(delta)
			if status == FrameState.Remove:
				self.frames.remove(frame)
			elif status == FrameState.Hide:
				frame['visible'] = False
			elif status == FrameState.Show:
				frame['visible'] = True
		#write input management code here

	def draw(self):
		for frame in self.frames:
			if frame['visible']:
				frame['frame'].draw()