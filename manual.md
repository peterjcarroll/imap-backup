# Email Backup Program User Manual

## Introduction

The Email Backup Program is a command line program written in Python that allows you to periodically backup emails from an IMAP server. The program creates a backup of the emails in a specified directory, which can be searched at a later date. The program is configured using a text file, and it ensures that it does not overwrite emails that have already been backed up.

## Installation

To use the Email Backup Program, you need to have Python installed on your system. You can download Python from the official website: https://www.python.org/downloads/

Once Python is installed, you can install the required dependencies by running the following command in your terminal:

```
pip install -r requirements.txt
```

## Configuration

Before running the Email Backup Program, you need to configure it using a text file. The configuration file is in INI format and contains the following sections:

### IMAP

- `server`: The IMAP server address.
- `username`: Your IMAP server username.
- `password`: Your IMAP server password.

### Backup

- `directory`: The directory where the backup files will be stored.
- `database_file`: The path to the SQLite database file used to track the backed up emails.

You can edit the `config.ini` file to set the appropriate values for your IMAP server and backup directory.

## Running the Program

To run the Email Backup Program, open your terminal and navigate to the directory where the program files are located. Then, run the following command:

```
python main.py config.ini
```

Replace `config.ini` with the path to your configuration file.

The program will connect to the IMAP server, backup the emails, and store them in the specified backup directory. It will also update the SQLite database to keep track of the backed up emails.

You can schedule the program to run periodically using a task scheduler or a cron job.

## Conclusion

The Email Backup Program provides a convenient way to backup emails from an IMAP server and store them in a searchable format. By following the instructions in this user manual, you can easily configure and run the program to ensure that your emails are backed up regularly.