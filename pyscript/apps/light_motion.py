# variables needed:
# motion_id - motion sensor (binary_sensor)
# light_id - related light entity (light or switch domain)
# brightness_id - Adaptive Lighting brightness (switch.adaptive_lighting_[room].brightness_pct)
# timer_id - timer helper
# duration_id - input_number helper for user duration input

import convert

# we'll use this later
registered_triggers = []

# First, we define a function that makes more functions.
def make_light_motion(config):

    # set trigger to motion sensor on
    @state_trigger(f"{config['motion_id']} == 'on'")

    def light_motion():
        # set unique task
        task.unique(f"light_motion_{config['motion_id']}")

        # cancel existing timer if it's active
        if state.get(config['timer_id']) == "Active":
            timer.cancel(entity_id=config['timer_id'])

        # turn the light on if it's off
        if state.get(config['light_id']) != "on":
            # check domain of light
            light_domain = convert.get_domain(config['light_id'])
            if light_domain == "light":
                # check for brightness value
                if state.get(config['brightness_id']) != "null":
                    light.turn_on(entity_id=config['light_id'],brightness_pct=state.get(config['brightness_id']))
                else:
                    light.turn_on(entity_id=config['light_id'])
            else:
                switch.turn_on(entity_id=config['light_id'])

        # wait until motion clears or light turns off
        task.wait_until(
                state_trigger=f"{config['motion_id']} == 'off'",
                state_trigger=f"{config['light_id']} == 'off'"
                )
        
        # check light is still on to avoid sending needless service calls
        if state.get(config['light_id']) == "on":
            if state.get(config['timer_id']) != "null":
                # check duration
                if float(state.get(config['duration_id'])) != 0:
                    # start timer if duration is non-zero
                    timer.start(entity_id=config['timer_id'],duration=state.sec_to_timer(float(config['duration_id'])*60))
                else:
                    # turn light off if duration is zero
                    if light_domain == "light":
                        light.turn_off(entity_id=config['light_id'])
                    else:
                        switch.turn_off(entity_id=config['light_id'])
            else:
                # turn light off if duration is undefined
                if light_domain == "light":
                    light.turn_off(entity_id=config['light_id'])
                else:
                    switch.turn_off(entity_id=config['light_id'])
    
    # now that we've made a function specifically for this config item
    # we need to register it in the global scope so pyscript sees it.
    # the easiest way to do that is add it to a global list.
    registered_triggers.append(light_motion)

# now we just need the startup trigger
@time_trigger('startup')
def light_motion_startup():
    for app in pyscript.app_config:
        make_light_motion(app)