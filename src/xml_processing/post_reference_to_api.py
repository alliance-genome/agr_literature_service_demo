
import json
import requests
import argparse
import re
from os import environ, path, listdir
import logging
import logging.config

from helper_post_to_api import generate_headers, update_token

# post to api data from sanitized_reference_json/
# python post_reference_to_api.py
#
# update auth0_token only
# python post_reference_to_api.py -a


log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logging.conf')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('literature logger')

# base_path = '/home/azurebrd/git/agr_literature_service_demo/src/xml_processing/'
base_path = environ.get('XML_PATH')

auth0_file = base_path + 'auth0_token'

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--authorization', action='store_true', help='update authorization token')
args = vars(parser.parse_args())

# keys that exist in data
# 2021-05-25 21:16:53,372 - literature logger - INFO - key abstract
# 2021-05-25 21:16:53,372 - literature logger - INFO - key citation
# 2021-05-25 21:16:53,372 - literature logger - INFO - key datePublished
# 2021-05-25 21:16:53,373 - literature logger - INFO - key dateArrivedInPubmed
# 2021-05-25 21:16:53,373 - literature logger - INFO - key dateLastModified
# 2021-05-25 21:16:53,373 - literature logger - INFO - key keywords
# 2021-05-25 21:16:53,373 - literature logger - INFO - key crossReferences
# 2021-05-25 21:16:53,373 - literature logger - INFO - key title
# 2021-05-25 21:16:53,373 - literature logger - INFO - key tags
# 2021-05-25 21:16:53,373 - literature logger - INFO - key issueName
# 2021-05-25 21:16:53,373 - literature logger - INFO - key issueDate
# 2021-05-25 21:16:53,373 - literature logger - INFO - key MODReferenceType
# 2021-05-25 21:16:53,373 - literature logger - INFO - key pubMedType
# 2021-05-25 21:16:53,373 - literature logger - INFO - key meshTerms
# 2021-05-25 21:16:53,373 - literature logger - INFO - key allianceCategory
# 2021-05-25 21:16:53,373 - literature logger - INFO - key volume
# 2021-05-25 21:16:53,373 - literature logger - INFO - key authors
# 2021-05-25 21:16:53,373 - literature logger - INFO - key pages
# 2021-05-25 21:16:53,373 - literature logger - INFO - key publisher
# 2021-05-25 21:16:53,373 - literature logger - INFO - key resource
# 2021-05-25 21:16:53,373 - literature logger - INFO - key language
# 2021-05-25 21:16:53,373 - literature logger - INFO - key modResources
# 2021-05-25 21:16:53,373 - literature logger - INFO - key MODReferenceTypes
# 2021-05-25 21:16:53,373 - literature logger - INFO - key resourceAbbreviation


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def post_references():
    json_storage_path = base_path + 'sanitized_reference_json/'

    files_to_process = []
    dir_list = listdir(json_storage_path)
    for filename in dir_list:
        # logger.info("%s", filename)
        if 'REFERENCE_' in filename and '.REFERENCE_' not in filename:
            # logger.info("%s", filename)
            files_to_process.append(json_storage_path + filename)

    keys_to_remove = {'nlm', 'primaryId', 'modResources', 'resourceAbbreviation'}
    remap_keys = dict()
    remap_keys['datePublished'] = 'date_published'
    remap_keys['dateArrivedInPubmed'] = 'date_arrived_in_pubmed'
    remap_keys['dateLastModified'] = 'date_last_modified'
    remap_keys['crossReferences'] = 'cross_references'
    remap_keys['issueName'] = 'issue_name'
    remap_keys['issueDate'] = 'issue_date'
    remap_keys['pubMedType'] = 'pubmed_type'
    remap_keys['meshTerms'] = 'mesh_terms'
    remap_keys['allianceCategory'] = 'category'
    remap_keys['MODReferenceType'] = 'mod_reference_types'
    remap_keys['MODReferenceTypes'] = 'mod_reference_types'
    remap_keys['plainLanguageAbstract'] = 'plain_language_abstract'
    remap_keys['pubmedAbstractLanguages'] = 'pubmed_abstract_languages'

    subkeys_to_remove = dict()
    remap_subkeys = dict()

    subkeys_to_remove['mesh_terms'] = {'referenceId'}
    subkeys_to_remove['tags'] = {'referenceId'}
    subkeys_to_remove['authors'] = {'referenceId', 'firstinit', 'firstInit', 'crossReferences', 'collectivename'}

    remap_subkeys['mesh_terms'] = dict()
    remap_subkeys['mesh_terms']['meshHeadingTerm'] = 'heading_term'
    remap_subkeys['mesh_terms']['meshQualfierTerm'] = 'qualifier_term'
    remap_subkeys['mesh_terms']['meshQualifierTerm'] = 'qualifier_term'

    remap_subkeys['mod_reference_types'] = dict()
    remap_subkeys['mod_reference_types']['referenceType'] = 'reference_type'

    remap_subkeys['tags'] = dict()
    remap_subkeys['tags']['tagName'] = 'tag_name'
    remap_subkeys['tags']['tagSource'] = 'tag_source'

    remap_subkeys['cross_references'] = dict()
    remap_subkeys['cross_references']['id'] = 'curie'

    remap_subkeys['authors'] = dict()
    remap_subkeys['authors']['authorRank'] = 'order'
    remap_subkeys['authors']['firstName'] = 'first_name'
    remap_subkeys['authors']['lastName'] = 'last_name'
    remap_subkeys['authors']['middleNames'] = 'middle_names'
    remap_subkeys['authors']['firstname'] = 'first_name'
    remap_subkeys['authors']['lastname'] = 'last_name'
    remap_subkeys['authors']['middlenames'] = 'middle_names'

    keys_found = set()

    token = ''
    if path.isfile(auth0_file):
        with open(auth0_file, 'r') as auth0_fh:
            token = auth0_fh.read().replace("\n", "")
            auth0_fh.close
    else:
        token = update_token()
    headers = generate_headers(token)

