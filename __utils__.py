import os
import datetime
import time
import csv

def make_list(inp):
    if not isinstance(inp, list):
        return [inp]
    else:
        return inp
    
def list_files_in_this_dir(directory):
    '''
    Returns a list containing the complete path to all the files contained in 
    the given directory
    '''
    tmp = os.listdir(directory)
    if tmp is None:
        return []
    tmp = make_list(tmp)
    tmp = [os.path.join(directory, item) for item in tmp]
    files = [item for item in tmp if os.path.isfile(item)]
    files.sort()
    return files

def this_moment(fmt = '%Y-%m-%d %H-%M-%S'):
    return datetime.datetime.fromtimestamp(time.time()).strftime(fmt)

def write_row_csv(CSVfile, newRow, mode = 'a'):
    # eventually create the csv folder
    os.makedirs(os.path.split(CSVfile)[0], exist_ok= True)
    f = open(CSVfile, mode, encoding='UTF8', newline='')
    writer = csv.writer(f)
    writer.writerow(newRow)
    f.close()


# -*- coding: utf-8 -*-
"""
Timer class
"""

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    """
    Simple timer for timing code(blocks).

    Parameters
    ----------
    name : str
        name of timer, optional
    text : str
        custom text, optional
    start : bool
        automatically start the timer when it's initialized, default is True

    Methods
    -------
    start
        start the timer

    stop
        stop the timer, prints and returns the time

    elap
        print the time elapsed from the start
        
    lap
        print the time between this lap and the previous one

    """

    def __init__(self, name="", text="{:0.4f} seconds", string_lap = 'lap  : ', 
                 string_elap = 'elap : ', string_stop = 'stop : ', start = True):
        self._start_time = None
        self._lap_time = 0.
        self._name = name
        self._text = text
        if self._name:
            self._string_lap = self._name + ' - ' + string_lap
            self._string_elap = self._name + ' - ' + string_elap
            self._string_stop = self._name + ' - ' + string_stop
        else:
            self._string_lap = string_lap
            self._string_elap = string_elap
            self._string_stop = string_stop

        if start:
            self.start()

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is already running. Use .stop() to stop it")
        self._start_time = time.perf_counter()

    def reset(self):
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")
        self._start_time = time.perf_counter()

    def lap(self, lap_name="", printTime = True):
        """Report the elapsed time wrt the previous lap"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")
        if self._lap_time:
            current_lap = time.perf_counter() - self._lap_time - self._start_time
            self._lap_time += current_lap
        else:
            self._lap_time = time.perf_counter() - self._start_time
            current_lap = self._lap_time
        if printTime:
            if lap_name:
                print(self._string_lap + self._text.format(current_lap) + ' [' + lap_name + ']')
            else:
                print(self._string_lap + self._text.format(current_lap))
        return current_lap

    def elap(self, elap_name="", printTime = True):
        """Report the elapsed time wrt to the start time or to the last reset"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")
        elapsed_time = time.perf_counter() - self._start_time
        if printTime:
            if elap_name:
                print(self._string_elap + self._text.format(elapsed_time) + ' [' + elap_name + ']')
            else:
                print(self._string_lap + self._text.format(elapsed_time))
        return elapsed_time

    def stop(self, printTime = True):
        """Stop the timer and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        self._lap_time = 0.
        if printTime:
            print(self._string_stop + self._text.format(elapsed_time))
        
        return elapsed_time
