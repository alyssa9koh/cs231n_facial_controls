
def compare_inputs(controller_inputs, ai_generated_inputs, time_threshold=0.01):
    correct_matches = 0
    total_comparisons = 0
    
    for ai_input in ai_generated_inputs:
        ai_timestamp = ai_input["timestamp"]
        
        # Find the matching controller input
        matching_controller_input = next((ci for ci in controller_inputs if abs(ci["timestamp"] - ai_timestamp) <= time_threshold), None)
        
        if matching_controller_input:
            # Compare details
            if ai_input["input_type"] == matching_controller_input["input_type"]:
                if ai_input["input_type"] == "keyboard":
                    if ai_input["key"] == matching_controller_input["key"]:
                        correct_matches += 1
                elif ai_input["input_type"] == "mouse":
                    if (ai_input["mouse_x"] == matching_controller_input["mouse_x"] and
                        ai_input["mouse_y"] == matching_controller_input["mouse_y"]):
                        correct_matches += 1
        
        total_comparisons += 1
    
    accuracy = correct_matches / total_comparisons if total_comparisons > 0 else 0
    return accuracy

accuracy = compare_inputs(controller_inputs, ai_generated_inputs)
print(f"Accuracy: {accuracy * 100:.2f}%")

