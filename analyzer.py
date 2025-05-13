import pandas as pd
import json

def analyze_logs(log_file='honeypot.log'):
    """Analyze honeypot logs and display summary."""
    logs = []
    try:
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    json_str = line.split(' - ', 1)[1].strip()
                    log_entry = json.loads(json_str)
                    logs.append(log_entry)
                except:
                    continue
        if not logs:
            print("No valid log entries found.")
            return

        df = pd.DataFrame(logs)
        print("\n=== TonyHoneypot Log Analysis ===")
        print(f"Total Connections: {len(df)}")
        print("\nTop 5 Source IPs:")
        print(df['ip'].value_counts().head())
        print("\nMost Recent 5 Connections:")
        print(df[['timestamp', 'ip', 'captured_port', 'data']].tail())
    except FileNotFoundError:
        print(f"Log file {log_file} not found.")
    except Exception as e:
        print(f"Error analyzing logs: {str(e)}")

if __name__ == "__main__":
    analyze_logs()
