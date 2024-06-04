import csv

__all__ = ['test_accuracy_calc_keyboard_main']


def compare_inputs(controller_inputs, ai_generated_inputs, time_threshold=0.01):
    correct_matches = 0
    total_comparisons = 0
    
    # Track which controller inputs have been matched
    matched_controller_inputs = [False] * len(controller_inputs)
    
    for ai_input in ai_generated_inputs:
        ai_event_type = ai_input["Event Type"]
        ai_event = ai_input["Event"]
        ai_timestamp = ai_input["Timestamp"]
        
        # Find the matching controller input
        matching_index = next(
            (index for index, ci in enumerate(controller_inputs) 
             if not matched_controller_inputs[index] and 
                abs(ci["Timestamp"] - ai_timestamp) <= time_threshold and 
                ci["Event Type"] == ai_event_type),
            None
        )
        
        if matching_index is not None:
            matching_controller_input = controller_inputs[matching_index]
            matched_controller_inputs[matching_index] = True
            
            # Compare details
            if ai_event == matching_controller_input["Event"]:
                correct_matches += 1
        
        total_comparisons += 1
    
    accuracy = correct_matches / total_comparisons if total_comparisons > 0 else 0
    return accuracy


def load_input_data(filename):
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


def test_accuracy_calc_keyboard_main():
    print('emwow')
    # # Load controller and AI generated inputs from CSV files
    # controller_inputs = load_input_data('./ignore_dump/controller_input_log.csv')
    # ai_generated_inputs = load_input_data('./ignore_dump/ai_generated_input_log.csv')

    # # Calculate the accuracy
    # accuracy = compare_inputs(controller_inputs, ai_generated_inputs)
    # print(f'Accuracy: {accuracy * 100:.2f}%')

