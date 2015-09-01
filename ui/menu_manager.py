from enum import Enum
from menu import Menu

class MenuStatus(Enum):
	Okay = 1
	Exit = 2

# master game state and flow manager
# updates and draws the topmost menu from a stack of menus
class MenuManager:

	def __init__(self, start_menu):
		self.menus=[]
		self.menus.append(start_menu)

	# update loop for menus
	# also calls draw on the current menu
	# returns False if the game should exit, True if it shouldn't
	def loop(self, delta):
		current_menu = self.menus.pop()
		status = current_menu.update(delta)

		if status == MenuStatus.Okay:
			current_menu.draw()
			self.menus.append(current_menu)
			#print("okay in " + current_menu.__class__.__name__)

		elif status == MenuStatus.Exit:
			#do anything else related to transitions here
			#on the one hand i feel like we could reuse MenuStatus, on the other hand that feels like a bad idea 
			#this causes the menu in question to fall off the face of the earth, unless something else is holding a reference to it, so far as I know
			current_menu.exit()
			print("exiting " + current_menu.__class__.__name__)
			if len(self.menus) == 0:
				return False

		#not a fan of overloading return types like this but it's easy for now - will need to change if menus ever require more involved init params
		elif isinstance(status, Menu):
			self.menus.append(current_menu)
			print("entering " + status.__class__.__name__)
			self.menus.append(status)

		else:
			raise RuntimeError("Menu " + current_menu.__class__.__name__ + " failed to provide a MenuStatus state or new menu to enter on exiting its update loop")

		return True