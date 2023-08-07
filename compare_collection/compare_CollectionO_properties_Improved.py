# compare DA collection objects
print("Compare DA collection objects")

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

cur.execute('SELECT  o.obj_guid, o.name, o.oid, o.oid_type, o.class, o.app_guid, a.name '
            'FROM dynamic_app_objects as o '
            'JOIN (SELECT name, app_guid, ppguid '
                'FROM dynamic_app '
                'WHERE ppguid = "BCCD4D17F0D7A56C92E4D3283BCD8D36") as a '
            'WHERE o.app_guid = a.app_guid ORDER BY o.app_guid')

# Save Result-set
v_103 = cur.fetchall()

# Save all v103 DAs related to linux base pack for testing purpose
cur2 = conn.cursor()
cur2.execute('SELECT app_guid, name '
            'FROM dynamic_app '
            'WHERE ppguid = "BCCD4D17F0D7A56C92E4D3283BCD8D36"'
            'ORDER BY ppguid ASC')

# Save Result-set
dynamic_apps_v103 = cur2.fetchall()
"""for x in v_103:
    if dynamic_apps_v103[0][0] == x[5]:
        print("si se pudo comparar " + str(dynamic_apps_v103[0][0]) + " " + str(x[5]))"""

conn.close()

print(" ")

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

cur.execute('SELECT o.obj_guid, o.name, o.oid, o.oid_type, o.class, o.app_guid, a.name '
            'FROM dynamic_app_objects as o '
            'JOIN (SELECT name, app_guid, ppguid '
                'FROM dynamic_app '
                'WHERE ppguid = "BCCD4D17F0D7A56C92E4D3283BCD8D36") as a '
            'WHERE o.app_guid = a.app_guid ORDER BY o.app_guid')

# Save Result-set
v_102 = cur.fetchall()

# Save all v102 DAs related to linux base pack for testing purpose
cur.execute('SELECT app_guid, name '
            'FROM dynamic_app '
            'WHERE ppguid = "BCCD4D17F0D7A56C92E4D3283BCD8D36" '
            'ORDER BY ppguid ASC')

# Save Result-set
dynamic_apps_v102 = cur.fetchall()

conn.close()
# ------------------------------------------------------------------
# Functions to compare two PP versions

# Compare items of two dictionaries and displays the key
# variable definition:
#   items           -> List of column's name
#   new_version     -> Aux list for handle items from the new version list
#   old_version     -> Aux list for handle items from the old version list
#   different_items      -> List that store not equals list between new_version and old_version
#   dic_new_version -> Dictionary to handle list_new_version
#   dic_old_version -> Dictionary to handle list_referent_past_version
def compare_single_list(list_new_version, list_referent_past_version):
    items = ["obj_guid", "obj_name", "oid", "oid_type","class_type", "app_guid", "app_name"]
    new_version = []
    old_version = []
    # Create dic_new_version var with all items from list_new_version
    for n in range(0, len(list_new_version)-1):
        new_version.append(list_new_version[n])
        dic_new_version = dict(zip(items, new_version))
    # Create dic_new_version var with all items from list_referent_past_version
    for n in range(0, len(list_referent_past_version)-1):
        old_version.append(list_referent_past_version[n])
        dic_old_version = dict(zip(items, old_version))

    # Check if the items in dic_new_version are not equals to dic_new_version and store the list in diff_items
    different_items = {k: dic_new_version[k] for k in dic_new_version if k in dic_old_version and dic_new_version[k] != dic_old_version[k]}


    """for k in dic_new_version:
        if k in dic_old_version and dic_new_version[k] != dic_old_version[k]:
            diff_items.append(k)
        else:
            equal.append(k)"""
    print(Fore.RED + str(list_new_version[1]) + Fore.BLUE + " Collection Object has the next differences between v103 and v102:" + Fore.RED + str(different_items))


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
    # Print the DA that not exist in v102
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
# Check if the new_version is greater than past_version and print it
# If not check if the new_version is smaller than past_version and print it
# If not these are equals and print it
# variable definition:
#   n_new_version   ->  number of elements in new_version list
#   n_past_version  ->  number of elements in past_version list
def count_item_of_two_version(new_version, past_version):
    n_new_version = len(new_version)
    n_past_version = len(past_version)
    if n_new_version > n_past_version:
        print(Fore.BLUE + "v_103({}) has more items than v_102({})".format(n_new_version, n_past_version))
    elif n_new_version < n_past_version:
        print(Fore.BLUE + "v_103({}) has less items than v_102({})".format(n_new_version, n_past_version))
    else:
        print(Fore.BLUE + "v_103({}) has the same items than v_102({})".format(n_new_version, n_past_version))

# ------------------------------------------------------------------
# compare properties
print(Fore.BLUE + "Compare DA Presentation objects")

#count_item_of_two_version(v_103, v_102)
print("")


#separate by presentatuon object by DAs


"""print(v_103[0])
print(v_102[0])"""

"""for list_v102, list_v103 in zip(v_102, v_103):
    print(list_v102[5])
    print(list_v103[5])
    print()"""

#compare_presentation_properties_two_pp_versions(v_102, v_103)
count_item_of_two_version(v_103, v_102)
print("")

dynamic_apps = []
for dynamicApps in dynamic_apps_v102:
    if dynamicApps not in dynamic_apps:
        dynamic_apps.append(dynamicApps)
for dynamicApps in dynamic_apps_v103:
    if dynamicApps not in dynamic_apps:
        dynamic_apps.append(dynamicApps)


for da in dynamic_apps:
    da_list_v102 = []
    da_list_v103 = []
    for simple_list in v_102:
        if simple_list[5] == da[0]:
            da_list_v102.append(simple_list)
    for simple_list in v_103:
        if simple_list[5] == da[0]:
            da_list_v103.append(simple_list)
    if len(da_list_v102) > len(da_list_v103):
        print(Fore.GREEN + str(da_list_v102[0][6]))
    else:
        print(Fore.GREEN + str(da_list_v103[0][6]))
    compare_properties_two_pp_versions(da_list_v102, da_list_v103)

