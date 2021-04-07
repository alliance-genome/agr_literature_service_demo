import time
import urllib
import argparse

import re
import requests

import os
from os import environ, path
import logging
import logging.config
import glob

from dotenv import load_dotenv

load_dotenv()


# python get_pubmed_xml.py -f /home/azurebrd/git/agr_literature_service_demo/src/xml_processing/inputs/alliance_pmids
# python get_pubmed_xml.py -f /home/azurebrd/git/agr_literature_service_demo/src/xml_processing/inputs/sample_set
# python get_pubmed_xml.py -f /home/azurebrd/git/agr_literature_service_demo/src/xml_processing/inputs/wormbase_pmids

# pipenv run python get_pubmed_xml.py -u "http://tazendra.caltech.edu/~azurebrd/cgi-bin/forms/generic.cgi?action=ListPmids"

# 1 hour 42 minutes to copy 646721 xml files / 12 G / 12466408 to s3 with
#  aws s3 cp pubmed_xml/ s3://agr-literature/develop/reference/metadata/pubmed/xml/ --recursive

# 1 hour 0 minutes 26 seconds to skip through files already in filesystem in agr-lit-dev, vs 2 minutes at dev.wormbase

# webenv
# https://www.ncbi.nlm.nih.gov/books/NBK25498/#chapter3.Application_3_Retrieving_large

# try using post like (works with 5000 in perl)
# https://www.ncbi.nlm.nih.gov/books/NBK25498/#chapter3.Application_4_Finding_unique_se


# Need to set up a queue that queries postgres to get a list of pubmed id that don't have a pubmed final flag
# Need to set up an S3 bucket to store xml
# Need to set up flags to take in pmids from postgres queue, file in filesystem, file in URL, list from command line

# to get set of pmids with search term 'elegans'
# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=elegans&retmax=100000000


log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('literature logger')


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--commandline', nargs='*', action='store', help='take input from command line flag')
parser.add_argument('-d', '--database', action='store_true', help='take input from database query')
parser.add_argument('-f', '--file', action='store', help='take input from entries in file with full path')
parser.add_argument('-r', '--restapi', action='store', help='take input from rest api')
parser.add_argument('-s', '--sample', action='store_true', help='test sample input from hardcoded entries')
parser.add_argument('-u', '--url', action='store', help='take input from entries in file at url')

args = vars(parser.parse_args())

# todo: save this in an env variable
# base_path = '/home/azurebrd/git/agr_literature_service_demo/src/xml_processing/'
base_path = environ.get('XML_PATH')
storage_path = base_path + 'pubmed_xml/'


def download_pubmed_xml(pmids_wanted):
    # 4.5 minutes to download 28994 wormbase records in 10000 chunks
    # 61 minutes to download 429899 alliance records in 10000 chunks
    # 127 minutes to download 646714 alliance records in 5000 chunks, failed on 280
    pmids_slice_size = 5000

    # comparing through a set instead of a list takes 2.6 seconds instead of 4256
    pmids_found = set()

    # this section reads pubmed xml files already acquired to skip downloading them.
    # to get full set, clear out storage_path, or comment out this section
    logger.info("Reading PubMed XML previously acquired")
    full_path_pmid_xml = glob.glob(storage_path + "*.xml")
    pmids_wanted_set = set(pmids_wanted)
    for elem in full_path_pmid_xml:
        elem = elem.replace(storage_path, '')
        elem = elem.replace('.xml', '')
        if elem in pmids_wanted_set:
            pmids_wanted_set.remove(elem)
    pmids_wanted = sorted(list(pmids_wanted_set))

#     for pmid in pmids_wanted:
#         print(pmid)

    logger.info("Starting download of new PubMed XML")

    for index in range(0, len(pmids_wanted), pmids_slice_size):
        pmids_slice = pmids_wanted[index:index + pmids_slice_size]
        pmids_joined = (',').join(pmids_slice)
        logger.debug("processing PMIDs %s", pmids_joined)

#         https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=10074449&retmode=xml

