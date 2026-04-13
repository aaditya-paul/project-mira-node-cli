import sys; import os; sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import importlib
try:
    tools_types = importlib.import_module("types.tools_types")
    Tool = tools_types.Tool
    Parameters = tools_types.Parameters
except ModuleNotFoundError:
    from pydantic import BaseModel
    class Tool(BaseModel):
        name: str
        description: str
        parameters: dict
    class Parameters(dict): pass

ALL_TOOLS = [
    # 🖱️ INPUT CONTROL
    "move_mouse",
    "mouse_click",
    "mouse_double_click",
    "mouse_right_click",
    "mouse_scroll",
    "drag_mouse",
    "type_text",
    "press_key",
    "press_hotkey",
    "hold_key",
    "release_key",

    # 🪟 WINDOW & APP CONTROL
    "open_app",
    "close_app",
    "focus_window",
    "minimize_window",
    "maximize_window",
    "resize_window",
    "switch_window",
    "list_running_apps",
    "get_active_window",

    # 🌐 BROWSER CONTROL
    "open_url",
    "search_browser",
    "go_back",
    "go_forward",
    "refresh_page",
    "click_element",
    "type_in_field",
    "submit_form",
    "scroll_page",
    "switch_tab",
    "open_new_tab",
    "close_tab",
    "download_file_from_browser",
    "upload_file",
    "scrape_page_content",

    # 🔍 SEARCH & INFO
    "web_search",
    "get_weather",
    "get_news",
    "lookup_definition",
    "get_stock_price",

    # 📂 FILE SYSTEM
    "read_file",
    "write_file",
    "append_file",
    "delete_file",
    "rename_file",
    "move_file",
    "copy_file",
    "create_folder",
    "delete_folder",
    "list_files",
    "search_files",
    "get_file_metadata",

    # ⬇️ DOWNLOADS & INSTALLS
    "download_file",
    "install_application",
    "uninstall_application",
    "open_downloads_folder",
    "manage_downloads",

    # 🎵 MEDIA CONTROL
    "play_music",
    "pause_music",
    "next_track",
    "previous_track",
    "set_volume",
    "mute_volume",
    "play_video",
    "pause_video",
    "seek_media",

    # 💬 COMMUNICATION
    "send_email",
    "read_email",
    "send_whatsapp_message",
    "read_whatsapp_messages",
    "send_telegram_message",
    "send_discord_message",
    "read_notifications",

    # ⚙️ SYSTEM CONTROL
    "shutdown_system",
    "restart_system",
    "sleep_system",
    "lock_screen",
    "change_brightness",
    "toggle_wifi",
    "toggle_bluetooth",
    "get_system_info",
    "get_battery_status",
    "set_wallpaper",

    # 👀 SCREEN & VISION
    "take_screenshot",
    "record_screen",
    "read_screen_text",
    "detect_ui_elements",
    "get_mouse_position",
    "get_pixel_color",

    # 🎙️ VOICE
    "speech_to_text",
    "text_to_speech",
    "wake_word_detect",

    # 🧠 MEMORY
    "store_memory",
    "retrieve_memory",
    "search_memory",
    "delete_memory",

    # 🧠 PLANNING
    "plan_task",
    "break_task_into_steps",
    "reflect_on_result",

    # 🔐 SAFETY
    "confirm_action",
    "block_action",
    "log_action",
    "audit_trail",

    # 🧩 ADVANCED AUTOMATION
    "run_script",
    "schedule_task",
    "cancel_task",
    "repeat_task",
    "conditional_task",

    # 🧑‍💻 DEV / POWER USER
    "run_terminal_command",
    "install_npm_package",
    "run_code",
    "debug_code",
    "git_clone_repo",
    "git_commit",
    "git_push",

    # 📊 DATA HANDLING
    "parse_pdf",
    "read_csv",
    "write_csv",
    "analyze_data",
    "generate_report",

    # 🧠 CONTEXT AWARENESS
    "get_current_time",
    "get_location",
    "get_active_app_context",
    "get_clipboard",
    "set_clipboard",
]

