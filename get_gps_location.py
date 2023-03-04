#!/usr/bin/env python3

import exifread

def get_gps_location(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        lat_ref = tags.get('GPS GPSLatitudeRef').values
        lat = tags.get('GPS GPSLatitude').values
        lon_ref = tags.get('GPS GPSLongitudeRef').values
        lon = tags.get('GPS GPSLongitude').values

        if lat_ref and lat and lon_ref and lon:
            lat_val = lat[0].num / float(lat[0].den)
            lat_val += lat[1].num / (60.0 * lat[1].den)
            lat_val += lat[2].num / (3600.0 * lat[2].den)
            if lat_ref == 'S':
                lat_val = -lat_val

            lon_val = lon[0].num / float(lon[0].den)
            lon_val += lon[1].num / (60.0 * lon[1].den)
            lon_val += lon[2].num / (3600.0 * lon[2].den)
            if lon_ref == 'W':
                lon_val = -lon_val

            return (lat_val, lon_val)
        else:
            return None

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: {} <image_file>'.format(sys.argv[0]))
        sys.exit(1)

    file_path = sys.argv[1]
    location = get_gps_location(file_path)
    if location:
        print('Latitude: {}\nLongitude: {}'.format(*location))
    else:
        print('Location not found.')
