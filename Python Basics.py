import random  # Import random module to generate random numbers

# Step 1: Create a list of 100 random integers between 0 and 1000
numbers = [random.randint(0, 1000) for _ in range(100)]  # List comprehension to generate random numbers

# Step 2: Sort the list from min to max manually (without using sort() or sorted())
# We'll use a simple algorithm called Bubble Sort
for i in range(len(numbers)):
    for j in range(0, len(numbers) - i - 1):
        if numbers[j] > numbers[j + 1]:  # Compare adjacent elements
            # Swap if the element found is greater than the next element
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

# Step 3: Separate even and odd numbers into different lists
even_numbers = [num for num in numbers if num % 2 == 0]  # Even numbers are divisible by 2
odd_numbers = [num for num in numbers if num % 2 != 0]   # Odd numbers are not divisible by 2

# Step 4: Calculate the average (mean) for each list
# We use sum() / len() formula, but first we check that list is not empty to avoid ZeroDivisionError
avg_even = sum(even_numbers) / len(even_numbers) if even_numbers else 0
avg_odd = sum(odd_numbers) / len(odd_numbers) if odd_numbers else 0

# Step 5: Print the results to console
print("Sorted numbers:", numbers)
print("Average of even numbers:", avg_even)
print("Average of odd numbers:", avg_odd)
