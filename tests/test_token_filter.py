import pytest
from .context import assembler

tf = assembler.template.token_filter

class TestTokenFilter:

    # add

    def test_add_1(self):
        res = tf.add_filter('7', '3')
        assert res == '10'

    def test_add_2(self):
        res = tf.add_filter('seven', '3')
        assert res == 'seven3'
    
    # addslashes

    def test_addslashes_1(self):
        res = tf.addslashes_filter(r"I'm testing", '')
        assert res == r"I\'m testing"

    def test_addslashes_2(self):
        res = tf.addslashes_filter(r'You are "funny"', '')
        assert res == r'You are \"funny\"'
    
    