tool_config = [

    # ─────────────────────────────────────────────
    # 🖱️ INPUT CONTROL
    # ─────────────────────────────────────────────
    Tool(
        name="move_mouse",
        description="Move the mouse cursor to a specific (x, y) coordinate on the screen.",
        parameters=Parameters(
            type="object",
            properties={
                "x": {"type": "integer", "description": "The x-coordinate to move the mouse to."},
                "y": {"type": "integer", "description": "The y-coordinate to move the mouse to."},
                "duration": {"type": "number", "description": "Duration of the movement in seconds. Defaults to 0.5."},
            },
            required=["x", "y"],
        ),
    ),
    Tool(
        name="mouse_click",
        description="Perform a mouse click at the current cursor position.",
        parameters=Parameters(
            type="object",
            properties={
                "button": {"type": "string", "enum": ["left", "right", "middle"], "description": "The mouse button to click."},
                "clicks": {"type": "integer", "description": "Number of clicks to perform. Defaults to 1."},
            },
            required=["button"],
        ),
    ),
    Tool(
        name="mouse_double_click",
        description="Perform a double-click with the specified mouse button at the current cursor position.",
        parameters=Parameters(
            type="object",
            properties={
                "button": {"type": "string", "enum": ["left", "right", "middle"], "description": "The mouse button to double-click."},
            },
            required=["button"],
        ),
    ),
    Tool(
        name="mouse_right_click",
        description="Perform a right-click at a specific (x, y) coordinate on the screen.",
        parameters=Parameters(
            type="object",
            properties={
                "x": {"type": "integer", "description": "The x-coordinate to right-click at."},
                "y": {"type": "integer", "description": "The y-coordinate to right-click at."},
            },
            required=["x", "y"],
        ),
    ),
    Tool(
        name="mouse_scroll",
        description="Scroll the mouse wheel up or down by a given number of units.",
        parameters=Parameters(
            type="object",
            properties={
                "direction": {"type": "string", "enum": ["up", "down"], "description": "The direction to scroll."},
                "amount": {"type": "integer", "description": "The number of scroll units."},
            },
            required=["direction", "amount"],
        ),
    ),
    Tool(
        name="drag_mouse",
        description="Click and drag the mouse from a start coordinate to an end coordinate.",
        parameters=Parameters(
            type="object",
            properties={
                "start_x": {"type": "integer", "description": "The starting x-coordinate."},
                "start_y": {"type": "integer", "description": "The starting y-coordinate."},
                "end_x": {"type": "integer", "description": "The ending x-coordinate."},
                "end_y": {"type": "integer", "description": "The ending y-coordinate."},
                "duration": {"type": "number", "description": "Duration of the drag in seconds. Defaults to 0.5."},
            },
            required=["start_x", "start_y", "end_x", "end_y"],
        ),
    ),
    Tool(
        name="type_text",
        description="Type a given text string at the current cursor position.",
        parameters=Parameters(
            type="object",
            properties={
                "text": {"type": "string", "description": "The text to type."},
                "interval": {"type": "number", "description": "Interval between keystrokes in seconds. Defaults to 0.1."},
            },
            required=["text"],
        ),
    ),
    Tool(
        name="press_key",
        description="Press a specific keyboard key once (e.g. 'enter', 'tab', 'escape').",
        parameters=Parameters(
            type="object",
            properties={
                "key": {"type": "string", "description": "The key to press (e.g. 'enter', 'tab', 'space', 'f5')."},
            },
            required=["key"],
        ),
    ),
    Tool(
        name="press_hotkey",
        description="Press a combination of keys simultaneously as a hotkey (e.g. Ctrl+C, Alt+F4).",
        parameters=Parameters(
            type="object",
            properties={
                "keys": {"type": "array", "items": {"type": "string"}, "description": "List of keys to press together (e.g. ['ctrl', 'c'])."},
            },
            required=["keys"],
        ),
    ),
    Tool(
        name="hold_key",
        description="Hold down a specific keyboard key until released.",
        parameters=Parameters(
            type="object",
            properties={
                "key": {"type": "string", "description": "The key to hold down."},
            },
            required=["key"],
        ),
    ),
    Tool(
        name="release_key",
        description="Release a keyboard key that is currently being held down.",
        parameters=Parameters(
            type="object",
            properties={
                "key": {"type": "string", "description": "The key to release."},
            },
            required=["key"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🪟 WINDOW & APP CONTROL
    # ─────────────────────────────────────────────
    Tool(
        name="open_app",
        description="Open an application by its name or executable path.",
        parameters=Parameters(
            type="object",
            properties={
                "app_name": {"type": "string", "description": "The display name of the application to open (e.g. 'Notepad', 'Chrome')."},
                "app_path": {"type": "string", "description": "The full file path to the application executable."},
            },
            required=["app_name"],
            oneOf=["app_name", "app_path"],
        ),
    ),
    Tool(
        name="close_app",
        description="Close a running application by its name.",
        parameters=Parameters(
            type="object",
            properties={
                "app_name": {"type": "string", "description": "The name of the application to close."},
            },
            required=["app_name"],
        ),
    ),
    Tool(
        name="focus_window",
        description="Bring a window to the foreground and give it focus by its title.",
        parameters=Parameters(
            type="object",
            properties={
                "window_title": {"type": "string", "description": "The title (or partial title) of the window to focus."},
            },
            required=["window_title"],
        ),
    ),
    Tool(
        name="minimize_window",
        description="Minimize the currently active window to the taskbar.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="maximize_window",
        description="Maximize the currently active window to fill the screen.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="resize_window",
        description="Resize the currently active window to the specified width and height in pixels.",
        parameters=Parameters(
            type="object",
            properties={
                "width": {"type": "integer", "description": "The desired window width in pixels."},
                "height": {"type": "integer", "description": "The desired window height in pixels."},
            },
            required=["width", "height"],
        ),
    ),
    Tool(
        name="switch_window",
        description="Switch focus to a different open window by its title.",
        parameters=Parameters(
            type="object",
            properties={
                "window_title": {"type": "string", "description": "The title (or partial title) of the window to switch to."},
            },
            required=["window_title"],
        ),
    ),
    Tool(
        name="list_running_apps",
        description="Return a list of all currently running application names and process IDs.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="get_active_window",
        description="Get the title and process information of the currently focused window.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🌐 BROWSER CONTROL
    # ─────────────────────────────────────────────
    Tool(
        name="open_url",
        description="Open a URL in the default web browser.",
        parameters=Parameters(
            type="object",
            properties={
                "url": {"type": "string", "description": "The fully qualified URL to open (e.g. 'https://example.com')."},
            },
            required=["url"],
        ),
    ),
    Tool(
        name="search_browser",
        description="Perform a Google search by opening the browser with the given query.",
        parameters=Parameters(
            type="object",
            properties={
                "query": {"type": "string", "description": "The search query string."},
            },
            required=["query"],
        ),
    ),
    Tool(
        name="go_back",
        description="Navigate back one step in the browser's history.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="go_forward",
        description="Navigate forward one step in the browser's history.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="refresh_page",
        description="Reload the currently active browser page.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="click_element",
        description="Click on a DOM element on the current web page identified by a CSS selector.",
        parameters=Parameters(
            type="object",
            properties={
                "selector": {"type": "string", "description": "The CSS selector of the element to click (e.g. '#submit-btn', '.nav-link')."},
            },
            required=["selector"],
        ),
    ),
    Tool(
        name="type_in_field",
        description="Type text into a web form input field identified by a CSS selector.",
        parameters=Parameters(
            type="object",
            properties={
                "selector": {"type": "string", "description": "The CSS selector of the input field (e.g. 'input[name=\"email\"]')."},
                "text": {"type": "string", "description": "The text to type into the field."},
            },
            required=["selector", "text"],
        ),
    ),
    Tool(
        name="submit_form",
        description="Submit a web form identified by a CSS selector.",
        parameters=Parameters(
            type="object",
            properties={
                "selector": {"type": "string", "description": "The CSS selector of the form element to submit."},
            },
            required=["selector"],
        ),
    ),
    Tool(
        name="scroll_page",
        description="Scroll the current web page up or down by a given number of pixels.",
        parameters=Parameters(
            type="object",
            properties={
                "direction": {"type": "string", "enum": ["up", "down"], "description": "The direction to scroll."},
                "amount": {"type": "integer", "description": "The number of pixels to scroll."},
            },
            required=["direction", "amount"],
        ),
    ),
    Tool(
        name="switch_tab",
        description="Switch to a browser tab by its zero-based index.",
        parameters=Parameters(
            type="object",
            properties={
                "tab_index": {"type": "integer", "description": "The zero-based index of the tab to switch to."},
            },
            required=["tab_index"],
        ),
    ),
    Tool(
        name="open_new_tab",
        description="Open a new empty tab in the current browser window.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="close_tab",
        description="Close the currently active browser tab.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="download_file_from_browser",
        description="Download a file from a given URL and save it to a local path.",
        parameters=Parameters(
            type="object",
            properties={
                "url": {"type": "string", "description": "The URL of the file to download."},
                "download_path": {"type": "string", "description": "The local file path where the download should be saved."},
            },
            required=["url", "download_path"],
        ),
    ),
    Tool(
        name="upload_file",
        description="Upload a local file to a web form's file input field.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The absolute local path of the file to upload."},
                "selector": {"type": "string", "description": "The CSS selector of the file input element."},
            },
            required=["file_path", "selector"],
        ),
    ),
    Tool(
        name="scrape_page_content",
        description="Extract and return the visible text content of the currently active web page.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🔍 SEARCH & INFO
    # ─────────────────────────────────────────────
    Tool(
        name="web_search",
        description="Perform a web search using the default search engine and return results.",
        parameters=Parameters(
            type="object",
            properties={
                "query": {"type": "string", "description": "The search query string."},
            },
            required=["query"],
        ),
    ),
    Tool(
        name="get_weather",
        description="Retrieve the current weather conditions for a given location.",
        parameters=Parameters(
            type="object",
            properties={
                "location": {"type": "string", "description": "The city or region to get weather for (e.g. 'London, UK')."},
            },
            required=["location"],
        ),
    ),
    Tool(
        name="get_news",
        description="Fetch the latest news headlines, optionally filtered by category.",
        parameters=Parameters(
            type="object",
            properties={
                "category": {"type": "string", "enum": ["general", "technology", "sports", "business", "health", "science", "entertainment"], "description": "The news category to filter by. Defaults to 'general'."},
                "count": {"type": "integer", "description": "Number of headlines to return. Defaults to 5."},
            },
        ),
    ),
    Tool(
        name="lookup_definition",
        description="Look up the dictionary definition of a word.",
        parameters=Parameters(
            type="object",
            properties={
                "word": {"type": "string", "description": "The word to look up."},
            },
            required=["word"],
        ),
    ),
    Tool(
        name="get_stock_price",
        description="Get the current market price for a given stock ticker symbol.",
        parameters=Parameters(
            type="object",
            properties={
                "symbol": {"type": "string", "description": "The stock ticker symbol (e.g. 'AAPL', 'TSLA')."},
            },
            required=["symbol"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 📂 FILE SYSTEM
    # ─────────────────────────────────────────────
    Tool(
        name="read_file",
        description="Read and return the text contents of a file at the given path.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The absolute or relative path of the file to read."},
            },
            required=["file_path"],
        ),
    ),
    Tool(
        name="write_file",
        description="Write (or overwrite) content to a file at the given path.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The absolute or relative path of the file to write."},
                "content": {"type": "string", "description": "The text content to write to the file."},
            },
            required=["file_path", "content"],
        ),
    ),
    Tool(
        name="append_file",
        description="Append content to the end of an existing file without overwriting it.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The path of the file to append to."},
                "content": {"type": "string", "description": "The text content to append."},
            },
            required=["file_path", "content"],
        ),
    ),
    Tool(
        name="delete_file",
        description="Permanently delete a file at the given path.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The path of the file to delete."},
            },
            required=["file_path"],
        ),
    ),
    Tool(
        name="rename_file",
        description="Rename a file at the given path to a new name.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The current path of the file."},
                "new_name": {"type": "string", "description": "The new filename (not a full path — just the name, e.g. 'report_v2.txt')."},
            },
            required=["file_path", "new_name"],
        ),
    ),
    Tool(
        name="move_file",
        description="Move a file from its current location to a new destination path.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The current path of the file."},
                "destination": {"type": "string", "description": "The destination directory or full path to move the file to."},
            },
            required=["file_path", "destination"],
        ),
    ),
    Tool(
        name="copy_file",
        description="Copy a file from its current location to a new destination path.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The path of the file to copy."},
                "destination": {"type": "string", "description": "The destination directory or full path for the copy."},
            },
            required=["file_path", "destination"],
        ),
    ),
    Tool(
        name="create_folder",
        description="Create a new directory (folder) at the specified path.",
        parameters=Parameters(
            type="object",
            properties={
                "folder_path": {"type": "string", "description": "The full path of the folder to create."},
            },
            required=["folder_path"],
        ),
    ),
    Tool(
        name="delete_folder",
        description="Permanently delete a folder and all of its contents at the specified path.",
        parameters=Parameters(
            type="object",
            properties={
                "folder_path": {"type": "string", "description": "The full path of the folder to delete."},
            },
            required=["folder_path"],
        ),
    ),
    Tool(
        name="list_files",
        description="List all files and subdirectories inside a given directory.",
        parameters=Parameters(
            type="object",
            properties={
                "directory": {"type": "string", "description": "The path of the directory to list."},
            },
            required=["directory"],
        ),
    ),
    Tool(
        name="search_files",
        description="Search for files matching a name pattern within a directory (supports wildcards).",
        parameters=Parameters(
            type="object",
            properties={
                "directory": {"type": "string", "description": "The root directory to search in."},
                "pattern": {"type": "string", "description": "The filename pattern to match (e.g. '*.txt', 'report_*')."},
            },
            required=["directory", "pattern"],
        ),
    ),
    Tool(
        name="get_file_metadata",
        description="Retrieve metadata for a file such as size, creation date, and modification date.",
        parameters=Parameters(
            type="object",
            properties={
                "file_path": {"type": "string", "description": "The path of the file to inspect."},
            },
            required=["file_path"],
        ),
    ),

    # ─────────────────────────────────────────────
    # ⬇️ DOWNLOADS & INSTALLS
    # ─────────────────────────────────────────────
    Tool(
        name="download_file",
        description="Download a file from a URL and save it to a local path.",
        parameters=Parameters(
            type="object",
            properties={
                "url": {"type": "string", "description": "The URL to download the file from."},
                "save_path": {"type": "string", "description": "The local path where the downloaded file should be saved."},
            },
            required=["url", "save_path"],
        ),
    ),
    Tool(
        name="install_application",
        description="Install an application by name using the system package manager or installer.",
        parameters=Parameters(
            type="object",
            properties={
                "app_name": {"type": "string", "description": "The name of the application to install."},
            },
            required=["app_name"],
        ),
    ),
    Tool(
        name="uninstall_application",
        description="Uninstall an application from the system by name.",
        parameters=Parameters(
            type="object",
            properties={
                "app_name": {"type": "string", "description": "The name of the application to uninstall."},
            },
            required=["app_name"],
        ),
    ),
    Tool(
        name="open_downloads_folder",
        description="Open the system's default Downloads folder in the file explorer.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="manage_downloads",
        description="Pause, resume, or cancel an active download.",
        parameters=Parameters(
            type="object",
            properties={
                "action": {"type": "string", "enum": ["pause", "resume", "cancel"], "description": "The action to apply to the active download."},
                "download_id": {"type": "string", "description": "The ID of the specific download to manage. If omitted, applies to the most recent download."},
            },
            required=["action"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🎵 MEDIA CONTROL
    # ─────────────────────────────────────────────
    Tool(
        name="play_music",
        description="Play a music track by name or file path.",
        parameters=Parameters(
            type="object",
            properties={
                "track": {"type": "string", "description": "The name or file path of the track to play."},
            },
            required=["track"],
        ),
    ),
    Tool(
        name="pause_music",
        description="Pause the currently playing music track.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="next_track",
        description="Skip to the next track in the current playlist or queue.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="previous_track",
        description="Go back to the previous track in the current playlist or queue.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="set_volume",
        description="Set the system or media volume to a specific level.",
        parameters=Parameters(
            type="object",
            properties={
                "volume": {"type": "integer", "description": "Volume level as a percentage from 0 (silent) to 100 (max)."},
            },
            required=["volume"],
        ),
    ),
    Tool(
        name="mute_volume",
        description="Toggle the system audio mute on or off.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="play_video",
        description="Open and play a video file from a given path.",
        parameters=Parameters(
            type="object",
            properties={
                "video_path": {"type": "string", "description": "The absolute or relative path to the video file."},
            },
            required=["video_path"],
        ),
    ),
    Tool(
        name="pause_video",
        description="Pause the currently playing video.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="seek_media",
        description="Seek the currently playing audio or video to a specific timestamp.",
        parameters=Parameters(
            type="object",
            properties={
                "position": {"type": "number", "description": "The target position in seconds from the start of the media."},
            },
            required=["position"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 💬 COMMUNICATION
    # ─────────────────────────────────────────────
    Tool(
        name="send_email",
        description="Send an email to a recipient with a subject and body.",
        parameters=Parameters(
            type="object",
            properties={
                "to": {"type": "string", "description": "The recipient's email address."},
                "subject": {"type": "string", "description": "The email subject line."},
                "body": {"type": "string", "description": "The body text of the email."},
                "cc": {"type": "string", "description": "Optional CC email address(es), comma-separated."},
            },
            required=["to", "subject", "body"],
        ),
    ),
    Tool(
        name="read_email",
        description="Retrieve and return recent emails from a specified account.",
        parameters=Parameters(
            type="object",
            properties={
                "account": {"type": "string", "description": "The email account address to read from."},
                "count": {"type": "integer", "description": "Number of recent emails to retrieve. Defaults to 5."},
            },
        ),
    ),
    Tool(
        name="send_whatsapp_message",
        description="Send a WhatsApp message to a phone number.",
        parameters=Parameters(
            type="object",
            properties={
                "phone_number": {"type": "string", "description": "The recipient's phone number in international format (e.g. '+919876543210')."},
                "message": {"type": "string", "description": "The text message to send."},
            },
            required=["phone_number", "message"],
        ),
    ),
    Tool(
        name="read_whatsapp_messages",
        description="Read and return the most recent WhatsApp messages.",
        parameters=Parameters(
            type="object",
            properties={
                "count": {"type": "integer", "description": "Number of recent messages to retrieve. Defaults to 10."},
            },
        ),
    ),
    Tool(
        name="send_telegram_message",
        description="Send a message to a Telegram chat or user by chat ID.",
        parameters=Parameters(
            type="object",
            properties={
                "chat_id": {"type": "string", "description": "The Telegram chat ID or username to send the message to."},
                "message": {"type": "string", "description": "The text message to send."},
            },
            required=["chat_id", "message"],
        ),
    ),
    Tool(
        name="send_discord_message",
        description="Send a message to a specific Discord channel by channel ID.",
        parameters=Parameters(
            type="object",
            properties={
                "channel_id": {"type": "string", "description": "The Discord channel ID to send the message to."},
                "message": {"type": "string", "description": "The text message to send."},
            },
            required=["channel_id", "message"],
        ),
    ),
    Tool(
        name="read_notifications",
        description="Read and return the current system notifications.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),

    # ─────────────────────────────────────────────
    # ⚙️ SYSTEM CONTROL
    # ─────────────────────────────────────────────
    Tool(
        name="shutdown_system",
        description="Shut down the operating system, optionally after a delay.",
        parameters=Parameters(
            type="object",
            properties={
                "delay": {"type": "integer", "description": "Delay in seconds before the shutdown is executed. Defaults to 0."},
            },
        ),
    ),
    Tool(
        name="restart_system",
        description="Restart the operating system, optionally after a delay.",
        parameters=Parameters(
            type="object",
            properties={
                "delay": {"type": "integer", "description": "Delay in seconds before the restart is executed. Defaults to 0."},
            },
        ),
    ),
    Tool(
        name="sleep_system",
        description="Put the computer into sleep (low-power) mode immediately.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="lock_screen",
        description="Lock the current user session and display the lock screen.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="change_brightness",
        description="Set the screen brightness to a specific level.",
        parameters=Parameters(
            type="object",
            properties={
                "brightness": {"type": "integer", "description": "Brightness level as a percentage from 0 (off) to 100 (full)."},
            },
            required=["brightness"],
        ),
    ),
    Tool(
        name="toggle_wifi",
        description="Turn WiFi on or off.",
        parameters=Parameters(
            type="object",
            properties={
                "state": {"type": "string", "enum": ["on", "off"], "description": "The desired WiFi state."},
            },
            required=["state"],
        ),
    ),
    Tool(
        name="toggle_bluetooth",
        description="Turn Bluetooth on or off.",
        parameters=Parameters(
            type="object",
            properties={
                "state": {"type": "string", "enum": ["on", "off"], "description": "The desired Bluetooth state."},
            },
            required=["state"],
        ),
    ),
    Tool(
        name="get_system_info",
        description="Return system information including OS, CPU, RAM, and disk usage.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="get_battery_status",
        description="Return the current battery charge level and charging status.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="set_wallpaper",
        description="Set the desktop wallpaper to a specified image file.",
        parameters=Parameters(
            type="object",
            properties={
                "image_path": {"type": "string", "description": "The absolute path to the image file to use as wallpaper."},
            },
            required=["image_path"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 👀 SCREEN & VISION
    # ─────────────────────────────────────────────
    Tool(
        name="take_screenshot",
        description="Capture a screenshot of the entire screen and optionally save it to a file.",
        parameters=Parameters(
            type="object",
            properties={
                "save_path": {"type": "string", "description": "The path to save the screenshot image. If omitted, the image is returned in memory."},
            },
        ),
    ),
    Tool(
        name="record_screen",
        description="Record the screen for a specified duration and save the video to a file.",
        parameters=Parameters(
            type="object",
            properties={
                "duration": {"type": "integer", "description": "Duration of the screen recording in seconds."},
                "save_path": {"type": "string", "description": "The file path to save the screen recording."},
            },
            required=["duration", "save_path"],
        ),
    ),
    Tool(
        name="read_screen_text",
        description="Use OCR to extract and return all visible text currently on the screen.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="detect_ui_elements",
        description="Detect and return a list of interactive UI elements visible on the screen (buttons, inputs, links, etc.).",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="get_mouse_position",
        description="Return the current (x, y) coordinates of the mouse cursor on the screen.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="get_pixel_color",
        description="Return the RGB color value of the pixel at the specified screen coordinates.",
        parameters=Parameters(
            type="object",
            properties={
                "x": {"type": "integer", "description": "The x-coordinate of the pixel."},
                "y": {"type": "integer", "description": "The y-coordinate of the pixel."},
            },
            required=["x", "y"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🎙️ VOICE
    # ─────────────────────────────────────────────
    Tool(
        name="speech_to_text",
        description="Listen to audio input from the microphone and convert it to a text string.",
        parameters=Parameters(
            type="object",
            properties={
                "duration": {"type": "integer", "description": "Duration in seconds to listen for audio. If omitted, listens until silence is detected."},
                "language": {"type": "string", "description": "BCP-47 language code for recognition (e.g. 'en-US'). Defaults to system language."},
            },
        ),
    ),
    Tool(
        name="text_to_speech",
        description="Convert a text string to spoken audio output through the system speakers.",
        parameters=Parameters(
            type="object",
            properties={
                "text": {"type": "string", "description": "The text to convert to speech."},
                "voice": {"type": "string", "description": "Optional voice name or ID to use for synthesis."},
                "rate": {"type": "number", "description": "Speech rate multiplier. 1.0 is normal speed."},
            },
            required=["text"],
        ),
    ),
    Tool(
        name="wake_word_detect",
        description="Start listening for a wake word phrase and trigger an action when detected.",
        parameters=Parameters(
            type="object",
            properties={
                "wake_word": {"type": "string", "description": "The wake word or phrase to listen for (e.g. 'hey assistant')."},
            },
        ),
    ),

    # ─────────────────────────────────────────────
    # 🧠 MEMORY
    # ─────────────────────────────────────────────
    Tool(
        name="store_memory",
        description="Persist a key-value pair in the agent's long-term memory store.",
        parameters=Parameters(
            type="object",
            properties={
                "key": {"type": "string", "description": "A unique identifier for the memory entry."},
                "value": {"type": "string", "description": "The value or information to store."},
            },
            required=["key", "value"],
        ),
    ),
    Tool(
        name="retrieve_memory",
        description="Retrieve a previously stored value from the agent's memory by its key.",
        parameters=Parameters(
            type="object",
            properties={
                "key": {"type": "string", "description": "The key of the memory entry to retrieve."},
            },
            required=["key"],
        ),
    ),
    Tool(
        name="search_memory",
        description="Search the agent's memory store for entries matching a query string.",
        parameters=Parameters(
            type="object",
            properties={
                "query": {"type": "string", "description": "A keyword or phrase to search for in stored memories."},
            },
            required=["query"],
        ),
    ),
    Tool(
        name="delete_memory",
        description="Delete a specific memory entry by its key.",
        parameters=Parameters(
            type="object",
            properties={
                "key": {"type": "string", "description": "The key of the memory entry to delete."},
            },
            required=["key"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🧠 PLANNING
    # ─────────────────────────────────────────────
    Tool(
        name="plan_task",
        description="Generate a high-level plan for completing a described task.",
        parameters=Parameters(
            type="object",
            properties={
                "task": {"type": "string", "description": "A natural-language description of the task to plan."},
            },
            required=["task"],
        ),
    ),
    Tool(
        name="break_task_into_steps",
        description="Decompose a high-level task into a sequence of concrete, actionable steps.",
        parameters=Parameters(
            type="object",
            properties={
                "task": {"type": "string", "description": "The task description to break down into steps."},
            },
            required=["task"],
        ),
    ),
    Tool(
        name="reflect_on_result",
        description="Evaluate the result of a completed task, identify issues, and suggest improvements.",
        parameters=Parameters(
            type="object",
            properties={
                "result": {"type": "string", "description": "A description of the result or outcome to reflect on."},
                "original_task": {"type": "string", "description": "The original task description for comparison."},
            },
            required=["result"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🔐 SAFETY
    # ─────────────────────────────────────────────
    Tool(
        name="confirm_action",
        description="Prompt the user to confirm a sensitive or irreversible action before executing it.",
        parameters=Parameters(
            type="object",
            properties={
                "action": {"type": "string", "description": "A description of the action requiring user confirmation."},
            },
            required=["action"],
        ),
    ),
    Tool(
        name="block_action",
        description="Prevent a specific action from being executed and log the reason.",
        parameters=Parameters(
            type="object",
            properties={
                "action": {"type": "string", "description": "A description of the action to block."},
                "reason": {"type": "string", "description": "The reason why this action is being blocked."},
            },
            required=["action"],
        ),
    ),
    Tool(
        name="log_action",
        description="Record an action to the audit log for traceability.",
        parameters=Parameters(
            type="object",
            properties={
                "action": {"type": "string", "description": "A description of the action to log."},
                "status": {"type": "string", "enum": ["success", "failure", "skipped"], "description": "The outcome status of the action."},
            },
            required=["action"],
        ),
    ),
    Tool(
        name="audit_trail",
        description="Retrieve the full audit trail of all logged actions in the current session.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🧩 ADVANCED AUTOMATION
    # ─────────────────────────────────────────────
    Tool(
        name="run_script",
        description="Execute a script file with optional arguments.",
        parameters=Parameters(
            type="object",
            properties={
                "script_path": {"type": "string", "description": "The absolute path to the script file to run."},
                "args": {"type": "array", "items": {"type": "string"}, "description": "Optional list of arguments to pass to the script."},
            },
            required=["script_path"],
        ),
    ),
    Tool(
        name="schedule_task",
        description="Schedule a task to run automatically at a specified date and time.",
        parameters=Parameters(
            type="object",
            properties={
                "task": {"type": "string", "description": "A description of the task to schedule."},
                "time": {"type": "string", "description": "The ISO 8601 datetime string when the task should run (e.g. '2024-12-01T09:00:00')."},
            },
            required=["task", "time"],
        ),
    ),
    Tool(
        name="cancel_task",
        description="Cancel a previously scheduled task by its task ID.",
        parameters=Parameters(
            type="object",
            properties={
                "task_id": {"type": "string", "description": "The unique ID of the scheduled task to cancel."},
            },
            required=["task_id"],
        ),
    ),
    Tool(
        name="repeat_task",
        description="Execute a task repeatedly at a fixed interval until stopped.",
        parameters=Parameters(
            type="object",
            properties={
                "task": {"type": "string", "description": "A description of the task to repeat."},
                "interval": {"type": "integer", "description": "The interval in seconds between each repetition."},
                "max_repetitions": {"type": "integer", "description": "Maximum number of times to repeat. If omitted, repeats indefinitely."},
            },
            required=["task", "interval"],
        ),
    ),
    Tool(
        name="conditional_task",
        description="Execute a task only if a specified condition evaluates to true.",
        parameters=Parameters(
            type="object",
            properties={
                "condition": {"type": "string", "description": "An expression or natural-language condition to evaluate before running the task."},
                "task": {"type": "string", "description": "The task to execute if the condition is true."},
                "else_task": {"type": "string", "description": "Optional task to execute if the condition is false."},
            },
            required=["condition", "task"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🧑‍💻 DEV / POWER USER
    # ─────────────────────────────────────────────
    Tool(
        name="run_terminal_command",
        description="Execute a shell command in the system terminal and return the output.",
        parameters=Parameters(
            type="object",
            properties={
                "command": {"type": "string", "description": "The shell command to execute (e.g. 'ls -la', 'ping google.com')."},
                "timeout": {"type": "integer", "description": "Timeout in seconds before the command is terminated. Defaults to 30."},
            },
            required=["command"],
        ),
    ),
    Tool(
        name="install_npm_package",
        description="Install a Node.js package using npm.",
        parameters=Parameters(
            type="object",
            properties={
                "package_name": {"type": "string", "description": "The name of the npm package to install (e.g. 'lodash', 'express')."},
                "global": {"type": "boolean", "description": "If true, installs the package globally. Defaults to false."},
            },
            required=["package_name"],
        ),
    ),
    Tool(
        name="run_code",
        description="Execute a snippet of Python or JavaScript code and return the output.",
        parameters=Parameters(
            type="object",
            properties={
                "code": {"type": "string", "description": "The source code to execute."},
                "language": {"type": "string", "enum": ["python", "javascript"], "description": "The programming language of the code snippet."},
            },
            required=["code", "language"],
        ),
    ),
    Tool(
        name="debug_code",
        description="Analyze a code snippet for errors and return debugging information and suggestions.",
        parameters=Parameters(
            type="object",
            properties={
                "code": {"type": "string", "description": "The code snippet to debug."},
                "language": {"type": "string", "enum": ["python", "javascript", "typescript", "other"], "description": "The programming language of the code."},
                "error_message": {"type": "string", "description": "Optional error message or traceback to provide additional context."},
            },
            required=["code"],
        ),
    ),
    Tool(
        name="git_clone_repo",
        description="Clone a remote Git repository to a local destination path.",
        parameters=Parameters(
            type="object",
            properties={
                "repo_url": {"type": "string", "description": "The HTTPS or SSH URL of the Git repository to clone."},
                "destination": {"type": "string", "description": "The local directory path where the repository should be cloned."},
            },
            required=["repo_url", "destination"],
        ),
    ),
    Tool(
        name="git_commit",
        description="Stage all current changes and create a Git commit with the given message.",
        parameters=Parameters(
            type="object",
            properties={
                "message": {"type": "string", "description": "The commit message describing the changes."},
            },
            required=["message"],
        ),
    ),
    Tool(
        name="git_push",
        description="Push committed changes to a remote Git repository branch.",
        parameters=Parameters(
            type="object",
            properties={
                "branch": {"type": "string", "description": "The name of the remote branch to push to. Defaults to the current tracking branch."},
            },
        ),
    ),

    # ─────────────────────────────────────────────
    # 📊 DATA HANDLING
    # ─────────────────────────────────────────────
    Tool(
        name="parse_pdf",
        description="Extract and return the text content from a PDF file.",
        parameters=Parameters(
            type="object",
            properties={
                "pdf_path": {"type": "string", "description": "The absolute path to the PDF file to parse."},
                "pages": {"type": "string", "description": "Optional page range to extract (e.g. '1-3', '5'). Defaults to all pages."},
            },
            required=["pdf_path"],
        ),
    ),
    Tool(
        name="read_csv",
        description="Read a CSV file and return its contents as a list of row objects.",
        parameters=Parameters(
            type="object",
            properties={
                "csv_path": {"type": "string", "description": "The path to the CSV file to read."},
                "delimiter": {"type": "string", "description": "The column delimiter character. Defaults to ','."},
            },
            required=["csv_path"],
        ),
    ),
    Tool(
        name="write_csv",
        description="Write a list of data records to a CSV file.",
        parameters=Parameters(
            type="object",
            properties={
                "csv_path": {"type": "string", "description": "The path of the CSV file to write to."},
                "data": {"type": "array", "description": "The array of row objects or arrays to write."},
                "headers": {"type": "array", "items": {"type": "string"}, "description": "Optional list of column header names."},
            },
            required=["csv_path", "data"],
        ),
    ),
    Tool(
        name="analyze_data",
        description="Perform statistical analysis on a dataset and return a summary (mean, median, distribution, etc.).",
        parameters=Parameters(
            type="object",
            properties={
                "data": {"type": "array", "description": "The dataset to analyze, as an array of values or row objects."},
                "analysis_type": {"type": "string", "enum": ["summary", "correlation", "distribution", "trends"], "description": "The type of analysis to perform. Defaults to 'summary'."},
            },
            required=["data"],
        ),
    ),
    Tool(
        name="generate_report",
        description="Generate a formatted report from a dataset in the specified format.",
        parameters=Parameters(
            type="object",
            properties={
                "data": {"type": "array", "description": "The data to include in the report."},
                "report_type": {"type": "string", "enum": ["summary", "detailed", "chart", "table"], "description": "The format/type of report to generate."},
                "title": {"type": "string", "description": "Optional title for the report."},
            },
            required=["data", "report_type"],
        ),
    ),

    # ─────────────────────────────────────────────
    # 🧠 CONTEXT AWARENESS
    # ─────────────────────────────────────────────
    Tool(
        name="get_current_time",
        description="Return the current local date and time.",
        parameters=Parameters(
            type="object",
            properties={
                "timezone": {"type": "string", "description": "Optional IANA timezone name (e.g. 'America/New_York'). Defaults to system timezone."},
                "format": {"type": "string", "description": "Optional datetime format string (e.g. '%Y-%m-%d %H:%M:%S'). Defaults to ISO 8601."},
            },
        ),
    ),
    Tool(
        name="get_location",
        description="Return the device's current geographic location (latitude, longitude, city).",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="get_active_app_context",
        description="Return contextual information about the currently focused application, including its title, process name, and open document.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="get_clipboard",
        description="Return the current text content of the system clipboard.",
        parameters=Parameters(
            type="object",
            properties={},
            required=[],
        ),
    ),
    Tool(
        name="set_clipboard",
        description="Set the system clipboard to the specified text content.",
        parameters=Parameters(
            type="object",
            properties={
                "content": {"type": "string", "description": "The text to write to the clipboard."},
            },
            required=["content"],
        ),
    ),
]