targetScope = 'subscription'

param resourceGroupName string = 'rg-foodtruckapi'

param appServicePlanName string = 'AppServicePlan-${uniqueString(resourceGroupName)}'

param webAppName string = 'webApp-${uniqueString(resourceGroupName)}'

param location string = 'West Europe'

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
  }
}

