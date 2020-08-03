from documentcloud import DocumentCloud
import logging
from glob import glob
import os.path
from os.path import join
import sys
import re
import shutil
from shutil import copyfile
from datetime import datetime
import getpass

USERNAME=input('Public DocumentCloud (beta) User email: ')
PASSWORD=getpass.getpass()

PROJECT_NAME=input('Documentcloud (beta) Project Name: ')
LOCAL_PATH=input('Document Dump Directory on your Mac (full path to the documents you wish to upload to documentcloud)? ')
PDF_UPLOAD=input('Location on your Mac where you will store the processed pdf files (this should not be the document dump directory) ')
LIBRE_OFFICE_LOCATION='/Applications/LibreOffice.app/Contents/MacOS/soffice'

timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
ERROR_LOG_PATH=f'./logs/error-{timestamp}.log'

import os
try:
    os.mkdir('./logs')
except FileExistsError:
    pass
   
try:
    os.mkdir(PDF_UPLOAD)
except FileExistsError:
    pass

error_log = open(ERROR_LOG_PATH, 'w')

def convert_word_doc(output_directory, files_to_be_processed):
    os.system(f"{LIBRE_OFFICE_LOCATION} --headless --invisible  --norestore --nolockcheck --convert-to pdf --outdir '{output_directory}' '{files_to_be_processed}'")
    convert_file_path, convert_filename = os.path.split(files_to_be_processed)
    extension = os.path.splitext(files_to_be_processed)[1]

def copy_file_for_upload(file_to_move, location_of_moved_files):
    copyfile(file_to_move, location_of_moved_files)

def prepare_files(PDF_UPLOAD):
    all_files = glob(join(LOCAL_PATH, '*'), recursive=True)

    word_files = []
    pdf_files = []
    other_files = []
    try:
        for file_to_process in all_files:
            extension = os.path.splitext(file_to_process)[1]
            if extension in ('.doc', '.docx', '.docm', '.docx'):
                word_files.append(file_to_process)
            elif extension.startswith('.pdf'):
                pdf_files.append(file_to_process)
            else:
                other_files.append(file_to_process)

        print(f'UNABLE TO UPLOAD THE FOLLOWING FILES, because we only support PDF and Word files:')
        print('\n'.join(other_files))

        for file_to_process in word_files:
            path, filename = os.path.split(file_to_process)
            print(f'Converting {filename} to PDF\n')
            convert_word_doc(PDF_UPLOAD, file_to_process)

        for file_to_process in pdf_files:
            path, filename = os.path.split(file_to_process)
            print(f'Copying {filename} to upload directory\n')
            copy_file_for_upload(file_to_process, f'{PDF_UPLOAD}/{filename}')
    except Exception as e:
        exc_type, value, traceback = sys.exc_info()
        print(f'Error converting {file_to_process}: {exc_type.__name__}: {value}')
        error_log.write(f'{file_to_process}\n')

def batch_upload_files(project_name, files_to_batch):
    if not files_to_batch:
        print('No files available to upload')
        return
    # Connect to documentcloud
    client = DocumentCloud(USERNAME, PASSWORD, loglevel=logging.INFO, timeout=30) #logging.INFO
    # Create the project
    project, created = client.projects.get_or_create_by_title(project_name)
    # Upload all the pdfs
    obj_list = client.documents.upload_directory(files_to_batch, handle_errors=True, project=project.id)

##TODO FUNCTION SINGLE DOCUMENT UPLOAD TO DOCUMENTCLOUD (may not be used)
def upload_file(project_name, file_to_upload):
    client = DocumentCloud(USERNAME, PASSWORD, loglevel=logging.INFO, timeout=30)
    project, created = client.projects.get_or_create_by_title(project_name)
    obj = client.documents.upload(file_to_upload, handle_errors=True, project=project.id)

prepare_files(PDF_UPLOAD)
batch_upload_files(PROJECT_NAME, PDF_UPLOAD)
