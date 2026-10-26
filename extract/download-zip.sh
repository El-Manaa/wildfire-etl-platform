ZIP_FOLDER="./minio_c/downloaded-zip/ZIP_$(date +%Y-%m-%d)"
if [[ ! -d  "$ZIP_FOLDER" && ! $(ls "$ZIP_FOLDER") ]]; then
  mkdir "$ZIP_FOLDER"
  declare -a VIIRS_URLS=(
    "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/shapes/zips/J1_VIIRS_C2_Global_24h.zip"
    "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-21-viirs-c2/shapes/zips/J2_VIIRS_C2_Global_24h.zip"
  )
  for URL in "${VIIRS_URLS[@]}"; do
      FILENAME="${URL##*/}"
      ZIPPATH="$ZIP_FOLDER/${FILENAME%.zip}_$(date +%Y-%m-%d).zip"
      curl -s "$URL" -o "$ZIPPATH" && echo "$ZIPPATH"
  done
  zip "$ZIP_FOLDER.zip" "$ZIP_FOLDER"
fi