#         default way without a library, using get
#         url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=" + pmids_joined + "&retmode=xml"
#         print url
#         f = urllib.urlopen(url)
#         xml_all = f.read()

#         using post with requests library, works well for 10000 pmids
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        parameters = {'db': 'pubmed', 'retmode': 'xml', 'id': pmids_joined}
        r = requests.post(url, data=parameters)
        xml_all = r.text
#         xml_all = r.text.encode('utf-8').strip()		# python2
        xml_split = xml_all.split("\n<Pubmed")		# some types are not PubmedArticle, like PubmedBookArticle, e.g. 32644453

        header = xml_split.pop(0)
        header = header + "\n<Pubmed" + xml_split.pop(0)
        footer = "\n\n</PubmedArticleSet>"

        for n in range(len(xml_split)):
            xml_split[n] = header + "\n<Pubmed" + xml_split[n]
            xml_split[n] = os.linesep.join([s for s in xml_split[n].splitlines() if s])

        for n in range(len(xml_split) - 1):
            xml_split[n] += footer

        for xml in xml_split:
            if re.search(r"<PMID[^>]*?>(\d+)</PMID>", xml):
                pmid_group = re.search(r"<PMID[^>]*?>(\d+)</PMID>", xml)
                pmid = pmid_group.group(1)
                pmids_found.add(pmid)
                filename = storage_path + pmid + '.xml'
                f = open(filename, "w")
                f.write(xml)
                f.close()

        if len(pmids_slice) == pmids_slice_size:
            logger.info("waiting to process more pmids")
            time.sleep(5)

    logger.info("Writing log of pmids_not_found")
    output_pmids_not_found_file = base_path + 'pmids_not_found'
    with open(output_pmids_not_found_file, "w") as pmids_not_found_file:
        for pmid in pmids_wanted:
            if pmid not in pmids_found:
                pmids_not_found_file.write("%s\n" % (pmid))
                logger.info("PMID %s not found in pubmed query", pmid)
        pmids_not_found_file.close()

    logger.info("Getting PubMed XML complete")


# to process one by one
#   for pmid in pmids_wanted:
# #    add some validation here
#     url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=" + pmid + "&retmode=xml"
#     filename = storage_path + pmid + '.xml'
# #     print url
# #     print filename
#     logger.info("Downloading %s into %s", url, filename)
#     urllib.urlretrieve(url, filename)
#     time.sleep( 5 )


if __name__ == "__main__":
    """ call main start function """
    pmids_wanted = []

#    python get_pubmed_xml.py -d
    if args['database']:
        logger.info("Processing database entries")

    elif args['restapi']:
        logger.info("Processing rest api entries")

#     python get_pubmed_xml.py -f /home/azurebrd/git/agr_literature_service_demo/src/xml_processing/inputs/pmid_file.txt
    elif args['file']:
        logger.info("Processing file input from %s", args['file'])
        with open(args['file'], 'r') as fp:
            pmid = fp.readline()
            while pmid:
                pmids_wanted.append(pmid.rstrip())
                pmid = fp.readline()

#     python get_pubmed_xml.py -u http://tazendra.caltech.edu/~azurebrd/var/work/pmid_sample
    elif args['url']:
        logger.info("Processing url input from %s", args['url'])
        req = urllib.request.urlopen(args['url'])
        data = req.read()
        lines = data.splitlines()
        for pmid in lines:
            pmids_wanted.append(str(int(pmid)))

#    python get_pubmed_xml.py -c 1234 4576 1828
    elif args['commandline']:
        logger.info("Processing commandline input")
        for pmid in args['commandline']:
            pmids_wanted.append(pmid)

#    python get_pubmed_xml.py -s
    elif args['sample']:
        logger.info("Processing hardcoded sample input")
        pmid = '12345678'
        pmids_wanted.append(pmid)
        pmid = '12345679'
        pmids_wanted.append(pmid)
        pmid = '12345680'
        pmids_wanted.append(pmid)

    else:
        logger.info("Processing database entries")

    download_pubmed_xml(pmids_wanted)
