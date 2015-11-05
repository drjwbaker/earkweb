__author__ = 'jan'

import os
from earkcore.metadata.mets.MetsManipulate import Mets
from earkcore.metadata.premis.PremisManipulate import Premis
from earkcore.metadata.identification import MetaIdentification
from config.config import root_dir
from earkcore.fixity.ChecksumAlgorithm import ChecksumAlgorithm


def filescan(path, mets, premis, tl):
    '''
    This function scans a directory for every file inside,
    and adds it to the submission METS/PREMIS.

    @return:    mets (METS file object updated with AIP content)
    @return:    premis (PREMIS file object updated with AIP content)
    '''

    # Add METS file groups
    mets.add_file_grp(['submission'])
    mets.add_file_grp(['schemas'])
    mets.add_file_grp(['customMD'])

    # path length
    # TODO: retrieve from somewhere
    workdir_length = len(path) - len('/submission')

    # Known metadata formats.
    # TODO: expand list of known meta data formats
    #md_type_list = {'ead': 'techMD',
    #                'eac-cpf': 'dmdSec',
    #                'premis': 'techMD'}

    # TODO: admids - correct relative path to PREMIS
    admids = []
    admids.append(mets.add_tech_md('file://./metadata/PREMIS.xml#Obj'))
    admids.append(mets.add_digiprov_md('file://./metadata/PREMIS.xml#Ingest'))
    admids.append(mets.add_rights_md('file://./metadata/PREMIS.xml#Right'))

    # TODO: new version: refer/link SIP METS

    # meta data
    for directory, subdirectory, filenames in os.walk(os.path.join(path, 'metadata')):
    # for directory, subdirectory, filenames in os.walk(path):
        for filename in filenames:
            rel_path_file = ('file://.' + directory[workdir_length:] + '/' + filename).decode('utf-8')
            if directory[-11:] == 'descriptive':
                # get xml type from the xml file (xml_tag will be 'ead', 'premis' etc.)
                xml_tag = MetaIdentification.MetaIdentification(os.path.join(directory, filename))
                mets.add_dmd_sec(xml_tag, rel_path_file)
                premis.add_object(rel_path_file)
            elif directory[-12:] == 'preservation':
                mets.add_tech_md(rel_path_file, admids)
                premis.add_object(rel_path_file)
            elif directory[-5:] == 'other':
                mets.add_file(['customMD'], rel_path_file, admids)
                premis.add_object(rel_path_file)
            elif directory[-7:] == 'schemas':
                mets.add_file(['schemas'], rel_path_file, admids)
                premis.add_object(rel_path_file)

    # content
    # TODO: fix SIP restructuring + path here! 'rep-000'
    # TODO: second representation? -> after file format migration
    for directory, subdirectory, filenames in os.walk(os.path.join(path, 'representations/rep-001')):
        for filename in filenames:
            rel_path_file = ('file://.' + directory[workdir_length:] + '/' + filename).decode('utf-8')
            mets.add_file(['submission'], rel_path_file, admids)
            premis.add_object(rel_path_file)

    return mets, premis


def main():
    ip_work_dir = '/var/data/earkweb/work/01bf885e-806e-42fb-a1aa-1e59fa668e02'

    # create submission METS
    mets_skeleton_file = root_dir + '/earkresources/METS_skeleton.xml'
    with open(mets_skeleton_file, 'r') as mets_file:
        submission_mets_file = Mets(wd=ip_work_dir, alg=ChecksumAlgorithm.SHA256)

    # create PREMIS
    premis_skeleton_file = root_dir + '/earkresources/PREMIS_skeleton.xml'
    with open(premis_skeleton_file, 'r') as premis_file:
        package_premis_file = Premis(premis_file)
    package_premis_file.add_agent('eark-aip-creation')

    # scan package, update METS and PREMIS
    aip_mets, aip_premis = filescan('/var/data/earkweb/work/01bf885e-806e-42fb-a1aa-1e59fa668e02/submission', submission_mets_file, package_premis_file)

    # print aip_mets
    # print aip_premis


if __name__ == '__main__':
    main()