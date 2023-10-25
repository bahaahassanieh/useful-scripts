import re
import string

def generate_yara_rule(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Find printable strings in the file
    strings = re.findall(b'[%s]{4,}' % re.escape(bytes(string.printable, 'ascii')), data)
    strings = [s.decode('ascii') for s in strings]

    rule_name = "rule_" + file_path.replace('.', '_').replace('/', '_')

    # Generate YARA rule
    rule = f"rule {rule_name} {{\n"
    rule += "    strings:\n"
    for i, s in enumerate(strings, 1):
        rule += f"        $string{i} = \"{s}\"\n"
    rule += "    condition:\n"
    rule += "        " + " or ".join(f"$string{i}" for i in range(1, len(strings) + 1))
    rule += "\n}"

    return rule

# Get file path from the user
file_path = input("Enter the path to the file: ")

# Generate the YARA rule
yara_rule = generate_yara_rule(file_path)

# Append the YARA rule to the file
with open('yara_rules', 'a') as f:
    f.write(yara_rule + '\n\n')  # Adding two newlines for separation between rules