#     url = 'http://localhost:49161/reference/'
    url = 'http://localhost:11223/reference/'
#     headers = {
#         'Authorization': 'Bearer <token_goes_here>',
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }

    resource_primary_id_to_curie_file = base_path + 'resource_primary_id_to_curie'
    reference_primary_id_to_curie_file = base_path + 'reference_primary_id_to_curie'
    errors_in_posting_reference_file = base_path + 'errors_in_posting_reference'

    already_processed_primary_id = set()
    if path.isfile(reference_primary_id_to_curie_file):
        with open(reference_primary_id_to_curie_file, 'r') as read_fh:
            for line in read_fh:
                line_data = line.split("\t")
                if line_data[0]:
                    already_processed_primary_id.add(line_data[0].rstrip())
            read_fh.close

    resource_to_curie = dict()
    with open(resource_primary_id_to_curie_file, 'r') as read_fh:
        for line in read_fh:
            line_data = line.rstrip().split("\t")
            if line_data[0]:
                resource_to_curie[line_data[0]] = line_data[1]
        read_fh.close

    with open(reference_primary_id_to_curie_file, 'a') as mapping_fh, open(errors_in_posting_reference_file, 'a') as error_fh:
        for filepath in files_to_process:
            # only test one file for run
            # if filepath != json_storage_path + 'REFERENCE_PUBMED_WB_1.json':
            #     continue
            # logger.info("opening file\t%s", filepath)
            f = open(filepath)
            reference_data = json.load(f)
            # counter = 0
            for entry in reference_data:

                # only take a couple of sample from each file for testing
                # counter += 1
                # if counter > 2:
                #     break

                # output what we get from the file before converting for the API
                # json_object = json.dumps(entry, indent=4)
                # print(json_object)

                primary_id = entry['primaryId']
                if primary_id in already_processed_primary_id:
                    continue
                # if primary_id != 'PMID:9643811':
                #     continue

                new_entry = dict()

                for key in entry:
                    keys_found.add(key)
#                     logger.info("key found\t%s\t%s", key, entry[key])
                    if key in remap_keys:
                        # logger.info("remap\t%s\t%s", key, remap_keys[key])
                        # this renames a key, but it can be accessed again in the for key loop, so sometimes a key is visited twice while another is skipped, so have to create a new dict to populate instead
                        # entry[remap_keys[key]] = entry.pop(key)
                        new_entry[remap_keys[key]] = entry[key]
                    elif key not in keys_to_remove:
                        new_entry[key] = entry[key]

                for key in remap_subkeys:
                    if key in new_entry:
                        # logger.info("%s\t%s\t%s", primary_id, key, new_entry[key])
                        new_list = []
                        for sub_element in new_entry[key]:
                            new_sub_element = dict()
                            for subkey in sub_element:
                                if subkey in remap_subkeys[key]:
                                    new_sub_element[remap_subkeys[key][subkey]] = sub_element[subkey]
