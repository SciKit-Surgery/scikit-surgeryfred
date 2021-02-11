# coding=utf-8

"""User interfaces for sksurgeryFRED"""

from sksurgeryfred.widgets.interactive_registration \
                import InteractiveRegistration

def run_demo(image):
    """Run FRED"""

    InteractiveRegistration(image)
