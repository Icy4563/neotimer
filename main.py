from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.widgets import Label, Digits
from textual.containers import HorizontalGroup
import time, asyncio, sys

# Class for the timer digits
class TimerDisplay(Digits):
    time = reactive(0)

    def watch_time(self, new_time):
        self.update(str(new_time))

#top right widget for notifications such as deleting solves
class NotificationCenter(Label):
    notification_text = reactive("")

    def watch_notification_text(self, new_text):
        self.update(str(new_text))

#class for the last solve widget in the bottom right
class LastSolve(Label):
    last_solve = reactive(0)

    def watch_last_solve(self, new_last_solve):
        self.update(str(new_last_solve))

# Class for the Average display
class Average(Label):
    averages = reactive("")

    def watch_averages(self, new_averages):
        self.update(str(new_averages))
# Horizontal group so Average and LastSolve sit on the same 'line'
class AvgandLastSolve(HorizontalGroup):
    def compose(self):
        yield Average("If you are reading this, you are very niche")
        yield LastSolve("last: none")

# Returns the necessary format of averages depending on user prefrence
def format_average(raw_avg:float, raw_avg5:float, raw_avg12:float, view:str):
    if view == "avg":
        return f"avg: {raw_avg:.2f}"

    elif view == "avg & avg5":
        return f"avg: {raw_avg:.2f}  |  ao5: {raw_avg5:.2f}"

    elif view == "avg & avg5 & avg12":
        return f"avg: {raw_avg:.2f}  |  ao5: {raw_avg5:.2f}  |  ao12: {raw_avg12:.2f}"

    elif view == "avg5":
        return f"ao5: {raw_avg5:.2f}"

# Basic function to get the average of all solves
def get_average(solves:list):
    sums = 0.0

    for solve in solves:
        solve = float(solve)
        sums += solve

    return (sums / len(solves)) if not len(solves) == 0 else 0.0 #Protect against ZeroDivisionError

def get_average5(solves:list):
    solves = solves[-5:] #only last 5 entries
    if len(solves) < 5:
        return 0.0 #only return something if there actually are 5 or more solves

    sums = 0.0

    for solve in solves:
        solve = float(solve)
        sums += solve

    return (sums / 5)

def get_average12(solves:list):
    solves = solves[-12:] #only last 12 entries
    if len(solves) < 12:
        return 0.0 #only return something if there actually are 12 or more solves

    sums = 0.0

    for solve in solves:
        solve = float(solve)
        sums += solve

    return (sums / 12)

