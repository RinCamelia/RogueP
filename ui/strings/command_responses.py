from ui.ui_event import UIEventType

command_response_table = {
	UIEventType.ActionQueueClear: "Queue cleared",
	UIEventType.ActionQueueRemove: "Calling function",
	UIEventType.ActionQueueAdd: "Added function call",
	UIEventType.InvalidCommand: "Bad command {}"
}