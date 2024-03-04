import json

# Path to the JSON file
file_path = 'plantae_2024.json'  # Replace 'path_to_your_file.json' with the actual file path

# Read the JSON data from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# Sort the dictionary items based on the 'order' value in ascending order
sorted_items = sorted(data.items(), key=lambda x: x[1]['order'])

# Convert the sorted list of tuples back into a dictionary
sorted_data = {item[0]: item[1] for item in sorted_items}

# Display or use the sorted data as needed
print(sorted_data)

# Write the sorted data back to the file
with open(file_path, 'w') as file:
    json.dump(sorted_data, file, indent=1)
