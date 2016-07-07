from flask import session
import requests
import sys
import datetime
import time
import json

REST_URL_SUFFIX = 'https://%s:9440/PrismGateway/services/rest/v1'
my_session = requests.Session()


def test_credentials(username, password, ip_address):
    session['ip_address'] = ip_address
    base_url = REST_URL_SUFFIX%session['ip_address']
    my_session.auth = (username, password)
    my_session.verify = False
    my_session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
    try:
        serverResponse = my_session.get(base_url + "/cluster", timeout=20)
        return serverResponse.status_code, json.loads(serverResponse.text)
    except Exception as ex:
        print "Nutant, we have a problem! %s" % ex


def get_events_data(investigate_date):

    def create_event_rest_url(date):
        start_time = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())
        end_time = start_time + (24*60*60)
        start_time_url = str(int(start_time)) + "000000"
        end_time_url = str(int(end_time)) + "000000"
        base_url = REST_URL_SUFFIX%session['ip_address']
        url = base_url + "/events?" + "startTimeInUsecs=" + start_time_url + "&endTimeInUsecs=" + end_time_url
        print url
        return url

    def login_event():
        user_info = element.get('contextValues')[0]
        event_info = element.get('contextValues')[-1].replace('{audit_user}', element.get(
            'contextValues')[0])
        event_info = event_info.replace('{ip_address}', element.get(
            'contextValues')[1])
        return user_info, event_info

    def container_event():
        user_info = element.get('contextValues')[-1]
        event_info = element.get('contextValues')[-2].replace('{container_name}', element.get('contextValues')[1])
        if event_info.startswith("Added"):
            event_info = event_info.replace('{storage_pool_name}', element.get('contextValues')[3])
        return user_info, event_info

    def nfs_datastore_event():
        user_info = element.get('contextValues')[-1]
        if element.get('contextValues')[-2].startswith("Creation"):
            event_info = element.get('contextValues')[-2].replace('{datastore_name}',
                                                                  element.get('contextValues')[0])
            event_info = event_info.replace('{container_name}', element.get('contextValues')[1])
        else:
            event_info = "datastore update event"
        return user_info, event_info

    def rep_sys_state_event():
        return "user info", "rep_sys_state_audit_event"

    def snap_ready_event():
        return "user info", "snap_ready_event"

    def remote_site_event():
        return "user info", "remote_site_event"

    def protection_domain_event():
        return "user info", "protection_domain_event"

    def register_vm_event():
        return "user info", "Register_vm_event"

    def restore_proctect_domain_vms_event():
        return "user info", "restore_protect_domain_vms_event"

    def mod_protect_domain_snap_event():
        return "user info", "mod_protect_domain_snap_event"

    def protect_domain_change_mode_event():
        return "user info", "protect_domain_change_mode_event"

    def pd_cron_sched_event():
        return "user info", "pd_cron_sched_event"

    def upgrade_info_event():
        return "user info", "upgrade_info_event"

    def software_release_event():
        return "user_info", "upgrade_info_event"

    def nfs_whitelist_event():
        return "user_info", "nfs_whitelist_event"

    def protect_domain_entities_event():
        return "user_info", "protect_domain_entities_event"

    def pd_OOB_sched_event():
        return "user_info", "pd_OOB_sched_event"

    event_types = {
        'LoginInfoAudit': login_event,
        'ContainerAudit': container_event,
        'NFSDatastoreAudit': nfs_datastore_event,
        'ReplicationSystemStateAudit': rep_sys_state_event,
        'SnapshotReadyAudit': snap_ready_event,
        'RemoteSiteAudit' : remote_site_event,
        'RegisterVmAudit': register_vm_event,
        'RestoreProtectionDomainVMsAudit' : restore_proctect_domain_vms_event,
        'ProtectionDomainAudit' : protection_domain_event,
        'ProtectionDomainChangeModeAudit' : protect_domain_change_mode_event,
        'ProtectionDomainEntitiesAudit': protect_domain_entities_event,
        'ModifyProtectionDomainSnapshotAudit': mod_protect_domain_snap_event,
        'PdCronScheduleAudit' : pd_cron_sched_event,
        'UpgradeInfoAudit' : upgrade_info_event,
        'SoftwareReleaseAudit': software_release_event,
        'NFSWhiteListAudit': nfs_whitelist_event,
        'PdOOBScheduleAudit': pd_OOB_sched_event,
    }

    print "create events URL"
    eventsURL = create_event_rest_url(investigate_date)
    serverResponse = my_session.get(eventsURL)
    json_events = json.loads(serverResponse.text)
    event_list = []
    for element in json_events['entities']:
        event_user, event_msg = event_types[element.get('alertTypeUuid')]()
        event_list.append((event_user, event_msg))
    for x in event_list: print x
    return event_list


from NTNXWhoDidWhat import app

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as ex:
        print ex
        sys.exit(1)
