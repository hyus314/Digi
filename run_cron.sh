#!/bin/bash

# Check if mysqlclient is installed
if ! python -c "import MySQLdb" 2>/dev/null; then
    echo "mysqlclient is not installed, installing..."
    pip install mysqlclient
fi

# Run the management command and redirect output to log file
cd /mnt/c/MyPrograms/Projects/Digi/project && python3 manage.py delete_expired_tokens >> /mnt/c/MyPrograms/Projects/Digi/project/log.txt 2>&1
