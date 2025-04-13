# variables needed:
# master_id - master light entity (light or switch domain)
# slave_id - related light entity (light or switch domain)

import convert

# we'll use this later
registered_triggers = []

# First, we define a function that makes more functions.
def make_light_sync(config):

    # set trigger to master entity value changes
    @state_trigger(f"{config['master_id']} == 'on'")
    @state_trigger(f"{config['master_id']} == 'off'")

    def light_sync():
        # set unique task
        task.unique(f"light_sync_{config['master_id']}_{config['slave_id']}")

        # process entities to determine domain of each
        slave_domain = convert.get_domain(config['slave_id'])
        master_domain = convert.get_domain(config['master_id'])

        if state.get(config['master_id']) != "on":
            # check brightness if master entity is a light
            if master_domain == "light":
                brightness_id = f"{config['master_id']}.brightness"
            # run correct service based on slave entity domain
            if slave_domain == "light":
                light.turn_on(entity_id=config['slave_id'],brightness=brightness_id)
            elif slave_domain == "switch":
                switch.turn_on(entity_id=config['slave_id'])
        else:
            # run correct service based on slave entity domain
            if slave_domain == "light":
                light.turn_off(entity_id=config['slave_id'])
            elif slave_domain == "switch":
                switch.turn_off(entity_id=config['slave_id'])

    # now that we've made a function specifically for this config item
    # we need to register it in the global scope so pyscript sees it.
    # the easiest way to do that is add it to a global list.
    registered_triggers.append(light_sync)

# now we just need the startup trigger
@time_trigger('startup')
def light_sync_startup():
    for app in pyscript.app_config:
        make_light_sync(app)