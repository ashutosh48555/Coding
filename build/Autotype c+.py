import pyautogui
import pyperclip
import keyboard
import io
import time


class AutoTyper:
    def __init__(self):
        self.spaces = 0
        self.x = 0  # Tracks indentation
        self.running = False  # Ensures only one instance of typing runs at a time

    def tabbing_mech(self, line):
        count_space = 0
        for char in line:
            if char == " ":
                count_space += 1
            elif char == "\t":
                count_space += 4
            else:
                break

        if self.spaces > count_space:
            back_tab = (self.spaces - count_space) // 4
            self.spaces = count_space
            for _ in range(back_tab):
                pyautogui.keyDown('shift')
                pyautogui.press('tab')
                pyautogui.keyUp('shift')
            return line.lstrip()
        elif self.spaces == count_space:
            return line.lstrip()
        elif self.spaces < count_space:
            self.spaces = count_space
            return line.lstrip()

    def start_autotyper(self):
        if self.running:
            return  # Prevent overlapping typing sessions
        self.running = True

        text = pyperclip.paste()
        if not text.strip():
            print("Clipboard is empty. Please copy some text.")
            self.running = False
            return

        delay_speed = 0  # Adjust typing speed delay here
        with io.StringIO(text) as f:
            for lines in f:
                if not lines.strip():
                    continue

                type_me = self.tabbing_mech(lines)  # Handles tabbing
                if type_me is not None:
                    pyautogui.typewrite(type_me, delay_speed)
                pyautogui.press('enter')

                if 'break\n' in lines or 'return\n' in lines or 'pass\n' in lines or 'continue\n' in lines:
                    self.x = 1
                else:
                    self.x = 0

        self.running = False


def main():
    typer = AutoTyper()
    print("AutoTyper is running...")
    print("Press ESC or F4 to type the clipboard content.")
    print("Press Ctrl+C to exit.")

    # Add hotkeys for starting the typing
    keyboard.add_hotkey('escape', typer.start_autotyper)
    keyboard.add_hotkey('f4', typer.start_autotyper)

    try:
        while True:
            time.sleep(1)  # Keeps the script running
    except KeyboardInterrupt:
        print("\nExiting AutoTyper.")


if __name__ == "__main__":
    main()
