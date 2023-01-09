# Open a file for writing
with open('myfile.txt', 'w') as f:
    # Write some text to the file
    f.write('Hello, world!')

# Open a file for reading
with open('myfile.txt', 'r') as f:
    # Read the contents of the file
    contents = f.read()
    print(contents)