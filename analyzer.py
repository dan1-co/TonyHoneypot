import pandas as pd
import json

def analyze_logs(log_file='honeypot.log'):
    """Analyze honeypot logs and display summary."""
    logs = []

    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    # Try to extract JSON from log line
                    json_str = line.split(' - ', 1)[1].strip()
                    log_entry = json.loads(json_str)
                    logs.append(log_entry)
                except (IndexError, json.JSONDecodeError):
                    continue  # Skip malformed lines

        if not logs:
            print("No valid log entries found.")
            return

        # Convert list of logs to DataFrame
        df = pd.DataFrame(logs)

        print("\n=== TonyHoneypot Log Analysis ===")
        print(f"Total Connections: {len(df)}")

        if 'ip' in df.columns:
            print("\nTop 5 Source IPs:")
            print(df['ip'].value_counts().head())
        else:
            print("\nNo 'ip' field found in logs.")

        # Display most recent 5 connections (only if required columns exist)
        print("\nMost Recent 5 Connections:")
        cols_to_show = [col for col in ['timestamp', 'ip', 'data'] if col in df.columns]
        if cols_to_show:
            print(df[cols_to_show].tail())
        else:
            print("Required columns for recent connections not found.")

    except FileNotFoundError:
        print(f"Log file '{log_file}' not found.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    analyze_logs()
