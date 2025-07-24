# Define your parameters
a = 8.37e+26
b = -27.01
c = -0.04

# Define your input x
pH = 8.6  # Replace this with your desired x value

# Compute the value of the function
ratio = a * (pH ** b) + c

print(f"The ratio of NaHCO3 to Na2CO3 at pH = {pH} is {ratio} to 1")
