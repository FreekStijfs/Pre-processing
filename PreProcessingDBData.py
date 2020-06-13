import pandas as pd
import datetime
csv = '<raw data.csv>'

# import the data, comma separated
df = pd.read_csv(csv, header= 0, sep=',')
# drop unnecessary columns
df.drop(['Method','ActionParameters'], axis=1, inplace=True)
# drop all cases in which the user could not be identified
# meaning an incorrect login
df = df.dropna()
# create a more meaningful action column by merging controller and the performed action in the controller
df["UserAction"] = df['Controller'] + " " + df['Action']
# drop the action and controller column
df.drop(['Controller', 'Action'], axis=1, inplace=True)
# export to csv
pd.to_datetime(df['DateTime'])
# df_date is a pandas series, which is a series of tuples
df_date= df['DateTime']
## create a list from the series to loop through
def create_list_form_series():
    new_list = []
    for i in df_date.iteritems():
        i = list(i)
        del i[0]
        i = str(i).strip("'[]'")
        new_list.append(i)
    return new_list
datetime_list = create_list_form_series()
max = len(datetime_list)
def check_time_difference(first, first_plus_one):
    time_login = datetime_list[first]
    time_login_date_time = datetime.datetime.strptime(time_login, '%Y-%m-%d %H:%M:%S.%f')
    time_session_end = datetime_list[first_plus_one]
    time_session_end_date_time = datetime.datetime.strptime(time_session_end, '%Y-%m-%d %H:%M:%S.%f')
    difference = time_session_end_date_time - time_login_date_time

    if difference.seconds > 0.5:
        return True
    else:

        return False
'''Check all records in the file. The max is defined in the beginning of the file
Returns all actual actions'''
def check_all_records():
    count = 0
    action_list = []
    for i in datetime_list:
        count2 = count + 1
        if check_time_difference(count,count2):
            action_list.append(i)
        count = count + 1
        if count == max -1:
            break
    return action_list
action_list = check_all_records()
#create a new dataframe that is only consisting of actions
df = df[df['DateTime'].isin(action_list)]
#dictionary for mapping the names used in the usage logs to actual actions
name_mapping = {
    'Addon IsEnabled' : 'Login',
    'Login Login' : 'Login',
    'Role Index' : 'Open Role Page',
    'User Index' : 'Open User Page',
    'Right Index' : 'Open Right page',
    'User Update' : 'Save User',
    'User Create' : 'Create User',
    'Article Index' : 'Open Article Page',
    'Role Create' : 'Create Role',
    'Role Update' : 'Update Role',
    'Environment Get' : 'Login',
    'Login AuthCheck' : 'Login',
    'Query Get' : 'Open Query Page',
    'Application Index' : 'Open Application Page',
    'Settings GetKTOSettings' : 'Open KTO Settings Page',
    'Criteria Index': 'Open Criteria Page',
    'Pathway Index' : 'Open Pathway Page',
    'PhaseWaypointPreceptMatrix Index' : 'Open PhaseWaypoint Page',
    'NotificationWaypoint Index' : 'Open Notification Page',
    'Organization Index' : 'Open Organization Page',
    'Login Logout' : 'Logout',
    'Addon IsEnabled' : 'Login',
    'Waypoint Index' : 'Open Waypoint Page',
    'PhaseWaypointFaqList Index' : 'Open PhaseWaypoint Page',
    'PhaseWaypointChecklist Index' : 'Open PhaseWaypoint Page',
    'PhaseWaypoint Index' : 'Open PhaseWaypoint page',
    'PhaseWaypointArticle Index' : 'Open PhaseWaypoint page',
    'PhaseWaypointQuestionnaire Index' : 'Open PhaseWaypoint page',
    'File Index' : 'Open File Page',
    'Department Index' : 'Open Department Page',
    'Settings GetVirtualAssistantSettings' : 'Setup Virtual assistant',
    'Phase Index' : 'Open Phase Page',
    'FaqList Index' : 'Open FAQ Page',
    'Notification Index' : 'Open Notification Page',
    'Application Read' : 'Open Application Page',
    'ApplicationMenuCategory ApplicationIndex' : 'Open ApplcationMenuCategory',
    'ApplicationMenuItem Index' : "Open ApplicationMenuItem",
    'ApplicationMenuItemArticle Index' : "Select Menu Item Type",
    'PhaseWaypoint Update' : 'Save PhaseWaypoint',
    'CareProvider Index' : 'Open Careprovider Page',
    'PhaseWaypoint Create' : 'Create PhaseWaypoint',
    'ApplicationMenuCategory UpdateCategory' : 'Update MenuCategory',
    'ApplicationMenuCategory CreateCategory' : 'Create MenuCategory',
    'ApplicationMenuItemFaqList Index' : 'Add FAQ to MenuItem',
    'ApplicationMenuItemTemplate Index' : 'Select MenuType',
    'Faq Index' : 'Open FAQ PAge',
    'ContentProfileIntroArticle Index' : 'Open Content Profile',
    'GeneralSetting GetBaseUrl' : 'Open General Settings Page',
    'StyleElement Index' : 'Set Style',
    'StyleElement Update' : 'Save Style'

}
#apply the dictionary to the dataframe
df['UserAction']= df['UserAction'].map(name_mapping)
#convert the df to csv
df.to_csv('<cleaned_data.csv>', header=['ID','DateTime','UserID','UserAction'])
