#!/usr/bin/python3

from pygbx import Gbx, GbxType
from pygbx.headers import ControlEntry, CGameCtnGhost
import numpy as np
import logging, sys, os, getopt


def fname_from_gbx(gbx_fname, repl):
    return os.path.basename(gbx_fname).replace(".Replay.Gbx", repl)


def get_event_time(event: ControlEntry) -> int:
    if event.event_name == "Respawn":
        time = int(event.time / 10) * 10
        if event.time % 10 == 0:
            time -= 10
        return time
    else:
        return int(event.time / 10) * 10 - 10


def event_to_analog_value(event: ControlEntry):
    val = np.int32((event.flags << 16) | event.enabled)
    val <<= np.int32(8)
    val >>= np.int32(8)
    return -val


def try_parse_old_ghost(g: Gbx):
    ghost = CGameCtnGhost(0)

    parser = g.find_raw_chunk_id(0x2401B00F)
    if parser:
        ghost.login = parser.read_string()

    parser = g.find_raw_chunk_id(0x2401B011)
    if parser:
        parser.seen_loopback = True
        g.read_ghost_events(ghost, parser, 0x2401B011)
        return ghost

    return None


# accel/brake/steer: inputs as [time,value] pairs
# ms_*             : input value every 10ms
def get_inputs(ghost, write_func=None):
    inputs = {
        "accel"  : np.array([-3000,0], ndmin=2),
        "brake"  : np.array([-3000,0], ndmin=2),
        "steerL" : np.array([-3000,0], ndmin=2),
        "steerR" : np.array([-3000,0], ndmin=2),

        "ms_accel"  : [],
        "ms_brake"  : [],
        "ms_steerL" : [],
        "ms_steerR" : [],

        "racetime" : ghost.events_duration,
        "cp_times" : ghost.cp_times
    }

    invert_axis = False
    for event in ghost.control_entries:
        if event.event_name == "_FakeDontInverseAxis":
            invert_axis = True
            break

    # Keep track of previous events to prioritize digital events
    last_event_time = 0
    last_event_digital = {
        "accel" : False,
        "brake" : False,
        "steer" : False
    }

    # Get events from replay file
    for event in ghost.control_entries:
        time = get_event_time(event)
        name = event.event_name
        value = event_to_analog_value(event)
        if invert_axis:
            value = -value

        if write_func:
            write_func(f"{time} {name} {value}\n")

        if name == "Accelerate":
            if value != 0:
                value = 1
            inputs["accel"] = np.append(inputs["accel"], [[time, value]], axis=0)
            last_event_digital["accel"] = True
        elif name == "AccelerateReal":
            if time == last_event_time and last_event_digital["accel"]:
                continue
            if value > 0:
                value = 1
            else:
                value = 0
            inputs["accel"] = np.append(inputs["accel"], [[time, value]], axis=0)
            last_event_digital["accel"] = False
        elif name == "Brake":
            if value != 0:
                value = 1
            inputs["brake"] = np.append(inputs["brake"], [[time, value]], axis=0)
            last_event_digital["brake"] = True
        elif name == "BrakeReal":
            if time == last_event_time and last_event_digital["brake"]:
                continue
            if value > 0:
                value = 1
            else:
                value = 0
            inputs["brake"] = np.append(inputs["brake"], [[time, value]], axis=0)
            last_event_digital["brake"] = False
        elif name == "SteerLeft":
            if value != 0:
                value = 65536
            inputs["steerL"] = np.append(inputs["steerL"], [[time, value]], axis=0)
            last_event_digital["steer"] = True
        elif name == "SteerRight":
            if value != 0:
                value = 65536
            inputs["steerR"] = np.append(inputs["steerR"], [[time, value]], axis=0)
            last_event_digital["steer"] = True
        elif name == "Steer":
            if time == last_event_time and last_event_digital["steer"]:
                continue
            if value > 0:
                inputs["steerR"] = np.append(inputs["steerR"], [[time, value]], axis=0)
                inputs["steerL"] = np.append(inputs["steerL"], [[time, 0]], axis=0)
            elif value < 0:
                inputs["steerR"] = np.append(inputs["steerR"], [[time, 0]], axis=0)
                inputs["steerL"] = np.append(inputs["steerL"], [[time, -value]], axis=0)
            else:
                inputs["steerR"] = np.append(inputs["steerR"], [[time, 0]], axis=0)
                inputs["steerL"] = np.append(inputs["steerL"], [[time, 0]], axis=0)
            last_event_digital["steer"] = False

        last_event_time = time

    # Extend last input to end of replay
    inputs["accel"] = np.append(inputs["accel"][:,:], [[inputs["racetime"], inputs["accel"][-1,1]]], axis=0)
    inputs["brake"] = np.append(inputs["brake"][:,:], [[inputs["racetime"], inputs["brake"][-1,1]]], axis=0)
    inputs["steerR"] = np.append(inputs["steerR"][:,:], [[inputs["racetime"], inputs["steerR"][-1,1]]], axis=0)
    inputs["steerL"] = np.append(inputs["steerL"][:,:], [[inputs["racetime"], inputs["steerL"][-1,1]]], axis=0)


    ## ms inputs
    accelIndex = 0
    brakeIndex = 0
    steerRIndex = 0
    steerLIndex = 0

    # Find state at time 0
    while inputs["accel"][accelIndex][0] < 0:
        accelIndex += 1

    while inputs["brake"][brakeIndex][0] < 0:
        brakeIndex += 1

    while inputs["steerR"][steerRIndex][0] < 0:
        steerRIndex += 1

    while inputs["steerL"][steerLIndex][0] < 0:
        steerLIndex += 1

    # Add info for every 10ms
    for i in range(0, int(inputs["racetime"]/10)+1):
        if 10*i >= inputs["accel"][accelIndex][0]:
            accelIndex += 1
        inputs["ms_accel"].append(inputs["accel"][accelIndex-1][1])

        if 10*i >= inputs["brake"][brakeIndex][0]:
            brakeIndex += 1
        inputs["ms_brake"].append(inputs["brake"][brakeIndex-1][1])

        if 10*i >= inputs["steerR"][steerRIndex][0]:
            steerRIndex += 1
        inputs["ms_steerR"].append(inputs["steerR"][steerRIndex-1][1])

        if 10*i >= inputs["steerL"][steerLIndex][0]:
            steerLIndex += 1
        inputs["ms_steerL"].append(inputs["steerL"][steerLIndex-1][1])

    return inputs


# Try to load ghost from path to GBX file
def ghost_from_gbx(path):
    g = Gbx(path)

    ghosts = g.get_classes_by_ids([GbxType.CTN_GHOST, GbxType.CTN_GHOST_OLD])
    if not ghosts:
        ghost = try_parse_old_ghost(g)
    else:
        ghost = ghosts[0]

    if not ghost:
        logging.error("No ghost found")
        return

    return ghost


# Get inputs directly from path
def get_inputs_gbx(path, write_func=None):
    ghost = ghost_from_gbx(path)

    if not ghost:
        return

    return get_inputs(ghost, write_func)



def process_path(path):
    inputs = get_inputs_gbx(path, sys.stdout.write)
    print(f"Race time: {inputs['racetime']}")
    print(f"CP times: {inputs['cp_times']}")


def main():
    # Read options & arguments
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hW:H:s",
            ["help", "width=", "height=", "save"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for filename in args:
        if filename.lower().endswith(".replay.gbx"):
            process_path(filename)

if __name__ == "__main__":
    main()
