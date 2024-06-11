
import os
class S3Sync:


    def sync_folder_to_s3(self,folder,aws_buket_url): #This will sync the required folders to s3 bucket from local(during development)/EC2(during production or depoyment). This will happen when training pipeline will be triggered(when data drift detected in real time or when triggered during development in local for experimentation)
        command = f"aws s3 sync {folder} {aws_buket_url} " #This is aws cli command where first attribute is source and second attribute is destination
        os.system(command) #To run the defined command inside terminal

    def sync_folder_from_s3(self,folder,aws_bucket_url): #This will sync required folders from s3 bucket(eg; during real time inferencing we will be requring the base models stored in s3 bucket)
        command = f"aws s3 sync  {aws_buket_url} {folder} "
        os.system(command)




