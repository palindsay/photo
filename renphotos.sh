#!/bin/bash

# Check for input directory
if [ $# -eq 0 ]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

input_dir="$1"

# Function to extract metadata and rename
rename_photo() {
  photo_path="$1"

  # Extract relevant metadata (DateTimeOriginal, CreateDate, Country, City)
  metadata=$(exiftool -s -s -s -d '%Y%m%d_%H' "$photo_path" \
                    -DateTimeOriginal -CreateDate -Country -City)

  # Extract date/time (prioritize DateTimeOriginal)
  datetime=$(echo "$metadata" | head -n 1)
  if [ -z "$datetime" ]; then
    echo "Skipping $photo_path: No date/time found"
    return
  fi

  # Extract location (if available)
  country=$(echo "$metadata" | grep -oP '(?<=Country\s:\s).*')
  city=$(echo "$metadata" | grep -oP '(?<=City\s:\s).*')
  location_suffix=""
  if [ ! -z "$country" ]; then
    location_suffix="_${country// /_}"
    if [ ! -z "$city" ]; then
      location_suffix="${location_suffix}_${city// /_}"
    fi
  fi

  # Construct new filename
  extension="${photo_path##*.}"
  if [ "$extension" = "HEIC" ]; then  # Special handling for HEIC
    extension="jpg"                    # Convert HEIC to JPG (optional)
  fi
  new_name="${datetime}${location_suffix}.${extension}"

  # Rename file (with overwrite check)
  if [ ! -f "$new_name" ]; then
    if [ "$extension" = "jpg" ] && [ -x "$(command -v heif-convert)" ]; then
      heif-convert "$photo_path" "$new_name" # Convert HEIC to JPG if necessary
      echo "Converted and renamed: $photo_path -> $new_name"
    else
      exiftool "-FileName=$new_name" "$photo_path"
      echo "Renamed: $photo_path -> $new_name"
    fi
  else
    echo "Skipping: $photo_path (file with name $new_name already exists)"
  fi
}

# Process photos (including all Sony RAW formats)
find "$input_dir" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \
                   -o -iname "*.cr2" -o -iname "*.nef" -o -iname "*.arw" \
                   -o -iname "*.orf" -o -iname "*.dng" -o -iname "*.HEIC" \
                   -o -iname "*.srf" -o -iname "*.sr2" \) | while read photo_path; do
  rename_photo "$photo_path"
done
