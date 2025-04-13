# variables needed:
# fan_id - fan entity (fan or switch domain)
# timer_id - timer helper
# duration_id - input_number helper for user duration input

import convert

# we'll use this later
registered_triggers = []

# First, we define a function that makes more functions.
def make_fan_timer(config):

    # trigger by fan turning on
    @state_trigger(f"{config['fan_id']} == 'on'")

    def fan_timer():

        # create unique task
        task.unique(f"fan_timer_{config['fan_id']}")

        # process entities to determine domain
        fan_domain = convert.get_domain(f"config['fan_id']")
        
        # start timer
        if float(config['duration_id']) != 0:
            # start timer if duration is non-zero
            timer.start(entity_id=config['timer_id'],duration=convert.sec_to_timer(float(config['duration_id'])*60))
        else:
            # start 15 minute timer if duration is zero
            timer.start(entity_id=config['timer_id'],duration=convert.sec_to_timer(15*60))
    
    # now that we've made a function specifically for this config item
    # we need to register it in the global scope so pyscript sees it.
    # the easiest way to do that is add it to a global list.
    registered_triggers.append(fan_timer)

# now we just need the startup trigger
@time_trigger('startup')
def fan_timer(startup):
    for app in pyscript.app_config:
        make_fan_timer(app)