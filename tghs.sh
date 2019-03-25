#!/usr/bin/env bash
DATE=`date +%Y-%m-%d`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PATH_TO_PID="${DIR}/.pid"
OUTPUT="${DIR}/.logs/${DATE}.log"

case "$1" in
  start)
      read pid < ${PATH_TO_PID}
      if [[ ! -z "$pid" && ps -p "$pid" > /dev/null ]]
      then
          echo "already running"
          exit 1
      fi
      git -c ${DIR} pull
      python3.7 tghs.py $2 >> ${OUTPUT} 2>&1 & echo $! > ${PATH_TO_PID} &
    ;;
  stop)
      pkill -9 -P $(<"$PATH_TO_PID")
      kill -9 $(<"$PATH_TO_PID")
      echo "" > ${PATH_TO_PID}
    ;;
  restart)
      pkill -9 -P $(<"$PATH_TO_PID")
      kill -9 $(<"$PATH_TO_PID")
      git -c ${DIR} pull
      python3.7 tghs.py $2 >> ${OUTPUT} 2>&1 & echo $! > ${PATH_TO_PID} &
    ;;
  *)
      echo "unknown command $1" >> ${OUTPUT}
esac
