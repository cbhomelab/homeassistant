# variables needed:
# slave_id - related light entity (light, fan, or switch domain)
# timer_id - timer helper

import convert

# we'll use this later
registered_triggers = []

# First, we define a function that makes more functions.
def make_timer_cancel(config):

    # set trigger to slave entity off
    @state_trigger(float(config['slave_id']) == "off")

    def timer_cancel():

        task.unique(f"timer_cancel_{config['timer_id']}")
        
        if state.get(config['timer_id']) == "Active":
            
            timer.cancel(entity_id=config['timer_id'])
    
    # now that we've made a function specifically for this config item
    # we need to register it in the global scope so pyscript sees it.
    # the easiest way to do that is add it to a global list.
    registered_triggers.append(timer_finished)

# now we just need the startup trigger
@time_trigger('startup')
def timer_cancel_startup():
    for app in pyscript.app_config:
        make_timer_cancel(app)