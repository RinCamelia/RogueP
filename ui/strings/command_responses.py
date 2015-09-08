from ui.ui_event import UIEventType

command_response_table = {
	UIEventType.ActionQueueClear: "(clear queue)",
	UIEventType.ActionQueueRemove: "(call %)",
	UIEventType.ActionQueueAdd: "(schedule %)",
	UIEventType.InvalidCommand: "(bad command)"
}