$strAcrName = "gallowsstarwarsacr"
$strResourceGroupName = "gallows-euw-rg"
$strLocation = "west europe"

# Create the Resource Group and the ACR
New-AzResourceGroup -Location $strLocation -Name $strResourceGroupName
$objAcr = New-AzContainerRegistry -ResourceGroupName $strResourceGroupName -Name $strAcrName -EnableAdminUser -Sku Basic
# Build the Containers and get the registry credential
az acr build --registry $strAcrName --image starwars-api .\api
az acr build --registry $strAcrName --image starwars-app .\app
az acr login --name $strAcrName
# Build the credential
$objCred = az acr credential show -n $strAcrName | ConvertFrom-Json
$cred = New-Object System.Management.Automation.PSCredential ($objCred.username, $(ConvertTo-SecureString $objCred.passwords[0].value -AsPlainText -Force) )
# Create the API Container
$apiSplat = @{
    ResourceGroupName  = $strResourceGroupName
    Name               = "starwars-api"
    Image              = ("{0}/starwars-api:latest" -f $objAcr.LoginServer)
    Port               = @(5000)
    RegistryCredential = $cred
    RestartPolicy      = "Never"
    IpAddressType      = "Public"
    DnsNameLabel       = "starwars-api"
}

$objApi = New-AzContainerGroup @apiSplat
# Create the App Container
$appSplat = @{
    ResourceGroupName  = $strResourceGroupName
    Name               = "starwars-app"
    Image              = ("{0}/starwars-app:latest" -f $objAcr.LoginServer)
    Port               = @(80)
    RegistryCredential = $cred
    RestartPolicy      = "Never"
    IpAddressType      = "Public"
    DnsNameLabel       = "starwars-app"
    EnvironmentVariable = @{"SW_URL"=$objApi.Fqdn}
}

$objApp = New-AzContainerGroup @appSplat
# View the returned content
(Invoke-WebRequest ("http://{0}:{1}" -f $objApp.Fqdn, $objApp.Ports[0].PortProperty)).Content