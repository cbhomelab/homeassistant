
# set trigger to master entity value changes
@state_trigger(f"switch.backyard_flood_lights == 'on'")
@state_trigger(f"switch.backyard_flood_lights == 'off'")

def light_sync():
    # set unique task
    task.unique(f"light_sync_backyard_floodlights")

    if state.get(switch.backyard_flood_lights) == "on":
        switch.turn_on(entity_id=switch.flood_lights)
    else:
        switch.turn_off(entity_id=switch.flood_lights)