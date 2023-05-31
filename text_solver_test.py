import json
import unittest
import pytest
import os
from cloud_funcs.solvers.text_analyzer import summarize_text

def test_summary():
    context = """
    Hi Joan,
    
    It's the third day of my London adventure and it's been amazing!
    We have visited some of the greatest monuments and galleries.
    I thought I was good at English, but I have a problem understanding people in shops and restaurants. I hope that will change soon! I'll send you some photos this evening.
    See you when I get back from the UK!
    
    Sara
    """

    response = summarize_text(context)
    print(response)

    assert True == False

if __name__ == '__main__':
    unittest.main()
