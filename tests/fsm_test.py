import sys
sys.path.append('../lib/')
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
