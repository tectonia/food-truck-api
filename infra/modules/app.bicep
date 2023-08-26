param appServicePlanName string
param webAppName string
param location string
@secure()
param secretKey string
@secure()
param postgresConnectionString string

resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'S1'
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.10'
      appCommandLine: 'gunicorn --bind=0.0.0.0 --timeout 600 api:api'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: '1'
        }
        {
          name: 'SECRET_KEY'
          value: secretKey
        }
        {
          name: 'AZURE_POSTGRESQL_CONNECTIONSTRING'
          value: postgresConnectionString
        }
      ]
    }
  }
}

resource webAppSlot 'Microsoft.Web/sites/slots@2022-09-01' = {
  name: 'staging'
  parent: webApp
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.10'
      appCommandLine: 'gunicorn --bind=0.0.0.0 --timeout 600 api:api'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: '1'
        }
        {
          name: 'SECRET_KEY'
          value: secretKey
        }
        {
          name: 'AZURE_POSTGRESQL_CONNECTIONSTRING'
          value: postgresConnectionString
        }
      ]
    }
  }
}
