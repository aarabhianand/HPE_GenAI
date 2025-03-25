import os
from datetime import datetime
import threading

class Logger:
    def __init__(self, port, data_dir):
        self.port = port
        self.data_dir = data_dir
        self.local_log_file = os.path.join(data_dir, f"logs_{port}.txt")
        self.global_log_file = "global_logs.txt"
        self.lock = threading.Lock()  # Thread-safe logging

        # Create log files if they don't exist
        for file in [self.local_log_file, self.global_log_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    f.write('')

    def _get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _write_log(self, file_path, message, prefix=""):
        with self.lock:
            with open(file_path, 'a') as f:
                f.write(f"{prefix}{message}\n")

    def info(self, message, global_log=False):
        timestamp = self._get_timestamp()
        local_entry = f"[{timestamp}][INFO] {message}"
        self._write_log(self.local_log_file, local_entry)

        if global_log:
            global_entry = f"[PORT {self.port}][{timestamp}][INFO] {message}"
            self._write_log(self.global_log_file, global_entry)

    def warn(self, message, global_log=False):
        timestamp = self._get_timestamp()
        local_entry = f"[{timestamp}][WARN] {message}"
        self._write_log(self.local_log_file, local_entry)

        if global_log:
            global_entry = f"[PORT {self.port}][{timestamp}][WARN] {message}"
            self._write_log(self.global_log_file, global_entry)

    def error(self, message, global_log=False):
        timestamp = self._get_timestamp()
        local_entry = f"[{timestamp}][ERROR] {message}"
        self._write_log(self.local_log_file, local_entry)

        if global_log:
            global_entry = f"[PORT {self.port}][{timestamp}][ERROR] {message}"
            self._write_log(self.global_log_file, global_entry)

    def cleanup_log(self, message):
        """
        Special logging for cleanup events.
        """
        timestamp = self._get_timestamp()
        log_entry = f"[{timestamp}][CLEANUP] {message}"
        self._write_log(self.local_log_file, log_entry)
        self._write_log(self.global_log_file, log_entry)


    def get_local_logs(self, last_n_lines=100):
        try:
            with open(self.local_log_file, 'r') as f:
                lines = f.readlines()
                return lines[-last_n_lines:]  # Return last N lines
        except Exception as e:
            return [f"Error reading logs: {str(e)}"]

    def get_global_logs(self, last_n_lines=100):
        try:
            with open(self.global_log_file, 'r') as f:
                lines = f.readlines()
                return lines[-last_n_lines:]  # Return last N lines
        except Exception as e:
            return [f"Error reading logs: {str(e)}"] 