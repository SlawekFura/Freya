basePath=$PWD
pathToDxf="${basePath}/${1}"
pathToOutput="${basePath}/${2}"

echo ${basePath}
echo $pathToDxf
echo $pathToOutput

cd $pathToOutput 
rm *.gcode
cd "$( dirname "$0" )" && pwd 
python3 "./Gen3DGcode.py" $pathToDxf $pathToOutput 
