#!/bin/bash

echo "🧼 Cleaning logs"
rm logs/isopalavial_interface
touch logs/isopalavial_interface
rm logs/firomactal_drive
touch logs/firomactal_drive
rm logs/ramistat_core
touch logs/ramistat_core

echo "🌎 Returning to earth"
echo "earth" > location

echo "❄️  Cooling to 40000 KRGs"
echo "40000" > ontarian_manifold

echo "🔒 Establishing secret key"
KEY=$(uuidgen)

printf "🖥️  Starting Isopalavial Interface "
API_KEY=$KEY python isopalavial_interface.py > logs/isopalavial_interface 2>&1 &
until $(curl -G --output /dev/null --silent --fail http://localhost:8000/healthcheck -H "X-Request-ID: healthcheck" -H "Content-Type: application/x-www-form-urlencoded" -H "accept: text/plain"); do
  printf "⏳"
  sleep 1
done
printf " ✅\n"

printf "🚂 Starting Firomactal Drive "
API_KEY=$KEY python firomactal_drive.py > logs/firomactal_drive 2>&1 &
until $(curl -G --output /dev/null --silent --fail http://localhost:8111/healthcheck -H "X-Request-ID: healthcheck" -H "Content-Type: application/x-www-form-urlencoded" -H "accept: text/plain"); do
  printf "⏳"
  sleep 1
done
printf " ✅\n"

printf "🧊 Starting Ramistat Core "
API_KEY=$KEY python ramistat_core.py > logs/ramistat_core 2>&1 &
until $(curl -G --output /dev/null --silent --fail http://localhost:8222/healthcheck -H "X-Request-ID: healthcheck" -H "Content-Type: application/x-www-form-urlencoded" -H "accept: text/plain"); do
  printf "⏳"
  sleep 1
done
printf " ✅\n"