# App class for NeoTimer
class NeoTimerApp(App):
    BINDINGS = [("alt+space", "start_timer", "Start the timer"),
    ("space", "stop_timer", "Stop the timer"),
    ("x", "delete_solve", "Delete the last solve"),
    ("2", "plus_two_solve", "Plus two the last solve")]# set the keybinds

    CSS_PATH = "neotimer.tcss" #CSS style file

    average_view = "avg5"

    def on_mount(self):
        self.theme = "textual-ansi"  #When the App starts, set the theme to ANSI so that colors depend on the user's system

    list_of_solves = [] #Initialize the list of solves, will be used to get averages later

    #boolean used to track the state of the timer
    timing = False

    def compose(self): #Place widgets on screen
        yield TimerDisplay("0.00")
        yield NotificationCenter("notifications")
        yield AvgandLastSolve() #HorizontalGroup that contains the Average widget and the LastSolve widget

    async def clear_notifications(self):
        await asyncio.sleep(4) #Amount of seconds to wait before clearing
        self.notification_widget.notification_text = ""

    #helper to simplify updating the notification widget
    def notify(self, new_notification_text:str):
        self.notification_widget = self.query_one(NotificationCenter)
        self.notification_widget.notification_text = new_notification_text
        asyncio.create_task(self.clear_notifications())
        

    #Async function that runs from start timer until stop timer to show time passing. Is async so that it doesn't block the detection of the keypress whilst the timer is running    
    async def show_progress(self, start_time):
        while self.timing:
            self.TimerDisplay = self.query_one(TimerDisplay)
            self.TimerDisplay.time = f"{(time.time() - start_time):.2f}"
            await asyncio.sleep(0.02)

    # Called when space+alt is pressed; if not timing, then start timing and
    # add show_progress as a background task so that users can see their times live
    async def action_start_timer(self):
        if not self.timing:
            self.start_time = time.time()
            self.timing = True
            asyncio.create_task(self.show_progress(self.start_time)) # Create a background task so that elif self.timing can run regardless of show_progress

    # If timing, stop timing. Only checks for 'space' so that you don't need to try and aim for alt+space after solving
    def action_stop_timer(self):        
        if self.timing:
            self.end_duration = f"{(time.time() - self.start_time):.2f}"
            self.TimerDisplay = self.query_one(TimerDisplay) #get the currently displayed TimerDisplay widget
            self.TimerDisplay.time = self.end_duration #Show the finished time on the TimerDisplay widget

            self.list_of_solves.append(self.end_duration) #add the latest solve to the list of solves

            self.Average = self.query_one(Average) #Get the displayed Average widget so we can access its reactive values so we can update the avg, ao5 and ao12

            self.Average.averages = format_average(get_average(self.list_of_solves), get_average5(self.list_of_solves), get_average12(self.list_of_solves), view=self.average_view)
                # give the format_average func all of the averages (avg, ao5 and ao12). format_average will then display the
                # averages as chosen by the user via average_view

            self.lastsolve = self.query_one(LastSolve) # get the displayed LastSolve widget
            
            self.lastsolve.last_solve = f"last: {float(self.list_of_solves[-2:][0]):.2f}" # Update the LastSolve widget

            self.timing = False #end the timer

    def action_plus_two_solve(self):
        last_solve = self.list_of_solves.pop() # get the last solve
        last_solve = float(last_solve) + 2.0 # add two to it
        self.list_of_solves.append(f"{last_solve:.2f}") # add it back to the solve history

        ##Update visible metrics##
        self.Average = self.query_one(Average) #Get the displayed Average widget so we can access its reactive values so we can update the avg, ao5 and ao12

        self.Average.averages = format_average(get_average(self.list_of_solves), get_average5(self.list_of_solves), get_average12(self.list_of_solves), view=self.average_view)
            # give the format_average func all of the averages (avg, ao5 and ao12). format_average will then display the
            # averages as chosen by the user via average_view

        self.lastsolve = self.query_one(LastSolve) # get the displayed LastSolve widget
        
        self.lastsolve.last_solve = f"last: {float(self.list_of_solves[-2:][0]):.2f}" # Update the LastSolve widget

        self.notify("Plus two'd last solve")


    def action_delete_solve(self):
        if not len(self.list_of_solves) == 0: # Remove the last solve and protect against list length being 0
            self.list_of_solves.pop()
        else:
            pass 

        self.Average = self.query_one(Average) #Get the displayed Average widget so we can access its reactive values so we can update the avg, ao5 and ao12

        self.Average.averages = format_average(get_average(self.list_of_solves), get_average5(self.list_of_solves), get_average12(self.list_of_solves), view=self.average_view)
            # give the format_average func all of the averages (avg, ao5 and ao12). format_average will then display the
            # averages as chosen by the user via average_view

        self.lastsolve = self.query_one(LastSolve) # get the displayed LastSolve widget
        
        self.lastsolve.last_solve = f"last: {float(self.list_of_solves[-2:][0]):.2f}" if not len(self.list_of_solves) == 0 else "Deleted all solves!" # Update the LastSolve widget and protect against list length being 0 if user deleted too many solves

        self.notify("Deleted the last solve")

app = NeoTimerApp()
app.run()

#TODO add a notification popup in the top right with messages for delete solve or plus two