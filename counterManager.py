import os

counter_file = 'counter.txt'

def create_counter_file():
    """Create the counter file and insert initial values (0,0,0)."""
    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as f:
            f.write('0,0')  # Initial values in the file

def read_counters():
    """Read all counter values from the file."""
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as f:
            values = f.read().strip().split(',')
            return [int(value) for value in values]  # Return a list of counter values
    else:
        return [0, 0]  # If the file doesn't exist, return default values

def write_counters(values):
    """Write all counter values to the file."""
    with open(counter_file, 'w') as f:
        f.write(','.join(map(str, values)))  # Write updated values back to the file

def reset_counter():
    """Reset all counter values to 0."""
    write_counters([0, 0])
    return True

def increment_counter(index):
    """Increment the value of a specific counter (by index)."""
    values = read_counters()  # Read all values at once
    values[index] += 1  # Increment the specified counter
    write_counters(values)  # Write all values back to the file
    return values[index]

def decrement_counter(index):
    """Decrement the value of a specific counter (by index)."""
    values = read_counters()  # Read all values at once
    if values[index] > 0:  # Only decrement if the value is greater than 0
        values[index] -= 1
        
        write_counters(values)  # Write all values back to the file
    return True

def get_counter(index):
    """Get the value of a specific counter (by index)."""
    values = read_counters()  # Read all values at once
    return values[index]
