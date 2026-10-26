#!/bin/bash

y=$1
x=$2

is_float() {
  [[ "$1" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]
}


if is_float $y && is_float $x; then
  URL="https://nominatim.openstreetmap.org/reverse?lat=$y&lon=$x&format=json&accept-language=en"
  curl "$URL" | jq '.address'  | jq -r '{country_code, country, state, region}'
fi

