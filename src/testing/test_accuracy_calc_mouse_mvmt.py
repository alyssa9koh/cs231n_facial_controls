import math
import re


from .test_utils import load_input_data


__all__ = ['test_accuracy_calc_mouse_mvmt_main', 'find_suggested_thresholds']


LOG_DIRECTORY = './src/ignore_dump/'
DEFAULT_TIME_THRESHOLD = 0.15
DEFAULT_DIST_THRESHOLD = 120


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

def analyze_differences(controller_inputs, program_inputs):
    time_diffs = []
    distance_diffs = []
    
    for program_input in program_inputs:
        if program_input["Event Type"] != "Mouse":
            continue
        
        program_pos = parse_mouse_event(program_input["Event"])
        program_timestamp = float(program_input["Timestamp"])
        
        closest_time_diff = float('inf')
        closest_distance = float('inf')
        
        for ci in controller_inputs:
            if ci["Event Type"] != "Mouse":
                continue
            
            controller_pos = parse_mouse_event(ci["Event"])
            controller_timestamp = float(ci["Timestamp"])
            
            time_diff = abs(controller_timestamp - program_timestamp)
            distance = calculate_distance(controller_pos, program_pos)
            
            if time_diff < closest_time_diff:
                closest_time_diff = time_diff
                closest_distance = distance
        
        time_diffs.append(closest_time_diff)
        distance_diffs.append(closest_distance)
    
    average_time_diff = sum(time_diffs) / len(time_diffs)
    average_distance_diff = sum(distance_diffs) / len(distance_diffs)
    
    return average_time_diff, average_distance_diff


def find_suggested_thresholds(controller_inputs=None, program_inputs=None):
    if not controller_inputs or not program_inputs:
        # Load the data
        print(f'This program will be loading CSV files from the folder {LOG_DIRECTORY}.')
        print('What is the file name of the controller input CSV?')
        controller_inputs_csv = input().strip()
        print('What is the file name of the program input CSV?')
        program_inputs_csv = input().strip()
        print('')

        controller_inputs = load_input_data(LOG_DIRECTORY + controller_inputs_csv)
        program_inputs = load_input_data(LOG_DIRECTORY + program_inputs_csv)

    # Analyze the differences
    average_time_diff, average_distance_diff = analyze_differences(controller_inputs, program_inputs)

    print(f"Suggested time threshold: {average_time_diff * 2:.4f} seconds")
    print(f"Suggested distance threshold: {average_distance_diff * 2:.2f} units")
    print('')
    return average_time_diff, average_distance_diff


def compare_mouse_movements(controller_inputs, program_inputs, time_threshold, distance_threshold):
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

    while True:
        print('Would you like to use custom thresholds for time and distance?')
        print('This program can also provide suggested thresholds.')
        print(f'The default thresholds are {DEFAULT_TIME_THRESHOLD} for time and {DEFAULT_DIST_THRESHOLD} for distance.')
        print('Please enter a number to indicate your choice.')
        print('1: Use custom thresholds; 2: Get suggested thresholds; anything else: use default thresholds')
        use_custom_thresholds_choice = input('')

        if use_custom_thresholds_choice == '1':
            print('Please enter a time threshold.')
            time_threshold = float(input(''))
            print('Please enter a distance threshold.')
            distance_threshold = float(input(''))
            break

        elif use_custom_thresholds_choice == '2':
            suggested_time_threshold, suggested_dist_threshold = find_suggested_thresholds(controller_inputs=controller_inputs, program_inputs=program_inputs)
            print('Would you like to use these suggested thresholds? Y/N')
            suggested_choice = input('')
            if suggested_choice == 'Y' or suggested_choice == 'y':
                time_threshold = suggested_time_threshold
                distance_threshold = suggested_dist_threshold
                break
        else:

            print('Using default thresholds.')
            time_threshold = DEFAULT_TIME_THRESHOLD
            distance_threshold = DEFAULT_DIST_THRESHOLD
            break
        print('')
    

    print('Running comparisons...')
    accuracy = compare_mouse_movements(controller_inputs, program_inputs, time_threshold, distance_threshold)
    print(f'Accuracy: {accuracy * 100:.2f}%')

