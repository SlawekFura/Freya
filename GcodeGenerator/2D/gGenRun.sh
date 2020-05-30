#!/bin/bash
basePath=$PWD
pathToDxf="${basePath}/${1}"
pathToOutput="${basePath}/${2}"

echo ${basePath}
echo $pathToDxf
echo $pathToOutput

cd $pathToOutput 
rm *.gcode
cd "$( dirname "$0" )" && pwd 
python3 "./genGcodeFromDXF.py" $pathToDxf $pathToOutput 
read varname