#                                     logger.info("remap subkey\t%s\t%s", subkey, remap_subkeys[key][subkey])
                                elif key not in subkeys_to_remove or subkey not in subkeys_to_remove[key]:
                                    new_sub_element[subkey] = sub_element[subkey]
                            new_list.append(new_sub_element)
                        new_entry[key] = new_list

                # can only enter agr resource curie, if resource does not map to one, enter nothing
                if 'resource' in new_entry:
                    if new_entry['resource'] in resource_to_curie:
                        new_entry['resource'] = resource_to_curie[new_entry['resource']]
                    else:
                        del new_entry['resource']
                if 'category' in new_entry:
                    new_entry['category'] = new_entry['category'].lower().replace(" ", "_")
                if 'tags' in new_entry:
                    for sub_element in new_entry['tags']:
                        if 'tag_name' in sub_element:
                            sub_element['tag_name'] = camel_to_snake(sub_element['tag_name'])
                if 'authors' in new_entry:
                    for author in new_entry['authors']:
                        if 'orcid' in author:
                            # orcid field in json has just the identifier, need to add the prefix
                            if 'ORCID:' not in author['orcid']:
                                author['orcid'] = 'ORCID:' + author['orcid']
                if 'cross_references' in new_entry:
                    new_entry['cross_references'] = list(filter(lambda x: 'curie' in x and 'NLM:' not in x['curie'] and 'ISSN:' not in x['curie'], new_entry['cross_references']))

                # output what is sent to API after converting file data
                # json_object = json.dumps(new_entry, indent=4)
                # print(json_object)

                headers = process_post(url, headers, new_entry, primary_id, mapping_fh, error_fh)


#    if wanting to output keys in data for figuring out mapping
#         for key in keys_found:
#             logger.info("key %s", key)

        mapping_fh.close
        error_fh.close


def process_post(url, headers, new_entry, primary_id, mapping_fh, error_fh):
    # output the json getting posted to the API
    # json_object = json.dumps(new_entry, indent = 4)
    # print(json_object)

    post_return = requests.post(url, headers=headers, json=new_entry)
    print(primary_id + ' text ' + str(post_return.text))
    print(primary_id + ' status_code ' + str(post_return.status_code))

    response_dict = dict()
    try:
        response_dict = json.loads(post_return.text)
    except ValueError:
        logger.info("%s\tValueError", primary_id)
        error_fh.write("ERROR %s primaryId did not convert to json\n" % (primary_id))
        return headers

    if (post_return.status_code == 201):
        response_dict = response_dict.replace('"', '')
        logger.info("%s\t%s", primary_id, response_dict)
        mapping_fh.write("%s\t%s\n" % (primary_id, response_dict))
    elif (post_return.status_code == 401):
        logger.info("%s\texpired token", primary_id)
        mapping_fh.write("%s\t%s\n" % (primary_id, response_dict))
        token = update_token()
        headers = generate_headers(token)
        headers = process_post(url, headers, new_entry, primary_id, mapping_fh, error_fh)
    elif (post_return.status_code == 500):
        logger.info("%s\tFAILURE", primary_id)
        mapping_fh.write("%s\t%s\n" % (primary_id, response_dict))
    # if redoing a run and want to skip errors of data having already gone in
    # elif (post_return.status_code == 409):
    #     continue
    else:
        logger.info("ERROR %s primaryId %s message %s", post_return.status_code, primary_id, response_dict['detail'])
        error_fh.write("ERROR %s primaryId %s message %s\n" % (post_return.status_code, primary_id, response_dict['detail']))
    return headers


# def generate_headers(token):
#     authorization = 'Bearer ' + token
#     headers = {
#         'Authorization': authorization,
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }
#     return headers
#
#
# def update_token():
#     url = 'https://alliancegenome.us.auth0.com/oauth/token'
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json'
#     }
#     header_dict = dict()
#     header_dict['audience'] = 'alliance'
#     header_dict['grant_type'] = 'client_credentials'
#     header_dict['client_id'] = environ.get('AUTH0_CLIENT_ID')
#     header_dict['client_secret'] = environ.get('AUTH0_CLIENT_SECRET')
#     # data for this api must be a string instead of a dict
#     header_entry = json.dumps(header_dict)
#     # logger.info("data %s data end", header_entry)
#     post_return = requests.post(url, headers=headers, data=header_entry)
#     # logger.info("post return %s status end", post_return.status_code)
#     # logger.info("post return %s text end", post_return.text)
#     response_dict = json.loads(post_return.text)
#     token = response_dict['access_token']
#     logger.info("token %s", token)
#     with open(auth0_file, 'w') as auth0_fh:
#         auth0_fh.write("%s" % (token))
#         auth0_fh.close
#     return token


if __name__ == "__main__":
    """ call main start function """
    logger.info("starting post_reference_to_api.py")

    if args['authorization']:
        update_token()

    else:
        post_references()

    logger.info("ending post_reference_to_api.py")

# pipenv run python post_reference_to_api.py
