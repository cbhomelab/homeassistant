# variables needed:
# humidity_id -  humidity rate of change (sensor domain)
# fan_id - fan entity (fan or switch domain)
# timer_id - timer helper
# duration_id - input_number helper for user duration input

import convert

# we'll use this later
registered_triggers = []

# First, we define a function that makes more functions.
def make_fan_humidity(config):

    # set trigger to master entity on
    @state_trigger(f"float(config['humidity_id']) > 0.6")

    def fan_humidity():
        # set unique task
        task.unique(f"fan_humidity_{config['fan_id']}")

        # process entities to determine domain of each
        fan_domain = convert.get_domain(f"config['fan_id']")
            
        # perform action
        if state.get(config['fan_id']) != "on":
            # substitute in the value from config
            if fan_domain == "fan":
                fan.turn_on(entity_id=config['fan_id'])
            elif fan_domain == "switch":
                switch.turn_on(entity_id=config['fan_id'])

        # wait for humidity to decrease with a 30 minute timeout
        trig_info = task.wait_until(
                        state_trigger="float(config['humidity_id']) < -0.4",
                        timeout=30*60
                    )
                    
        # if timed out, start the timer
        if trig_info["trigger_type"] == "timeout":
            # non-zero duration
            if float(state.get(config['duration_id'])) != 0:
                # start timer if duration is non-zero
                timer.start(entity_id=config['timer_id'],duration=convert.sec_to_timer(float(state.get(config['duration_id']))*60))
            else:
                # start 15 minute timer if duration is zero
                timer.start(entity_id=config['timer_id'],duration=convert.sec_to_timer(15*60))
        # humidity decreased within 30 minutes
        else:
            # check state of fan
            if state.get(config['fan_id']) != "off":
                # 
                if fan_domain == "fan":
                    fan.turn_off(entity_id=config['fan_id'])
                elif fan_domain == "switch":
                    switch.turn_off(entity_id=config['fan_id'])

    
    # now that we've made a function specifically for this config item
    # we need to register it in the global scope so pyscript sees it.
    # the easiest way to do that is add it to a global list.
    registered_triggers.append(fan_humidity)

# now we just need the startup trigger
@time_trigger('startup')
def fan_humidity(startup):
    for app in pyscript.app_config:
        make_fan_humidity(app)