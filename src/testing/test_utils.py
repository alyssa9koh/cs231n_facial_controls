import csv


# Function to save input events to a CSV file
def save_to_csv(events, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Event Type', 'Event', 'Timestamp'])
        writer.writerows(events)
        