import pandas as pd
from datetime import datetime, timedelta

def analyze_file(input_file):
    # Load the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Check if required columns exist
    required_columns = {'Employee Name', 'Position Status', 'Time', 'Time Out', 'Timecard Hours (as Time)'}
    if not required_columns.issubset(df.columns):
        missing_columns = required_columns - set(df.columns)
        print(f"Missing required columns: {missing_columns}")
        return

    # Convert 'Time' and 'Time Out' columns to datetime with AM/PM format
    df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M %p', errors='coerce')
    df['Time Out'] = pd.to_datetime(df['Time Out'], format='%m/%d/%Y %I:%M %p', errors='coerce')

    # Sort the DataFrame by employee name and date
    df.sort_values(by=['Employee Name', 'Time'], inplace=True)

    # Initialize variables for consecutive days and previous time_out
    consecutive_days_worked = 0
    prev_time_out = None

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        name = row['Employee Name']
        position_status = row['Position Status']
        time_in = row['Time']
        time_out = row['Time Out']

        # Check for 'NaT' values in time_in or time_out
        if pd.isna(time_in) or pd.isna(time_out):
            continue  # Skip this row if either time_in or time_out is missing

        # Calculate time between shifts
        if prev_time_out is not None:
            time_between_shifts = (time_in - prev_time_out).total_seconds() / 3600  # Convert seconds to hours
        else:
            time_between_shifts = None

        # Handle NaN values in 'Timecard Hours (as Time)'
        if pd.notna(row['Timecard Hours (as Time)']):
            hours_worked = row['Timecard Hours (as Time)'].split(':')
            hours_worked = int(hours_worked[0]) + int(hours_worked[1]) / 60  # Convert HH:mm to decimal hours
        else:
            # If 'Timecard Hours (as Time)' is NaN, set hours_worked to 0
            hours_worked = 0

        # Check conditions and print relevant information
        if consecutive_days_worked >= 7:
            print(f"Employee: {name}, Position: {position_status}, Worked for 7 consecutive days")
        if time_between_shifts is not None and 1 < time_between_shifts < 10:
            print(f"Employee: {name}, Position: {position_status}, Less than 10 hours between shifts")
        if hours_worked > 14:
            print(f"Employee: {name}, Position: {position_status}, Worked more than 14 hours in a single shift")

        # Update variables for the next iteration
        consecutive_days_worked = 0 if (time_out.date() - time_in.date()).days > 1 else consecutive_days_worked + 1
        prev_time_out = time_out

if __name__ == "__main__":
    input_file = r"C:\Users\parik\OneDrive\Desktop\pyhton\Assignment_Timecard.csv"
    analyze_file(input_file)
