basePath=$PWD
pathToDxf="${basePath}/${1}"
pathToOutput="${basePath}/${2}"
optimization=${3}

#echo ${basePath}
#echo $pathToDxf
#echo $pathToOutput
#echo $optimization

cd $pathToOutput 
if [ -f "*.gcode" ]
then
    rm *.gcode
    echo "All gcode files removed!"
fi

cd "$( dirname "$0" )" && pwd 
python3 "./Gen3DGcode.py" $pathToDxf $pathToOutput $optimization
