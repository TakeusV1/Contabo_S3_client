import boto3, os
from pathlib import Path
from config import *

s3 = boto3.client("s3",endpoint_url=endpoint_url,aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)

def upload_file(path:str) -> str:
    if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        
    path = Path(path).absolute().as_posix()
    s3.upload_file(path, bucket_name, str(path.split('/')[-1]))
    return f'\nFile Uploaded !\nLink : {sharing_link+'/'+str(path.split('/')[-1])}'

def delete_file(filename:str) -> str:
    s3.delete_object(Bucket=bucket_name,Key=filename)
    return f'\nFile {filename} deleted !'

while True:
    os.system('cls')
    print("#######################\n## Contabo S3 Client ##\n#######################\n\n1 - Upload\n2 - Delete\n3 - List Files\n")
    menu = input("> ")
    
    if str(menu) == '1':
        os.system('cls')
        path = str(input('enter file path > '))
        print(upload_file(path))
        input('\n(Return) > ')
    
    elif str(menu) == '2':
        os.system('cls')
        
        files = s3.list_objects_v2(Bucket=bucket_name,Delimiter = "/")
        file_list = {}
        file_id = 0
        for key in files['Contents']:
            file_id += 1
            file_list[file_id] = key['Key']
            print(f'- ID : {file_id} | {key['Key']}')
        
        print(f"\nObject(s) = {len(file_list)}")
        
        ask = input('(ID) > ')
        
        try:
            if int(ask) not in file_list:
                print('\nFile NOT FOUND')
            else:        
                print(delete_file(file_list[int(ask)]))
            input('\n(Return) > ')
        except:
            pass    
    
    elif str(menu) == '3':
        os.system('cls')
        
        files = s3.list_objects_v2(Bucket=bucket_name,Delimiter = "/")
        for key in files['Contents']:
            print(f'- {key['Key']} | Date : {str(key['LastModified']).split('.')[0]} | Size : {round(float(key['Size'])/(1024 * 1024),2)} MO')

        input('\n(Return) > ')
    else:
        break
