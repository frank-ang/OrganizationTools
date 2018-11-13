'''module to identify and remov IAM objects/entities'''
from __future__ import print_function

import boto3

#remove group policys from all groups
def rm_group_policies(iam, current_groups, delete):
    for group in iam.list_groups()['Groups']:
        if group['GroupName'] in current_groups:
            print("Skip group policy for group: " + group['GroupName'])
            continue

        inline_policy = iam.list_group_policies(GroupName=group['GroupName'])
        for pol in inline_policy['PolicyNames']:
            print("Remove group: " + group['GroupName'] \
                + " inline policy: " + pol, end=' ')
            if delete:
                iam.delete_group_policy(GroupName=group['GroupName'],
                                        PolicyName=pol)
                print(" \t[Done]")
            else:
                print()
                        
        attached_policy = iam.list_attached_group_policies(
            GroupName=group['GroupName'])

        for pol in attached_policy['AttachedPolicies']:
            print("Remove group: " + group['GroupName']  \
                + " attached policy: " + pol['PolicyName'], end=' ')
            if delete:
                iam.detach_group_policy(
                    GroupName=group['GroupName'], PolicyArn=pol['PolicyArn'])
                print(" \t[Done]")
            else:
                print()

#remove users from all groups
def rm_group_users(iam, users, current_user, delete):
    current_groups = []
    for user in users:
        groups = iam.list_groups_for_user(UserName=user['UserName'])
        for group in groups['Groups']:
            if user['UserName'] == current_user:
                print("Skip user[" + user['UserName'] + "] in group: " \
                    + group['GroupName'])
                current_groups.append(group['GroupName'])
                continue
            
            print("Remove user[" + user['UserName'] + "] from group: " \
                + group['GroupName'], end=' ')
            if delete:
                iam.remove_user_from_group(
                    GroupName=group['GroupName'],
                    UserName=user['UserName'])
                print(" \t[Done]")
            else:
                print()

    return current_groups

#delete groups
def rm_groups(iam, current_groups, delete):
    for group in iam.list_groups()['Groups']:
        if group['GroupName'] in current_groups:
            print("Skip group: " + group['GroupName'])
            continue

        print("Remove group: " + group['GroupName'], end=' ')
        if delete:
            iam.delete_group(GroupName=group['GroupName'])
            print(" \t[Done]")
        else:
            print()

#remove user policies
def rm_user_policies(iam, users, current_user, delete):
    for user in users:
        if current_user == user['UserName']:
            continue

        inline_policies = iam.list_user_policies(UserName=user['UserName'])
        for pol in inline_policies['PolicyNames']:
            print("Remove user[" + user['UserName'] + "] inline policy: " + pol, end=' ')
            if delete: 
                iam.delete_user_policy(UserName=user['UserName'],
                                       PolicyName=pol)
                print(" \t[Done]")
            else:
                print()

        attached_policies = iam.list_attached_user_policies(
            UserName=user['UserName'])
        for pol in attached_policies['AttachedPolicies']:
            print("Remove user[" + user['UserName'] + "] attached policy: " \
                + pol['PolicyName'], end=' ')
            if delete:
                iam.detach_user_policy(UserName=user['UserName'], \
                                       PolicyArn=pol['PolicyArn'])
                print(" \t[Done]")
            else:
                print()

#remove user login profile
def rm_user_login_profile(iam, users, delete):
    for user in users:
        try:
            print("Remove user[" + user['UserName'] + "] login profile", end=' ')
            if delete:
                iam.delete_login_profile(UserName=user['UserName'])
                print(" \t[Done]")
            else:
                print()
        except:
            # if user doesn't have a login profile, an exception will be thrown.
            # we just ignore it here
            if delete:
                print(" \t[Done]")
            else:
                print()
            pass

#remove user ssh public keys
def rm_user_ssh_keys(iam, users, delete):
    for user in users:
        keys = iam.list_ssh_public_keys(UserName=user['UserName'])
        for key in keys['SSHPublicKeys']:
            print("Remove user[" + user['UserName'] + "] ssh public key: " \
                + key['SSHPublicKeyId'], end=' ')
            if delete:
                iam.delete_ssh_public_key(UserName=user['UserName'],
                                          SSHPublicKeyId=key['SSHPublicKeyId'])
                print(" \t[Done]")
            else:
                print()

#remove user ssh public keys
def rm_user_mfa(iam, users, delete):
    for user in users:
        mfas = iam.list_mfa_devices(UserName=user['UserName'])
        for mfa in mfas['MFADevices']:
            print("Deactivate user[" + user['UserName'] + "] mfa device: " \
                + mfa['SerialNumber'], end=' ')
            if delete:
                iam.deactivate_mfa_device(UserName=user['UserName'],
                                          SerialNumber=mfa['SerialNumber'])
                print(" \t[Done]")
            else:
                print()

    virtual_mfas = iam.list_virtual_mfa_devices()
    for vmfa in virtual_mfas['VirtualMFADevices']:
        print("Remove use virtual mfa device: " + vmfa['SerialNumber'], end=' ')
        if delete:
            iam.delete_virtual_mfa_device(SerialNumber=vmfa['SerialNumber'])
            print(" \t[Done]")
        else:
            print()

