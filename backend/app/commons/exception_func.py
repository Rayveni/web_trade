import functools
from sys import exc_info
from os import path
import traceback
def exception(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return (True,),function(*args, **kwargs)
        except Exception as err:
            # log the exception
            err = f"There was an exception in {function.__name__} error {err} in {traceback.extract_tb(exc_info()[-1])[1]}"
            return (False,err),None

    return wrapper
	
