import pandas as pd
import pytest
from apartment_hunt.deuwo import dropping_distant_columns
from apartment_hunt.send_email import send_email



def test_dropping_distant_columns():
    # Create a dummy DataFrame
    data = {
        'wrk_id': ['494957'],
        'strasse': ['Knobelsdorffstr. 1'],
        'plz': ['14059'],
        'ort': ['Berlin OT Charlottenburg'],
        'land': ['Deutschland'],
        'objektnr_extern': ['89-1649240010'],
        'lat': ['52.5132372'],
        'lon': ['13.2966411'],
        'titel': ['WBS-Pflichtig - Familienfreundliche Wohnung'],
        'vermarktungsart_kauf': ['0'],
        'objektart': ['Wohnung'],
        'selbst_vertriebspartner': [None],
        'vermarktungsart_miete': ['1'],
        'preis': ['619.75'],
        'groesse': ['79.75'],
        'anzahl_zimmer': ['3'],
        'objektadresse_freigeben': ['1'],
        'tour_link_360': [None],
        'is_on_favlist': ['0'],
        'preview_img_url': ['https://cdn.wohnraumkarte.com/insertions/bc3bcd1fcc7487e2c7ed12e60a1338b6f45c6e77.jpg'],
        'has_grundriss': [False],
        'has_video': [False],
        'object_viewed': [False],
        'slug': ['3-zimmer-etagenwohnung-mit-balkon-zur-miete-in-berlin-charlottenburg-(wbs)'],
        'images': [[
            {'url': 'https://cdn.wohnraumkarte.com/insertions/bc3bcd1fcc7487e2c7ed12e60a1338b6f45c6e77.jpg', 'type': 'bild'},
            {'url': 'https://cdn.wohnraumkarte.com/insertions/091b054cefe5daea89007d565f9f21209f18e45d.jpg', 'type': 'bild'},
            {'url': 'https://cdn.wohnraumkarte.com/insertions/8123e692ae1c0113eebdf118422f3e6de8489b7c.jpg', 'type': 'kampagne'}
        ]]
    }
    
    df = pd.DataFrame(data)
    
    # Apply the function
    result_df = dropping_distant_columns(df)
    
    # Expected columns after dropping
    expected_columns = set(df.columns) - {'images', 'titel', 'tour_link_360', 'wrk_id', 'land', 'vermarktungsart_miete', 'has_video', 'preview_img_url'}
    
    # Assert that the dropped columns are removed
    assert set(result_df.columns) == expected_columns, "Some columns were not dropped correctly."
    
    # Assert that the shape is correct
    assert result_df.shape[1] == len(expected_columns), "Unexpected number of columns remaining."

if __name__ == "__main__":
    pytest.main()
