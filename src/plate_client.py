import requests
import json
import io
from models.plate_reader import PlateReader


plate_reader = PlateReader.load_from_file("/home/student/ds-backend/model_weights/plate_reader_model.pth")
sets = set([10022, 9965])


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class PlateReaderClient:
    def __init__(self, host: str):
        self.host = host

    def read_plate_number(self, im):
        res = requests.post(
            f'{self.host}/readPlateNumber',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=im,
        )

        return res.json()

    def read_image_id(self, ids):
        result = json.dumps({"id":ids}, default=set_default)
        try:
            res = requests.post(f'{self.host}/images', data=result, timeout=5)  
        except Exception as e:
            return {"error": "Error publishing: " + str(e)}      
        return res.json()


def get_im(id):
    if int(id):
        id = int(id)
        if id in sets:
            try:
                res = requests.get(f'http://51.250.83.169:7878/images/{id}', timeout=5)
            except Exception as e:
                return str("Error publishing: " + str(e))
                if res.status_code > 499:
                    return str("error 500")
                if res.status_code >399 and res.status_code < 500:
                    return str("error 400")
                elif res.status_code >199 and res.status_code < 300:
                    return io.BytesIO(res.content)
                else:
                     return str("error 300")
        else:
            return str("not in list id")
    else:
        return str("not id")


def solution():
    client = PlateReaderClient(host='http://127.0.0.1:8080')
    res = client.read_image_id(["10022", "9965"])
    dict_answer = {}
    if "error" not in res:
        for id in res["id"]:
            im = get_im(id)
            if type(im) is str:
                dict_answer[id] = im
            else:
                dict_answer[id] = plate_reader.read_text(im)
    else:
        return json.dumps(res)
    return json.dumps(dict_answer)


if __name__ == "__main__":
    dict_answer = solution()
    print(dict_answer)
    