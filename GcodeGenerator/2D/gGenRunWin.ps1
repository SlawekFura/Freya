$basePath=$PWD
$dxfPath="$($basePath)\$($args[0])"
$outputPath="$($basePath)\$($args[1])"
$ScriptPath= $PSScriptRoot

#Write-Host $basePath
#Write-Host $dxfPath
#Write-Host $outputPath

cd $outputPath 
rm *.gcode
cd "$ScriptPath"  
Write-Host $ScriptPath
python "./genGcodeFromDXF.py" $dxfPath $outputPath 
cd $basePath
