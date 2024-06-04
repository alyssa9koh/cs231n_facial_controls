import csv

__all__ = ['test_accuracy_calc_keyboard_main']


LOG_DIRECTORY_PARENT = 'src'
LOG_DIRECTORY = './ignore_dump/'


def compare_inputs(controller_inputs, program_inputs, time_threshold=0.01):
    correct_matches = 0
    total_comparisons = 0
    
    # Track which controller inputs have been matched
    matched_controller_inputs = [False] * len(controller_inputs)
    
    for program_input in program_inputs:
        program_event_type = program_input["Event Type"]
        program_event = program_input["Event"]
        program_timestamp = program_input["Timestamp"]
        
        # Find the matching controller input
        matching_index = next(
            (index for index, ci in enumerate(controller_inputs) 
             if not matched_controller_inputs[index] and 
                abs(float(ci["Timestamp"]) - float(program_timestamp)) <= time_threshold and 
                ci["Event Type"] == program_event_type),
            None
        )
        
        if matching_index is not None:
            matching_controller_input = controller_inputs[matching_index]
            matched_controller_inputs[matching_index] = True
            
            # Compare details
            if program_event == matching_controller_input["Event"]:
                correct_matches += 1
        
        total_comparisons += 1
    
    accuracy = correct_matches / total_comparisons if total_comparisons > 0 else 0
    return accuracy


def load_input_data(filename):
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


def test_accuracy_calc_keyboard_main():
    print(f'This program will be loading CSV files from the folder {LOG_DIRECTORY} located in {LOG_DIRECTORY_PARENT}.')
    print('What is the file name of the controller input CSV?')
    controller_inputs_csv = input('')
    print('What is the file name of the program input CSV?')
    program_inputs_csv = input('')
    print('')

    print('Loading files...')
    # Load controller and program inputs from CSV files
    controller_inputs = load_input_data(LOG_DIRECTORY + controller_inputs_csv)
    print(f'Loaded controller inputs csv: {LOG_DIRECTORY}{controller_inputs_csv}')
    program_inputs = load_input_data(LOG_DIRECTORY + program_inputs_csv)
    print(f'Loaded program inputs csv: {LOG_DIRECTORY}{program_inputs_csv}')
    print('')

    # Calculate the accuracy
    print('Running comparisons...')
    accuracy = compare_inputs(controller_inputs, program_inputs)
    print(f'Accuracy: {accuracy * 100:.2f}%')

