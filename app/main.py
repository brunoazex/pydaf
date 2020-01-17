if __name__ == "__main__":
    import sys, os, inspect    
    from lib.app import App
    
    root_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    exit_code = App.instance().run(root_path) or 0
    exit(exit_code)
else:
    raise ImportError("Run this file directly, don't import it!")
