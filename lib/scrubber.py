import os
import piexif
import tempfile
import re
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

def get_metadata(filepath):
  """Extracts Exif metadata from an image file."""
  try:
    with Image.open(filepath) as img:
      exif_data = img._getexif()
      if not exif_data:
        return {}, "No EXIF metadata found."

      metadata = {}
      for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        metadata[tag_name] = value
      return metadata, None
  except Exception as e:
      return None, f"Error reading metadata: {e}"


def scrub_file(filepath, tags_to_remove=None, remove_all=False, in_place=False):
  """
  Scrubs metadata from a file, with options for selective, full, and in-place scrubbing.
  Returns a dictionary of the data that was removed and any error message.
  """
  try:
    if in_place:
      temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(filepath))
      os.close(temp_fd)
      output_path = temp_path
    else:
      dir_name, file_name = os.path.split(filepath)
      name, ext = os.path.splitext(file_name)
      output_path = os.path.join(dir_name, f"{name}_scrubbed{ext}")

    with Image.open(filepath) as img:
      img_format = img.format
      original_metadata, error = get_metadata(filepath)
      removed_data = {}
      
      #if no raw EXIF bytes, nothing to scrub.
      if 'exif' not in img.info:
        img.save(output_path, format=img_format)
        if in_place and os.path.exists(temp_path):
          os.remove(temp_path)
        return {}, "No EXIF metadata found. File was copied without changes."

      if remove_all:
        removed_data = original_metadata
        img.save(output_path, format=img_format)

      #selective and profile-based scrubbing.
      elif tags_to_remove:
        exif_bytes = img.info.get('exif')
        try:
          exif_dict = piexif.load(exif_bytes)
        except Exception:
          #if broken EXIF block; copy file without changes.
          img.save(output_path, format=img_format)
          if in_place and os.path.exists(temp_path):
              os.remove(temp_path)
          return {}, "Image contains invalid EXIF data. File was copied without changes."

        if exif_dict is None:
          img.save(output_path, format=img_format)
          if in_place and os.path.exists(temp_path):
              os.remove(temp_path)
          return {}, "Image contains invalid EXIF data. File was copied without changes."

        #creates a lookup table to find tag IDs from their names (e.g 'Make' -> 271)
        name_to_id = {v: k for k, v in TAGS.items()}

        #handles each tag from the profile list.
        for tag_name in tags_to_remove:
          #remove the entire GPS IFD when requested.
          if tag_name == 'GPSInfo':
            if 'GPS' in exif_dict and exif_dict['GPS']:
              removed_data['GPSInfo'] = exif_dict['GPS']
              exif_dict['GPS'] = {}
            # move to next tag after handling GPSInfo
            continue

          # handle non-GPS tags by name -> numeric id lookup
          tag_id = name_to_id.get(tag_name)
          #skips unknown tag names.
          if tag_id is None:
            continue

          #EXIF data is split into sections (IFDs). 
          #removes the tag from any IFD it appears in.
          for ifd_name in ('0th', 'Exif', 'GPS', '1st'):
            if ifd_name in exif_dict and isinstance(exif_dict[ifd_name], dict) and tag_id in exif_dict[ifd_name]:
              original_value = exif_dict[ifd_name][tag_id]
              removed_data[tag_name] = original_value
              del exif_dict[ifd_name][tag_id]

        #ensures selective removal succeeds even on imperfect EXIF blocks.
        def _safe_dump(edict):
          """ 
          Retry loop - remove offending tag ids reported by piexif
          until dump succeeds or nothing left to remove.
          """
          attempts = 0
          while True:
            try:
              return piexif.dump(edict)
            except Exception as e:
              attempts += 1
              if attempts > 10:
                  raise

              msg = str(e)
              #finds the first integer in the error message; piexif
              m = re.search(r"(\d+)", msg)
              if not m:
                #if couldn't parse tag id from message, re-raise
                raise
              bad_id = int(m.group(1))

              removed_any = False
              for ifd_nm in ('0th', 'Exif', 'GPS', '1st', 'thumbnail'):
                #some IFD entries may be None instead of dicts 
                #record as removed due to invalid type
                if ifd_nm in edict and isinstance(edict[ifd_nm], dict) and bad_id in edict[ifd_nm]:
                  name = TAGS.get(bad_id, bad_id)
                  if name not in removed_data:
                      removed_data[name] = 'removed_due_to_invalid_type'
                  edict[ifd_nm].pop(bad_id, None)
                  removed_any = True

              if not removed_any:
                # if nothing removed can't recover
                raise

        new_exif_bytes = _safe_dump(exif_dict)
        img.save(output_path, exif=new_exif_bytes, format=img_format)
      
      else:
        #when no scrubbing option is chosen.
        img.save(output_path, exif=img.info['exif'], format=img_format)
        return {}, "No scrubbing option selected. File was copied without changes."

      if in_place:
        shutil.move(temp_path, filepath)

      return removed_data, None

  except Exception as e:
    if in_place and 'temp_path' in locals() and os.path.exists(temp_path):
      os.remove(temp_path)
    return None, f"Error processing file: {e}"