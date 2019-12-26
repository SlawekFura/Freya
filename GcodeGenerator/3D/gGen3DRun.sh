script=${0}
scriptPath=`dirname $script`
basePath=$PWD
pathToDxf="${basePath}/${1}"
pathToOutput="${basePath}/${2}"
optimization=${3}

#echo ${basePath}
#echo $pathToDxf
#echo $pathToOutput
#echo $optimization

cd "$scriptPath/Generated" 
dirWithGenerated='GcodeGenerator/3D/Generated'
if [[ $PWD == *"$dirWithGenerated"* ]]; then
  rm *
  echo "All generated files deleted!"
fi
echo $PWD

cd $pathToOutput 
if [ -f "*.gcode" ]
then
    rm *.gcode
    echo "All gcode files removed!"
fi

cd "$( dirname "$0" )" && pwd 
python "./Gen3DGcode.py" $pathToDxf $pathToOutput $optimization
