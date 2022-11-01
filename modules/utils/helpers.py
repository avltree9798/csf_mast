from plistlib import load as load_plist

GOOGLE_API_URL = [
    (
        "Static Map API",
        "https://maps.googleapis.com/maps/api/staticmap?center=45,10&zoom=7&size=400x400&key="
    ), (
        "Street View API",
        "https://maps.googleapis.com/maps/api/streetview?size=400x400&location=40.720032,-73.988354&fov=90&heading=235&pitch=10&key="
    ), (
        "Directions API",
        "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood4&key="
    ), (
        "Geocode API",
        "https://maps.googleapis.com/maps/api/geocode/json?latlng=40,30&key="
    ), (
        "Distance Matrix API",
        "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101,-73.89188969999998&destinations=40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key="
    ), (
        "Find Place From Text API",
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key="
    ), (
        "Autocomplete API",
        "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=Bingh&types=%28cities%29&key="
    ), (
        "Elevation API",
        "https://maps.googleapis.com/maps/api/elevation/json?locations=39.7391536,-104.9847034&key="
    ), (
        "Timezone API",
        "https://maps.googleapis.com/maps/api/timezone/json?location=39.6034810,-119.6822510&timestamp=1331161200&key="
    ), (
        "Roads API",
        "https://roads.googleapis.com/v1/nearestRoads?points=60.170880,24.942795|60.170879,24.942796|60.170877,24.942796&key="
    ), (
        "Route to Traveled API",
        "https://roads.googleapis.com/v1/snapToRoads?path=-35.27801,149.12958|-35.28032,149.12907&interpolate=true&key="
    ), (
        "Speed Limit-Roads API",
        "https://maps.googleapis.com/maps/api/place/details/json?place_id=ChIJN1t_tDeuEmsRUsoyG83frY4&fields=name,rating,formatted_phone_number&key="
    ), (
        "Nearby Search-Places API",
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=100&types=food&name=harbour&key="
    ), (
        "Text Search-Places API",
        "https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+Sydney&key="
    ), (
        "Places Photo API",
        "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=CnRtAAAATLZNl354RwP_9UKbQ_5Psy40texXePv4oAlgP4qNEkdIrkyse7rPXYGd9D_Uj1rVsQdWT4oRz4QrYAJNpFX7rzqqMlZw2h2E2y5IKMUZ7ouD_SlcHxYq1yL4KbKUv3qtWgTK0A6QbGh87GB3sscrHRIQiG2RrmU_jF4tENr9wGS_YxoUSSDrYjWmrNfeEHSGSc3FyhNLlBU&key="
    ), (
        "Query Autocomplete-Places API",
        "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?input=pizza+near%20par&key="
    ), (
        "Embed (Basic-Free) API",
        "https://www.google.com/maps/embed/v1/place?q=Seattle&key="
    ),
    (
        "Embed (Advanced-Paid) API",
        "https://www.google.com/maps/embed/v1/search?q=record+stores+in+Seattle&key="
    ),
    (
        "Geolocation API",
        "https://www.googleapis.com/geolocation/v1/geolocate?key="
    )
]


def plist_parse(file: str) -> {}:
    plist = {}
    with open(file, 'rb') as fp:
        plist = load_plist(fp)
        fp.close()
    return plist
