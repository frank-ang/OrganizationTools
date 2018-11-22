from __future__ import print_function
import sys, boto3

#
# cleanup resources in account, e.g. from General Immersion day ASG labs
#
def autoscaling_main(region_name, session, delete=False):

    asg_client = session.client('autoscaling', region_name=region_name);
    asgs = asg_client.describe_auto_scaling_groups()['AutoScalingGroups'];
    for asg in asgs:
        asgName = asg['AutoScalingGroupName']
        print("Found Autoscaling Group: %s" % asgName)
        if delete:
            print("Deleting Autoscaling Group: %s" % (asgName))
            response = asg_client.delete_auto_scaling_group(AutoScalingGroupName=asgName, ForceDelete=True)

    launch_configs = asg_client.describe_launch_configurations()['LaunchConfigurations']
    for launch_config in launch_configs:
        launch_config_name = launch_config['LaunchConfigurationName']
        print("Found LaunchConfiguration: %s" % launch_config_name)
        if delete:
            print("Deleting LaunchConfiguration: %s" % launch_config_name)
            response = asg_client.delete_launch_configuration(LaunchConfigurationName=launch_config_name)

    ec2_client = session.client('ec2', region_name=region_name);
    key_pairs = ec2_client.describe_key_pairs()['KeyPairs'];
    for key_pair in key_pairs:
        key_pair_name = key_pair['KeyName']
        print("Found Keypair: %s" % key_pair_name)
        if delete:
            print("Deleting Keypair: %s" % (key_pair_name))
            response = ec2_client.delete_key_pair(KeyName=key_pair_name)

    security_groups = ec2_client.describe_security_groups()['SecurityGroups'];
    for security_group in security_groups:
        security_group_name = security_group['GroupName']
        security_group_id = security_group['GroupId']
        print("Found security group: %s / %s" % (security_group_name, security_group_id))
        # preserve the default Security group
        if delete and security_group_name != 'default':
            print("Deleting security group: %s / %s" % (security_group_name, security_group_id)) 
            try:
                response = ec2_client.delete_security_group(GroupId=security_group_id);
            except Exception as e:
                # Best-effort. eat the exception.
                if hasattr(e, 'message'):
                    print("Unexpected error: " + e.message)
 


