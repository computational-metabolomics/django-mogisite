# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from mbrowse.models import Compound
from misa.models import Organism, StudySample, StudySample, SampleType
from dma.models import Dma
from dma.utils.initdma import create_investigation_study
from dma.utils.assaymapping import map_assays_to_directories
from galaxy.models import GalaxyInstanceTracking, GalaxyUser
import csv
import os

def example_setup(mysql_user, mysql_password):
    print 'Starting setup'
    # create superuser
    assay_mapping_test_pth = '/home/tomnl/code/django-dma/dma/tests/assay_mapping.csv'
    compound_sql_pth = '/home/tomnl/Dropbox/compounds_and_spectra01Jun2018.sql'
    user = User.objects.create_user('tnl495', password='mogi123')
    user.is_superuser = True
    user.is_staff = True
    user.save()


    # create DMA study (with compound)
    dma = Dma.objects.create(name='Daphnia magna', organism=Organism.objects.get(name='Daphnia magna'))
    dma.save()
    sts = SampleType.objects.all()
    investigation, study = create_investigation_study(name=dma.name, description=dma.description)
    ss = StudySample.objects.create(study=study, sample_name='ANIMAL', sampletype=sts[0])
    ss.save()
    ss = StudySample.objects.create(study=study, sample_name='BLANK', sampletype=sts[1])
    ss.save()
    StudySample.objects.create(study=study, sample_name='COMPOUND', sampletype=sts[2])
    ss.save()

    # add assays via file (e.g. batch upload of files)
    with open(assay_mapping_test_pth, 'rb') as assay_mapping_file:
        reader = csv.DictReader(assay_mapping_file)
        assay_mapping = [row for row in reader]

    map_assays_to_directories(assay_mapping, user.id, study.id, '')

    # Add Galaxy Instance (W4M local)

    git = GalaxyInstanceTracking(url = 'http://127.0.0.1:8080/',
                           name = 'W4M docker',
                           ftp_host = '127.0.0.1',
                           ftp_port = '8021')

    git.save()

    # Add Galaxy user
    gu = GalaxyUser(user = user,
               email = 'thomas.nigel.lawson@gmail.com',
               api_key = '7e51b04d6072de7856eb67ec6b751580',
               galaxyinstancetracking = git)

    gu.save()

    # Add compounds
    cmd = 'mysql -h localhost -u {} --password={} mogi < {}'.format(mysql_user, mysql_password, compound_sql_pth)
    print cmd
    os.system(cmd)
