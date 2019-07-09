# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from galaxy.models import GalaxyInstanceTracking, GalaxyUser
from misa.utils.isa_upload import upload_assay_data_files_dir
from misa.forms import UploadAssayDataFilesForm

def example_setup():
    print('Starting setup')
    # create superuser
    user = User.objects.create_user('admin', password='admin')
    user.is_superuser = True
    user.is_staff = True
    user.save()


    # Add Galaxy Instance (W4M local)
    git = GalaxyInstanceTracking(url='http://127.0.0.1:8080/',
                                 name='docker-galaxy',
                                 ftp_host='127.0.0.1',
                                 galaxy_root_path='/home/tomnl/galaxy_storage3',
                                 ftp_port='8021')
    git.save()

    # Add Galaxy user
    gu = GalaxyUser(internal_user=user,
                    email='admin@galaxy.org',
                    api_key='69036d683598cf92085b50ab6e53029b',
                    galaxyinstancetracking=git)

    gu.save()
