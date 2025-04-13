# variables needed:
# slave_id - related light entity (light, fan, or switch domain)
# timer_id - timer helper

import convert

# we'll use this later
registered_triggers = []

# First, we define a function that makes more functions.
def make_timer_finished(config):

    # set trigger to timer finished on
    @event_trigger('timer.finished')

    def timer_finished(**kwargs):
        # filter for proper timer id
        if kwargs['entity_id'] == f"config['timer_id']":
            # set unique task
            task.unique(f"timer_finished_{config['timer_id']}")

            # turn the entity off if it's on
            if state.get(config['slave_id']) != "on":
                # check domain of slave
                slave_domain = convert.get_domain(config['slave_id'])
                if slave_domain == "light":
                    light.turn_off(entity_id=config['slave_id'])
                elif slave_domain == "fan":
                    fan.turn_off(entity_id=config['slave_id'])
                elif slave_domain == "switch":
                    switch.turn_off(entity_id=config['slave_id'])
    
    # now that we've made a function specifically for this config item
    # we need to register it in the global scope so pyscript sees it.
    # the easiest way to do that is add it to a global list.
    registered_triggers.append(timer_finnished)

# now we just need the startup trigger
@time_trigger('startup')
def timer_finished_startup():
    for app in pyscript.app_config:
        make_timer_finished(app)