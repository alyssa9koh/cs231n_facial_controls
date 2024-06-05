import math
import re


from .test_utils import load_input_data


__all__ = ['test_accuracy_calc_mouse_mvmt_main']


LOG_DIRECTORY = './src/ignore_dump/'


def parse_mouse_event(event):
    match = re.search(r'\((\d+),\s*(\d+)\)', event)
    if match:
        x, y = match.groups()
        return int(x), int(y)
    else:
        raise ValueError(f"Cannot parse mouse event: {event}")

def calculate_distance(pos1, pos2):
    # Euclidean distance between two positions
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def compare_mouse_movements(controller_inputs, program_inputs, time_threshold=0.01, distance_threshold=5):
    correct_matches = 0
    total_comparisons = 0
    
    matched_controller_inputs = [False] * len(controller_inputs)
    
    for program_input in program_inputs:
        if program_input["Event Type"] != "Mouse":
            continue
        
        program_pos = parse_mouse_event(program_input["Event"])
        program_timestamp = float(program_input["Timestamp"])
        
        matching_index = next(
            (index for index, ci in enumerate(controller_inputs)
             if not matched_controller_inputs[index] and
                abs(float(ci["Timestamp"]) - program_timestamp) <= time_threshold and
                ci["Event Type"] == "Mouse" and
                calculate_distance(parse_mouse_event(ci["Event"]), program_pos) <= distance_threshold),
            None
        )
        
        if matching_index is not None:
            matched_controller_inputs[matching_index] = True
            correct_matches += 1
        
        total_comparisons += 1
    
    accuracy = correct_matches / total_comparisons if total_comparisons > 0 else 0
    return accuracy

def test_accuracy_calc_mouse_mvmt_main():
    print(f'This program will be loading CSV files from the folder {LOG_DIRECTORY}.')
    print('What is the file name of the controller input CSV?')
    controller_inputs_csv = input().strip()
    print('What is the file name of the program input CSV?')
    program_inputs_csv = input().strip()
    print('')

    print('Loading files...')
    controller_inputs = load_input_data(LOG_DIRECTORY + controller_inputs_csv)
    print(f'Loaded controller inputs csv: {LOG_DIRECTORY}{controller_inputs_csv}')
    program_inputs = load_input_data(LOG_DIRECTORY + program_inputs_csv)
    print(f'Loaded program inputs csv: {LOG_DIRECTORY}{program_inputs_csv}')
    print('')

    print('Running comparisons...')
    accuracy = compare_mouse_movements(controller_inputs, program_inputs)
    print(f'Accuracy: {accuracy * 100:.2f}%')

