helpFunction()
{
   echo ""
   echo "Usage: $0 [OPTIONS] [ARGS]"
   echo "Options:"
   echo "\t-h, --help, -?, --?               Display this help"
   echo "\t-t, --target=[console|container]  Sets target"
   echo "\t-m, --mode=[prod|dev]             App mode"
   echo "\nArgs:"
   echo "\t-b, --build                       When target is container, rebuilds container if it is already built"
   exit 1 # Exit script after printing help
}

TARGET=console
MODE=prod
BUILD=no

for i in "$@"
do
case $i in
   -t=*|--target=*)
      TARGET="${i#*=}"
      shift # past argument=value
      ;;
   -m=*|--mode=*)
      MODE="${i#*=}"
      shift # past argument=value
      ;;
   -b|--build)
      BUILD=YES
      shift # past argument with no value
      ;;
   -h|--help|-\?|--\?)
      helpFunction
      ;;
   *)
      # unknown option
      helpFunction
      ;;
esac
done
echo "App mode: $MODE"
# Begin script in case all parameter
if [[ $TARGET == "container" ]]
then
   if [[ $BUILD == "YES" ]]
   then
      echo "Building container before run..."
      docker-compose -f ./container/docker-compose.yml --project-directory=container build
   fi
   echo "Running app in container..."
   APP_MODE=$MODE docker-compose -f ./container/docker-compose.yml --project-directory=container run app
else
   echo "Running app in console..."
   APP_MODE=$MODE python3 ./app/main.py
fi
