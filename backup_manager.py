'''
This file contains the BackupManager class responsible for managing the backup process.
'''
import imaplib
import os
import configparser
import sqlite3
class BackupManager:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.db_file = self.config['Backup']['database_file']
        self.create_database()
    def create_database(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS backed_up_emails
                     (email_id TEXT, folder TEXT)''')
        conn.commit()
        conn.close()
    def backup_emails(self):
        # Connect to the IMAP server
        imap_server = imaplib.IMAP4_SSL(self.config['IMAP']['server'])
        imap_server.login(self.config['IMAP']['username'], self.config['IMAP']['password'])
        imap_server.select()
        # Get the list of folders
        _, folder_list = imap_server.list()
        folders = [folder.decode().split(' "/" ')[1] for folder in folder_list]
        # Create a backup directory if it doesn't exist
        backup_dir = self.config['Backup']['directory']
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        # Iterate over the folders and backup emails
        for folder in folders:
            self.backup_folder(imap_server, folder, backup_dir)
        # Logout from the IMAP server
        imap_server.logout()
    def backup_folder(self, imap_server, folder, backup_dir):
        # Select the folder
        imap_server.select(folder)
        # Get the list of emails in the folder
        _, email_ids = imap_server.search(None, 'ALL')
        email_ids = email_ids[0].split()
        # Create a folder in the backup directory for the current folder
        folder_dir = os.path.join(backup_dir, folder)
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        # Iterate over the emails and backup if not already backed up
        for email_id in email_ids:
            if self.is_email_backed_up(email_id, folder):
                continue
            email_filename = os.path.join(folder_dir, f"{email_id}.eml")
            _, email_data = imap_server.fetch(email_id, '(RFC822)')
            with open(email_filename, 'wb') as f:
                f.write(email_data[0][1])
            self.mark_email_as_backed_up(email_id, folder)
    def is_email_backed_up(self, email_id, folder):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT email_id FROM backed_up_emails WHERE email_id=? AND folder=?", (email_id, folder))
        result = c.fetchone()
        conn.close()
        return result is not None
    def mark_email_as_backed_up(self, email_id, folder):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO backed_up_emails (email_id, folder) VALUES (?, ?)", (email_id, folder))
        conn.commit()
        conn.close()