'''
This is the main file that will be executed to run the command line program for backing up emails from an IMAP server.
'''
import argparse
from backup_manager import BackupManager
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Email Backup Program')
    parser.add_argument('config_file', help='Path to the configuration file')
    args = parser.parse_args()
    # Create an instance of BackupManager and start the backup process
    backup_manager = BackupManager(args.config_file)
    backup_manager.backup_emails()
if __name__ == '__main__':
    main()