# 1. Import necessary libraries (csv, datetime)
# 2. Define function to load tasks from CSV file
#    - Open CSV file in read mode
#    - Create CSV reader object
#    - Parse each row into a task dictionary
#    - Return list of task dictionaries
# 3. Define function to save tasks to CSV file
#    - Open CSV file in write mode
#    - Create CSV writer object
#    - Write header row
#    - Write each task as a row
# 4. Define function to add a task
#    - Take task description, due date, priority
#    - Create new task dictionary
#    - Add to task list
#    - Save updated list to CSV
# 5. Define function to mark task as complete
#    - Take task index
#    - Update task status
#    - Save updated list to CSV
# 6. Define function to list all tasks
#    - Loop through task list
#    - Format and print each task
# 7. Main program:
#    - Load existing tasks
#    - Display menu of options
#    - Handle user input for various operations
#    - Repeat until user chooses to exit

# Libraries:

# csv: For reading/writing CSV files
# datetime: For handling task due dates

# Implementation Notes:

# Store tasks in a CSV with columns for description, due date, priority, status
# Add sorting and filtering capabilities (e.g., by priority, due date)
