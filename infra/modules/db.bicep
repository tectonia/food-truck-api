param postgreSQLServerName string
param postrgreSQLDatabaseName string
param location string
param adminUsername string
@secure()
param adminPassword string

resource postgreSQLServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = {
  name: postgreSQLServerName
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: adminUsername
    administratorLoginPassword: adminPassword
    storage: {
      storageSizeGB: 32
      autoGrow: 'Disabled'
    }
  }
}

resource postgreSQLDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-03-01-preview'= {
  name: postrgreSQLDatabaseName
  parent: postgreSQLServer
  properties: {
    charset: 'UTF8'
    collation: 'English_United States.1252'
  }
}
