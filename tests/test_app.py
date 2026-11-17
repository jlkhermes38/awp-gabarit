from app_dash import detail
from streamlit.testing.v1 import AppTest


def test_streamlit_demarre():
    at = AppTest.from_file("../fil_rouge/app_streamlit.py", default_timeout=30).run()
    assert not at.exception


def test_streamlit_filtre_carburant():
    at = AppTest.from_file("../fil_rouge/app_streamlit.py", default_timeout=30).run()
    at.selectbox[0].select("E10").run()
    assert at.metric[2].label == "Stations"
    assert int(at.metric[2].value) > 0


def test_dash_detail_sans_clic():
    lignes, titre = detail(None, "E10")
    assert lignes == [] and titre == "Aucune commune sélectionnée"


def test_dash_detail_apres_clic():
    lignes, titre = detail({"points": [{"x": "Orléans"}]}, "E10")
    assert titre == "Stations à Orléans"
    assert all(ligne["ville"] == "Orléans" for ligne in lignes)