#remove user ssh public keys
def rm_user_signing_certificates(iam, users, delete):
    for user in users:
        certs = iam.list_signing_certificates(UserName=user['UserName'])
        for cert in certs['Certificates']:
            print("Remove user[" + user['UserName'] \
                + "] signing certificate: " + cert['CertificateId'], end=' ')
            if delete:
                iam.delete_signing_certificate(UserName=user['UserName'],
                    CertificateId= cert['CertificateId'])
                print(" \t[Done]")
            else:
                print()

#remove user keys
def rm_user_keys(iam, users, current_key_id, delete):
    current_user = None
    for user in users:
        keys = iam.list_access_keys(UserName=user['UserName'])
        for key_metadata in keys['AccessKeyMetadata']:
            if  key_metadata['AccessKeyId'] == current_key_id:
                current_user = user['UserName']
                print("Skip access key for user[" \
                    + user['UserName'] + "] Key: " + key_metadata['AccessKeyId'])
            else:
                print("Remove user[" + user['UserName'] + "] key: " \
                    + key_metadata['AccessKeyId'], end=' ')
                if delete:
                    iam.delete_access_key(
                        UserName=user['UserName'],
                        AccessKeyId=key_metadata['AccessKeyId']
                    )
                    print(" \t[Done]")
                else:
                    print()

    return current_user

#remove users
def rm_user(iam, users, current_user, delete):
    for user in users:
        print("Remove user: " + user['UserName'], end=' ')
        if delete:
            #keep current user
            if user['UserName'] != current_user:
                iam.delete_user(UserName=user['UserName'])
                print(" \t[Done]")
            else:
                print(" \tSkip user since we are using it now!")
        else:
            print()


def rm_alias(iam, delete):
    aliases = iam.list_account_aliases()
    for a in aliases['AccountAliases']:
        print("Remove account alias: " + a, end=' ')
        if delete:
            iam.delete_account_alias(AccountAlias=a)
            print(" \t[Done]")
        else:
            print()


def rm_roles(iam, delete):
    roles = iam.list_roles()
    for role in roles['Roles']:
        profiles = iam.list_instance_profiles_for_role(
            RoleName=role['RoleName'])
        for profile in profiles['InstanceProfiles']:
            print("Remove role profile: " + profile['InstanceProfileName'], end=' ')
            if delete:
                iam.remove_role_from_instance_profile(
                    InstanceProfileName=profile['InstanceProfileName'],
                    RoleName=role['RoleName']
                )
                print(" \t[Done]")
            else:
                print()

        poldoc = str(role['AssumeRolePolicyDocument'])
        #skip roles can assume; delete them could cause problems
        if poldoc is not None and poldoc.find('arn:aws:iam:') == -1:
            policies = iam.list_role_policies(RoleName=role['RoleName'])
            for policy in policies['PolicyNames']:
                print("Remove role policy: " + policy, end=' ')
                if delete:
                    iam.delete_role_policy(
                        RoleName=role['RoleName'],
                        PolicyName=policy
                    )
                    print(" \t[Done]")
                else:
                    print()

            attached_policies = iam.list_attached_role_policies(
                RoleName=role['RoleName'])
            for policy in attached_policies['AttachedPolicies']:
                print("Detach role policy: " + policy['PolicyName'], end=' ')
                if delete:
                    iam.detach_role_policy(
                        RoleName=role['RoleName'],
                        PolicyArn=policy['PolicyArn']
                    )
                    print(" \t[Done]")
                else:
                    print()
            
            print("Remove role[" + role['RoleName'] + "]", end=' ')
            if delete:
                iam.delete_role(RoleName=role['RoleName'])
                print("[Done]")
            else:
                print()
        else:
            print(" \tSkip role[" + role['RoleName'] + "]")
            continue

def iam_main(access_key, session, delete=False):
    iam = session.client('iam');

    users = iam.list_users()['Users']
    current_user_name = rm_user_keys(iam, users, access_key, delete)

    current_group_names = rm_group_users(iam, users, current_user_name, delete)
    rm_group_policies(iam, current_group_names, delete)
    rm_groups(iam, current_group_names, delete)

    rm_user_policies(iam, users, current_user_name, delete)
    rm_user_login_profile(iam, users, delete)
    rm_user_ssh_keys(iam, users, delete)
    rm_user_mfa(iam, users, delete)
    rm_user_signing_certificates(iam, users, delete)
    rm_user(iam, users, current_user_name, delete)

    rm_alias(iam, delete)
    ## not sure if this is safe: rm_roles(iam, delete)
