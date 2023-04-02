from src.models.Simple import build_chart

class SimpleControllers:
    def getSimple(genre):
        ret = build_chart(genre)
        return ret.to_json(orient = "records")[1:-1].replace('},{', '} {')