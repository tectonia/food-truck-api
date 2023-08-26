targetScope = 'subscription'

param resourceGroupName string = 'rg-foodtruckapi'
param appServicePlanName string = 'AppServicePlan-${uniqueString(resourceGroupName)}'
param webAppName string = 'webApp-${uniqueString(resourceGroupName)}'
param postrgreSQLServerName string = 'postgres-${uniqueString(resourceGroupName)}'
param postrgreSQLDatabaseName string = 'foodtrucks'
param location string = 'West Europe'
param adminUsername string
@secure()
param adminPassword string
@secure()
param secretKey string
var postgresConnectionString = 'host=${postrgreSQLServerName}.postgres.database.azure.com port=5432 dbname=${postrgreSQLDatabaseName} user=${adminUsername} password=${adminPassword}'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2022-09-01' = {
  name: resourceGroupName
  location: location
}

module app 'modules/app.bicep' = {
  name: 'app'
  scope: resourceGroup
  params: {
    appServicePlanName: appServicePlanName
    webAppName: webAppName
    location: location
    secretKey: secretKey
    postgresConnectionString: postgresConnectionString
  }
}

module database 'modules/db.bicep' = {
  name: 'database'
  scope: resourceGroup
  params: {
    location: location
    postgreSQLServerName: postrgreSQLServerName
    postrgreSQLDatabaseName: postrgreSQLDatabaseName
    adminUsername: adminUsername
    adminPassword: adminPassword
  }
}
