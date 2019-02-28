import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\lib')))
from fsm import FSM


my_state_machine = FSM()


my_state_machine.on_event('send')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('timeout')

my_state_machine.on_event('send')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('finish')

my_state_machine.on_event('send')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('resend')
my_state_machine.on_event('finish')

my_state_machine.on_event('send')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('finish')

my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('timeout')

my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('finish')


my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('resend')
my_state_machine.on_event('finish')

my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('')
my_state_machine.on_event('finish')
