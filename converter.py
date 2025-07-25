import json

def default_value(base: dict, key, value=0):
 base.setdefault(key, value)

def process_events(events, keys):
 for event in events:
  for key in keys:
   default_value(event, key)

def replace(base: list, fr: str, to: str):
 for struct in base:
  struct[to] = struct.pop(fr)

def revert_index_structure(structure, v4_name, v4_data, v3_name):
 events_data = structure[v4_data]
 for idx, event in enumerate(structure[v4_name]):
  event_index = int(event.pop("i"))
  structure[v4_name][idx] = {**event, **events_data[event_index]}
 del structure[v4_data]
 if v4_name != v3_name:
  structure[v3_name] = structure.pop(v4_name)

def main():
 input_path = input("input file path: ")
 output_path = input("output file path: ")
 if not output_path.strip():
  if "." in input_path:
   output_path = input_path.rsplit(".", 1)[0] + ".v3.dat"
  else:
   output_path = input_path + ".v3.dat"

 with open(input_path, "r") as f:
  structure = json.load(f)

 structure["version"] = "3.3.0"

 # Set default values
 process_events(structure["basicEvents"], ["b", "i"])
 process_events(structure["basicEventsData"], ["t", "i", "f"])
 process_events(structure["colorBoostEvents"], ["b", "i"])
 process_events(structure["waypoints"], ["b", "i"])
 process_events(structure["waypointsData"], ["x", "y", "d", "c", "f", "p", "t", "r", "n", "s", "l"])
 process_events(structure["eventBoxGroups"], ["b", "g"])
 for event_box in structure["eventBoxGroups"]:
  for e_box in event_box["e"]:
   default_value(e_box, "f")
   default_value(e_box, "e")
   for l_box in e_box["l"]:
    default_value(l_box, "b")
    default_value(l_box, "i")
 process_events(structure["lightColorEventBoxes"], ["w", "d", "s", "t", "b", "e"])
 process_events(structure["lightColorEvents"], ["p", "e", "c", "s", "f", "sb", "sf"])
 process_events(structure["lightRotationEventBoxes"], ["w", "d", "s", "t", "b", "e", "a", "r"])
 process_events(structure["lightRotationEvents"], ["p", "e", "r", "d", "l"])
 process_events(structure["lightTranslationEventBoxes"], ["w", "d", "s", "t", "b", "e"])
 process_events(structure["lightTranslationEvents"], ["p", "e", "t"])
 process_events(structure["fxEventBoxes"], ["w", "d", "s", "t", "b", "e"])
 process_events(structure["floatFxEvents"], ["p", "e", "v"])

 # Main structure changes
 revert_index_structure(structure, "basicEvents", "basicEventsData", "basicBeatmapEvents")

 # Boost color events
 for boost_event in structure["colorBoostEventsData"]:
  boost_event["o"] = boost_event.pop("b") == 1
 revert_index_structure(structure, "colorBoostEvents", "colorBoostEventsData", "colorBoostBeatmapEvents")

 # Waypoints
 revert_index_structure(structure, "waypoints", "waypointsData", "waypoints")

 # Event box group processing
 index_filters = structure["indexFilters"]
 color_event_boxes = structure["lightColorEventBoxes"]
 color_events = structure["lightColorEvents"]
 rotation_event_boxes = structure["lightRotationEventBoxes"]
 rotation_events = structure["lightRotationEvents"]
 translation_event_boxes = structure["lightTranslationEventBoxes"]
 translation_events = structure["lightTranslationEvents"]
 fx_event_boxes = structure["fxEventBoxes"]
 fx_events = structure["floatFxEvents"]

 replace(color_event_boxes, "s", "r")
 replace(color_event_boxes, "e", "i")
 replace(color_events, "p", "i")
 for e in color_events:
  e.pop("e", None)

 replace(rotation_event_boxes, "e", "i")
 replace(translation_event_boxes, "s", "r")
 replace(translation_event_boxes, "e", "i")
 structure["_fxEventsCollection"] = {"_fl": [], "_il": []}
 fxfl_collection = structure["_fxEventsCollection"]["_fl"]
 fxfl_event_index_tracker = 0
 replace(fx_event_boxes, "e", "i")

 event_box_lists = [
  color_event_boxes, rotation_event_boxes, translation_event_boxes, fx_event_boxes
 ]
 event_lists = [
  color_events, rotation_events, translation_events, fx_events
 ]
 group_names = [
  "lightColorEventBoxGroups", "lightRotationEventBoxGroups",
  "lightTranslationEventBoxGroups", "vfxEventBoxGroups"
 ]

 for name in group_names:
  structure[name] = []

 for index, event_box in enumerate(structure["eventBoxGroups"]):
  event_box_type = event_box["t"]
  new_body = {"b": event_box["b"], "g": event_box["g"], "e": []}
  for e_body in event_box["e"]:
   new_e_body = {"f": index_filters[e_body["f"]]}
   new_e_body.update(event_box_lists[event_box_type - 1][e_body["e"]])
   new_e_body["l"] = []
   if event_box_type != 4:
    for l_body in e_body["l"]:
     new_l_body = {"b": l_body["b"]}
     new_l_body.update(event_lists[event_box_type - 1][l_body["i"]])
     new_e_body["l"].append(new_l_body)
    new_body["e"].append(new_e_body)
   else:
    for l_body in e_body["l"]:
     new_fl_event = {"b": l_body["b"]}
     new_fl_event.update(event_lists[3][l_body["i"]])
     fxfl_collection.append(new_fl_event)
     new_e_body["l"].append(fxfl_event_index_tracker)
     fxfl_event_index_tracker += 1
    new_body["e"].append(new_e_body)
  structure[group_names[event_box_type - 1]].append(new_body)

 # Cleanup
 for key in [
  "eventBoxGroups", "indexFilters",
  "lightColorEventBoxes", "lightColorEvents",
  "lightRotationEventBoxes", "lightRotationEvents",
  "lightTranslationEventBoxes", "lightTranslationEvents",
  "fxEventBoxes", "floatFxEvents"
 ]:
  structure.pop(key, None)

 # Write output
 try:
  with open(output_path, "r") as f:
   output_contents = json.load(f)
  output_contents.update(structure)
 except Exception:
  output_contents = structure

 with open(output_path, "w") as o:
  json.dump(output_contents, o, separators=(',', ':'))

if __name__ == "__main__":
 main()
