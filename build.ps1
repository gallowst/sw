$strResourceGroupName = "gallows-euw-rg"
$strLocation = "west europe"

# Create the Resource Group
New-AzResourceGroup -Location $strLocation -Name $strResourceGroupName

# Create the API Container
$apiPort1 = New-AzContainerInstancePortObject -Port 5000 -Protocol TCP
$apiContainer = New-AzContainerInstanceObject -Name "starwars-api" -Image "docker.io/gallows/sw:api" -RequestCpu 0.5 -RequestMemoryInGb 0.5 -Port @($apiPort1)
$apiContainerGroup = New-AzContainerGroup -ResourceGroupName $strResourceGroupName -Name "starwars-api" -Location $strLocation -Container $apiContainer -OsType Linux -RestartPolicy "Never" -IpAddressType Public -IPAddressDnsNameLabel starwars-api

# Create the App Container
$appSplat = @{
    ResourceGroupName  = $strResourceGroupName
    Name               = "starwars-app"
    Image              = "docker.io/gallows/sw:app"
    Port               = @(80)
    RestartPolicy      = "Never"
    IpAddressType      = "Public"
    DnsNameLabel       = "starwars-app"
    EnvironmentVariable = @{"SW_URL"=$objApi.Fqdn}
}

$appenv1 = New-AzContainerInstanceEnvironmentVariableObject -Name "SW_URL" -Value $apiContainerGroup.IPAddressFqdn
$appPort1 = New-AzContainerInstancePortObject -Port 80 -Protocol TCP
$appContainer = New-AzContainerInstanceObject -Name "starwars-app" -Image "docker.io/gallows/sw:app" -RequestCpu 0.5 -RequestMemoryInGb 0.5 -Port @($appPort1) -EnvironmentVariable @($appEnv1)
$appContainerGroup = New-AzContainerGroup -ResourceGroupName $strResourceGroupName -Name "starwars-app" -Location $strLocation -Container $appContainer -OsType Linux -RestartPolicy "Never" -IpAddressType Public -IPAddressDnsNameLabel starwars-app

# View the returned content
(Invoke-WebRequest ("http://{0}:{1}" -f $appContainerGroup.IpAddressFqdn, $appContainerGroup.IPAddressPort.Port1)).Content