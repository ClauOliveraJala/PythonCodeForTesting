# Module Imports
import mariadb
import sys
from colorama import Fore


# Connect to MariaDB Platform - SL1 with linux base pack PP v103
try:
    conn = mariadb.connect(
        user="root",
        password="em7admin",
        host="192.168.1.230",
        port=7706,
        database="master"
    )
except mariadb.Error as e:
    print(f'Error connecting to MariaDB Platform: {e}')
    sys.exit(1)

# Get Cursor - query that returns all DAs of LBP PP v103
cur = conn.cursor()
cur.execute(
    'SELECT app_guid, name, app_type, version, state, poll, env_type, cu_affinity '
    'FROM dynamic_app WHERE ppguid = (SELECT ppguid from powerpack '
    'WHERE name = "linux base pack")')

# Print Result-set
v103 = cur.fetchall()
conn.close()

# Connect to MariaDB Platform - SL1 with Linux base pack PP v102
try:
    conn = mariadb.connect(
        user="root",
        password="em7admin",
        host="192.168.1.231",
        port=7706,
        database="master"

    )
except mariadb.Error as e:
    print(f'Error connecting to MariaDB Platform: {e}')
    sys.exit(1)

# Get Cursor - query that returns DAs od LBP PP v102
cur = conn.cursor()
cur.execute(
    'SELECT app_guid, name, app_type, version, state, poll, env_type, cu_affinity '
    'FROM dynamic_app WHERE ppguid = (SELECT ppguid from powerpack '
    'WHERE name = "linux base pack")')

# Print Result-set
v102 = cur.fetchall()
# print(v102)
conn.close()

print(" ")

# ----------------------------------------------------------------------------------------------------------------------
# Functions to compare DAs properties of v103 and v102

# convert list to dictionary and Compare items of two dictionaries and displays the key
# variable definition:
#   items           -> List of column's name
#   new_version     -> Aux list for handle items from the new version list
#   old_version     -> Aux list for handle items from the old version list
#   different_items -> List that store not equals list matches between new_version and old_version
#   dic_new_version -> Dictionary to handle list_new_version
#   dic_old_version -> Dictionary to handle list_old_version
def compare_single_list(list_new_version, list_referent_past_version):
    items = ["app_guid", "name", "app_type", "version", "state", "poll", "env_type", "cu_affinity"]
    new_version = []
    old_version = []
    # Create dic_new_version var with all items from list_new_version
    for n in range(0, len(list_new_version)):
        new_version.append(list_new_version[n])
        dic_new_version = dict(zip(items, new_version))
    # Create dic_new_version var with all items from list_old_version
    for n in range(0, len(list_referent_past_version)):
        old_version.append(list_referent_past_version[n])
        dic_old_version = dict(zip(items, old_version))

    # Check if the items in dic_new_version are not equals to dic_new_version and store the list in diff_items
    different_items = {k: dic_new_version[k] for k in dic_new_version if
                       k in dic_old_version and dic_new_version[k] != dic_old_version[k]}
    # print(different_items)
    diff = different_items.keys()
    print(Fore.BLUE + list_new_version[1] + " DA has the next differences properties between v103 and v102:")
    print(Fore.RED + str(diff))


    """for k in dic_new_version:
        if k in dic_old_version and dic_new_version[k] != dic_old_version[k]:
            diff_items.append(k)
    print(Fore.YELLOW + str(list_new_version[1]) + " DA has the next differences between v103 and v102:")
    print(Fore.RED + str(diff_items))"""
    print("")

# search the app_guid of single list in a list of lists
# if find an app_guid it calls to compare single list function and compare each item
# variable definition:
#   not_exist   -> List that store all the list that don't exist in lists_master
#   exist       -> List that store all the list that exist in lists_master

def find_list(single_list, lists_master):
    not_exist = []
    exist = []
    # Check if any sublist in lists_master with single_list have equal app_guid
    # Then store that list in exist var
    # if not store them in not_exist
    for index in lists_master:
        if single_list[0] == index[0]:
            compare_single_list(single_list, index)
            exist.append(single_list[1])
            break
        else:
            if single_list[1] not in not_exist:
                not_exist.append(single_list[1])
    for n in not_exist:
        if n not in exist:
            print(Fore.YELLOW + n + " is not in v102")


# Compare properties of two versions
# Check if a any new version list exist is equals to the past version
def compare_properties_two_pp_versions(past_version, new_version):
    for n in new_version:
        find_list(n, past_version)


# Function - compare quantity of items of two PP versions(v102,v103)




# Function to count the items of each version and the compare. which one has more items
def count_item_of_two_version(new_version, past_version):
    n_new_version = len(new_version)
    n_past_version = len(past_version)
    if n_new_version > n_past_version:
        print(Fore.BLUE + "v_103({}) has more items than v_102({})".format(n_new_version, n_past_version))
    elif n_new_version < n_past_version:
        print(Fore.BLUE + "v_103({}) has less items than v_102({})".format(n_new_version, n_past_version))
    else:
        print(Fore.BLUE + "v_103({}) has the same items than v_102({})".format(n_new_version, n_past_version))


# --------------------------------------------------------------------------------------------------------------------

# compare DAs properties - call functions
count_item_of_two_version(v103, v102)
print("")

compare_properties_two_pp_versions(v102, v103)
