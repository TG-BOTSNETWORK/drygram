# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
from drygram import Poll, Quiz, PollOption

def test_poll_and_quiz():
    options = [PollOption("Yes", 10), PollOption("No", 5)]
    poll = Poll(id="p1", question="OK?", options=options, total_voter_count=15, is_closed=False)
    assert poll.id == "p1"
    assert poll.total_voter_count == 15
    
    quiz = Quiz(id="q1", question="1+1=?", options=options, correct_option_id=0, total_voter_count=15)
    assert quiz.id == "q1"
    assert quiz.correct_option_id == 0
