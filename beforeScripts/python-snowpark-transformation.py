import os
import json

configMap = {
    'database': 'WORKSPACE_DATABASE',
    'schema': 'WORKSPACE_SCHEMA',
    'host': 'WORKSPACE_DOMAIN',
    'user': 'WORKSPACE_USER',
    'password': 'WORKSPACE_PASSWORD',
    'warehouse': 'WORKSPACE_WAREHOUSE',
}

with open('/data/config.json') as configFile:
    config = json.load(configFile)

workspaceConfig = config.get('authorization', {}).get('workspace', {})
for configProp, envProp in configMap.items():
    os.environ[envProp] = workspaceConfig.get(configProp, '')
